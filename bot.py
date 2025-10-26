import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
# !!! IMPORTANT: Fill these in with your information !!!
YOUR_PLAYGROUND_NAME = "My Awesome Playground"  # The *exact name* to search for in Fortnite
YOUR_PLAYGROUND_LINK = "https://your-fortnite-playground-link.com"  # The direct link for existing players
HELPFUL_CHANNEL_LINK = "https://t.me/rejoinsnousetgagne" # Your main channel
# !!!!!!!!!!!!!!!!!!!!!


# --- LANGUAGE STRINGS ---
STRINGS = {
    'en': {
        'disclaimer': (
            "**Disclaimer:** This bot is an unofficial guide and is not affiliated with "
            "Epic Games or Fortnite. We will *never* ask for your password."
        ),
        'lang_prompt': "Please select your language:",
        'welcome': (
            "Welcome! You're diving into an immersive gaming adventure. "
            "This bot will help you set up your account, join the game, and start playing."
        ),
        'main_menu_text': "Please choose an option from the menu below:",
        # --- BUTTONS ---
        'new_player_btn': "New player",
        'existing_player_btn': "Existing player",
        'helpful_channel_btn': "Full guide in channel",
        'support_btn': "Support",
        'back_btn': "⬅️ Back to Main Menu",
        'yes_btn': "Yes",
        'no_btn': "No",
        
        # --- SHARED MESSAGES ---
        'go_to_channel': "Please see our channel for instructions on this step.",
        'go_to_channel_btn': "Go to Channel",
        'influencer_q': "Were you introduced to this game by an influencer?",
        'influencer_prompt': "Please provide the influencer's name or @username:",
        'influencer_thanks': "Thank you! We have noted the influencer's name.",
        'influencer_no': "Got it. Please see our channel for the next instruction.",
        'play_130_hours_q': "Did you start the game and play 130 hours for free this week?",
        'play_130_hours_no': "You have to start the game and play every single day for free before progressing.\n\nAre you able to play at least 130 hours a week?",
        'play_130_hours_no_b2': "Please see our channel for instructions on managing your time.",
        'like_q': "With your account, will you click on the like button every single time before your 1 hour play session ended during your 130 hours of play this week?",
        'like_no': "You have to click on the like button every single time before your 1 hour play session ended.\n\nDo you want our guidance on that?",
        'like_no_b1': "Please see our channel for instruction 11.",
        'like_no_b2_existing': "Okay. I will play and let you know in the support session later on.",
        'like_no_b2_new': "Okay. I will play and let you know in the support session later on.",
        'like_no_b2_support': "I have proof that I played 130 hours this week and I liked every single time, and I am wishing to share it with you guys.",
        'save_favorite_q': "Did you save the reward Island to your favorites?",
        'save_favorite_no': "You have to save the reward Island to your favorites and play.\n\nDo you want our guidance on that?",
        'save_favorite_no_b1': "Please see our channel for instruction 12.",
        'save_favorite_no_b2': "I have proof I saved the reward Island to my favorites and I actually play on it.",
        'find_island_q': "Have you searched and found the reward Island?",
        'find_island_no': "You have to search the reward Island in the search bar and just choose it.\n\nDo you want our guidance for that?",
        'find_island_no_b1': "Here are the best codes to play. Just copy one of them and enter it on the search bar:\n\n`CODE123`\n`ISLAND456`\n`MAP789`",
        'find_island_no_b2': "Okay, I already chose one code.",
        'follow_setup_q': "Did you follow the full setup to be able to play with friends and progress together without any worries?",
        'follow_setup_no': "You have to follow the exact setup. Do you need our guidance?",
        'follow_setup_no_b1': "Please see our channel and look at instruction 9.",
        'follow_setup_no_b2': "No, I finally fixed everything, I want to move to the next step.",
        'use_vpn_q': "Did you use a VPN?",
        'use_vpn_no': "Please download and use a VPN set to the USA before going any further to create all your authentic profiles. To play, you don't need to use it.\n\nDid you finally use a VPN?",
        'use_vpn_no_b2': "Please see our channel for guidance on VPNs.",
        'create_cloud_profile_q': "Did you already create a cloud gaming profile?",
        'create_cloud_profile_no': "Please create a cloud gaming profile. Do you want our assistance?",
        'create_cloud_profile_no_b1': "Use this link to get started:",
        'create_cloud_profile_no_b1_btn': "Go to Xbox Cloud Gaming",
        'create_cloud_profile_no_b2': "I already have one, I want the next step.",
        'receive_epic_code_q': "Did you receive the code from Epic Games to activate your cloud gaming account?",
        'receive_epic_code_no': "Please, you have to receive the code. Do you want our guidance to help you with that?",
        'receive_epic_code_no_b1': "Use this link to activate:",
        'receive_epic_code_no_b1_btn': "Go to EpicGames.com/activate",
        'receive_epic_code_no_b2': "Please see our channel for help.",
        'create_epic_profile_q': "Did you create your Epic Games profile?",
        'create_epic_profile_no': "Please, you have to create your Epic Games profile. Do you need our guidance?",
        'create_epic_profile_no_b1': "Use this link to create your profile:",
        'create_epic_profile_no_b1_btn': "Go to EpicGames.com",
        'create_epic_profile_no_b2': "Please see our channel for help.",
        'create_shortcut_q': "Did you create a shortcut of the cloud gaming to play it like an installed app directly from your Homescreen?",
        'create_shortcut_no': "You have to create a shortcut to play Fortnite from your homescreen. Do you want our guidance with that?",
        'create_shortcut_no_b1': "Please see our channel for this guide.",
        'create_shortcut_no_b2': "No, I finally created a shortcut.",
        'launch_game_q': "Have you launched the game?",
        'launch_game_no': "You have to launch the game. Do you need our guidance?",
        'launch_game_no_b1': "Use this link to launch the game:",
        'launch_game_no_b1_btn': "Launch Fortnite on Xbox Cloud",
        'launch_game_no_b2': "Please see our channel for help.",

        # --- NEW PLAYER ---
        'new_player_start': (
            "You're diving into an immersive gaming adventure. This bot will help you set up your account, join the game, start playing and progressing.\n\n"
            "**Cloud Gaming Reminder:**\n"
            "Your session lasts for 1 hour. The game will close, and you will have to launch it again to keep playing."
        ),
        
        # --- EXISTING PLAYER ---
        'existing_player_start': (
            "Welcome back!\n\n"
            "**Cloud Gaming Reminder:**\n"
            "Your session lasts for 1 hour. The game will close, and you will have to launch it again to keep playing. "
            "You probably know this since you already followed all the instructions."
        ),
        
        # --- SUPPORT ---
        'support_start': (
            "In order to get in touch with us, you need to answer these questions so we can determine which stage of the process you’re at. "
            "If everything has been done correctly, you’ll be able to receive your reward."
        ),
        'support_final_q': "Make sure you completed every single step before sending us your @. Did you complete every single step and play at least 130 hours this week?",
        'support_final_yes': "Okay, please type your Telegram @username (like @myusername) and you will be contacted soon. By providing your @username, you consent to our support team contacting you directly.",
        'support_final_no': "Please complete all steps in the channel guides first.",
        'support_thanks': "Thank you! Your @username has been noted. We will get in touch with you as soon as possible.",
        'invalid_username': "That doesn't look like a valid @username. Please start with '@' and try again, or type /cancel.",
    },
    'fr': {
        'disclaimer': (
            "**Avertissement :** Ce bot est un guide non officiel et n'est pas affilié à "
            "Epic Games ou Fortnite. Nous ne vous demanderons *jamais* votre mot de passe."
        ),
        'lang_prompt': "Veuillez sélectionner votre langue :",
        'welcome': (
            "Bienvenue ! Tu plonges dans une aventure de jeu immersive. "
            "Ce bot t'aidera à configurer ton compte, à rejoindre la partie et à commencer à jouer."
        ),
        'main_menu_text': "Veuillez choisir une option dans le menu ci-dessous :",
        # --- BUTTONS ---
        'new_player_btn': "Nouveau joueur",
        'existing_player_btn': "Joueur existant",
        'helpful_channel_btn': "Guide complet sur le canal",
        'support_btn': "Support",
        'back_btn': "⬅️ Retour au Menu Principal",
        'yes_btn': "Oui",
        'no_btn': "Non",
        
        # --- SHARED MESSAGES ---
        'go_to_channel': "Veuillez consulter notre canal pour les instructions sur cette étape.",
        'go_to_channel_btn': "Aller au Canal",
        'influencer_q': "Avez-vous été introduit à ce jeu par un influenceur ?",
        'influencer_prompt': "Veuillez fournir le nom ou le @username de l'influenceur :",
        'influencer_thanks': "Merci ! Nous avons noté le nom de l'influenceur.",
        'influencer_no': "Compris. Veuillez consulter notre canal pour la prochaine instruction.",
        'play_130_hours_q': "Avez-vous commencé le jeu et joué 130 heures gratuitement cette semaine ?",
        'play_130_hours_no': "Vous devez commencer le jeu et jouer chaque jour gratuitement avant de progresser.\n\nÊtes-vous capable de jouer au moins 130 heures par semaine ?",
        'play_130_hours_no_b2': "Veuillez consulter notre canal pour des instructions sur la gestion de votre temps.",
        'like_q': "Avec votre compte, cliquerez-vous sur le bouton 'J'aime' à chaque fois avant la fin de votre session de jeu d'une heure pendant vos 130 heures de jeu cette semaine ?",
        'like_no': "Vous devez cliquer sur le bouton 'J'aime' à chaque fois avant la fin de votre session d'une heure.\n\nVoulez-vous notre aide pour cela ?",
        'like_no_b1': "Veuillez consulter notre canal pour l'instruction 11.",
        'like_no_b2_existing': "D'accord. Je jouerai et vous le ferai savoir dans la session de support plus tard.",
        'like_no_b2_new': "D'accord. Je jouerai et vous le ferai savoir dans la session de support plus tard.",
        'like_no_b2_support': "J'ai la preuve que j'ai joué 130 heures cette semaine et que j'ai 'aimé' à chaque fois, et je souhaite la partager avec vous.",
        'save_favorite_q': "Avez-vous sauvegardé l'île de récompense dans vos favoris ?",
        'save_favorite_no': "Vous devez sauvegarder l'île de récompense dans vos favoris et y jouer.\n\nVoulez-vous notre aide pour cela ?",
        'save_favorite_no_b1': "Veuillez consulter notre canal pour l'instruction 12.",
        'save_favorite_no_b2': "J'ai la preuve que j'ai sauvegardé l'île de récompense dans mes favoris et que j'y joue actuellement.",
        'find_island_q': "Avez-vous cherché et trouvé l'île de récompense ?",
        'find_island_no': "Vous devez chercher l'île de récompense dans la barre de recherche et la choisir.\n\nVoulez-vous notre aide pour cela ?",
        'find_island_no_b1': "Voici les meilleurs codes pour jouer. Copiez-en un et entrez-le dans la barre de recherche :\n\n`CODE123`\n`ISLAND456`\n`MAP789`",
        'find_island_no_b2': "D'accord, j'ai déjà choisi un code.",
        'follow_setup_q': "Avez-vous suivi la configuration complète pour pouvoir jouer avec des amis et progresser ensemble sans soucis ?",
        'follow_setup_no': "Vous devez suivre la configuration exacte. Avez-vous besoin de notre aide ?",
        'follow_setup_no_b1': "Veuillez consulter notre canal et regarder l'instruction 9.",
        'follow_setup_no_b2': "Non, j'ai finalement tout arrangé, je veux passer à l'étape suivante.",
        'use_vpn_q': "Avez-vous utilisé un VPN ?",
        'use_vpn_no': "Veuillez télécharger et utiliser un VPN localisé aux États-Unis avant d'aller plus loin pour créer tous vos profils authentiques. Pour jouer, vous n'avez pas besoin de l'utiliser.\n\nAvez-vous finalement utilisé un VPN ?",
        'use_vpn_no_b2': "Veuillez consulter notre canal pour obtenir de l'aide sur les VPN.",
        'create_cloud_profile_q': "Avez-vous déjà créé un profil de cloud gaming ?",
        'create_cloud_profile_no': "Veuillez créer un profil de cloud gaming. Voulez-vous notre assistance ?",
        'create_cloud_profile_no_b1': "Utilisez ce lien pour commencer :",
        'create_cloud_profile_no_b1_btn': "Aller sur Xbox Cloud Gaming",
        'create_cloud_profile_no_b2': "J'en ai déjà un, je veux l'étape suivante.",
        'receive_epic_code_q': "Avez-vous reçu le code d'Epic Games pour activer votre compte de cloud gaming ?",
        'receive_epic_code_no': "S'il vous plaît, vous devez recevoir le code. Voulez-vous notre aide pour cela ?",
        'receive_epic_code_no_b1': "Utilisez ce lien pour activer :",
        'receive_epic_code_no_b1_btn': "Aller sur EpicGames.com/activate",
        'receive_epic_code_no_b2': "Veuillez consulter notre canal pour obtenir de l'aide.",
        'create_epic_profile_q': "Avez-vous créé votre profil Epic Games ?",
        'create_epic_profile_no': "S'il vous plaît, vous devez créer votre profil Epic Games. Avez-vous besoin de notre aide ?",
        'create_epic_profile_no_b1': "Utilisez ce lien pour créer votre profil :",
        'create_epic_profile_no_b1_btn': "Aller sur EpicGames.com",
        'create_epic_profile_no_b2': "Veuillez consulter notre canal pour obtenir de l'aide.",
        'create_shortcut_q': "Avez-vous créé un raccourci du cloud gaming pour y jouer comme une application installée directement depuis votre écran d'accueil ?",
        'create_shortcut_no': "Vous devez créer un raccourci pour jouer à Fortnite depuis votre écran d'accueil. Voulez-vous notre aide pour cela ?",
        'create_shortcut_no_b1': "Veuillez consulter notre canal pour ce guide.",
        'create_shortcut_no_b2': "Non, j'ai finalement créé un raccourci.",
        'launch_game_q': "Avez-vous lancé le jeu ?",
        'launch_game_no': "Vous devez lancer le jeu. Avez-vous besoin de notre aide ?",
        'launch_game_no_b1': "Utilisez ce lien pour lancer le jeu :",
        'launch_game_no_b1_btn': "Lancer Fortnite sur Xbox Cloud",
        'launch_game_no_b2': "Veuillez consulter notre canal pour obtenir de l'aide.",

        # --- NEW PLAYER ---
        'new_player_start': (
            "Tu plonges dans une aventure de jeu immersive. Ce bot t'aidera à configurer ton compte, à rejoindre la partie, à commencer à jouer et à progresser.\n\n"
            "**Rappel Cloud Gaming :**\n"
            "Votre session dure 1 heure. Le jeu se fermera, et vous devrez le relancer pour continuer à jouer."
        ),
        
        # --- EXISTING PLAYER ---
        'existing_player_start': (
            "Content de te revoir !\n\n"
            "**Rappel Cloud Gaming :**\n"
            "Votre session dure 1 heure. Le jeu se fermera, et vous devrez le relancer pour continuer à jouer. "
            "Tu le sais probablement déjà puisque tu as suivi toutes les instructions."
        ),
        
        # --- SUPPORT ---
        'support_start': (
            "Pour nous contacter, vous devez répondre à ces questions afin que nous puissions déterminer à quelle étape du processus vous vous trouvez. "
            "Si tout a été fait correctement, vous pourrez recevoir votre récompense."
        ),
        'support_final_q': "Assurez-vous d'avoir complété chaque étape avant de nous envoyer votre @. Avez-vous complété chaque étape et joué au moins 130 heures cette semaine ?",
        'support_final_yes': "D'accord, veuillez taper votre @nomdutilisateur Telegram (comme @monpseudo) et vous serez contacté bientôt. En fournissant votre @nomdutilisateur, vous consentez à ce que notre équipe d'assistance vous contacte directement.",
        'support_final_no': "Veuillez d'abord compléter toutes les étapes dans les guides du canal.",
        'support_thanks': "Merci ! Votre @nomdutilisateur a été noté. Nous vous contacterons dès que possible.",
        'invalid_username': "Cela ne ressemble pas à un @nomdutilisateur valide. Veuillez commencer par '@' et réessayer, ou tapez /cancel.",
    }
}

