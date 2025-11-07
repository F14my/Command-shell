import os
from src.modules.logger import log_command

class PwdHandler:
    """Implementation of 'pwd' command.

    Works like Unix 'pwd' to print current working directory.
    """
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run pwd command with given arguments."""
        self.handle_pwd(args)

    def handle_pwd(self, args: list[str]) -> None:
        """Print current working directory path."""
        print(f"Current working directory: {os.getcwd().replace("\\", "/")}")
