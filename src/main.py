from src.bash import Bash

def main() -> None:
    bash = Bash()
    while True:
        try:
            user_input = input()
            bash.execute(user_input)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as error:
            print(error)


if __name__ == "__main__":
    main()
