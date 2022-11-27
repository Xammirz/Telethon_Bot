import os
import logging
import requests
from deep_translator import GoogleTranslator
from telethon import TelegramClient, events
from telethon.tl.custom import Message
import texts
api_id = 11877746
api_hash = 'e8812a280b09564b137b1de49ce06b09'
client = TelegramClient('tests', api_id, api_hash)

with TelegramClient('how_m', api_id, api_hash) as client:
    for message in client.iter_messages('me'):
        print(message.sender_id, ':', message.text)
class Bot(TelegramClient):
    def __init__(self, *args):
        super().__init__(*args)
        self.me = None

def random_dog_url():
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    data = r.json()
    url = data['message']
    return url


def random_cat_url():
    r = requests.get('https://api.thecatapi.com/v1/images/search')
    data = r.json()[0]
    url = data['url']
    return url


bot = Bot('bot', api_id, api_hash)
bot.parse_mode = 'HTML'
logging.basicConfig(level=logging.INFO)


@bot.on(events.NewMessage(func=lambda e: e.text.lower() == 'ты кто'))
async def who_are_you(event: Message):
    await event.reply('Я умный, сделанный умным, в меру нужный бот в полном расцвете сил!')


@bot.on(events.NewMessage(func=lambda e: e.text.lower() == '/start'))
async def help(event: Message):
    await event.reply(texts.star)


@bot.on(events.NewMessage(func=lambda e: e.text.lower() == '/cat'))
async def send_cat(event: Message):
    imgURL = requests.get(random_cat_url()).content
    with open('random_cat.jpg', 'wb') as f:
        f.write(imgURL)
    await event.reply('Вот тебе котик!',
                           file='random_cat.jpg')
    os.remove('random_cat.jpg')


@bot.on(events.NewMessage(func=lambda e: e.text.lower() == '/dog'))
async def send_dog(event: Message):
    imgURL = requests.get(random_dog_url()).content
    with open('random_dog.jpg', 'wb') as f:
        f.write(imgURL)
    await event.reply('СОБАЧКА',file='random_dog.jpg')
    os.remove('random_dog.jpg')


@bot.on(events.NewMessage(func=lambda e: e.text.lower() == '/bored'))
async def bored(event: Message):
    request_actitvity = requests.get('http://www.boredapi.com/api/activity/')
    text_english = request_actitvity.json()['activity']
    text_russian = GoogleTranslator(source='auto', target='ru')
    result = text_russian.translate(text_english)
    await event.reply(result)


@bot.on(events.ChatAction(func=lambda e: (e.user_added or e.user_joined)
                          and e.user_id != bot.me.id))
async def greet(event: events.ChatAction.Event):
    await event.respond('Добро пожаловать!')


async def start():
    # Подключиться к серверу
    await bot.connect()
    
    # Войти через токен. Метод sign_in возвращает информацию о боте. Мы сразу сохраним её в bot.me
    bot.me = await bot.sign_in(bot_token=texts.BOT_TOKEN)
    
    # Начать получать апдейты от Телеграма и запустить все хендлеры
    await bot.run_until_disconnected()

bot.loop.run_until_complete(start())