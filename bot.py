import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = '5962225082:AAEXpaOlYM1xJbal1EYp4F4_C8Any9Rccbo'
TELEGRAM_API_BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
NEWS_API_BASE_URL = 'https://newsapi.org/v2'
NEWS_API_KEY = '2c3c2198c93640868409c2b898458a30'

NEWS_COMMAND = '/news'

def get_latest_news(category):
    """Retrieve the latest news from News API"""
    url = f'{NEWS_API_BASE_URL}/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'country': 'tr',  # Replace with the desired country code
        'category': category,
        'pageSize': 10  # Specify the number of news articles to retrieve
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    news_data = response.json()
    return news_data

def handle_command(update: Update, context: CallbackContext):
    """Handle incoming commands from Telegram users"""
    chat_id = update.message.chat_id
    command = update.message.text
    if command == '/start':
        # Send the start page to the user
        keyboard = [[InlineKeyboardButton("Get News", callback_data='news')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id, "Welcome to the News Bot! Click the button below to get started.", reply_markup=reply_markup)
    elif command == '/news':
        # Send the news menu to the user
        keyboard = [
            [InlineKeyboardButton("Business", callback_data='business')],
            [InlineKeyboardButton("Entertainment", callback_data='entertainment')],
            [InlineKeyboardButton("Health", callback_data='health')],
            [InlineKeyboardButton("Science", callback_data='science')],
            [InlineKeyboardButton("Sports", callback_data='sports')],
            [InlineKeyboardButton("Technology", callback_data='technology')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id, 'Please choose a category:', reply_markup=reply_markup)
    else:
        # Handle unknown commands
        context.bot.send_message(chat_id, 'Unknown command. Please use /start to get started.')

def handle_callback(update: Update, context: CallbackContext):
    """Handle incoming callback queries from Telegram users"""
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data
    if data == 'news':
        # Send the news menu to the user
        keyboard = [
            [InlineKeyboardButton("Business", callback_data='business')],
            [InlineKeyboardButton("Entertainment", callback_data='entertainment')],
            [InlineKeyboardButton("Health", callback_data='health')],
            [InlineKeyboardButton("Science", callback_data='science')],
            [InlineKeyboardButton("Sports", callback_data='sports')],
            [InlineKeyboardButton("Technology", callback_data='technology')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Please choose a category:', reply_markup=reply_markup)
    elif data in ['business', 'entertainment', 'health', 'science', 'sports', 'technology']:
        # Retrieve and send the latest news for the selected category
        try:
            news_data = get_latest_news(data)
            articles = news_data['articles']
            for article in articles:
                title = article['title']
                description = article['description']
                url = article['url']
                # Format the news article as a text message
                text = f'*{title}*\n{description}\nRead more: {url}'
                context.bot.send_message(chat_id, text, parse_mode='Markdown')
        except Exception as e:
            # Handle any errors that may occur during news retrieval
            context.bot.send_message(chat_id, 'Failed to retrieve news. Please try again later.')
            print(e)

def main():
    """Main function to handle incoming updates from Telegram"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_command))
    dispatcher.add_handler(CommandHandler('news', handle_command))
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()