import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import openai

class Reference:
    """
    Stores the previous response from the chatGPT API.
    """
    def __init__(self) -> None:
        self.response = ""

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a reference object to store the previous response
reference = Reference()

# Bot token for BotFather
TOKEN = os.getenv("TOKEN")

# Selected model used from OpenAI API
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    """
    Clears the previous conversation and context.
    """
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    Handler to welcome users and clear previous conversation context.
    """
    clear_past()
    await message.reply("What's up? I'm an AI Bot programmed by @abundancealex!\nWhat can i help you answer?")

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    Handler to clear previous conversation and context.
    """
    clear_past()
    await message.reply("You've cleared our chat memory.")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    Handler to display the help menu.
    """
    help_command = """ 
    Hi there, I'm chatGPT bot created by @abundancealex Please follow these commands -
    /start - to start the conversation 
    /clear - to clear the past conversation and context. 
    /help  - to get this help menu. 
    I hope this helps.
    """ 
    await message.reply(help_command) 

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    Handler to process user input and generate a response from OpenAi API.
    """
    print(f">» USER: \n{message.text}") 
    response = openai.ChatCompletion.create( 
        model=MODEL_NAME, 
        messages=[ 
            {"role": "system", "content": ("You are the Concise Coach, you speak in Dwane Johnsons voice. An assistant that provides brief, supportive advice for complex tasks."
             "You are knowledgeable in various fields and are patient and understanding. "
             "Always strive to break down complicated processes into digestible steps, and avoid overloading users with information.")},
            {"role": "user", "content": "I want to learn programming. Where do I start?"},
            {"role": "assistant", "content": "You got it, buddy! Kick off your programming journey with a versatile language like Python, and remember, just like in the gym, consistency is key!"},
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ]
    ) 
    reference.response = response['choices'][0]['message']['content'] 
    print(f">» chatGPT: \n{reference. response}") 
    await bot.send_message(chat_id=message.chat.id, text=f"{reference.response}") 


if __name__ == '__main__':
    print("Starting...")
    executor.start_polling(dispatcher, skip_updates=True)
    print("Stopped")