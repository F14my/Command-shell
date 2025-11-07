import os
from src.modules.logger import log_command

class CdHandler:
    """Implementation of 'cd' command.

    Works like Unix 'cd' to change current directory.
    """
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run cd command with given arguments."""
        self.handle_cd(args)

    def handle_cd(self, args: list[str]) -> None:
        """Change current working directory to specified path."""
        if not args:
            path = os.path.expanduser("~")
        else:
            path = "".join(args)
            if path.startswith("~"):
                path = os.path.expanduser("~") + path[1::]
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"cd: cannot find '{path}': No such directory")
