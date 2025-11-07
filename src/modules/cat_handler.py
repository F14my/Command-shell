import os
from src.modules.logger import log_command

class CatHandler:
    """Implementation of 'cat' command.

    Works like Unix 'cat' to display file contents.
    """
    @log_command
    def execute(self, args: list[str], shell) -> None:
        """Run cat command with given arguments."""
        self.handle_cat(args)

    def handle_cat(self, args: list[str]) -> None:
        """Read file and print its contents line by line."""
        path = "".join([arg for arg in args if not arg.startswith("-")])
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = file.readlines()
                for line in data:
                    print(line)
                if not data:
                    print()
        else:
            raise ValueError(f"cat: Cannot open '{path}': Cannot open directory")
