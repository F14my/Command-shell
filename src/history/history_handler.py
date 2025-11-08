import json

from src.constants import HISTORY_FILE
from src.modules.logger import log_command


class HistoryHandler:
    """Print previously executed commands saved in the history file."""
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Show recent commands from history.

        Args:
            args (list[str]): Optional number of commands to show (default: 10).
            shell: The shell instance (unused).

        Raises:
            ValueError: If more than one argument is given.
        """
        if len(args) > 1:
            raise ValueError("history: Too many arguments")
        n = int(args[0]) if args else 10
        self.handle_history(n)

    def handle_history(self, n: int) -> None:
        """Print the last n commands from history.

        Args:
            n (int): Number of commands to show from the end of history.
        """
        with open(HISTORY_FILE, "r", encoding="utf-8") as read:
            data = json.load(read)
            for cmd_id, command in enumerate(data["stack"][n:]):
                print(cmd_id + 1, command["command"])