# --- Bot Links ---
XBOX_LINK = "https://www.xbox.com/fr-FR/play/games/fortnite/BT5P2X999VH2"
EPIC_ACTIVATE_LINK = "http://epicgames.com/activate"
EPIC_REGISTER_LINK = "https://www.epicgames.com/id/register" # Changed from "epicgames.com" for better UX

# Define states for ConversationHandler
(SELECT_LANG, MAIN_MENU, 
 NEW_PLAYER_START, NP_Q1_VPN, NP_Q2_CLOUD, NP_Q3_EPIC_CODE, NP_Q4_EPIC_PROFILE, NP_Q5_SHORTCUT, 
 NP_Q6_LAUNCH, NP_Q7_FIND_ISLAND, NP_Q8_SETUP, NP_Q9_PLAY_130, NP_Q10_LIKE, NP_Q11_SAVE, NP_Q12_INFLUENCER,
 
 EXISTING_PLAYER_START, EP_Q1_FIND_ISLAND, EP_Q2_SETUP, EP_Q3_PLAY_130, EP_Q4_LIKE, EP_Q5_SAVE, EP_Q6_INFLUENCER,
 
 SUPPORT_START, S_Q1_VPN, S_Q2_CLOUD, S_Q3_EPIC_CODE, S_Q4_EPIC_PROFILE, S_Q5_SHORTCUT, 
 S_Q6_LAUNCH, S_Q7_FIND_ISLAND, S_Q8_SETUP, S_Q9_PLAY_130, S_Q10_LIKE, S_Q11_SAVE, S_Q12_INFLUENCER,
 S_Q13_FINAL, S_Q14_GET_USERNAME,
 
 GET_INFLUENCER_NAME
) = range(37)


