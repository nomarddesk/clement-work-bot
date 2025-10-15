import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# --- Configuration ---
BOT_TOKEN = "8344380865:AAHJ3U860YnHoANuiBuPUcJvmNsZvTx6zhU"  # Get this from BotFather on Telegram
TELEGRAM_CHANNEL_LINK = "https://t.me/AICCTOKEN1"
INSTAGRAM_LINK = "https://www.instagram.com/aicctoken1"
DISCORD_LINK = "https://discord.com/invite/zcudDUgqSr"
YOUTUBE_LINK = "https://www.youtube.com/@aicc-token2025"
TIKTOK_LINK = "https://www.tiktok.com/@aicctoken1"
# TWITTER_LINK has been removed as per the new flow
MIN_REFERRALS_FOR_WITHDRAWAL = 10
REWARD_PER_TASK = 1  # Reward for completing one task
REWARD_PER_REFERRAL = 3 # Reward for one successful referral
DATA_FILE = "airdrop_data.json"

# --- Bot Logic ---

# Enable logging to see errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for the conversation (AWAIT_TWITTER_FOLLOW removed)
(
    START_ROUTES,
    AWAIT_CHANNEL_JOIN,
    AWAIT_INSTAGRAM_FOLLOW,
    AWAIT_DISCORD_JOIN,
    AWAIT_YOUTUBE_SUBSCRIBE,
    AWAIT_TIKTOK_FOLLOW,
    MAIN_MENU,
    AWAIT_WALLET_ADDRESS,
) = range(8)

# --- Data Handling Functions ---

def load_user_data():
    """Loads user data from a JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_user_data(data):
    """Saves user data to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Helper Functions ---

def get_user_id_str(update: Update):
    """Gets the user's ID as a string."""
    return str(update.effective_user.id)

