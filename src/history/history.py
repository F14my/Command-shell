from src.constants import HISTORY_FILE
from pathlib import Path
import json
import os


class HistoryManager:
    def __init__(self):
        try:
            file = open(HISTORY_FILE, "r")
        except FileNotFoundError:
            with open(HISTORY_FILE, "w", encoding="utf-8") as write:
                data = {
                    "stack": [],
                }
                json.dump(data, write, indent=4)

    def add(self, command: str, args: list[str]):
        if command in ["undo", "history"]:
            return
        with open(HISTORY_FILE, "r", encoding="utf-8") as read:
            data = json.load(read)
            stack = {
                "command": command,
                "args": args,
                "cwd": os.getcwd(),
            }
            data["stack"].append(stack)
        with open(HISTORY_FILE, "w", encoding="utf-8") as write:
            json.dump(data, write, indent=4)