# --- Helper Function to get strings ---
def s(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Gets the language string dict for the user."""
    return STRINGS.get(context.user_data.get('lang', 'en'), STRINGS['en'])

# --- Helper Function for "Go to Channel" ---
async def go_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_key: str) -> int:
    """Sends a message with a 'Go to Channel' button."""
    lang_strings = s(context)
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(lang_strings['go_to_channel_btn'], url=HELPFUL_CHANNEL_LINK)],
        [InlineKeyboardButton(lang_strings['back_btn'], callback_data="main_menu")]
    ]
    await query.edit_message_text(
        text=lang_strings[message_key],
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return MAIN_MENU

# --- Helper Function for Simple Yes/No Question ---
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question_key: str, next_state_yes: int, next_state_no: int, back_state=MAIN_MENU) -> int:
    """Sends a question with Yes/No buttons."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings['yes_btn'], callback_data=f"yes_{next_state_yes}")],
        [InlineKeyboardButton(lang_strings['no_btn'], callback_data=f"no_{next_state_no}")],
    ]
    if back_state == MAIN_MENU:
        keyboard.append([InlineKeyboardButton(lang_strings['back_btn'], callback_data="main_menu")])
    
    text = lang_strings[question_key]
    
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    return next_state_yes # The 'parent' state for this question

