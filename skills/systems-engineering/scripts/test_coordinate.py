"""Проверки координации: конфликты записи, версии, лимиты и непройденные ворота."""
from __future__ import annotations

from datetime import timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("coordinate.py")
SPEC = importlib.util.spec_from_file_location("coordinate", SCRIPT)
COORD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COORD)


class CoordinationTests(unittest.TestCase):
    """Проверяет наблюдаемые инварианты, не запуская моделей или системный код."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "src").mkdir()
        (self.root / "src/driver.c").write_text("int ready;\n")
        (self.root / "report.txt").write_text("Подтверждённое наблюдение тестовой среды.\n")
        self.run_cli("init", "--kind", "research")
        self.run_cli("snapshot", "--path", "src/driver.c")
        self.state = json.loads((self.root / ".systems/state.json").read_text())
        self.snapshot = next(iter(self.state["snapshots"]))

    def run_cli(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        """Запускает только файловый CLI; неверный результат сохраняет диагностический вывод."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(self.root), *args],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode == 0, ok, result.stderr + result.stdout)
        return result

    def task(self, task_id: str = "research", gate: str = "research",
             paths: list[str] | None = None) -> dict:
        """Создаёт минимальное независимое задание по публичному контракту."""
        return {"kind": "task", "id": task_id, "agent": COORD.GATE_ROLES[gate][0],
                "goal": "Проверить контракт тестового модуля.", "snapshot": self.snapshot,
                "gate": gate, "depends_on": [], "write_paths": paths or []}

    def result(self, task: dict, status: str = "pass", attempt: int = 1,
               block: bool = False) -> dict:
        """Возвращает пакет с реальным файловым доказательством."""
        digest = hashlib.sha256((self.root / "report.txt").read_bytes()).hexdigest()
        return {"kind": "result", "id": task["id"], "agent": task["agent"],
                "attempt": attempt, "snapshot": task["snapshot"], "status": status,
                "summary": "Проверка завершена.", "safety_block": block,
                "evidence": [{"path": "report.txt", "sha256": digest}], "limitations": []}

    def accept(self, task: dict) -> None:
        """Проводит независимое задание и его результат."""
        out = COORD.dispatch(self.state, task, self.root)
        COORD.complete(self.state, self.result(task, attempt=out["attempt"]), self.root)

    def test_cli_acceptance_and_no_reinitialization(self) -> None:
        task = self.task()
        p = self.root / "task.json"
        p.write_text(json.dumps(task))
        self.run_cli("dispatch", "--packet", str(p))
        p.write_text(json.dumps(self.result(task)))
        self.run_cli("complete", "--packet", str(p))
        output = self.run_cli("finish", "--snapshot", self.snapshot)
        self.assertEqual(json.loads(output.stdout)["status"], "complete")
        self.run_cli("init", "--kind", "driver", ok=False)

    def test_overlapping_directory_rejected_and_released(self) -> None:
        first = self.task("a", paths=["src"])
        COORD.dispatch(self.state, first, self.root)
        with self.assertRaisesRegex(ValueError, "Конфликт"):
            COORD.dispatch(self.state, self.task("b", paths=["src/driver.c"]), self.root)
        COORD.complete(self.state, self.result(first), self.root)
        COORD.dispatch(self.state, self.task("b", paths=["src/driver.c"]), self.root)

    def test_escape_and_symlink_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            COORD.dispatch(self.state, self.task(paths=["../outside"]), self.root)
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "escape").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                COORD.dispatch(self.state, self.task(paths=["escape/file.c"]), self.root)

    def test_parallel_cap_and_dependencies(self) -> None:
        missing = self.task("waiting")
        missing["depends_on"] = ["unknown"]
        with self.assertRaisesRegex(ValueError, "Зависимость"):
            COORD.dispatch(self.state, missing, self.root)
        for i in range(3):
            COORD.dispatch(self.state, self.task(str(i)), self.root)
        with self.assertRaisesRegex(ValueError, "три"):
            COORD.dispatch(self.state, self.task("four"), self.root)

    def test_stale_attempt_and_wrong_snapshot_rejected(self) -> None:
        task = self.task()
        COORD.dispatch(self.state, task, self.root)
        result = self.result(task, attempt=2)
        with self.assertRaisesRegex(ValueError, "Устаревший"):
            COORD.complete(self.state, result, self.root)
        result = self.result(task)
        result["snapshot"] = "other"
        with self.assertRaisesRegex(ValueError, "Устаревший"):
            COORD.complete(self.state, result, self.root)

    def test_required_runtime_cannot_be_skipped(self) -> None:
        self.state["required_gates"] = COORD.REQUIRED["driver"]
        for gate in ["build", "static", "security"]:
            self.accept(self.task(gate, gate))
        with self.assertRaisesRegex(ValueError, "runtime"):
            COORD.finish(self.state, self.snapshot, self.root)

    def test_modified_source_invalidates_finish(self) -> None:
        self.accept(self.task())
        (self.root / "src/driver.c").write_text("int changed_abi;\n")
        with self.assertRaisesRegex(ValueError, "изменились"):
            COORD.finish(self.state, self.snapshot, self.root)

    def test_evidence_tampering_invalidates_finish(self) -> None:
        self.accept(self.task())
        (self.root / "report.txt").write_text("Изменённый отчёт.\n")
        with self.assertRaisesRegex(ValueError, "Доказательство"):
            COORD.finish(self.state, self.snapshot, self.root)

    def test_security_hold_allows_only_remediation(self) -> None:
        security = self.task("security", "security")
        COORD.dispatch(self.state, security, self.root)
        COORD.complete(self.state, self.result(security, "fail", block=True), self.root)
        with self.assertRaisesRegex(ValueError, "Security hold"):
            COORD.dispatch(self.state, self.task("build", "build"), self.root)
        self.accept(self.task("repair", "repair"))
        out = COORD.dispatch(self.state, security, self.root)
        COORD.complete(self.state, self.result(security, attempt=out["attempt"]), self.root)
        self.assertFalse(self.state["safety_hold"])

    def test_retry_and_global_limits(self) -> None:
        task = self.task()
        for attempt in range(1, 6):
            COORD.dispatch(self.state, task, self.root)
            COORD.complete(self.state, self.result(task, "fail", attempt), self.root)
        with self.assertRaisesRegex(ValueError, "пять"):
            COORD.dispatch(self.state, task, self.root)
        self.state["max_dispatches"] = self.state["dispatches"]
        with self.assertRaisesRegex(ValueError, "лимит заданий"):
            COORD.dispatch(self.state, self.task("another"), self.root)

    def test_deadline_and_stop_prevent_new_work(self) -> None:
        self.state["deadline"] = (COORD.now() - timedelta(seconds=1)).isoformat()
        with self.assertRaisesRegex(ValueError, "deadline"):
            COORD.dispatch(self.state, self.task(), self.root)
        self.run_cli("stop", "--reason", "Ручная остановка.")
        self.run_cli("finish", "--snapshot", self.snapshot, ok=False)

    def test_unknown_field_and_fake_role_rejected(self) -> None:
        task = self.task()
        task["extra_permission"] = "write_everything"
        with self.assertRaises(COORD.ValidationError):
            COORD.VALIDATOR.validate(task)
        task = self.task()
        task["agent"] = "application-ui"
        with self.assertRaisesRegex(ValueError, "Роль"):
            COORD.dispatch(self.state, task, self.root)


    def test_pass_without_evidence_and_bad_hash_rejected(self) -> None:
        task = self.task()
        COORD.dispatch(self.state, task, self.root)
        result = self.result(task)
        result["evidence"] = []
        with self.assertRaisesRegex(ValueError, "доказательства"):
            COORD.complete(self.state, result, self.root)
        result = self.result(task)
        result["evidence"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Хеш"):
            COORD.complete(self.state, result, self.root)

    def test_oversized_state_does_not_destroy_previous_state(self) -> None:
        path = self.root / ".systems/state.json"
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, "4 MiB"):
            COORD.atomic_json(path, {"too_large": "x" * (4 * 1024 * 1024)})
        self.assertEqual(path.read_bytes(), before)

    def test_simultaneous_cli_dispatch_serializes_conflicts(self) -> None:
        packets = []
        for task_id in ["a", "b"]:
            p = self.root / (task_id + ".json")
            p.write_text(json.dumps(self.task(task_id, paths=["src"])))
            packets.append(p)
        children = [
            subprocess.Popen([sys.executable, str(SCRIPT), "--project", str(self.root),
                              "dispatch", "--packet", str(p)],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for p in packets
        ]
        for child in children:
            child.communicate(timeout=20)
        self.assertEqual(sorted(child.returncode for child in children), [0, 2])


if __name__ == "__main__":
    unittest.main()
