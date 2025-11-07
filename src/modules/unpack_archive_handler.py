import os
import shutil
from src.modules.logger import log_command


class UnzipHandler:
    """Implementation of 'unzip' command to extract zip archives."""
    def __init__(self):
        self.command = "unzip"

    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run unzip command with given arguments."""
        if len(args) != 1:
            raise ValueError(f"{self.command}: Too many or too much arguments. Usage: {self.command} <archive.zip>")
        path = os.path.join(os.getcwd(), args[0])
        self.unzip(path)

    def unzip(self, path: str) -> None:
        """Extract zip archive to current directory."""
        shutil.unpack_archive(path, os.path.join(os.getcwd(), os.path.basename(path)).split(".")[0])


class UntarHandler(UnzipHandler):
    """Implementation of 'untar' command to extract tar archives."""
    def __init__(self):
        super().__init__()
        self.command = "untar"