# --- Helper Function for Yes/No with B1/B2 options ---
async def ask_question_with_options(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                    question_key: str, # e.g., 'use_vpn_q'
                                    next_state_yes: int, # e.g., NP_Q2_CLOUD
                                    no_message_key: str, # e.g., 'use_vpn_no'
                                    b1_text_key: str, # e.g., 'yes_btn'
                                    b1_callback: str, # e.g., 'yes_NP_Q2_CLOUD'
                                    b2_text_key: str, # e.g., 'no_btn'
                                    b2_callback: str, # e.g., 'no_go_to_channel'
                                    current_state: int, # e.g., NP_Q1_VPN
                                    back_state=MAIN_MENU) -> int:
    """Handles the 'No' branch with two new options (B1, B2)."""
    lang_strings = s(context)
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(lang_strings[b1_text_key], callback_data=b1_callback)],
        [InlineKeyboardButton(lang_strings[b2_text_key], callback_data=b2_callback)],
    ]
    if back_state == MAIN_MENU:
        keyboard.append([InlineKeyboardButton(lang_strings['back_btn'], callback_data="main_menu")])

    await query.edit_message_text(
        text=lang_strings[no_message_key],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    return current_state # Stay in the same state, waiting for B1 or B2 response


# --- Main Bot Flow ---

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: Shows disclaimer and asks for language."""
    text = (
        f"{STRINGS['en']['disclaimer']}\n\n"
        f"{STRINGS['fr']['disclaimer']}\n\n"
        "------\n\n"
        f"{STRINGS['en']['lang_prompt']}\n\n"
        f"{STRINGS['fr']['lang_prompt']}"
    )
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data="en"),
            InlineKeyboardButton("Français 🇫🇷", callback_data="fr"),
        ]
    ]
    if update.message:
        await update.message.reply_text(
            text=text, 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )
    return SELECT_LANG

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen language and shows the main menu."""
    query = update.callback_query
    lang = query.data
    context.user_data['lang'] = lang
    return await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = None) -> int:
    """Shows the main menu buttons."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings['new_player_btn'], callback_data="new_player_start")],
        [InlineKeyboardButton(lang_strings['existing_player_btn'], callback_data="existing_player_start")],
        [InlineKeyboardButton(lang_strings['support_btn'], callback_data="support_start")],
        [InlineKeyboardButton(lang_strings['helpful_channel_btn'], url=HELPFUL_CHANNEL_LINK)],
    ]
    
    text = message or lang_strings['main_menu_text']
    
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    return MAIN_MENU

# --- Button Handlers for Main Menu ---
async def new_player_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start of the New Player flow. Asks Q1."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['new_player_start'], parse_mode='Markdown')
    # --- FIX: Pass the *next* state for "Yes" ---
    return await ask_question(update, context, 'use_vpn_q', NP_Q2_CLOUD, NP_Q1_VPN)

async def existing_player_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start of the Existing Player flow. Asks Q1."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['existing_player_start'], parse_mode='Markdown')
    # --- FIX: Pass the *next* state for "Yes" ---
    return await ask_question(update, context, 'find_island_q', EP_Q2_SETUP, EP_Q1_FIND_ISLAND)

async def support_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start of the Support flow. Asks Q1."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['support_start'], parse_mode='Markdown')
    # --- FIX: Pass the *next* state for "Yes" ---
    return await ask_question(update, context, 'use_vpn_q', S_Q2_CLOUD, S_Q1_VPN)

# --- Fallback for "No" answers with B1/B2 options ---
async def handle_no_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generic handler for 'No' -> B1/B2 questions."""
    query = update.callback_query
    await query.answer()
    
    # Extract data from callback_data, e.g., "no_NP_Q1_VPN"
    _, state_name = query.data.split('_', 1)
    
    # This is a big mapping of states to their corresponding "No" branch options
    # Format: STATE_NAME: (question_key, next_state_yes, no_message_key, b1_text, b1_cb, b2_text, b2_cb, current_state)
    NO_BRANCH_MAP = {
        'NP_Q1_VPN': ('use_vpn_q', NP_Q2_CLOUD, 'use_vpn_no', 'yes_btn', f'yes_{NP_Q2_CLOUD}', 'no_btn', 'no_go_to_channel_vpn', NP_Q1_VPN),
        'NP_Q2_CLOUD': ('create_cloud_profile_q', NP_Q3_EPIC_CODE, 'create_cloud_profile_no', 'yes_btn', 'no_link_xbox', 'create_cloud_profile_no_b2', f'yes_{NP_Q3_EPIC_CODE}', NP_Q2_CLOUD),
        'NP_Q3_EPIC_CODE': ('receive_epic_code_q', NP_Q4_EPIC_PROFILE, 'receive_epic_code_no', 'yes_btn', 'no_link_epic_activate', 'no_btn', 'no_go_to_channel_epic_code', NP_Q3_EPIC_CODE),
        'NP_Q4_EPIC_PROFILE': ('create_epic_profile_q', NP_Q5_SHORTCUT, 'create_epic_profile_no', 'yes_btn', 'no_link_epic_register', 'no_btn', 'no_go_to_channel_epic_profile', NP_Q4_EPIC_PROFILE),
        'NP_Q5_SHORTCUT': ('create_shortcut_q', NP_Q6_LAUNCH, 'create_shortcut_no', 'create_shortcut_no_b1', 'no_go_to_channel_shortcut', 'create_shortcut_no_b2', f'yes_{NP_Q6_LAUNCH}', NP_Q5_SHORTCUT),
        'NP_Q6_LAUNCH': ('launch_game_q', NP_Q7_FIND_ISLAND, 'launch_game_no', 'yes_btn', 'no_link_xbox', 'no_btn', 'no_go_to_channel_launch', NP_Q6_LAUNCH),
        'NP_Q7_FIND_ISLAND': ('find_island_q', NP_Q8_SETUP, 'find_island_no', 'find_island_no_b1', 'no_print_codes', 'find_island_no_b2', f'yes_{NP_Q8_SETUP}', NP_Q7_FIND_ISLAND),
        'NP_Q8_SETUP': ('follow_setup_q', NP_Q9_PLAY_130, 'follow_setup_no', 'yes_btn', 'no_go_to_channel_setup9', 'follow_setup_no_b2', f'yes_{NP_Q9_PLAY_130}', NP_Q8_SETUP),
        'NP_Q9_PLAY_130': ('play_130_hours_q', NP_Q10_LIKE, 'play_130_hours_no', 'yes_btn', f'yes_{NP_Q10_LIKE}', 'no_btn', 'no_go_to_channel_play130', NP_Q9_PLAY_130),
        'NP_Q10_LIKE': ('like_q', NP_Q11_SAVE, 'like_no', 'yes_btn', 'no_go_to_channel_like11', 'like_no_b2_new', f'yes_{NP_Q11_SAVE}', NP_Q10_LIKE),
        'NP_Q11_SAVE': ('save_favorite_q', NP_Q12_INFLUENCER, 'save_favorite_no', 'yes_btn', 'no_go_to_channel_save12', 'save_favorite_no_b2', f'yes_{NP_Q12_INFLUENCER}', NP_Q11_SAVE),

        'EP_Q1_FIND_ISLAND': ('find_island_q', EP_Q2_SETUP, 'find_island_no', 'find_island_no_b1', 'no_print_codes', 'find_island_no_b2', f'yes_{EP_Q2_SETUP}', EP_Q1_FIND_ISLAND),
        'EP_Q2_SETUP': ('follow_setup_q', EP_Q3_PLAY_130, 'follow_setup_no', 'yes_btn', 'no_go_to_channel_setup9', 'follow_setup_no_b2', f'yes_{EP_Q3_PLAY_130}', EP_Q2_SETUP),
        'EP_Q3_PLAY_130': ('play_130_hours_q', EP_Q4_LIKE, 'play_130_hours_no', 'yes_btn', f'yes_{EP_Q4_LIKE}', 'no_btn', 'no_go_to_channel_play130', EP_Q3_PLAY_130),
        'EP_Q4_LIKE': ('like_q', EP_Q5_SAVE, 'like_no', 'yes_btn', 'no_go_to_channel_like11', 'like_no_b2_existing', f'yes_{EP_Q5_SAVE}', EP_Q4_LIKE),
        'EP_Q5_SAVE': ('save_favorite_q', EP_Q6_INFLUENCER, 'save_favorite_no', 'yes_btn', 'no_go_to_channel_save12', 'save_favorite_no_b2', f'yes_{EP_Q6_INFLUENCER}', EP_Q5_SAVE),

        'S_Q1_VPN': ('use_vpn_q', S_Q2_CLOUD, 'use_vpn_no', 'yes_btn', f'yes_{S_Q2_CLOUD}', 'no_btn', 'no_go_to_channel_vpn', S_Q1_VPN),
        'S_Q2_CLOUD': ('create_cloud_profile_q', S_Q3_EPIC_CODE, 'create_cloud_profile_no', 'yes_btn', 'no_link_xbox', 'create_cloud_profile_no_b2', f'yes_{S_Q3_EPIC_CODE}', S_Q2_CLOUD),
        'S_Q3_EPIC_CODE': ('receive_epic_code_q', S_Q4_EPIC_PROFILE, 'receive_epic_code_no', 'yes_btn', 'no_link_epic_activate', 'no_btn', 'no_go_to_channel_epic_code', S_Q3_EPIC_CODE),
        'S_Q4_EPIC_PROFILE': ('create_epic_profile_q', S_Q5_SHORTCUT, 'create_epic_profile_no', 'yes_btn', 'no_link_epic_register', 'no_btn', 'no_go_to_channel_epic_profile', S_Q4_EPIC_PROFILE),
        'S_Q5_SHORTCUT': ('create_shortcut_q', S_Q6_LAUNCH, 'create_shortcut_no', 'create_shortcut_no_b1', 'no_go_to_channel_shortcut', 'create_shortcut_no_b2', f'yes_{S_Q6_LAUNCH}', S_Q5_SHORTCUT),
        'S_Q6_LAUNCH': ('launch_game_q', S_Q7_FIND_ISLAND, 'launch_game_no', 'yes_btn', 'no_link_xbox', 'no_btn', 'no_go_to_channel_launch', S_Q6_LAUNCH),
        'S_Q7_FIND_ISLAND': ('find_island_q', S_Q8_SETUP, 'find_island_no', 'find_island_no_b1', 'no_print_codes', 'find_island_no_b2', f'yes_{S_Q8_SETUP}', S_Q7_FIND_ISLAND),
        'S_Q8_SETUP': ('follow_setup_q', S_Q9_PLAY_130, 'follow_setup_no', 'yes_btn', 'no_go_to_channel_setup9', 'follow_setup_no_b2', f'yes_{S_Q9_PLAY_130}', S_Q8_SETUP),
        'S_Q9_PLAY_130': ('play_130_hours_q', S_Q10_LIKE, 'play_130_hours_no', 'yes_btn', f'yes_{S_Q10_LIKE}', 'no_btn', 'no_go_to_channel_play130', S_Q9_PLAY_130),
        'S_Q10_LIKE': ('like_q', S_Q11_SAVE, 'like_no', 'yes_btn', 'no_go_to_channel_like11', 'like_no_b2_support', f'yes_{S_Q11_SAVE}', S_Q10_LIKE),
        'S_Q11_SAVE': ('save_favorite_q', S_Q12_INFLUENCER, 'save_favorite_no', 'yes_btn', 'no_go_to_channel_save12', 'save_favorite_no_b2', f'yes_{S_Q12_INFLUENCER}', S_Q11_SAVE),
    }

    if state_name not in NO_BRANCH_MAP:
        logger.warning(f"No_option handler called with unknown state: {state_name}")
        return MAIN_MENU

    (question_key, next_state_yes, no_message_key, b1_text, b1_cb, b2_text, b2_cb, current_state) = NO_BRANCH_MAP[state_name]
    
    return await ask_question_with_options(
        update, context,
        question_key, next_state_yes, no_message_key,
        b1_text_key=b1_text, b1_callback=b1_cb,
        b2_text_key=b2_text, b2_callback=b2_cb,
        current_state=current_state
    )

