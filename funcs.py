import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, ContextTypes, ConversationHandler, ExtBot, filters, MessageHandler



load_dotenv()
TOKEN = os.getenv("nsfg_unhingedbot")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    
)


async def receive_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # assert user, "User not found"
    user_input = update.message.text #update.effective_message.text handles both message and edited_message
    print(f"Received input from {user.id}: {user_input}")
    completion = client.chat.completions.create(
        model="SentientAGI/Dobby-Mini-Unhinged-Plus-Llama-3.1-8B:featherless-ai",
        messages=[
        {
            "role": "user",
            "content": user_input
        }
    ],
    )
    await update.message.reply_text(completion.choices[0].message.content)
    print(f"Response: {completion.choices}")
    return completion.choices

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, receive_input))

    #run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()