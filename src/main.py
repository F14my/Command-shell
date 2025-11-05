from src.bash import Bash
from src.format_input import get_curr_dir


def main() -> None:
    bash = Bash()
    while True:
        try:
            user_input = input(f"{get_curr_dir()}: ")
            bash.execute(user_input)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as error:
            print(error)


if __name__ == "__main__":
    main()