# --- Handlers for "No" B1/B2 options ---

async def handle_no_go_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles B2 'No' options that redirect to the channel."""
    query = update.callback_query
    await query.answer()
    
    # Extract the specific message key from callback, e.g., "no_go_to_channel_vpn"
    key_suffix = query.data.split('_')[-1]
    
    # Map of suffixes to message keys
    CHANNEL_MESSAGE_MAP = {
        'vpn': 'use_vpn_no_b2',
        'epic_code': 'receive_epic_code_no_b2',
        'epic_profile': 'create_epic_profile_no_b2',
        'shortcut': 'create_shortcut_no_b1',
        'launch': 'launch_game_no_b2',
        'setup9': 'follow_setup_no_b1',
        'play130': 'play_130_hours_no_b2',
        'like11': 'like_no_b1',
        'save12': 'save_favorite_no_b1',
        'influencer13': 'influencer_no', # From Support Q12
    }
    
    message_key = CHANNEL_MESSAGE_MAP.get(key_suffix, 'go_to_channel') # Default message
    return await go_to_channel(update, context, message_key)

async def handle_no_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles B1 'Yes' options that provide a link."""
    lang_strings = s(context)
    query = update.callback_query
    await query.answer()
    
    # Extract link type from callback, e.g., "no_link_xbox"
    link_type = query.data.split('_')[-1]
    
    LINK_MAP = {
        'xbox': (lang_strings['create_cloud_profile_no_b1'], lang_strings['create_cloud_profile_no_b1_btn'], XBOX_LINK),
        'epic_activate': (lang_strings['receive_epic_code_no_b1'], lang_strings['receive_epic_code_no_b1_btn'], EPIC_ACTIVATE_LINK),
        'epic_register': (lang_strings['create_epic_profile_no_b1'], lang_strings['create_epic_profile_no_b1_btn'], EPIC_REGISTER_LINK),
    }
    
    if link_type not in LINK_MAP:
        logger.warning(f"No_link handler called with unknown link type: {link_type}")
        return MAIN_MENU

    text, btn_text, url = LINK_MAP[link_type]
    
    keyboard = [
        [InlineKeyboardButton(btn_text, url=url)],
        [InlineKeyboardButton(lang_strings['back_btn'], callback_data="main_menu")]
    ]
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return MAIN_MENU

