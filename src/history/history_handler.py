from src.history.history import HistoryManager

history_manager = HistoryManager()


class HistoryHandler:
    def execute(self, args: list[str], shell):
        n = int(args[0]) if args else 10
        self.show_history(n)

    def show_history(self, n):
        for i, cmd in enumerate(history_manager.get_last(n)):
            print(f"{i+1} {cmd}")
