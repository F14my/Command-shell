import json

from src.constants import HISTORY_FILE


class HistoryHandler:
    def execute(self, args: list[str], shell) -> None:
        if len(args) > 1:
            raise ValueError("history: Too many arguments")
        n = int(args[0]) if args else 10
        self.handle_history(n)

    def handle_history(self, n: int):
        with open(HISTORY_FILE, "r", encoding="utf-8") as read:
            data = json.load(read)
            for cmd_id, command in enumerate(data["stack"][:n]):
                print(cmd_id + 1, command["command"])