async def handle_no_print_codes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles B1 'Yes I want codes'."""
    lang_strings = s(context)
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton(lang_strings['back_btn'], callback_data="main_menu")]]
    await query.edit_message_text(
        text=lang_strings['find_island_no_b1'],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    return MAIN_MENU

# --- Handler for "Yes" answers ---
async def handle_yes_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generic handler for 'Yes' answers, moves to the next question."""
    query = update.callback_query
    await query.answer()
    
    # Extract data from callback_data, e.g., "yes_NP_Q2_CLOUD"
    _, state_name = query.data.split('_', 1)

    # Map of "Yes" callbacks to the *next* question to ask
    # Format: CURRENT_STATE_NAME: (next_question_key, next_state_yes, next_state_no)
    # --- FIX: Corrected the entire map's logic ---
    YES_BRANCH_MAP = {
        # --- New Player Flow ---
        'NP_Q2_CLOUD': ('create_cloud_profile_q', NP_Q3_EPIC_CODE, NP_Q2_CLOUD),
        'NP_Q3_EPIC_CODE': ('receive_epic_code_q', NP_Q4_EPIC_PROFILE, NP_Q3_EPIC_CODE),
        'NP_Q4_EPIC_PROFILE': ('create_epic_profile_q', NP_Q5_SHORTCUT, NP_Q4_EPIC_PROFILE),
        'NP_Q5_SHORTCUT': ('create_shortcut_q', NP_Q6_LAUNCH, NP_Q5_SHORTCUT),
        'NP_Q6_LAUNCH': ('launch_game_q', NP_Q7_FIND_ISLAND, NP_Q6_LAUNCH),
        'NP_Q7_FIND_ISLAND': ('find_island_q', NP_Q8_SETUP, NP_Q7_FIND_ISLAND),
        'NP_Q8_SETUP': ('follow_setup_q', NP_Q9_PLAY_130, NP_Q8_SETUP),
        'NP_Q9_PLAY_130': ('play_130_hours_q', NP_Q10_LIKE, NP_Q9_PLAY_130),
        'NP_Q10_LIKE': ('like_q', NP_Q11_SAVE, NP_Q10_LIKE),
        'NP_Q11_SAVE': ('save_favorite_q', NP_Q12_INFLUENCER, NP_Q11_SAVE),
        'NP_Q12_INFLUENCER': ('influencer_q', GET_INFLUENCER_NAME, NP_Q12_INFLUENCER),

        # --- Existing Player Flow ---
        'EP_Q2_SETUP': ('follow_setup_q', EP_Q3_PLAY_130, EP_Q2_SETUP),
        'EP_Q3_PLAY_130': ('play_130_hours_q', EP_Q4_LIKE, EP_Q3_PLAY_130),
        'EP_Q4_LIKE': ('like_q', EP_Q5_SAVE, EP_Q4_LIKE),
        'EP_Q5_SAVE': ('save_favorite_q', EP_Q6_INFLUENCER, EP_Q5_SAVE),
        'EP_Q6_INFLUENCER': ('influencer_q', GET_INFLUENCER_NAME, EP_Q6_INFLUENCER),

        # --- Support Flow ---
        'S_Q2_CLOUD': ('create_cloud_profile_q', S_Q3_EPIC_CODE, S_Q2_CLOUD),
        'S_Q3_EPIC_CODE': ('receive_epic_code_q', S_Q4_EPIC_PROFILE, S_Q3_EPIC_CODE),
        'S_Q4_EPIC_PROFILE': ('create_epic_profile_q', S_Q5_SHORTCUT, S_Q4_EPIC_PROFILE),
        'S_Q5_SHORTCUT': ('create_shortcut_q', S_Q6_LAUNCH, S_Q5_SHORTCUT),
        'S_Q6_LAUNCH': ('launch_game_q', S_Q7_FIND_ISLAND, S_Q6_LAUNCH),
        'S_Q7_FIND_ISLAND': ('find_island_q', S_Q8_SETUP, S_Q7_FIND_ISLAND),
        'S_Q8_SETUP': ('follow_setup_q', S_Q9_PLAY_130, S_Q8_SETUP),
        'S_Q9_PLAY_1S0': ('play_130_hours_q', S_Q10_LIKE, S_Q9_PLAY_130),
        'S_Q10_LIKE': ('like_q', S_Q11_SAVE, S_Q10_LIKE),
        'S_Q11_SAVE': ('save_favorite_q', S_Q12_INFLUENCER, S_Q11_SAVE),
        'S_Q12_INFLUENCER': ('influencer_q', GET_INFLUENCER_NAME, S_Q12_INFLUENCER),
        'S_Q13_FINAL': ('support_final_q', S_Q14_GET_USERNAME, S_Q13_FINAL),
    }

    if state_name not in YES_BRANCH_MAP:
        logger.warning(f"Yes_option handler called with unknown state: {state_name}")
        return MAIN_MENU

    (question_key, next_state_yes, next_state_no) = YES_BRANCH_MAP[state_name]
    
    # Special case for influencer question
    if question_key == 'influencer_q':
        context.user_data['next_state_after_influencer'] = "main_menu" # NP/EP flows end
        if state_name.startswith('S_'):
             context.user_data['next_state_after_influencer'] = f'yes_{S_Q13_FINAL}' # Support flow continues
        return await ask_question(update, context, 'influencer_q', GET_INFLUENCER_NAME, next_state_no) # 'No' for influencer is custom

    # Special case for support final question
    if question_key == 'support_final_q':
        return await ask_question(update, context, 'support_final_q', S_Q14_GET_USERNAME, S_Q13_FINAL) # 'No' for final q is custom

    return await ask_question(update, context, question_key, next_state_yes, next_state_no)


