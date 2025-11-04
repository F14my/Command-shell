from src.constants import HISTORY_FILE
from pathlib import Path
import json
import time


class HistoryManager:
    def __init__(self):
        try:
            file = open(HISTORY_FILE, "r")
        except FileNotFoundError:
            with open(HISTORY_FILE, "w", encoding="utf-8") as write:
                data = {
                    "stack": [],
                    "last_id": 0
                }
                json.dump(data, write, indent=4)

    def add(self, command: str, args: list[str]):
        if command in ["undo", "history"]:
            return
        src = dst = None
        if command in ["cp", "mv"]:
            src = str(Path.cwd() / args[0])
            dst = str(Path.cwd() / args[1].split("/")[0])
        if command == "rm":
            src = str(Path.cwd() / args[0])
        with open(HISTORY_FILE, "r", encoding="utf-8") as read:
            data = json.load(read)
            stack = {
                "id": data["last_id"] + 1,
                "command": command,
                "src": src,
                "dst": dst,
                "timestamp": time.time(),
            }
            data["stack"].append(stack)
            data["last_id"] += 1
        with open(HISTORY_FILE, "w", encoding="utf-8") as write:
            json.dump(data, write, indent=4)
