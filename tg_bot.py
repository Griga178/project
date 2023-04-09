from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = "6082839155:AAFoaaNse3yEyqwaw7kPS9USuFBNAhtQ4hM"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    print("запуск send_welcome", msg)
    print(msg.reply_to_message('2'))
    # await msg.reply_to_message(f'Я бот. Приятно познакомиться, {msg.from_user.first_name}')
    await msg.reply_to_message('2')

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
   if msg.text.lower() == 'привет':
       await msg.answer('Привет!')
   else:
       await msg.answer('Не понимаю, что это значит.')


# функции
# задается вопрос принимается ответ (input)
# обращение к User.Tasks

if __name__ == '__main__':
   executor.start_polling(dp)