# --- Special "No" Handlers ---

async def handle_influencer_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles 'No' to the influencer question."""
    query = update.callback_query
    await query.answer()
    
    # Support flow has a different "No" answer
    if query.data.startswith('no_S_'):
        return await go_to_channel(update, context, 'influencer_no') # S_Q12_INFLUENCER
    
    # NP and EP flows just go back to main menu
    return await show_main_menu(update, context, message=s(context)['influencer_no'])

async def handle_support_final_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles 'No' to the final support question."""
    return await go_to_channel(update, context, 'support_final_no') # S_Q13_FINAL


# --- Text Input Handlers ---

async def get_influencer_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for influencer name."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['influencer_prompt'])
    return GET_INFLUENCER_NAME

async def save_influencer_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves influencer name and moves to next step."""
    influencer_name = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} submitted influencer name: {influencer_name}")
    
    await update.message.reply_text(s(context)['influencer_thanks'])
    
    # Go to the next step we saved earlier
    next_step_callback = context.user_data.pop('next_state_after_influencer', 'main_menu')
    
    if next_step_callback == 'main_menu':
        return await show_main_menu(update, context)
    else:
        # This is for the Support flow
        return await handle_yes_option(update, context) # Manually trigger next question

async def get_support_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for @username."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['support_final_yes'], parse_mode='Markdown')
    return S_Q14_GET_USERNAME

async def save_support_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves @username and logs it."""
    username = update.message.text
    if username.startswith('@') and len(username) > 2:
        user_id = update.message.from_user.id
        logger.info(f"*** SUPPORT REQUEST from user {user_id}: {username} ***")
        
        await update.message.reply_text(s(context)['support_thanks'])
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(s(context)['invalid_username'])
        return S_Q14_GET_USERNAME # Stay in this state

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels any active conversation and returns to main menu."""
    await update.message.reply_text("Action cancelled.", reply_markup=ReplyKeyboardRemove())
    return await show_main_menu(update, context)


def main() -> None:
    """Run the bot."""
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN environment variable not set!")
        return

    application = Application.builder().token(token).build()

    # --- This is the main conversation handler ---
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_cmd)],
        states={
            SELECT_LANG: [
                CallbackQueryHandler(set_language, pattern="^(en|fr)$")
            ],
            MAIN_MENU: [
                CallbackQueryHandler(new_player_flow, pattern="^new_player_start$"),
                CallbackQueryHandler(existing_player_flow, pattern="^existing_player_start$"),
                CallbackQueryHandler(support_flow, pattern="^support_start$"),
            ],
            
            # --- Auto-generated "Yes" handlers ---
            # These just move to the next question state
            NP_Q1_VPN: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q2_CLOUD}$")],
            NP_Q2_CLOUD: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q3_EPIC_CODE}$")],
            NP_Q3_EPIC_CODE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q4_EPIC_PROFILE}$")],
            NP_Q4_EPIC_PROFILE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q5_SHORTCUT}$")],
            NP_Q5_SHORTCUT: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q6_LAUNCH}$")],
            NP_Q6_LAUNCH: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q7_FIND_ISLAND}$")],
            NP_Q7_FIND_ISLAND: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q8_SETUP}$")],
            NP_Q8_SETUP: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q9_PLAY_130}$")],
            NP_Q9_PLAY_130: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q10_LIKE}$")],
            NP_Q10_LIKE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q11_SAVE}$")],
            NP_Q11_SAVE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{NP_Q12_INFLUENCER}$")],
            NP_Q12_INFLUENCER: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_GET_INFLUENCER_NAME$")],

            EP_Q1_FIND_ISLAND: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{EP_Q2_SETUP}$")],
            EP_Q2_SETUP: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{EP_Q3_PLAY_130}$")],
            EP_Q3_PLAY_130: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{EP_Q4_LIKE}$")],
            EP_Q4_LIKE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{EP_Q5_SAVE}$")],
            EP_Q5_SAVE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{EP_Q6_INFLUENCER}$")],
            EP_Q6_INFLUENCER: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_GET_INFLUENCER_NAME$")],
            
            S_Q1_VPN: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q2_CLOUD}$")],
            S_Q2_CLOUD: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q3_EPIC_CODE}$")],
            S_Q3_EPIC_CODE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q4_EPIC_PROFILE}$")],
            S_Q4_EPIC_PROFILE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q5_SHORTCUT}$")],
            S_Q5_SHORTCUT: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q6_LAUNCH}$")],
            S_Q6_LAUNCH: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q7_FIND_ISLAND}$")],
            S_Q7_FIND_ISLAND: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q8_SETUP}$")],
            S_Q8_SETUP: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q9_PLAY_130}$")],
            S_Q9_PLAY_130: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q10_LIKE}$")],
            S_Q10_LIKE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q11_SAVE}$")],
            S_Q11_SAVE: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q12_INFLUENCER}$")],
            S_Q12_INFLUENCER: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q13_FINAL}$")],
            S_Q13_FINAL: [CallbackQueryHandler(handle_yes_option, pattern=f"^yes_{S_Q14_GET_USERNAME}$")],
            
            # --- "No" handlers (B1/B2) ---
            # These are more complex and are routed to generic handlers
            **{
                state: [
                    CallbackQueryHandler(handle_no_option, pattern=f"^no_{state_name}$"),
                    CallbackQueryHandler(handle_no_go_to_channel, pattern="^no_go_to_channel_"),
                    CallbackQueryHandler(handle_no_link, pattern="^no_link_"),
                    CallbackQueryHandler(handle_no_print_codes, pattern="^no_print_codes$"),
                    CallbackQueryHandler(handle_yes_option, pattern="^yes_"), # Catches B1/B2 "Yes" answers
                ]
                for state, state_name in [
                    (NP_Q1_VPN, 'NP_Q1_VPN'), (NP_Q2_CLOUD, 'NP_Q2_CLOUD'), (NP_Q3_EPIC_CODE, 'NP_Q3_EPIC_CODE'),
                    (NP_Q4_EPIC_PROFILE, 'NP_Q4_EPIC_PROFILE'), (NP_Q5_SHORTCUT, 'NP_Q5_SHORTCUT'), (NP_Q6_LAUNCH, 'NP_Q6_LAUNCH'),
                    (NP_Q7_FIND_ISLAND, 'NP_Q7_FIND_ISLAND'), (NP_Q8_SETUP, 'NP_Q8_SETUP'), (NP_Q9_PLAY_130, 'NP_Q9_PLAY_130'),
                    (NP_Q10_LIKE, 'NP_Q10_LIKE'), (NP_Q11_SAVE, 'NP_Q11_SAVE'),
                    (EP_Q1_FIND_ISLAND, 'EP_Q1_FIND_ISLAND'), (EP_Q2_SETUP, 'EP_Q2_SETUP'), (EP_Q3_PLAY_130, 'EP_Q3_PLAY_130'),
                    (EP_Q4_LIKE, 'EP_Q4_LIKE'), (EP_Q5_SAVE, 'EP_Q5_SAVE'),
                    (S_Q1_VPN, 'S_Q1_VPN'), (S_Q2_CLOUD, 'S_Q2_CLOUD'), (S_Q3_EPIC_CODE, 'S_Q3_EPIC_CODE'),
                    (S_Q4_EPIC_PROFILE, 'S_Q4_EPIC_PROFILE'), (S_Q5_SHORTCUT, 'S_Q5_SHORTCUT'), (S_Q6_LAUNCH, 'S_Q6_LAUNCH'),
                    (S_Q7_FIND_ISLAND, 'S_Q7_FIND_ISLAND'), (S_Q8_SETUP, 'S_Q8_SETUP'), (S_Q9_PLAY_130, 'S_Q9_PLAY_130'),
                    (S_Q10_LIKE, 'S_Q10_LIKE'), (S_Q11_SAVE, 'S_Q11_SAVE'),
                    
                    # Special "No" handlers for last questions
                    (NP_Q12_INFLUENCER, 'NP_Q12_INFLUENCER'),
                    (EP_Q6_INFLUENCER, 'EP_Q6_INFLUENCER'),
                    (S_Q12_INFLUENCER, 'S_Q12_INFLUENCER'),
                    (S_Q13_FINAL, 'S_Q13_FINAL'),
                ]
            },
            
            # Special "No" handlers
            NP_Q12_INFLUENCER: [CallbackQueryHandler(handle_influencer_no, pattern="^no_NP_Q12_INFLUENCER$")],
            EP_Q6_INFLUENCER: [CallbackQueryHandler(handle_influencer_no, pattern="^no_EP_Q6_INFLUENCER$")],
            S_Q12_INFLUENCER: [CallbackQueryHandler(handle_influencer_no, pattern="^no_S_Q12_INFLUENCER$")],
            S_Q13_FINAL: [CallbackQueryHandler(handle_support_final_no, pattern="^no_S_Q13_FINAL$")],
            
            # --- Text Input States ---
            GET_INFLUENCER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_influencer_name)
            ],
            S_Q14_GET_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_support_username)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(show_main_menu, pattern="^main_menu$"),
            CommandHandler("start", start_cmd),
            CommandHandler("cancel", cancel)
        ],
        per_message=False # Allows different users to be in different states
    )

    application.add_handler(conv_handler)

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()


