import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
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
        logger.info(full_command)
        try:
            result = func(self, args, shell)
            logger.info(f"SUCCESS: {self.__class__.__name__}")
            return result
        except Exception as e:
            logger.error(f"ERROR {self.__class__.__name__}: {e}")
            raise
    return wrapper
