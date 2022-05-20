import logging
from logging.handlers import RotatingFileHandler
import os
import time

from dotenv import load_dotenv
import telegram

import parser


RETRY_TIME = 60

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s',
    handlers=[
        RotatingFileHandler(
            filename='fl_new_work_bot.log',
            maxBytes=50000000,
            backupCount=5),
    ]
)
logger = logging.getLogger(__name__)


load_dotenv()
TELEGRAM_TOKEN = os.getenv('TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message(bot, message):
    """Функция для отправки сообщения ботом."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info('Сообщение отправлено успешно')
    except telegram.TelegramError:
        logger.exception('Cбой при отправке сообщения')


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = [
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID
    ]
    for token in tokens:
        if token is None:
            logger.critical(f'отсутствует токен {token}')
            return False
    return True


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    old_data = []
#    current_timestamp = int(time.time())
    while check_tokens():
        try:
            parsed_data = parser.parser()
            for data in parsed_data:
                if data not in old_data:
                    message = data['Задача'] + '\n' + data['Ссылка']
                    send_message(bot, message)
                    time.sleep(3)
            old_data = parsed_data
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)


if __name__ == '__main__':
    main()
