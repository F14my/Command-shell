import os

class CatHandler:
    def execute(self, args: list[str], shell) -> None:
        self.handle_cat(args)

    def handle_cat(self, args: list[str]) -> None:
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
