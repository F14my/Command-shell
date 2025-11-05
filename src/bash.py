import shlex

from src.modules.pwd_handler import PwdHandler
from src.modules.ls_handler import LsHandler
from src.modules.mv_handler import MvHandler
from src.modules.rm_handler import RmHandler
from src.modules.cat_handler import CatHandler
from src.modules.cp_handler import CpHandler
from src.modules.cd_handler import CdHandler
from src.modules.make_archive_handler import ZipHandler
from src.modules.make_archive_handler import TarHandler
from src.modules.unpack_archive_handler import UnzipHandler
from src.modules.unpack_archive_handler import UntarHandler
from src.modules.logger import logger
from src.modules.grep_handler import GrepHandler

from src.history.history import HistoryManager
from src.history.history_handler import HistoryHandler

from src.undo.undo import UndoHandler

import platform
from typing import Protocol

UNIX = True if platform.system() == "Darwin" else False


class CommandHandler(Protocol):
    def execute(self, args: list[str], shell: "Bash") -> str | None | ValueError: ...


class Bash:
    def __init__(self) -> None:
        self.complex_commands: dict[str, CommandHandler] = {
            "pwd": PwdHandler(),
            "ls": LsHandler(),
            "cd": CdHandler(),
            "rm": RmHandler(),
            "cat": CatHandler(),
            "cp": CpHandler(),
            "mv": MvHandler(),
            "zip": ZipHandler(),
            "unzip": UnzipHandler(),
            "tar": TarHandler(),
            "untar": UntarHandler(),
            "grep": GrepHandler(),
            "history": HistoryHandler(),
            "undo": UndoHandler(),
        }

    def execute(self, command_line: str) -> ValueError | None:
        history_manager = HistoryManager()

        command, args = self.parse_command(command_line)

        logger.info(command_line)
        if command in self.complex_commands:
            result = self.complex_commands[command].execute(args, self)
            if isinstance(result, str) or not result:
                history_manager.add(command, args)
            return result
        else:
            logger.error(f"Command not found: {command}")
            return ValueError(f"Command not found: {command}")

    def parse_command(self, command_line: str) -> tuple[str, list[str]]:
        parts = shlex.split(command_line)
        return parts[0], parts[1::]
