import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# --- Configuration ---
# IMPORTANT: Replace these values with your actual data
BOT_TOKEN = "8344380865:AAHJ3U860YnHoANuiBuPUcJvmNsZvTx6zhU"  # Get this from BotFather on Telegram
TELEGRAM_CHANNEL_LINK = "YOUR_AICC_TELEGRAM_CHANNEL_LINK_HERE"
TWITTER_LINK = "YOUR_AICC_X_PROFILE_LINK_HERE"
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

# Define states for the conversation
(
    START_ROUTES,
    AWAIT_CHANNEL_JOIN,
    AWAIT_TWITTER_FOLLOW,
    MAIN_MENU,
    AWAIT_WALLET_ADDRESS,
) = range(5)

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


# --- Conversation Handler Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the bot interaction.
    Handles new users and referrals.
    """
    user = update.effective_user
    user_id = get_user_id_str(update)
    data = load_user_data()

    # Check if user is already in the system
    if user_id in data:
        if data[user_id].get("tasks_completed", False):
            await show_main_menu(update, context, "Welcome back!")
            return MAIN_MENU
        else:
            # User started but didn't finish, restart the process
            await update.message.reply_text(
                "Welcome back! It looks like you haven't completed all the tasks yet. Let's start from the beginning."
            )
            # Fallthrough to start the tasks
    else:
        # New user
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
    return await ask_to_join_channel(update, context)


async def ask_to_join_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Task 1: Asks the user to join the Telegram channel."""
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
    return AWAIT_CHANNEL_JOIN


async def handle_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to join the channel."""
    user_id = get_user_id_str(update)
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
    
    return await ask_to_follow_twitter(update, context)


async def ask_to_follow_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Task 2: Asks the user to follow on Twitter."""
    keyboard = [[InlineKeyboardButton("Follow on X (Twitter)", url=TWITTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "Task 2: Please follow our official X (Twitter) account\\.\n\n"
        "After following, please send a screenshot as proof\\.\n\n"
        "*Warning:* Do not attempt to cheat the system\\. All task submissions are manually verified, "
        "and submitting fake proof will result in your withdrawal being declined\\."
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    return AWAIT_TWITTER_FOLLOW


async def handle_twitter_follow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response after asking to follow on Twitter and completes the tasks."""
    user_id = get_user_id_str(update)
    data = load_user_data()

    # Final task reward
    data[user_id]["balance"] += REWARD_PER_TASK
    data[user_id]["tasks_completed"] = True

    # Check for referral and reward the referrer
    referrer_id = data[user_id].get("referred_by")
    if referrer_id and referrer_id in data:
        data[referrer_id]["referrals"] += 1
        data[referrer_id]["balance"] += REWARD_PER_REFERRAL
        logger.info(f"User {referrer_id} referral count incremented.")

    save_user_data(data)

    message = (
        "🎉 All tasks completed\\! Thank you for your participation\\.\n\n"
        "⚠️ *Important:* Hope you didn't cheat the system\\. All tasks will be verified manually before your airdrop withdrawal is processed\\."
    )
    await update.message.reply_text(
        message,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )
    await show_main_menu(update, context, "You can now check your balance or get your referral link.")
    return MAIN_MENU


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Displays the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("🔗 Get Referral Link", callback_data="referral")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
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
    bot_username = (await context.bot.get_me()).username
    referral_link = f"https.t.me/{bot_username}?start={user_id}"

    message = (
        f"Your unique referral link is:\n\n`{escape_markdown(referral_link)}`\n\n"
        f"Share this link with your friends\\. You will earn ${REWARD_PER_REFERRAL} AICC for each friend who joins and completes all the tasks\\."
    )

    await query.message.reply_text(message, parse_mode=constants.ParseMode.MARKDOWN_V2)
    return MAIN_MENU


async def withdraw_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the 'Withdraw' button press."""
    query = update.callback_query
    await query.answer()
    user_id = get_user_id_str(update)
    data = load_user_data()
    user_data = data.get(user_id, {})

    if user_data.get("wallet_address"):
        await query.message.reply_text(f"You have already submitted your wallet address: `{escape_markdown(user_data['wallet_address'])}`", parse_mode=constants.ParseMode.MARKDOWN_V2)
        return MAIN_MENU

    if user_data.get("referrals", 0) >= MIN_REFERRALS_FOR_WITHDRAWAL:
        await query.message.reply_text(
            "Congratulations! You are eligible for withdrawal.\n\n"
            "Please enter your BEP-20 (Binance Smart Chain) wallet address to receive your AICC tokens."
        )
        return AWAIT_WALLET_ADDRESS
    else:
        needed = MIN_REFERRALS_FOR_WITHDRAWAL - user_data.get("referrals", 0)
        await query.message.reply_text(
            f"You are not yet eligible for withdrawal.\n"
            f"You need at least {MIN_REFERRALS_FOR_WITHDRAWAL} referrals to withdraw.\n"
            f"You currently have {user_data.get('referrals', 0)} referrals. You need {needed} more."
        )
        return MAIN_MENU


async def save_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the user's wallet address."""
    wallet_address = update.message.text
    user_id = get_user_id_str(update)
    data = load_user_data()

    # Basic validation for wallet address (can be improved)
    if not (wallet_address.startswith("0x") and len(wallet_address) == 42):
         await update.message.reply_text("That doesn't look like a valid wallet address. Please try again.")
         return AWAIT_WALLET_ADDRESS

    data[user_id]["wallet_address"] = wallet_address
    save_user_data(data)

    logger.info(f"User {user_id} submitted wallet: {wallet_address}")
    await update.message.reply_text(
        "Thank you! Your wallet address has been saved.\n"
        "We will process your airdrop distribution after manual verification. Please be patient."
    )
    await show_main_menu(update, context, "You can still check your balance or invite more friends.")
    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Action cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_CHANNEL_JOIN: [MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_channel_join)],
            AWAIT_TWITTER_FOLLOW: [MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_twitter_follow)],
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

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()

