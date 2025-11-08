import shutil
import os
from src.modules.logger import log_command
from src.constants import TRASH


class RmHandler:
    """Implementation of 'rm' command.

    Works like Unix 'rm' to remove files or directories.
    """
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run rm command with given arguments."""
        keys = [arg for arg in args if arg.startswith("-")]
        files = [arg for arg in args if not arg.startswith("-")]
        self.handle_rm(keys, files)

    def handle_rm(self, keys: list[str], files: list[str]) -> None:
        """Remove files or directories safely to .trash."""
        os.makedirs(TRASH, exist_ok=True)
        for file in files:
            abs_path = os.path.abspath(file)
            root_dir = os.path.abspath(os.sep)
            current_dir = os.getcwd()
            parent_dir = os.path.dirname(current_dir)

            if abs_path == root_dir or abs_path == parent_dir:
                raise PermissionError(f"rm: You cannot remove '{file}'!")

            try:
                if "-r" in keys or os.path.isdir(file):
                    response = input(f"rm: remove write-protected directory '{file}'? ")
                    if response.lower() in ['y', 'yes']:
                        os.chmod(file, 0o777)
                        os.chmod(TRASH, 0o777)
                        shutil.move(file, TRASH)
                else:
                    shutil.move(file, TRASH)
            except PermissionError:
                raise PermissionError(f"rm: Permission denied: '{file}'")
            except FileNotFoundError:
                raise FileNotFoundError(f"rm: Cannot delete '{file}': No such file or directory")
            except Exception as error:
                raise error
