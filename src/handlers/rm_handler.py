import shutil
import os

class RmHandler:
    def execute(self, args: list[str], shell) -> None:
        keys = [arg for arg in args if arg.startswith("-")]
        file = [arg for arg in args if not arg.startswith("-")][0]
        self.handle_rm(keys, file)

    def handle_rm(self, keys: list[str], file: str) -> None:
        try:
            if "-r" in keys or os.path.isdir(file):
                response = input(f"rm: remove write-protected directory '{file}'? ")
                if response.lower() in ['y', 'yes']:
                    shutil.rmtree(file)
            else:
                os.remove(file)
        except PermissionError:
            raise PermissionError(f"rm: Permission denied: '{file}'")
        except FileNotFoundError:
            print(f"rm: Cannot delete '{file}': No such file or directory")
        except Exception as error:
            raise error
