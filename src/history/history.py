from pathlib import Path

class HistoryManager:
    def __init__(self, max_size: int = 1000):
        self.history_file = Path.cwd()  / ".history"
        self.max_size = max_size

    def add(self, command: str):
        if "history" not in command:
            with open(self.history_file, "a", encoding="utf-8") as write_file:
                write_file.write(command + "\n")

    def get_last(self, n: int = 10) -> list[str]:
        with open(self.history_file, "r") as read_file:
            output = [line.strip() for line in read_file.readlines()][:n]
        return output
