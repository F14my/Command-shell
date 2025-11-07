from src.constants import HISTORY_FILE
from pathlib import Path
import json
import os


class HistoryManager:
    """Save command history to JSON file for later use.

    Creates history file on first use and adds each executed command
    with its arguments and working directory. This enables features
    like viewing and undo history.
    """
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
        """Add a success command to history.

        Args:
            command (str): Name of the command.
            args (list[str]): Arguments that were used with the command.
        """
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
