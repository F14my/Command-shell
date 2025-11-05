import shutil
import os
from src.modules.logger import log_command


class ZipHandler:
    def __init__(self):
        self.format = "zip"

    @log_command
    def execute(self, args: list[str], shell) -> None:
        path = os.path.join(os.getcwd(), args[0])
        if len(args) == 1:
            name = args[0]
        elif len(args) == 2:
            name = args[1].split(".")[0]
        else:
            raise ValueError(
                f"{self.format}: Too many or too much arguments. Usage: {self.format} <folder> <archive.zip>")
        self.handle_zip(path, name)

    def handle_zip(self, path: str, name: str) -> None:
        shutil.make_archive(name, self.format, path)


class TarHandler(ZipHandler):
    def __init__(self):
        super().__init__()
        self.format = "tar"
