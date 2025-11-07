import shutil
from src.modules.logger import log_command

class MvHandler:
    """Implementation of 'mv' command.

    Works like Unix 'mv' to move or rename files.
    """
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run mv command with given arguments."""
        self.handle_mv(args)

    def handle_mv(self, args: list[str]) -> None:
        """Move or rename files from source to target."""
        if len(args) < 2:
            raise ValueError("mv: Missing file operand")
        source, target = args[0], args[1]
        try:
            shutil.move(source, target)
        except FileNotFoundError:
            raise FileNotFoundError(f"mv: Cannot stat '{source}': No such file or directory")
        except PermissionError:
            raise PermissionError(f"mv: Cannot move '{source}': Permission denied")
