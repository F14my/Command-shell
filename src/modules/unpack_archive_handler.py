import os
import shutil
from src.modules.logger import log_command


class UnzipHandler:
    def __init__(self):
        self.command = "unzip"

    @log_command
    def execute(self, args: list[str], shell) -> None:
        if len(args) != 1:
            raise ValueError(f"{self.command}: Too many or too much arguments. Usage: {self.command} <archive.zip>")
        path = os.path.join(os.getcwd(), args[0])
        self.unzip(path)

    def unzip(self, path: str) -> None:
        shutil.unpack_archive(path, os.path.join(os.getcwd(), os.path.basename(path)).split(".")[0])


class UntarHandler(UnzipHandler):
    def __init__(self):
        super().__init__()
        self.command = "untar"
