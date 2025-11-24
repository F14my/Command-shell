import shutil
import os
import hashlib
import time

from src.modules.logger import log_command
from src.constants import TRASH


def make_trash_name(abs_path: str) -> str:
    ts = int(time.time() * 1000)
    h = hashlib.sha256(abs_path.encode("utf-8")).hexdigest()[:6]
    base = os.path.basename(abs_path) or "item"
    return f"{ts}_{h}_{base}"


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

            trash_name = make_trash_name(abs_path)
            trash_target = os.path.join(TRASH, trash_name)

            try:
                if "-r" in keys or os.path.isdir(abs_path):
                    response = input(f"rm: remove write-protected directory '{file}'? ")
                    if response.lower() in ["y", "yes"]:
                        os.chmod(abs_path, 0o777)
                        os.chmod(TRASH, 0o777)
                        shutil.move(abs_path, trash_target)
                else:
                    shutil.move(abs_path, trash_target)
            except PermissionError:
                raise PermissionError(f"rm: Permission denied: '{file}'")
            except FileNotFoundError:
                raise FileNotFoundError(f"rm: Cannot delete '{file}': No such file or directory")
            except Exception as error:
                raise error
