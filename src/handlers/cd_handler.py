import os

class CdHandler:
    def execute(self, args: list[str], shell) -> None:
        self.handle_cd(args)

    def handle_cd(self, args: list[str]):
        if not args:
            path = os.path.expanduser("~")
        else:
            path = "".join(args).replace("/", "\\")
            if path.startswith("~"):
                path = os.path.expanduser("~") + path[1::]
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"cd: cannot find '{path}': No such directory")
