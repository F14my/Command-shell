import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('logs/bash.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('Bash')


def log_command(func):
    def wrapper(self, args, shell):
        command_name = self.__class__.__name__.replace('Handler', '').lower()
        full_command = f"{command_name} {' '.join(args)}"
        try:
            result = func(self, args, shell)
            logger.info(f"SUCCESS: {full_command}")
            return result
        except Exception as e:
            logger.error(f"{self.__class__.__name__} {e}")
            raise

    return wrapper
