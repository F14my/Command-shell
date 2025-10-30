import shutil
import os

class CpHandler:
    def execute(self, args: list[str], shell) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]
        self.handle_cp(keys, files)

    def handle_cp(self, keys: list[str], files: list[str]) -> None:
        if len(files) < 2:
            raise ValueError("cp: Missing file operand")
        source, target = files[0], files[1]
        try:
            if "-r" in keys or os.path.isdir(source):
                shutil.copytree(source, target)
            else:
                shutil.copy(source, target)
        except PermissionError:
            raise PermissionError(f"cp: Permission denied: '{source}'")
        except FileNotFoundError:
            print(f"cp: Cannot stat '{source}': No such file or directory")
        except shutil.SameFileError:
            print(f"cp: '{source}' and '{target}' are the same file")
