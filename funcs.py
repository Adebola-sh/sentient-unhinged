import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, ContextTypes, CommandHandler,ConversationHandler, ExtBot, filters, MessageHandler



load_dotenv()
TOKEN = os.getenv("nsfg_unhingedbot")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    
)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    assert user
    assert update.effective_chat

    welcome_message = f"""Hello! I am your Unhinged AI Bot built by 
    <a href='https://x.com/nosinglefuck'>NSFG</a> ⬩ (No Single Fucks Given) on X(twitter). 
    \n\nSend me any text and I'll respond with something interesting!"""

  
    await update.effective_chat.send_message(
        welcome_message 
    )


async def receive_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    assert user, "User not found"
    user_input = update.message.text #update.effective_message.text handles both message and edited_message
    print(f"Received input from {user.username}: {user_input}")
    if user_input.lower() in ["/start", "/help"]:
        await start_handler(update, context)
        return
    else:
        try:
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
            print(f"Response: {completion.choices[0].message.content}")
            return completion.choices[0].message.content
        except APIConnectionError as e:
            error_message = "Sorry, I'm having trouble connecting to the AI service right now. Please try again later."
            await update.message.reply_text(error_message)
            print(f"APIConnectionError: {e}")
            return error_message

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, receive_input))
    application.add_handler(CommandHandler("start", start_handler))

    #run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()