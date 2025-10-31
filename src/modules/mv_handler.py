import shutil
from src.modules.logger import log_command

class MvHandler:
    @log_command
    def execute(self, args: list[str], shell) -> None:
        self.handle_mv(args)

    def handle_mv(self, args: list[str]) -> None:
        if len(args) < 2:
            raise ValueError("mv: Missing file operand")
        source, target = args[0], args[1]
        try:
            shutil.move(source, target)
        except FileNotFoundError:
            raise FileNotFoundError(f"mv: Cannot stat '{source}': No such file or directory")
        except PermissionError:
            raise PermissionError(f"mv: Cannot move '{source}': Permission denied")
