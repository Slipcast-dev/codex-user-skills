"""Регрессионные проверки переходов контроллера без записи состояния на диск."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location(
    "loop_controller", Path(__file__).parents[1] / "scripts/loop_controller.py")
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class ControllerTests(unittest.TestCase):
    """Проверяет контроль доказательств и границы бюджета."""

    def setUp(self) -> None:
        self.state = {
            "status": "open", "goal": "test", "iteration": 0,
            "max_loop_iterations": 12,
            "tasks": [{
                "id": "T1", "skill": "test", "objective": "test",
                "status": "verifying", "attempts": 0, "max_attempts": 3,
                "verification": [{"cmd": "true", "expect_exit": 0}],
                "evidence": [],
            }],
        }

    @property
    def task(self) -> dict:
        return self.state["tasks"][0]

    def call(self, command: str, **kwargs: object) -> int:
        """Эмулирует файловую границу, сохраняя реальные переходы контроллера."""
        args = SimpleNamespace(
            state="unused", task="T1", phase="verify", exit_code=0,
            evidence="наблюдение", cwd=".", waive=None, reason=None)
        for key, value in kwargs.items():
            setattr(args, key, value)

        def save(state: dict, path: str) -> None:
            # JSON не сохраняет общие ссылки между вложенными объектами.
            self.state = json.loads(json.dumps(state))

        with patch.object(controller, "load", side_effect=lambda _: copy.deepcopy(self.state)), \
             patch.object(controller, "save", side_effect=save), \
             contextlib.redirect_stdout(io.StringIO()):
            return getattr(controller, "cmd_" + command)(args)

    def test_claim_cannot_replace_execution(self) -> None:
        before = copy.deepcopy(self.state)
        self.assertEqual(self.call("record"), 6)
        self.assertEqual(self.state, before)

    def test_mixed_checks_need_execution_first(self) -> None:
        self.task["verification"].append({"kind": "manual-evidence"})
        self.assertEqual(self.call("record"), 6)
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.assertEqual(self.call("verify"), 0)
        self.assertEqual(self.task["status"], "verifying")
        self.assertEqual(self.call("record"), 0)
        self.assertEqual(self.task["status"], "verified")

    def test_manual_only(self) -> None:
        self.task["verification"] = [{"kind": "manual-evidence"}]
        self.assertEqual(self.call("record"), 0)
        self.assertEqual(self.task["status"], "verified")

    def test_empty_evidence_is_rejected_without_mutation(self) -> None:
        self.task["verification"] = []
        before = copy.deepcopy(self.state)
        self.assertEqual(self.call("record", evidence="  \n"), 6)
        self.assertEqual(self.state, before)

    def test_changed_checks_invalidate_receipt(self) -> None:
        self.task["verification"].append({"kind": "manual-evidence"})
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.call("verify")
        self.task["verification"][0]["cmd"] = "false"
        self.assertEqual(self.call("record"), 6)

    def test_execute_invalidates_receipt(self) -> None:
        self.task["verification"].append({"kind": "manual-evidence"})
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.call("verify")
        self.assertEqual(self.call("record", phase="execute"), 0)
        self.assertNotIn("executable_verification", self.task)
        self.assertEqual(self.call("record"), 6)

    def test_retry_does_not_reuse_success(self) -> None:
        self.task["verification"].append({"kind": "manual-evidence"})
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.call("verify")
        self.call("record", exit_code=1)
        self.assertEqual(self.task["attempts"], 1)
        self.call("record", phase="execute")
        self.assertEqual(self.call("record"), 6)

    def test_budget_blocks_record_without_mutation(self) -> None:
        self.state["iteration"] = 12
        before = copy.deepcopy(self.state)
        self.assertEqual(self.call("record"), 5)
        self.assertEqual(self.state, before)

    def test_budget_blocks_process_and_mutation(self) -> None:
        self.state["iteration"] = 12
        before = copy.deepcopy(self.state)
        with patch.object(controller.subprocess, "run") as run:
            self.assertEqual(self.call("verify"), 5)
            run.assert_not_called()
        self.assertEqual(self.state, before)

    def test_final_allowed_iteration_can_finish(self) -> None:
        self.state["iteration"] = 11
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.assertEqual(self.call("verify"), 0)
        self.assertEqual(self.state["iteration"], 12)
        self.assertEqual(self.task["status"], "verified")
        self.assertEqual(self.call("close"), 0)

    def test_manual_check_cannot_extend_budget(self) -> None:
        self.state["iteration"] = 11
        self.task["verification"].append({"kind": "manual-evidence"})
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "", "")):
            self.assertEqual(self.call("verify"), 5)
        self.assertEqual(self.call("record"), 5)
        self.assertEqual(self.call("close"), 4)

    def test_closed_state_never_launches_process(self) -> None:
        self.state["status"] = "closed"
        with patch.object(controller.subprocess, "run") as run:
            self.assertEqual(self.call("verify"), 6)
            run.assert_not_called()

    def test_failed_check_stays_unverified(self) -> None:
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 1, "", "failure")):
            self.call("verify")
        self.assertEqual(self.task["status"], "pending")
        self.assertEqual(self.task["attempts"], 1)
        self.assertEqual(self.call("close"), 4)

    def test_attempt_cap_blocks_all_work(self) -> None:
        self.task["attempts"] = 3
        with patch.object(controller.subprocess, "run") as run:
            self.assertEqual(self.call("verify"), 2)
            run.assert_not_called()
        self.assertEqual(self.call("record", phase="execute"), 2)

    def test_expected_nonzero_exit_is_success(self) -> None:
        self.task["verification"][0]["expect_exit"] = 7
        with patch.object(controller.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 7, "", "")):
            self.assertEqual(self.call("verify"), 0)
        self.assertEqual(self.task["status"], "verified")

    def test_timeout_cannot_match_expected_exit(self) -> None:
        self.task["verification"][0]["expect_exit"] = 124
        with patch.object(controller.subprocess, "run",
                          side_effect=subprocess.TimeoutExpired("test", 120)):
            self.call("verify")
        self.assertEqual(self.task["status"], "pending")

    def test_pending_cannot_skip_execute(self) -> None:
        self.task["status"] = "pending"
        before = copy.deepcopy(self.state)
        self.assertEqual(self.call("record"), 6)
        self.assertEqual(self.state, before)


if __name__ == "__main__":
    unittest.main()
