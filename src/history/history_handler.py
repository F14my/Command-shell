import json

from src.constants import HISTORY_FILE


class HistoryHandler:
    def execute(self, args: list[str], shell) -> None:
        self.handle_history()

    def handle_history(self):
        with open(HISTORY_FILE, "r", encoding="utf-8") as read:
            data = json.load(read)
            for command in data["stack"]:
                print(command["id"], command["command"])
