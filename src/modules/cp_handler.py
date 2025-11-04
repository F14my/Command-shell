import shutil
import os
from src.modules.logger import log_command


class CpHandler:
    @log_command
    def execute(self, args: list[str], shell) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]
        if len(files) > 2:
            raise ValueError("cp: Too many arguments")
        if len(files) < 2:
            raise ValueError("cp: Missing file operand")
        self.handle_cp(keys, files)

    def handle_cp(self, keys: list[str], files: list[str]) -> None:
        source, target = files[0], files[1]
        try:
            target_dir = os.path.dirname(target)
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)
            if "-r" in keys:
                shutil.copytree(source, target)
            else:
                if os.path.isdir(source):
                    raise ValueError("cp: use -r to copy directory")
                shutil.copy(source, target)
        except PermissionError:
            raise PermissionError(f"cp: Permission denied: '{source}'")
        except FileNotFoundError:
            raise FileNotFoundError(f"cp: Cannot stat '{source}': No such file or directory")
        except shutil.SameFileError:
            raise ValueError(f"cp: '{source}' and '{target}' are the same file")
