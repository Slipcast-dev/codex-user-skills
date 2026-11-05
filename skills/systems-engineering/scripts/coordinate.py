#!/usr/bin/env python3
"""Файловая координация заданий Codex без запуска моделей, процессов сборки и оборудования.

Блокировка действует только между вызовами этого инструмента. Она не ограничивает права ОС
и не заменяет независимую VM/HIL. JSON Schema проверяет форму пакетов, не истинность отчёта.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Iterator

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    raise SystemExit("Нужен Python с установленным jsonschema; пакеты автоматически не устанавливаются.")

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "references/packets.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
GATE_ROLES = {"design":["systems-architect"],"research":["hardware-os-researcher"],"implementation":["kernel-driver","firmware-rtos","ipc-daemon","application-ui"],"repair":["systems-bug-fixer"],"build":["build-toolchain"],"static":["static-analysis-critic","code-reviewer"],"security":["memory-security-critic"],"runtime":["sandbox-hil-verifier"],"tests":["test-engineer"],"monitor":["supervisor"]}
REQUIRED = {
    "driver": ["build", "static", "security", "runtime"],
    "firmware": ["build", "static", "security", "runtime"],
    "service": ["build", "static", "security", "runtime"],
    "application": ["build", "static", "security"],
    "research": ["research"],
    "planning": ["design"],
}
MAX_PACKET_BYTES = 65536


def now() -> datetime:
    """Возвращает UTC для сохраняемых сроков и событий."""
    return datetime.now(timezone.utc)


def read_json(path: Path) -> dict[str, Any]:
    """Читает ограниченный по размеру JSON-объект, не загружая произвольный большой журнал."""
    with path.open("rb") as stream:
        data = stream.read(MAX_PACKET_BYTES + 1)
    if len(data) > MAX_PACKET_BYTES:
        raise ValueError("JSON-пакет превышает 64 KiB.")
    value = json.loads(data)
    if not isinstance(value, dict):
        raise ValueError("Ожидается JSON-объект.")
    return value


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    """Записывает состояние заменой в том же каталоге, не оставляя половину JSON."""
    encoded = json.dumps(value, ensure_ascii=False, indent=2)
    if len(encoded.encode("utf-8")) > 4 * 1024 * 1024:
        raise ValueError("Состояние превысит 4 MiB; запись отклонена.")
    fd, temp = tempfile.mkstemp(prefix=".state-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def project_path(root: Path, relative: str) -> Path:
    """Запрещает выход из проекта, включая переход через symlink и служебные каталоги."""
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Нужен относительный путь внутри проекта: " + relative)
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Путь выходит из проекта: " + relative)
    rel = resolved.relative_to(root)
    if any(part.casefold() in {".git", ".systems"} for part in rel.parts):
        raise ValueError("Служебная область не может принадлежать исполнителю: " + relative)
    return resolved



def fingerprint(root: Path, paths: list[str]) -> tuple[str, dict[str, str]]:
    """Хеширует явно выбранные исходные файлы; полноту списка определяет диспетчер."""
    if not paths or len(paths) > 2000:
        raise ValueError("Для snapshot нужны 1–2000 исходных файлов.")
    inventory = {}
    for relative in sorted(set(paths)):
        p = project_path(root, relative)
        if not p.is_file():
            raise ValueError("Snapshot принимает только файлы: " + relative)
        with p.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        inventory[str(p.relative_to(root))] = digest
    digest = hashlib.sha256(json.dumps(inventory, sort_keys=True).encode()).hexdigest()
    return "sha256:" + digest, inventory


def check_snapshot(state: dict[str, Any], snapshot: str, root: Path) -> None:
    """Сверяет содержимое исходников с зарегистрированным snapshot перед воротами."""
    expected = state["snapshots"].get(snapshot)
    if expected is None:
        raise ValueError("Snapshot не зарегистрирован командой snapshot.")
    actual, inventory = fingerprint(root, list(expected))
    if actual != snapshot or inventory != expected:
        raise ValueError("Исходники snapshot изменились; зарегистрируйте новую версию и повторите gates.")

def overlaps(left: str, right: str) -> bool:
    """Учитывает вложенные области; на macOS консервативно считает регистр незначимым."""
    if sys.platform == "darwin":
        left, right = left.casefold(), right.casefold()
    a, b = Path(left), Path(right)
    return a == b or a in b.parents or b in a.parents


@contextmanager
def locked(root: Path) -> Iterator[Path]:
    """Сериализует изменения состояния между процессами; macOS/Linux, локальная ФС."""
    directory = root / ".systems"
    if directory.is_symlink():
        raise ValueError(".systems не должен быть symlink.")
    directory.mkdir(mode=0o700, exist_ok=True)
    for name in ["coordination.lock", "state.json"]:
        if (directory / name).is_symlink():
            raise ValueError("Служебный файл не должен быть symlink.")
    with (directory / "coordination.lock").open("a+") as stream:
        os.chmod(directory / "coordination.lock", 0o600)
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield directory / "state.json"
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def event(state: dict[str, Any], action: str, task_id: str = "") -> None:
    """Добавляет короткое событие без полных запросов, секретов и логов."""
    state["revision"] += 1
    state["events"].append({"at": now().isoformat(), "action": action, "id": task_id})
    state["events"] = state["events"][-200:]


def packet(path: Path, kind: str) -> dict[str, Any]:
    """Проверяет типизированный пакет и запрещает неизвестные поля."""
    value = read_json(path)
    VALIDATOR.validate(value)
    if value["kind"] != kind:
        raise ValueError("Неверный kind пакета.")
    return value


def check_deadline(state: dict[str, Any]) -> None:
    """Проверяет deadline на границах операций; не прерывает уже работающего агента."""
    if state["status"] != "running":
        raise ValueError("Запуск остановлен или завершён.")
    if now() >= datetime.fromisoformat(state["deadline"]):
        raise ValueError("Истёк deadline; остановите агентов штатным средством Codex.")


def dispatch(state: dict[str, Any], value: dict[str, Any], root: Path) -> dict[str, Any]:
    """Резервирует пути и попытку; сам не создаёт сессию агента."""
    check_deadline(state)
    if value["snapshot"] not in state["snapshots"]:
        raise ValueError("Сначала зарегистрируйте snapshot.")
    if value["gate"] not in {"implementation", "repair", "monitor"}:
        check_snapshot(state, value["snapshot"], root)
    if value["agent"] not in GATE_ROLES[value["gate"]]:
        raise ValueError("Роль не может выдавать этот gate.")
    if state["safety_hold"] and value["gate"] not in {"repair", "security", "design", "research", "monitor"}:
        raise ValueError("Security hold: разрешены только исправление и исследование риска.")
    active = [t for t in state["tasks"].values() if t["status"] == "running"]
    if len(active) >= 3:
        raise ValueError("Уже работают три агента.")
    if state["dispatches"] >= state["max_dispatches"]:
        raise ValueError("Исчерпан лимит заданий.")
    old = state["tasks"].get(value["id"])
    if old and old["status"] in {"running", "pass"}:
        raise ValueError("Task ID уже выполняется или принят; для новой версии задайте новый ID.")
    if old and (old["packet"]["agent"], old["packet"]["gate"]) != (value["agent"], value["gate"]):
        raise ValueError("При повторе нельзя менять роль и назначение gate.")
    attempt = old["attempt"] + 1 if old else 1
    if attempt > 5:
        raise ValueError("Исчерпано пять попыток task ID.")
    for dep in value["depends_on"]:
        if dep == value["id"] or state["tasks"].get(dep, {}).get("status") != "pass":
            raise ValueError("Зависимость не принята: " + dep)
    paths = [str(project_path(root, p)) for p in value["write_paths"]]
    if any(Path(p) == root for p in paths):
        raise ValueError("Назначьте конкретную область, а не весь проект.")
    for task in active:
        if any(overlaps(a, b) for a in paths for b in task["resolved_paths"]):
            raise ValueError("Конфликт областей записи с " + task["packet"]["id"])
    task = {"packet": value, "attempt": attempt, "status": "running", "resolved_paths": paths}
    state["tasks"][value["id"]] = task
    state["dispatches"] += 1
    event(state, "dispatch", value["id"])
    return {"task": value, "attempt": attempt, "remaining_attempts": 5 - attempt,
            "deadline": state["deadline"], "remaining_dispatches": state["max_dispatches"] - state["dispatches"]}


def complete(state: dict[str, Any], value: dict[str, Any], root: Path) -> dict[str, Any]:
    """Принимает результат только активной попытки и проверяет хеши файлов-доказательств."""
    task = state["tasks"].get(value["id"])
    if not task or task["status"] != "running":
        raise ValueError("Нет активной попытки.")
    expected = task["packet"]
    if (value["agent"], value["attempt"], value["snapshot"]) != (expected["agent"], task["attempt"], expected["snapshot"]):
        raise ValueError("Устаревший результат или несовпадающая роль/snapshot.")
    if value["status"] == "pass" and (not value["evidence"] or value["safety_block"]):
        raise ValueError("pass требует доказательства и отсутствия safety_block.")
    for item in value["evidence"]:
        p = project_path(root, item["path"])
        if not p.is_file():
            raise ValueError("Доказательство не является файлом: " + item["path"])
        with p.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != item["sha256"]:
            raise ValueError("Хеш доказательства не совпал: " + item["path"])
    task["status"] = value["status"]
    task["result"] = value
    gate = expected["gate"]
    if value["safety_block"] or (gate == "security" and value["status"] != "pass"):
        state["safety_hold"] = True
    # Снять hold может лишь успешная повторная проверка security без иных активных угроз.
    if gate == "security" and value["status"] == "pass":
        unresolved = [t for t in state["tasks"].values()
                      if t.get("result", {}).get("safety_block")
                      and t["packet"]["snapshot"] == value["snapshot"]]
        if not unresolved:
            state["safety_hold"] = False
    event(state, "complete:" + value["status"], value["id"])
    late = now() >= datetime.fromisoformat(state["deadline"])
    return {"id": value["id"], "status": value["status"], "safety_hold": state["safety_hold"],
            "late": late, "run_status": state["status"]}


def finish(state: dict[str, Any], snapshot: str, root: Path) -> dict[str, Any]:
    """Закрывает запуск только при актуальных обязательных gates и отсутствии активной работы."""
    check_deadline(state)
    if state["safety_hold"]:
        raise ValueError("Нельзя закрыть запуск при security hold.")
    if any(t["status"] == "running" for t in state["tasks"].values()):
        raise ValueError("Есть незавершённые задания.")
    check_snapshot(state, snapshot, root)
    accepted = set()
    for task in state["tasks"].values():
        if task["packet"]["snapshot"] == snapshot:
            if task["status"] != "pass":
                raise ValueError("Есть непринятое задание итоговой версии.")
            for item in task["result"]["evidence"]:
                p = project_path(root, item["path"])
                with p.open("rb") as stream:
                    if hashlib.file_digest(stream, "sha256").hexdigest() != item["sha256"]:
                        raise ValueError("Доказательство изменилось после приёмки: " + item["path"])
            accepted.add(task["packet"]["gate"])
    missing = set(state["required_gates"]) - accepted
    if missing:
        raise ValueError("Не пройдены обязательные gates: " + ", ".join(sorted(missing)))
    state["status"] = "complete"
    state["final_snapshot"] = snapshot
    event(state, "finish")
    return {"status": "complete", "snapshot": snapshot, "gates": sorted(accepted)}


def main() -> int:
    """Обрабатывает CLI; ошибки не меняют состояние и возвращают ненулевой exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--kind", choices=REQUIRED, required=True)
    init.add_argument("--timeout", type=int, default=1800)
    init.add_argument("--max-dispatches", type=int, default=30)
    for name in ["dispatch", "complete"]:
        cmd = sub.add_parser(name)
        cmd.add_argument("--packet", type=Path, required=True)
    sub.add_parser("status")
    snap = sub.add_parser("snapshot")
    snap.add_argument("--path", action="append", required=True)
    stop = sub.add_parser("stop")
    stop.add_argument("--reason", required=True)
    end = sub.add_parser("finish")
    end.add_argument("--snapshot", required=True)
    args = parser.parse_args()
    try:
        root = args.project.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Проект должен быть каталогом.")
        with locked(root) as path:
            if args.command == "init":
                if path.exists():
                    raise ValueError("Состояние уже существует; оно не будет перезаписано.")
                if not 1 <= args.timeout <= 86400 or not 1 <= args.max_dispatches <= 100:
                    raise ValueError("Timeout: 1–86400 секунд; max-dispatches: 1–100.")
                state = {"version": 1, "project": str(root), "status": "running", "revision": 0,
                         "kind": args.kind, "required_gates": REQUIRED[args.kind],
                         "deadline": (now() + timedelta(seconds=args.timeout)).isoformat(),
                         "max_dispatches": args.max_dispatches, "dispatches": 0,
                         "safety_hold": False, "tasks": {}, "events": [], "snapshots": {}}
                event(state, "init")
                output = state
            else:
                # Состояние включает историю и может быть больше пакета, но остаётся ограниченным.
                if path.stat().st_size > 4 * 1024 * 1024:
                    raise ValueError("Состояние превышает 4 MiB.")
                state = json.loads(path.read_text())
                if state.get("version") != 1 or state.get("project") != str(root):
                    raise ValueError("Несовместимое состояние или другой проект.")
                if args.command == "status":
                    output = {k: state[k] for k in ["status", "revision", "deadline", "required_gates", "safety_hold", "dispatches", "max_dispatches"]}
                    output["expired"] = now() >= datetime.fromisoformat(state["deadline"])
                    output["tasks"] = {key: {"agent": t["packet"]["agent"], "status": t["status"],
                                             "attempt": t["attempt"], "snapshot": t["packet"]["snapshot"]}
                                       for key, t in state["tasks"].items()}
                elif args.command == "snapshot":
                    check_deadline(state)
                    digest, inventory = fingerprint(root, args.path)
                    if digest not in state["snapshots"] and len(state["snapshots"]) >= 100:
                        raise ValueError("Исчерпан лимит 100 snapshots.")
                    state["snapshots"][digest] = inventory
                    event(state, "snapshot")
                    output = {"snapshot": digest, "files": len(inventory)}
                elif args.command == "dispatch":
                    output = dispatch(state, packet(args.packet, "task"), root)
                elif args.command == "complete":
                    output = complete(state, packet(args.packet, "result"), root)
                elif args.command == "stop":
                    if state["status"] == "complete":
                        raise ValueError("Запуск уже завершён.")
                    state["status"] = "stopped"
                    event(state, "stop")
                    output = {"status": "stopped", "reason": args.reason,
                              "action": "Основной чат должен отдельно прервать активных агентов штатными инструментами."}
                    state["stop_reason"] = args.reason
                else:
                    output = finish(state, args.snapshot, root)
            if args.command != "status":
                atomic_json(path, state)
            print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ValidationError) as error:
        print(json.dumps({"error": str(error)[:2048]}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