def escape_markdown(text: str) -> str:
    """Helper function to escape telegram markdown characters."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)


# --- Task Prompting Functions ---

async def ask_to_join_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Task 1: Asks the user to join the Telegram channel."""
    logger.info(f"Asking user {get_user_id_str(update)} to join Telegram channel.")
    keyboard = [[InlineKeyboardButton("Join Channel", url=TELEGRAM_CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 1: Please join our Telegram Channel\\.\n\n"
        "After joining, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def ask_to_follow_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Task 2: Asks the user to follow on Instagram."""
    logger.info(f"Asking user {get_user_id_str(update)} to follow Instagram.")
    keyboard = [[InlineKeyboardButton("Follow on Instagram", url=INSTAGRAM_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 2: Please follow our official Instagram account\\.\n\n"
        "After following, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def ask_to_join_discord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Task 3: Asks the user to join the Discord server."""
    logger.info(f"Asking user {get_user_id_str(update)} to join Discord.")
    keyboard = [[InlineKeyboardButton("Join Discord", url=DISCORD_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 3: Please join our Discord Server\\.\n\n"
        "After joining, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def ask_to_subscribe_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Task 4: Asks the user to subscribe on YouTube."""
    logger.info(f"Asking user {get_user_id_str(update)} to subscribe to YouTube.")
    keyboard = [[InlineKeyboardButton("Subscribe on YouTube", url=YOUTUBE_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 4: Please subscribe to our YouTube Channel\\.\n\n"
        "After subscribing, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def ask_to_follow_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Task 5: Asks the user to follow on TikTok."""
    logger.info(f"Asking user {get_user_id_str(update)} to follow TikTok.")
    keyboard = [[InlineKeyboardButton("Follow on TikTok", url=TIKTOK_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 5: Please follow our TikTok account\\.\n\n"
        "After following, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def ask_for_wallet_address_as_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Final Task: Asks for BNB wallet address."""
    logger.info(f"Asking user {get_user_id_str(update)} for wallet address as final task.")
    message = (
        "🎉 All social tasks completed\\!\n\n"
        "For the final task, please submit your BNB \\(BEP\\-20\\) address to get your airdrop tokens\\."
    )
    await update.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)


# --- Conversation Handler Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the bot interaction.
    Handles new users and referrals.
    """
    user = update.effective_user
    user_id = get_user_id_str(update)
    logger.info(f"User {user.id} ({user.username}) started the bot.")
    data = load_user_data()

    # Check if user is already in the system
    if user_id in data:
        if data[user_id].get("tasks_completed", False):
            logger.info(f"User {user_id} is already registered and completed tasks. Showing main menu.")
            await show_main_menu(update, context, "Welcome back!")
            return MAIN_MENU
        else:
            # User started but didn't finish, restart the process
            logger.info(f"User {user_id} is restarting the tasks.")
            await update.message.reply_text(
                "Welcome back! It looks like you haven't completed all the tasks yet. Let's start from the beginning."
            )
    else:
        # New user
        logger.info(f"New user {user_id} is starting the airdrop.")
        data[user_id] = {
            "username": user.username,
            "tasks_completed": False,
            "referrals": 0,
            "balance": 0,
            "wallet_address": None,
            "referred_by": None,
        }
        await update.message.reply_text(
            f"Welcome to the AICC Airdrop, {user.first_name}!\n\n"
            "Complete a few simple tasks to earn AICC tokens."
        )

        # Handle referral
        if context.args:
            referrer_id = context.args[0]
            if referrer_id in data and referrer_id != user_id:
                data[user_id]["referred_by"] = referrer_id
                logger.info(f"User {user_id} was referred by {referrer_id}")

    save_user_data(data)
    await ask_to_join_channel(update, context)
    return AWAIT_CHANNEL_JOIN


async def handle_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to join the channel."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} submitted proof for Telegram channel.")
    data = load_user_data()
    data[user_id]["balance"] += REWARD_PER_TASK
    save_user_data(data)

    message = (
        "Thank you for your submission\\.\n\n"
        "⚠️ *Important:* Hope you didn't cheat the system\\. All tasks will be verified manually "
        "before your airdrop withdrawal is processed\\.\n\n"
        "Now for the next task\\."
    )
    await update.message.reply_text(
        message,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    
    await ask_to_follow_instagram(update, context)
    return AWAIT_INSTAGRAM_FOLLOW


async def handle_instagram_follow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to follow on Instagram."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} submitted proof for Instagram.")
    data = load_user_data()
    data[user_id]["balance"] += REWARD_PER_TASK
    save_user_data(data)

    message = (
        "Thank you for your submission\\.\n\n"
        "⚠️ *Important:* Hope you didn't cheat the system\\. All tasks will be verified manually "
        "before your airdrop withdrawal is processed\\.\n\n"
        "Now for the next task\\."
    )
    await update.message.reply_text(
        message,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    
    await ask_to_join_discord(update, context)
    return AWAIT_DISCORD_JOIN


async def handle_discord_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to join Discord."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} submitted proof for Discord.")
    data = load_user_data()
    data[user_id]["balance"] += REWARD_PER_TASK
    save_user_data(data)

    message = (
        "Thank you for your submission\\.\n\n"
        "⚠️ *Important:* Hope you didn't cheat the system\\. All tasks will be verified manually "
        "before your airdrop withdrawal is processed\\.\n\n"
        "Now for the next task\\."
    )
    await update.message.reply_text(
        message,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    
    await ask_to_subscribe_youtube(update, context)
    return AWAIT_YOUTUBE_SUBSCRIBE


async def handle_youtube_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to subscribe on YouTube."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} submitted proof for YouTube.")
    data = load_user_data()
    data[user_id]["balance"] += REWARD_PER_TASK
    save_user_data(data)

    message = (
        "Thank you for your submission\\.\n\n"
        "⚠️ *Important:* Hope you didn't cheat the system\\. All tasks will be verified manually "
        "before your airdrop withdrawal is processed\\.\n\n"
        "Now for the final social task\\."
    )
    await update.message.reply_text(
        message,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    
    await ask_to_follow_tiktok(update, context)
    return AWAIT_TIKTOK_FOLLOW


async def handle_tiktok_follow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to follow on TikTok, now the final social task."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} submitted proof for TikTok. All social tasks complete.")
    data = load_user_data()

    # Final social task reward
    data[user_id]["balance"] += REWARD_PER_TASK
    data[user_id]["tasks_completed"] = True

    # Check for referral and reward the referrer
    referrer_id = data[user_id].get("referred_by")
    if referrer_id and referrer_id in data:
        data[referrer_id]["referrals"] += 1
        data[referrer_id]["balance"] += REWARD_PER_REFERRAL
        logger.info(f"User {referrer_id} referral count incremented by user {user_id}.")

    save_user_data(data)
    
    await ask_for_wallet_address_as_task(update, context)
    return AWAIT_WALLET_ADDRESS


async def save_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the user's wallet address after tasks are completed."""
    wallet_address = update.message.text
    user_id = get_user_id_str(update)
    data = load_user_data()

    # Basic validation for wallet address
    if not (wallet_address.startswith("0x") and len(wallet_address) == 42):
         logger.warning(f"User {user_id} submitted an invalid wallet address: {wallet_address}")
         await update.message.reply_text("That doesn't look like a valid BEP-20 wallet address. It should start with '0x' and be 42 characters long. Please try again.")
         return AWAIT_WALLET_ADDRESS

    data[user_id]["wallet_address"] = wallet_address
    save_user_data(data)

    logger.info(f"User {user_id} successfully submitted wallet: {wallet_address}")
    
    message = (
        "Thank you\\! Your wallet address has been saved\\.\n\n"
        "The final step is to invite friends\\. While this is optional, you need "
        f"*{MIN_REFERRALS_FOR_WITHDRAWAL} successful referrals* to unlock your airdrop withdrawal\\.\n\n"
        "Click the button in the menu below to get your unique referral link\\."
    )
    
    await update.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)
    await show_main_menu(update, context, "You can now check your balance or get your referral link to invite friends\\.")
    return MAIN_MENU


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Displays the main menu keyboard."""
    logger.info(f"Showing main menu to user {get_user_id_str(update)}.")
    keyboard = [
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("🔗 Get Referral Link", callback_data="referral")],
        [InlineKeyboardButton("💸 Withdraw Status", callback_data="withdraw")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # If called from a button press, use the query object
    if update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=reply_markup)
    else: # If called from a message command
        await update.message.reply_text(text, reply_markup=reply_markup)


async def balance_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the 'Balance' button press."""
    query = update.callback_query
    await query.answer()
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} requested their balance.")
    data = load_user_data()
    
    balance = data.get(user_id, {}).get("balance", 0)
    referrals = data.get(user_id, {}).get("referrals", 0)

    await query.message.reply_text(
        f"Your current status:\n\n"
        f"💰 Balance: ${balance} AICC\n"
        f"👥 Referrals: {referrals}"
    )
    return MAIN_MENU


async def referral_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the 'Referral Link' button press."""
    query = update.callback_query
    await query.answer()
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} requested their referral link.")
    bot_username = (await context.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    message = (
        f"Your unique referral link is:\n\n`{escape_markdown(referral_link)}`\n\n"
        f"Share this link with your friends\\. You will earn ${REWARD_PER_REFERRAL} AICC for each friend who joins and completes all the tasks\\."
    )

    await query.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)
    return MAIN_MENU


async def withdraw_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the 'Withdraw' button press, which now acts as a status check."""
    query = update.callback_query
    await query.answer()
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} initiated withdrawal status check.")
    data = load_user_data()
    user_data = data.get(user_id, {})

    if not user_data.get("wallet_address"):
        await query.message.reply_text("You must complete all the tasks to submit your wallet address first.")
        return MAIN_MENU

    wallet_address_md = f"`{escape_markdown(user_data['wallet_address'])}`"
    if user_data.get("referrals", 0) >= MIN_REFERRALS_FOR_WITHDRAWAL:
        logger.info(f"User {user_id} is eligible for withdrawal.")
        message = (
            "Congratulations\\! You have met the referral requirement\\.\n\n"
            "Your airdrop will be sent to your saved address after manual verification of your tasks\\.\n\n"
            f"Your saved address: {wallet_address_md}"
        )
        await query.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)
    else:
        needed = MIN_REFERRALS_FOR_WITHDRAWAL - user_data.get("referrals", 0)
        logger.info(f"User {user_id} is not yet eligible for withdrawal.")
        message = (
            "You are not yet eligible for withdrawal\\.\n"
            f"You need at least *{MIN_REFERRALS_FOR_WITHDRAWAL}* referrals\\. You currently have *{user_data.get('referrals', 0)}*\\.\n"
            f"You need *{needed}* more\\.\n\n"
            "Your airdrop will be sent to your saved address once you meet the requirement\\.\n\n"
            f"Your saved address: {wallet_address_md}"
        )
        await query.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)
        
    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user_id = get_user_id_str(update)
    logger.info(f"User {user_id} cancelled the conversation.")
    await update.message.reply_text("Action cancelled.")
    return ConversationHandler.END

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # A more robust filter that accepts any message type for task submissions, but ignores commands.
    submission_filter = filters.ALL & (~filters.COMMAND)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_CHANNEL_JOIN: [MessageHandler(submission_filter, handle_channel_join)],
            AWAIT_INSTAGRAM_FOLLOW: [MessageHandler(submission_filter, handle_instagram_follow)],
            AWAIT_DISCORD_JOIN: [MessageHandler(submission_filter, handle_discord_join)],
            AWAIT_YOUTUBE_SUBSCRIBE: [MessageHandler(submission_filter, handle_youtube_subscribe)],
            AWAIT_TIKTOK_FOLLOW: [MessageHandler(submission_filter, handle_tiktok_follow)],
            MAIN_MENU: [
                CallbackQueryHandler(balance_button, pattern="^balance$"),
                CallbackQueryHandler(referral_button, pattern="^referral$"),
                CallbackQueryHandler(withdraw_button, pattern="^withdraw$"),
            ],
            AWAIT_WALLET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_wallet)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Add the error handler
    application.add_error_handler(error_handler)

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()

