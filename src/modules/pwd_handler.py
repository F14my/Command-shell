import os
from src.modules.logger import log_command

class PwdHandler:
    @log_command
    def execute(self, args: list[str], shell) -> None:
        self.handle_pwd(args)

    def handle_pwd(self, args: list[str]) -> None:
        print(f"Current working directory: {os.getcwd().replace("\\", "/")}")
