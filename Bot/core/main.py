from core.bot import BotTelegram
import config

if __name__ == '__main__':
    bot = BotTelegram(config.TOKEN_BOT, config.PROXY)
    bot.start_and_work()
