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
# !!! IMPORTANT: Fill in all your links and codes here !!!
CONFIGURATION = {
    'YOUR_CHANNEL_LINK': "https://t.me/rejoinsnousetgagne", # Your main channel
    'XBOX_LINK': "https://www.xbox.com/fr-FR/play/games/fortnite/BT5P2X999VH2",
    'EPIC_ACTIVATE_LINK': "http://epicgames.com/activate",
    'EPIC_REGISTER_LINK': "https://www.epicgames.com/id/register", # Using register link, not just epicgames.com
    'ISLAND_CODES': [
        "4828-9033-2281",  # <-- Change this
        "2753-4695-7191", # <-- Change this
        "9689-1352-5966"    # <-- Change this
    ]
}
# !!!!!!!!!!!!!!!!!!!!!


# --- LANGUAGE STRINGS ---
# All text from your script is here
STRINGS = {
    'en': {
        'disclaimer': (
            "**Disclaimer:** This bot is an unofficial guide and is not affiliated with "
            "Epic Games or Fortnite. We will *never* ask for your password."
        ),
        'lang_prompt': "Please select your language:",
        'welcome': "Welcome! Are you a New or Existing Player?",
        'main_menu_text': "Please choose an option:",
        'btn_existing': "Existing Player",
        'btn_new': "New Player",
        'btn_support': "Support/Troubleshooting",
        'btn_back': "⬅️ Back to Main Menu",
        'btn_yes': "Yes",
        'btn_no': "No",
        'go_to_channel': "Please see our channel for instructions on this step.",
        'go_to_channel_btn': "Go to Channel",
        'codes_message': "Just copy one of them and enter it on the search bar:",
        'btn_continue': "Continue ➡️",
        
        # --- Existing Player ---
        'ep_start': "Note: Since you're playing on the cloud, your session will last for 1 hour. The game will close, and you will have to launch it again to keep playing. You probably know this because you already followed all the instructions.",
        'ep_q1': "Have you searched and found the reward Island?",
        'ep_q1_no': "No, you have to search the reward Island in the search bar and just choose it. Do you want our guidance for that?",
        'ep_q1_b1': "Yes, I want the best codes to play.",
        'ep_q1_b2': "No, I already chose one code.",
        'ep_q2': "Did you follow the full setup to be able to play with friends and progress together without any worries?",
        'ep_q2_yes': "Yes, I'm ready for the next step.",
        'ep_q2_no': "No, you have to follow the exact setup. Do you need our guidance?",
        'ep_q2_b1': "Yes",
        'ep_q2_b1_action': "Go to our channel and look at instruction 9.",
        'ep_q2_b2': "No, I finally fixed everything, I want to move to the next step.",
        'ep_q3': "Did you start the game and play 130 hours for free this week?",
        'ep_q3_no': "No, you have to start the game and play every single day for free before aiming for the reward. Are you able to play at least 130 hours a week?",
        'ep_q3_b2': "No",
        'ep_q3_b2_action': "Go to our channel and look for instruction 10.",
        'ep_q4': "With your existing account, will you click on the like button every single time before your 1-hour play session ended during your 130 hours of play this week?",
        'ep_q4_no': "No, you have to click on the like button every single time before your 1-hour play session ended during your 130 hours a week. Do you want our guidance on that?",
        'ep_q4_b1_action': "Go to our channel and look for instruction 11.",
        'ep_q4_b2': "No, I will play and let you know in the support session later on.",
        'ep_q5': "Did you save the reward Island to your favorites?",
        'ep_q5_no': "No, you have to save the reward Island to your favorites and play. Do you want our guidance on that?",
        'ep_q5_b1_action': "Go to our channel and look for instruction 12.",
        'ep_q5_b2': "No, I have proof I saved the reward Island to my favorites and I actually play on it.",
        'ep_q6': "Were you introduced to this game by an influencer?",
        'ep_q6_yes': "Yes, provide the name please:",
        'ep_q6_no_action': "Go to our channel and look for instruction 13.",
        'ep_end_flow': "Thank you for the information.",
        
        # --- New Player ---
        'np_start': "Note: You're diving into an immersive gaming adventure. This bot will help you set up your account, join the game, start playing, and progressing. Because you are playing on the cloud, your session will last for 1 hour. The game will close, and you will have to launch it again to keep playing.",
        'np_q1': "Did you use a VPN?",
        'np_q1_no': "No. Please download and use a VPN in the USA before going any further to create all your authentic profiles, but to play, you don’t use it. Did you finally use a VPN?",
        'np_q1_b1': "If yes",
        'np_q1_b2': "If no",
        'np_q1_b2_action': "Please go to our channel for VPN recommendations.",
        'np_q2': "Did you already create a cloud gaming profile?",
        'np_q2_no': "If no, please create a cloud gaming profile. Do you want our assistance?",
        'np_q2_b1_action': "Click here to create your profile:",
        'np_q2_b1_btn': "Go to Xbox Cloud Gaming",
        'np_q2_b2': "No, I already have one, I want the next step.",
        'np_q3': "Did you receive the code from Epic Games to activate your cloud gaming account?",
        'np_q3_yes': "Yes, I received the code, I want the next step.",
        'np_q3_no': "Please, you have to receive the code. Do you want our guidance to help you with that?",
        'np_q3_b1_action': "Click here to activate your account:",
        'np_q3_b1_btn': "Go to epicgames.com/activate",
        'np_q3_b2': "No",
        'np_q3_b2_action': "Please go to our channel for help with this step.",
        'np_q4': "Did you create your Epic Games profile?",
        'np_q4_no': "No, please you have to create your Epic Games profile. Do you need our guidance?",
        'np_q4_b1_action': "Click here to create your profile:",
        'np_q4_b1_btn': "Go to Epic Games",
        'np_q4_b2': "No",
        'np_q4_b2_action': "Please go to our channel for help with this step.",
        'np_q5': "Did you create a shortcut of the cloud gaming to play it like an installed app directly from your Homescreen?",
        'np_q5_no': "No, you have to create a shortcut to play Fortnite from your homescreen. Do you want our guidance with that?",
        'np_q5_b1': "Yes, I want to see it in the channel.",
        'np_q5_b1_action': "Please see our channel for a guide on creating shortcuts.",
        'np_q5_b2': "No, I finally created a shortcut.",
        'np_q6': "Have you launched the game?",
        'np_q6_no': "No, you have to launch the game. Do you need our guidance?",
        'np_q6_b1_action': "Click here to launch the game:",
        'np_q6_b1_btn': "Launch Fortnite",
        'np_q6_b2_action': "Please go to our channel if you have trouble launching.",
        'np_q7': "Have you searched and found the reward Island?",
        'np_q8': "Did you follow the full setup to be able to play with friends and progress together without any worries?",
        'np_q9': "Will you start the game and play 130 hours for free this week?",
        'np_q10': "With your new account, will you click on the like button every single time before your 1-hour play session ended during your 130 hours of play this week?",
        'np_q11': "Will you save the reward Island to your favorites?",
        'np_q12': "Were you introduced to this game by an influencer?",
        'np_end_flow': "Thank you. You are all set up.",

        # --- Support ---
        's_start': "Note: In order to get in touch with us, you need to answer these questions so we can determine which stage of the process you’re at. If everything has been done correctly, you’ll be able to receive your reward.",
        # Q1-Q11 are identical to New Player
        's_q10_b2': "No, I have proof that I played 130 hours this week and I liked every single time, and I am wishing to share it with you guys.",
        's_q12': "Were you introduced to this game by an influencer?",
        's_q12_yes': "Yes, provide the name please:",
        's_q12_no': "No",
        's_q12_action': "Thank you. An expert will review your information. Please answer the final question.",
        's_q13': "Make sure you completed every single step before sending us your @. Did you complete every single step and play at least 130 hours this week?",
        's_q13_yes': "Yes, I did it and I will send you all the necessary screenshots.",
        's_q13_no': "No",
        's_q13_no_action': "Please complete all steps in the channel guide before requesting support.",
        's_end_flow': "Thank you. We will review your submission and get in touch.",
        
        # --- Text Prompts ---
        'prompt_influencer': "Please type the name of the influencer who introduced you to the game and press send:",
        'prompt_username': "Thank you. Please type your Telegram @username (e.g., @myusername) and an expert will review your case. By providing your @, you consent to being contacted.",
        'prompt_thanks_influencer': "Thank you! We have recorded the influencer's name.",
        'prompt_thanks_username': "Thank you! Your request has been submitted. An expert will get in touch with you soon.",
        'prompt_invalid_username': "That doesn't look like a valid @username. Please start with '@' and try again, or type /cancel.",

    },
    'fr': {
        'disclaimer': (
            "**Avertissement :** Ce bot est un guide non officiel et n'est pas affilié à "
            "Epic Games ou Fortnite. Nous ne vous demanderons *jamais* votre mot de passe."
        ),
        'lang_prompt': "Veuillez sélectionner votre langue :",
        'welcome': "Bienvenue ! Êtes-vous un Joueur Actuel ou un Nouveau Joueur ?",
        'main_menu_text': "Veuillez choisir une option :",
        'btn_existing': "Joueur Actuel",
        'btn_new': "Nouveau Joueur",
        'btn_support': "Support/Dépannage",
        'btn_back': "⬅️ Retour au Menu Principal",
        'btn_yes': "Oui",
        'btn_no': "Non",
        'go_to_channel': "Veuillez consulter notre canal pour les instructions sur cette étape.",
        'go_to_channel_btn': "Aller au Canal",
        'codes_message': "Copiez-en un et entrez-le dans la barre de recherche :",
        'btn_continue': "Continuer ➡️",
        
        # --- Existing Player ---
        'ep_start': "Note : Puisque vous jouez sur le cloud, votre session durera 1 heure. Le jeu se fermera et vous devrez le relancer pour continuer à jouer. Vous le savez probablement déjà car vous avez suivi toutes les instructions.",
        'ep_q1': "Avez-vous cherché et trouvé l'Île de Récompense ?",
        'ep_q1_no': "Non, vous devez chercher l'Île de Récompense dans la barre de recherche et la choisir. Souhaitez-vous notre aide pour cela ?",
        'ep_q1_b1': "Oui, je veux les meilleurs codes pour jouer.",
        'ep_q1_b2': "Non, j'ai déjà choisi un code.",
        'ep_q2': "Avez-vous suivi la configuration complète pour pouvoir jouer avec des amis et progresser ensemble sans soucis ?",
        'ep_q2_yes': "Oui, je suis prêt pour la prochaine étape.",
        'ep_q2_no': "Non, vous devez suivre la configuration exacte. Avez-vous besoin de notre aide ?",
        'ep_q2_b1': "Oui",
        'ep_q2_b1_action': "Allez sur notre canal et consultez l'instruction 9.",
        'ep_q2_b2': "Non, j'ai finalement tout réglé, je veux passer à l'étape suivante.",
        'ep_q3': "Avez-vous démarré le jeu et joué 130 heures gratuitement cette semaine ?",
        'ep_q3_no': "Non, vous devez commencer le jeu et jouer tous les jours gratuitement avant de viser la progression. Êtes-vous capable de jouer au moins 130 heures par semaine ?",
        'ep_q3_b2': "Non",
        'ep_q3_b2_action': "Allez sur notre canal et consultez l'instruction 10.",
        'ep_q4': "Avec votre compte existant, cliquerez-vous sur le bouton 'J'aime' à chaque fois avant la fin de votre session de jeu d'une heure durant vos 130 heures de jeu cette semaine ?",
        'ep_q4_no': "Non, vous devez cliquer sur le bouton 'J'aime' à chaque fois avant la fin de votre session de jeu d'une heure durant vos 130 heures par semaine. Souhaitez-vous notre aide pour cela ?",
        'ep_q4_b1_action': "Allez sur notre canal et consultez l'instruction 11.",
        'ep_q4_b2': "Non, je vais jouer et je vous informerai lors de la session de support plus tard.",
        'ep_q5': "Avez-vous enregistré l'Île de Récompense dans vos favoris ?",
        'ep_q5_no': "Non, vous devez enregistrer l'Île de Récompense dans vos favoris et jouer. Souhaitez-vous notre aide pour cela ?",
        'ep_q5_b1_action': "Allez sur notre canal et consultez l'instruction 12.",
        'ep_q5_b2': "Non, j'ai la preuve que j'ai enregistré l'Île de Récompense dans mes favoris et que j'y joue réellement.",
        'ep_q6': "Ce jeu vous a-t-il été présenté par un influenceur ?",
        'ep_q6_yes': "Oui, veuillez indiquer le nom :",
        'ep_q6_no_action': "Allez sur notre canal et consultez l'instruction 13.",
        'ep_end_flow': "Merci pour les informations.",

        # --- New Player ---
        'np_start': "Note : Tu plonges dans une aventure de jeu immersive. Ce bot t'aidera à configurer ton compte, à rejoindre la partie, à commencer à jouer et à progresser. Parce que tu joues sur le cloud, ta session durera 1 heure. Le jeu se fermera, et tu devras le relancer pour continuer à jouer.",
        'np_q1': "Avez-vous utilisé un VPN ?",
        'np_q1_no': "Non. Veuillez télécharger et utiliser un VPN aux USA avant d'aller plus loin pour créer tous vos profils authentiques, mais pour jouer, vous ne l'utilisez pas. Avez-vous finalement utilisé un VPN ?",
        'np_q1_b1': "Si oui",
        'np_q1_b2': "Si non",
        'np_q1_b2_action': "Veuillez consulter notre canal pour des recommandations de VPN.",
        'np_q2': "Avez-vous déjà créé un profil de jeu en cloud ?",
        'np_q2_no': "Si non, veuillez créer un profil de jeu en cloud. Souhaitez-vous notre assistance ?",
        'np_q2_b1_action': "Cliquez ici pour créer votre profil :",
        'np_q2_b1_btn': "Aller sur Xbox Cloud Gaming",
        'np_q2_b2': "Non, j'en ai déjà un, je veux l'étape suivante.",
        'np_q3': "Avez-vous reçu le code d'Epic Games pour activer votre compte de jeu en cloud ?",
        'np_q3_yes': "Oui, j'ai reçu le code, je veux l'étape suivante.",
        'np_q3_no': "S'il vous plaît, vous devez recevoir le code. Souhaitez-vous notre aide pour cela ?",
        'np_q3_b1_action': "Cliquez ici pour activer votre compte :",
        'np_q3_b1_btn': "Aller sur epicgames.com/activate",
        'np_q3_b2': "Non",
        'np_q3_b2_action': "Veuillez consulter notre canal pour obtenir de l'aide.",
        'np_q4': "Avez-vous créé votre profil Epic Games ?",
        'np_q4_no': "Non, s'il vous plaît, vous devez créer votre profil Epic Games. Avez-vous besoin de notre aide ?",
        'np_q4_b1_action': "Cliquez ici pour créer votre profil :",
        'np_q4_b1_btn': "Aller sur Epic Games",
        'np_q4_b2': "Non",
        'np_q4_b2_action': "Veuillez consulter notre canal pour obtenir de l'aide.",
        'np_q5': "Avez-vous créé un raccourci du jeu en cloud pour y jouer comme une application installée directement depuis votre écran d'accueil ?",
        'np_q5_no': "Non, vous devez créer un raccourci pour jouer à Fortnite depuis votre écran d'accueil. Souhaitez-vous notre aide pour cela ?",
        'np_q5_b1': "Oui, je veux le voir sur la chaîne.",
        'np_q5_b1_action': "Veuillez consulter notre canal pour un guide sur les raccourcis.",
        'np_q5_b2': "Non, j'ai finalement créé un raccourci.",
        'np_q6': "Avez-vous lancé le jeu ?",
        'np_q6_no': "Non, vous devez lancer le jeu. Avez-vous besoin de notre aide ?",
        'np_q6_b1_action': "Cliquez ici pour lancer le jeu :",
        'np_q6_b1_btn': "Lancer Fortnite",
        'np_q6_b2_action': "Veuillez consulter notre canal si vous avez des problèmes.",
        'np_q7': "Avez-vous cherché et trouvé l'Île de Récompense ?",
        'np_q8': "Avez-vous suivi la configuration complète pour pouvoir jouer avec des amis et progresser ensemble sans soucis ?",
        'np_q9': "Allez-vous démarrer le jeu et jouer 130 heures gratuitement cette semaine ?",
        'np_q10': "Avec votre nouveau compte, cliquerez-vous sur le bouton 'J'aime' à chaque fois avant la fin de votre session de jeu d'une heure durant vos 130 heures de jeu cette semaine ?",
        'np_q11': "Allez-vous enregistrer l'Île de Récompense dans vos favoris ?",
        'np_q12': "Ce jeu vous a-t-il été présenté par un influenceur ?",
        'np_end_flow': "Merci. Vous êtes prêt.",

        # --- Support ---
        's_start': "Note : Pour nous contacter, vous devez répondre à ces questions afin que nous puissions déterminer à quelle étape du processus vous vous trouvez. Si tout a été fait correctement, vous pourrez recevoir votre récompense.",
        # Q1-Q11 are identical to New Player
        's_q10_b2': "Non, j'ai la preuve que j'ai joué 130 heures cette semaine et que j'ai aimé à chaque fois, et je souhaite la partager avec vous.",
        's_q12': "Ce jeu vous a-t-il été présenté par un influenceur ?",
        's_q12_yes': "Oui, veuillez indiquer le nom :",
        's_q12_no': "Non",
        's_q12_action': "Merci. Un expert examinera vos informations. Veuillez répondre à la dernière question.",
        's_q13': "Assurez-vous d'avoir complété chaque étape avant de nous envoyer votre @. Avez-vous complété chaque étape et joué au moins 130 heures cette semaine ?",
        's_q13_yes': "Oui, je l'ai fait et je vous enverrai toutes les captures d'écran nécessaires.",
        's_q13_no': "Non",
        's_q13_no_action': "Veuillez compléter toutes les étapes dans le guide du canal avant de demander du support.",
        's_end_flow': "Merci. Nous examinerons votre soumission et vous contacterons.",
        
        # --- Text Prompts ---
        'prompt_influencer': "Veuillez taper le nom de l'influenceur qui vous a présenté le jeu et appuyez sur envoyer :",
        'prompt_username': "Merci. Veuillez taper votre @nomdutilisateur Telegram (par ex., @monpseudo) et un expert examinera votre cas. En fournissant votre @, vous consentez à être contacté.",
        'prompt_thanks_influencer': "Merci ! Nous avons enregistré le nom de l'influenceur.",
        'prompt_thanks_username': "Merci ! Votre demande a été soumise. Un expert vous contactera bientôt.",
        'prompt_invalid_username': "Cela ne ressemble pas à un @nomdutilisateur valide. Veuillez commencer par '@' et réessayer, ou tapez /cancel.",
    }
}

# Define states for ConversationHandler
(
    SELECT_LANG, MAIN_MENU,
    EP_START, EP_Q1, EP_Q2, EP_Q3, EP_Q4, EP_Q5, EP_Q6, EP_GET_INFLUENCER,
    NP_START, NP_Q1, NP_Q2, NP_Q3, NP_Q4, NP_Q5, NP_Q6, NP_Q7, NP_Q8, NP_Q9, NP_Q10, NP_Q11, NP_Q12, NP_GET_INFLUENCER,
    S_START, S_Q1, S_Q2, S_Q3, S_Q4, S_Q5, S_Q6, S_Q7, S_Q8, S_Q9, S_Q10, S_Q11, S_Q12, S_Q13, S_GET_INFLUENCER, S_GET_USERNAME,
    EP_Q1_CODES_DONE, EP_END_FLOW,
    
    # New states for NP flow continuation
    NP_Q2_URL_DONE, NP_Q3_URL_DONE, NP_Q4_URL_DONE, NP_Q5_GOTO_DONE, NP_Q6_URL_DONE,
    NP_Q7_CODES_DONE, NP_Q8_GOTO_DONE, NP_Q10_GOTO_DONE, NP_Q11_GOTO_DONE, NP_END_FLOW,

    # New states for S flow continuation
    S_Q2_URL_DONE, S_Q3_URL_DONE, S_Q4_URL_DONE, S_Q5_GOTO_DONE, S_Q6_URL_DONE,
    S_Q7_CODES_DONE, S_Q8_GOTO_DONE, S_Q10_GOTO_DONE, S_Q11_GOTO_DONE, S_Q12_ACTION_DONE, S_END_FLOW

) = range(61)


# === HELPER FUNCTIONS ===

def s(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Gets the language string dict for the user."""
    return STRINGS.get(context.user_data.get('lang', 'en'), STRINGS['en'])

def get_config(key: str) -> str | list:
    """Gets a value from the CONFIGURATION dict."""
    return CONFIGURATION.get(key, f"ERROR_NO_CONFIG_FOR_{key}")

async def send_go_to_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_key: str, next_state: int = None):
    """Sends a message with a 'Go to Channel' button."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings['go_to_channel_btn'], url=get_config('YOUR_CHANNEL_LINK'))],
    ]
    if next_state:
        keyboard.append([InlineKeyboardButton(lang_strings['btn_continue'], callback_data=f"continue_{next_state}")])
    else:
        keyboard.append([InlineKeyboardButton(lang_strings['btn_back'], callback_data="main_menu")])

    await query.edit_message_text(
        text=lang_strings[message_key],
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return MAIN_MENU if not next_state else next_state

async def send_go_to_link(update: Update, context: ContextTypes.DEFAULT_TYPE, message_key: str, button_key: str, config_link_key: str, next_state: int = None):
    """Sends a message with a 'Go to Link' button."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings[button_key], url=get_config(config_link_key))],
    ]
    if next_state:
        keyboard.append([InlineKeyboardButton(lang_strings['btn_continue'], callback_data=f"continue_{next_state}")])
    else:
        keyboard.append([InlineKeyboardButton(lang_strings['btn_back'], callback_data="main_menu")])

    await query.edit_message_text(
        text=lang_strings[message_key],
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return MAIN_MENU if not next_state else next_state

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question_key: str, current_state: int, yes_text_key='btn_yes', no_text_key='btn_no'):
    """Sends a standard Yes/No question."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [
            InlineKeyboardButton(lang_strings[yes_text_key], callback_data=f"yes_{current_state}"),
            InlineKeyboardButton(lang_strings[no_text_key], callback_data=f"no_{current_state}")
        ],
        [InlineKeyboardButton(lang_strings['btn_back'], callback_data="main_menu")]
    ]
    
    text = lang_strings[question_key]
    
    if query:
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    else:
        # This happens on /start
        await update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        
    return current_state

async def send_b_options(update: Update, context: ContextTypes.DEFAULT_TYPE, message_key: str, b1_key: str, b2_key: str, current_state: int):
    """Sends the B-1 and B-2 options for a 'No' answer."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings[b1_key], callback_data=f"b1_{current_state}")],
        [InlineKeyboardButton(lang_strings[b2_key], callback_data=f"b2_{current_state}")],
        [InlineKeyboardButton(lang_strings['btn_back'], callback_data="main_menu")]
    ]
    
    await query.answer()
    await query.edit_message_text(
        text=lang_strings[message_key],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    return current_state

async def send_codes(update: Update, context: ContextTypes.DEFAULT_TYPE, next_state: int) -> int:
    """Sends the list of island codes."""
    lang_strings = s(context)
    query = update.callback_query
    
    codes = get_config('ISLAND_CODES')
    codes_text = "\n".join(f"`{code}`" for code in codes)
    text = f"{lang_strings['codes_message']}\n\n{codes_text}"
    
    keyboard = [
        [InlineKeyboardButton(s(context)['btn_continue'], callback_data=f"continue_{next_state}")],
        [InlineKeyboardButton(lang_strings['btn_back'], callback_data="main_menu")]
    ]
    
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    return next_state

# === START & MAIN MENU ===

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
            InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton("Français 🇫🇷", callback_data="lang_fr"),
        ]
    ]
    if update.message:
        await update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        
    return SELECT_LANG

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen language and shows the main menu."""
    query = update.callback_query
    context.user_data['lang'] = query.data.split('_')[1] # 'lang_en' -> 'en'
    return await show_main_menu(update, context, welcome=True)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, welcome: bool = False) -> int:
    """Shows the main 3-button menu."""
    lang_strings = s(context)
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton(lang_strings['btn_existing'], callback_data="existing_start")],
        [InlineKeyboardButton(lang_strings['btn_new'], callback_data="new_start")],
        [InlineKeyboardButton(lang_strings['btn_support'], callback_data="support_start")],
    ]
    
    text = lang_strings['welcome'] if welcome else lang_strings['main_menu_text']
    
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        # Failsafe for /cancel or other returns
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
    return MAIN_MENU

# === FLOW ENTRY POINTS ===

async def existing_player_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['ep_start'], parse_mode='Markdown')
    return await send_question(update, context, 'ep_q1', EP_Q1)

async def new_player_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['np_start'], parse_mode='Markdown')
    return await send_question(update, context, 'np_q1', NP_Q1)

async def support_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['s_start'], parse_mode='Markdown')
    return await send_question(update, context, 'np_q1', S_Q1) # Support Q1 is same as NP Q1

# === TEXT INPUT HANDLERS ===

async def get_influencer(update: Update, context: ContextTypes.DEFAULT_TYPE, next_state: int) -> int:
    """Asks for influencer name."""
    query = update.callback_query
    await query.answer()
    context.user_data['next_state_after_influencer'] = next_state
    await query.edit_message_text(text=s(context)['prompt_influencer'])
    return context.user_data['current_influencer_state'] # e.g., EP_GET_INFLUENCER

async def save_influencer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves influencer name and moves to the next logical step."""
    influencer_name = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} submitted influencer name: {influencer_name}")
    
    await update.message.reply_text(s(context)['prompt_thanks_influencer'])
    
    next_state = context.user_data.pop('next_state_after_influencer', MAIN_MENU)
    
    if next_state == MAIN_MENU:
        return await show_main_menu(update, context)
    elif next_state == EP_END_FLOW:
        await update.message.reply_text(s(context)['ep_end_flow'])
        return await show_main_menu(update, context)
    elif next_state == NP_END_FLOW:
        await update.message.reply_text(s(context)['np_end_flow'])
        return await show_main_menu(update, context)
    else:
        # This is for the Support flow, move to Q13
        return await send_question(update, context, 's_q13', S_Q13, 's_q13_yes', 's_q13_no')

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for @username."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=s(context)['prompt_username'])
    return S_GET_USERNAME

async def save_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves @username and logs it."""
    username = update.message.text
    if username.startswith('@') and len(username) > 2:
        user_id = update.message.from_user.id
        logger.info(f"*** SUPPORT REQUEST from user {user_id}: {username} ***")
        
        await update.message.reply_text(s(context)['prompt_thanks_username'])
        await update.message.reply_text(s(context)['s_end_flow'])
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(s(context)['prompt_invalid_username'])
        return S_GET_USERNAME # Stay in this state

# === GENERIC BUTTON HANDLERS ===

async def handle_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles all 'Yes' button presses."""
    query = update.callback_query
    state = int(query.data.split('_')[1]) # 'yes_10' -> 10 (which is EP_Q1)

    # Map of "Yes" press in STATE -> action (ask next question)
    YES_MAP = {
        # Existing Player
        EP_Q1: lambda: send_question(update, context, 'ep_q2', EP_Q2, 'ep_q2_yes'),
        EP_Q2: lambda: send_question(update, context, 'ep_q3', EP_Q3),
        EP_Q3: lambda: send_question(update, context, 'ep_q4', EP_Q4),
        EP_Q4: lambda: send_question(update, context, 'ep_q5', EP_Q5),
        EP_Q5: lambda: send_question(update, context, 'ep_q6', EP_Q6, 'ep_q6_yes'),
        EP_Q6: lambda: get_influencer(update, context, next_state=EP_END_FLOW),
        
        # New Player
        NP_Q1: lambda: send_question(update, context, 'np_q2', NP_Q2),
        NP_Q2: lambda: send_question(update, context, 'np_q3', NP_Q3, 'np_q3_yes'),
        NP_Q3: lambda: send_question(update, context, 'np_q4', NP_Q4),
        NP_Q4: lambda: send_question(update, context, 'np_q5', NP_Q5),
        NP_Q5: lambda: send_question(update, context, 'np_q6', NP_Q6),
        NP_Q6: lambda: send_question(update, context, 'ep_q1', NP_Q7), # Q7 is same as EP Q1
        NP_Q7: lambda: send_question(update, context, 'ep_q2', NP_Q8, 'ep_q2_yes'), # Q8 is same as EP Q2
        NP_Q8: lambda: send_question(update, context, 'ep_q3', NP_Q9), # Q9 is same as EP Q3
        NP_Q9: lambda: send_question(update, context, 'ep_q4', NP_Q10), # Q10 is same as EP Q4
        NP_Q11: lambda: send_question(update, context, 'ep_q5', NP_Q11), # Q11 is same as EP Q5
        NP_Q11: lambda: send_question(update, context, 'ep_q6', NP_Q12, 'ep_q6_yes'), # Q12 is same as EP Q6
        NP_Q12: lambda: get_influencer(update, context, next_state=NP_END_FLOW),

        # Support
        S_Q1: lambda: send_question(update, context, 'np_q2', S_Q2),
        S_Q2: lambda: send_question(update, context, 'np_q3', S_Q3, 'np_q3_yes'),
        S_Q3: lambda: send_question(update, context, 'np_q4', S_Q4),
        S_Q4: lambda: send_question(update, context, 'np_q5', S_Q5),
        S_Q5: lambda: send_question(update, context, 'np_q6', S_Q6),
        S_Q6: lambda: send_question(update, context, 'ep_q1', S_Q7), # Q7
        S_Q7: lambda: send_question(update, context, 'ep_q2', S_Q8, 'ep_q2_yes'), # Q8
        S_Q8: lambda: send_question(update, context, 'ep_q3', S_Q9), # Q9
        S_Q9: lambda: send_question(update, context, 'ep_q4', S_Q10), # Q10
        S_Q10: lambda: send_question(update, context, 'ep_q5', S_Q11), # Q11
        S_Q11: lambda: send_question(update, context, 's_q12', S_Q12, 's_q12_yes', 's_q12_no'), # Q12
        S_Q12: lambda: get_influencer(update, context, next_state=S_Q13), # 'Yes' -> Get Influencer
        S_Q13: lambda: get_username(update, context), # 'Yes' -> Get Username
    }
    
    action = YES_MAP.get(state)
    if action:
        return await action()
    
    logger.warning(f"No 'YES' action defined for state {state}")
    return MAIN_MENU

async def handle_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles all 'No' button presses."""
    query = update.callback_query
    state = int(query.data.split('_')[1]) # 'no_10' -> 10 (which is EP_Q1)

    # Map of "No" press in STATE -> action (show B1/B2 options)
    NO_MAP = {
        # Existing Player
        EP_Q1: lambda: send_b_options(update, context, 'ep_q1_no', 'ep_q1_b1', 'ep_q1_b2', EP_Q1),
        EP_Q2: lambda: send_b_options(update, context, 'ep_q2_no', 'ep_q2_b1', 'ep_q2_b2', EP_Q2),
        EP_Q3: lambda: send_b_options(update, context, 'ep_q3_no', 'btn_yes', 'ep_q3_b2', EP_Q3), # B1 is "Yes"
        EP_Q4: lambda: send_b_options(update, context, 'ep_q4_no', 'btn_yes', 'ep_q4_b2', EP_Q4), # B1 is "Yes"
        EP_Q5: lambda: send_b_options(update, context, 'ep_q5_no', 'btn_yes', 'ep_q5_b2', EP_Q5), # B1 is "Yes"
        EP_Q6: lambda: send_go_to_channel(update, context, 'ep_q6_no_action'),

        # New Player
        NP_Q1: lambda: send_b_options(update, context, 'np_q1_no', 'np_q1_b1', 'np_q1_b2', NP_Q1),
        NP_Q2: lambda: send_b_options(update, context, 'np_q2_no', 'btn_yes', 'np_q2_b2', NP_Q2),
        NP_Q3: lambda: send_b_options(update, context, 'np_q3_no', 'btn_yes', 'np_q3_b2', NP_Q3),
        NP_Q4: lambda: send_b_options(update, context, 'np_q4_no', 'btn_yes', 'np_q4_b2', NP_Q4),
        NP_Q5: lambda: send_b_options(update, context, 'np_q5_no', 'np_q5_b1', 'np_q5_b2', NP_Q5),
        NP_Q6: lambda: send_b_options(update, context, 'np_q6_no', 'btn_yes', 'btn_no', NP_Q6),
        NP_Q7: lambda: send_b_options(update, context, 'ep_q1_no', 'ep_q1_b1', 'ep_q1_b2', NP_Q7),
        NP_Q8: lambda: send_b_options(update, context, 'ep_q2_no', 'ep_q2_b1', 'ep_q2_b2', NP_Q8),
        NP_Q9: lambda: send_b_options(update, context, 'ep_q3_no', 'btn_yes', 'btn_no', NP_Q9),
        NP_Q10: lambda: send_b_options(update, context, 'ep_q4_no', 'ep_q4_b1_action', 'ep_q4_b2', NP_Q10), # Use B1 text
        NP_Q11: lambda: send_b_options(update, context, 'ep_q5_no', 'btn_yes', 'ep_q5_b2', NP_Q11),
        NP_Q12: lambda: send_go_to_channel(update, context, 'ep_q6_no_action'), # Same as EP_Q6

        # Support
        S_Q1: lambda: send_b_options(update, context, 'np_q1_no', 'np_q1_b1', 'np_q1_b2', S_Q1),
        S_Q2: lambda: send_b_options(update, context, 'np_q2_no', 'btn_yes', 'np_q2_b2', S_Q2),
        S_Q3: lambda: send_b_options(update, context, 'np_q3_no', 'btn_yes', 'np_q3_b2', S_Q3),
        S_Q4: lambda: send_b_options(update, context, 'np_q4_no', 'btn_yes', 'np_q4_b2', S_Q4),
        S_Q5: lambda: send_b_options(update, context, 'np_q5_no', 'np_q5_b1', 'np_q5_b2', S_Q5),
        S_Q6: lambda: send_b_options(update, context, 'np_q6_no', 'btn_yes', 'btn_no', S_Q6),
        S_Q7: lambda: send_b_options(update, context, 'ep_q1_no', 'ep_q1_b1', 'ep_q1_b2', S_Q7),
        S_Q8: lambda: send_b_options(update, context, 'ep_q2_no', 'ep_q2_b1', 'ep_q2_b2', S_Q8),
        S_Q9: lambda: send_b_options(update, context, 'ep_q3_no', 'btn_yes', 'btn_no', S_Q9),
        S_Q10: lambda: send_b_options(update, context, 'ep_q4_no', 'btn_yes', 's_q10_b2', S_Q10), # Special B2
        S_Q11: lambda: send_b_options(update, context, 'ep_q5_no', 'btn_yes', 'ep_q5_b2', S_Q11),
        S_Q12: lambda: send_question(update, context, 's_q13', S_Q13, 's_q13_yes', 's_q13_no'), # 'No' -> Skip influencer, go to Q13
        S_Q13: lambda: send_go_to_channel(update, context, 's_q13_no_action'),
    }

    action = NO_MAP.get(state)
    if action:
        return await action()
    
    logger.warning(f"No 'NO' action defined for state {state}")
    return MAIN_MENU

async def handle_b_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles all B-1 and B-2 button presses."""
    query = update.callback_query
    parts = query.data.split('_') # 'b1_10'
    b_option = parts[0] # 'b1' or 'b2'
    state = int(parts[1]) # 10 (which is EP_Q1)

    # Map of "B" press in STATE -> action
    # We only need to map B1 and B2 presses. "Yes" B-options are handled by handle_yes
    # e.g., Q3 B-1 is 'btn_yes', so its callback is 'yes_EP_Q4', handled by handle_yes
    B_MAP = {
        # Existing Player
        EP_Q1: {
            'b1': lambda: send_codes(update, context, next_state=EP_Q1_CODES_DONE),
            'b2': lambda: send_question(update, context, 'ep_q2', EP_Q2, 'ep_q2_yes') # Go to Q2
        },
        EP_Q2: {
            'b1': lambda: send_go_to_channel(update, context, 'ep_q2_b1_action'),
            'b2': lambda: send_question(update, context, 'ep_q3', EP_Q3) # Go to Q3
        },
        EP_Q3: {
            'b1': lambda: send_question(update, context, 'ep_q4', EP_Q4), # B1 is "Yes" -> Go to Q4
            'b2': lambda: send_go_to_channel(update, context, 'ep_q3_b2_action')
        },
        EP_Q4: {
            'b1': lambda: send_go_to_channel(update, context, 'ep_q4_b1_action'),
            'b2': lambda: send_question(update, context, 'ep_q5', EP_Q5) # B2 is "No..." -> Go to Q5
        },
        EP_Q5: {
            'b1': lambda: send_go_to_channel(update, context, 'ep_q5_b1_action'),
            'b2': lambda: send_question(update, context, 'ep_q6', EP_Q6, 'ep_q6_yes') # Go to Q6
        },
        
        # New Player
        NP_Q1: {
            'b1': lambda: send_question(update, context, 'np_q2', NP_Q2), # B1 is "Yes" -> Go to Q2
            'b2': lambda: send_go_to_channel(update, context, 'np_q1_b2_action')
        },
        NP_Q2: {
            'b1': lambda: send_go_to_link(update, context, 'np_q2_b1_action', 'np_q2_b1_btn', 'XBOX_LINK', next_state=NP_Q3),
            'b2': lambda: send_question(update, context, 'np_q3', NP_Q3, 'np_q3_yes') # Go to Q3
        },
        NP_Q3: {
            'b1': lambda: send_go_to_link(update, context, 'np_q3_b1_action', 'np_q3_b1_btn', 'EPIC_ACTIVATE_LINK', next_state=NP_Q4),
            'b2': lambda: send_go_to_channel(update, context, 'np_q3_b2_action')
        },
        NP_Q4: {
            'b1': lambda: send_go_to_link(update, context, 'np_q4_b1_action', 'np_q4_b1_btn', 'EPIC_REGISTER_LINK', next_state=NP_Q5),
            'b2': lambda: send_go_to_channel(update, context, 'np_q4_b2_action')
        },
        NP_Q5: {
            'b1': lambda: send_go_to_channel(update, context, 'np_q5_b1_action', next_state=NP_Q6),
            'b2': lambda: send_question(update, context, 'np_q6', NP_Q6) # Go to Q6
        },
        NP_Q6: {
            'b1': lambda: send_go_to_link(update, context, 'np_q6_b1_action', 'np_q6_b1_btn', 'XBOX_LINK', next_state=NP_Q7),
            'b2': lambda: send_go_to_channel(update, context, 'np_q6_b2_action')
        },
        NP_Q7: { # Same as EP_Q1
            'b1': lambda: send_codes(update, context, next_state=NP_Q7_CODES_DONE),
            'b2': lambda: send_question(update, context, 'ep_q2', NP_Q8, 'ep_q2_yes') # Go to Q8
        },
        NP_Q8: { # Same as EP_Q2
            'b1': lambda: send_go_to_channel(update, context, 'ep_q2_b1_action', next_state=NP_Q9),
            'b2': lambda: send_question(update, context, 'ep_q3', NP_Q9) # Go to Q9
        },
        NP_Q9: { # Same as EP_Q3
            'b1': lambda: send_question(update, context, 'ep_q4', NP_Q10), # B1 is "Yes" -> Go to Q10
            'b2': lambda: send_go_to_channel(update, context, 'ep_q3_b2_action')
        },
        NP_Q10: { # Use B1 text, not "Yes"
            'b1': lambda: send_go_to_channel(update, context, 'ep_q4_b1_action', next_state=NP_Q11),
            'b2': lambda: send_question(update, context, 'ep_q5', NP_Q11) # B2 is "No..." -> Go to Q11
        },
        NP_Q11: { # Same as EP_Q5
            'b1': lambda: send_go_to_channel(update, context, 'ep_q5_b1_action', next_state=NP_Q12),
            'b2': lambda: send_question(update, context, 'ep_q6', NP_Q12, 'ep_q6_yes') # Go to Q12
        },

        # Support (Mostly same as New Player)
        S_Q1: {
            'b1': lambda: send_question(update, context, 'np_q2', S_Q2), # B1 is "Yes" -> Go to Q2
            'b2': lambda: send_go_to_channel(update, context, 'np_q1_b2_action')
        },
        S_Q2: {
            'b1': lambda: send_go_to_link(update, context, 'np_q2_b1_action', 'np_q2_b1_btn', 'XBOX_LINK', next_state=S_Q3),
            'b2': lambda: send_question(update, context, 'np_q3', S_Q3, 'np_q3_yes') # Go to Q3
        },
        S_Q3: {
            'b1': lambda: send_go_to_link(update, context, 'np_q3_b1_action', 'np_q3_b1_btn', 'EPIC_ACTIVATE_LINK', next_state=S_Q4),
            'b2': lambda: send_go_to_channel(update, context, 'np_q3_b2_action')
        },
        S_Q4: {
            'b1': lambda: send_go_to_link(update, context, 'np_q4_b1_action', 'np_q4_b1_btn', 'EPIC_REGISTER_LINK', next_state=S_Q5),
            'b2': lambda: send_go_to_channel(update, context, 'np_q4_b2_action')
        },
        S_Q5: {
            'b1': lambda: send_go_to_channel(update, context, 'np_q5_b1_action', next_state=S_Q6),
            'b2': lambda: send_question(update, context, 'np_q6', S_Q6) # Go to Q6
        },
        S_Q6: {
            'b1': lambda: send_go_to_link(update, context, 'np_q6_b1_action', 'np_q6_b1_btn', 'XBOX_LINK', next_state=S_Q7),
            'b2': lambda: send_go_to_channel(update, context, 'np_q6_b2_action')
        },
        S_Q7: { # Same as EP_Q1
            'b1': lambda: send_codes(update, context, next_state=S_Q7_CODES_DONE),
            'b2': lambda: send_question(update, context, 'ep_q2', S_Q8, 'ep_q2_yes') # Go to Q8
        },
        S_Q8: { # Same as EP_Q2
            'b1': lambda: send_go_to_channel(update, context, 'ep_q2_b1_action', next_state=S_Q9),
            'b2': lambda: send_question(update, context, 'ep_q3', S_Q9) # Go to Q9
        },
        S_Q9: { # Same as EP_Q3
            'b1': lambda: send_question(update, context, 'ep_q4', S_Q10), # B1 is "Yes" -> Go to Q10
            'b2': lambda: send_go_to_channel(update, context, 'ep_q3_b2_action')
        },
        S_Q10: { # Special B2
            'b1': lambda: send_go_to_channel(update, context, 'ep_q4_b1_action', next_state=S_Q11),
            'b2': lambda: send_question(update, context, 'ep_q5', S_Q11) # B2 is "No..." -> Go to Q11
        },
        S_Q11: { # Same as EP_Q5
            'b1': lambda: send_go_to_channel(update, context, 'ep_q5_b1_action', next_state=S_Q12),
            'b2': lambda: send_question(update, context, 's_q12', S_Q12, 's_q12_yes', 's_q12_no') # Go to Q12
        },
    }

    action = B_MAP.get(state, {}).get(b_option)
    if action:
        return await action()
    
    logger.warning(f"No 'B_OPTION' action defined for state {state} and option {b_option}")
    return MAIN_MENU

# === FALLBACKS ===

async def cancel(update: Update, context: ContextTypes.DEFAULT_ENTRY_POINT) -> int:
    """Cancels and ends the conversation."""
    lang_strings = s(context)
    if update.message:
        await update.message.reply_text(
            lang_strings['main_menu_text'], reply_markup=ReplyKeyboardRemove()
        )
    return await show_main_menu(update, context)


def main() -> None:
    """Run the bot."""
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN environment variable not set!")
        return

    application = Application.builder().token(token).build()

    # --- This is the main conversation handler ---
    
    # Define all question states
    question_states = [
        EP_Q1, EP_Q2, EP_Q3, EP_Q4, EP_Q5, EP_Q6,
        NP_Q1, NP_Q2, NP_Q3, NP_Q4, NP_Q5, NP_Q6, NP_Q7, NP_Q8, NP_Q9, NP_Q10, NP_Q11, NP_Q12,
        S_Q1, S_Q2, S_Q3, S_Q4, S_Q5, S_Q6, S_Q7, S_Q8, S_Q9, S_Q10, S_Q11, S_Q12, S_Q13
    ]
    
    # Create handlers for all question states
    state_handlers = {
        state: [
            CallbackQueryHandler(handle_yes, pattern=f"^yes_{state}$"),
            CallbackQueryHandler(handle_no, pattern=f"^no_{state}$"),
            CallbackQueryHandler(handle_b_option, pattern=f"^b1_{state}$"),
            CallbackQueryHandler(handle_b_option, pattern=f"^b2_{state}$"),
        ] for state in question_states
    }
    
    # Add handler for code "continue" button
    state_handlers[EP_Q1_CODES_DONE] = [CallbackQueryHandler(lambda u, c: send_question(u, c, 'ep_q2', EP_Q2, 'ep_q2_yes'), pattern=f"^continue_{EP_Q1_CODES_DONE}$")]
    
    # Add handlers for all new NP "continue" buttons
    NP_CONTINUE_MAP = {
        NP_Q2_URL_DONE:   lambda u, c: send_question(u, c, 'np_q3', NP_Q3, 'np_q3_yes'),
        NP_Q3_URL_DONE:   lambda u, c: send_question(u, c, 'np_q4', NP_Q4),
        NP_Q4_URL_DONE:   lambda u, c: send_question(u, c, 'np_q5', NP_Q5),
        NP_Q5_GOTO_DONE:  lambda u, c: send_question(u, c, 'np_q6', NP_Q6),
        NP_Q6_URL_DONE:   lambda u, c: send_question(u, c, 'ep_q1', NP_Q7),
        NP_Q7_CODES_DONE: lambda u, c: send_question(u, c, 'ep_q2', NP_Q8, 'ep_q2_yes'),
        NP_Q8_GOTO_DONE:  lambda u, c: send_question(u, c, 'ep_q3', NP_Q9),
        NP_Q10_GOTO_DONE: lambda u, c: send_question(u, c, 'ep_q5', NP_Q11),
        NP_Q11_GOTO_DONE: lambda u, c: send_question(u, c, 'ep_q6', NP_Q12, 'ep_q6_yes'),
    }
    
    for state, action in NP_CONTINUE_MAP.items():
        state_handlers[state] = [CallbackQueryHandler(action, pattern=f"^continue_{state}$")]
    
    # Add handlers for all new S "continue" buttons
    S_CONTINUE_MAP = {
        S_Q2_URL_DONE:    lambda u, c: send_question(u, c, 'np_q3', S_Q3, 'np_q3_yes'),
        S_Q3_URL_DONE:    lambda u, c: send_question(u, c, 'np_q4', S_Q4),
        S_Q4_URL_DONE:    lambda u, c: send_question(u, c, 'np_q5', S_Q5),
        S_Q5_GOTO_DONE:   lambda u, c: send_question(u, c, 'np_q6', S_Q6),
        S_Q6_URL_DONE:    lambda u, c: send_question(u, c, 'ep_q1', S_Q7),
        S_Q7_CODES_DONE:  lambda u, c: send_question(u, c, 'ep_q2', S_Q8, 'ep_q2_yes'),
        S_Q8_GOTO_DONE:   lambda u, c: send_question(u, c, 'ep_q3', S_Q9),
        S_Q10_GOTO_DONE:  lambda u, c: send_question(u, c, 'ep_q5', S_Q11),
        S_Q11_GOTO_DONE:  lambda u, c: send_question(u, c, 's_q12', S_Q12, 's_q12_yes', 's_q12_no'),
        S_Q12_ACTION_DONE: lambda u, c: send_question(u, c, 's_q13', S_Q13, 's_q13_yes', 's_q13_no'),
    }

    for state, action in S_CONTINUE_MAP.items():
        state_handlers[state] = [CallbackQueryHandler(action, pattern=f"^continue_{state}$")]

    # Add text input handlers
    state_handlers[EP_GET_INFLUENCER] = [MessageHandler(filters.TEXT & ~filters.COMMAND, save_influencer)]
    state_handlers[NP_GET_INFLUENCER] = [MessageHandler(filters.TEXT & ~filters.COMMAND, save_influencer)]
    state_handlers[S_GET_INFLUENCER] = [MessageHandler(filters.TEXT & ~filters.COMMAND, save_influencer)]
    state_handlers[S_GET_USERNAME] = [MessageHandler(filters.TEXT & ~filters.COMMAND, save_username)]

    # Add special states
    state_handlers[SELECT_LANG] = [CallbackQueryHandler(set_language, pattern="^lang_(en|fr)$")]
    state_handlers[MAIN_MENU] = [
        CallbackQueryHandler(existing_player_start, pattern="^existing_start$"),
        CallbackQueryHandler(new_player_start, pattern="^new_start$"),
        CallbackQueryHandler(support_start, pattern="^support_start$"),
    ]
    
    # Store the influencer states for the helper function
    for state in [EP_Q6, NP_Q12, S_Q12]:
        state_handlers[state].append(
             CallbackQueryHandler(
                 lambda u, c, s=state: get_influencer(u, c, next_state=(S_Q13 if s == S_Q12 else (EP_END_FLOW if s == EP_Q6 else NP_END_FLOW))),
                 pattern=f"^yes_{state}$"
             )
        )
    # Add special handler for S_Q12_NO
    state_handlers[S_Q12].append(
        CallbackQueryHandler(
            lambda u, c: send_go_to_channel(u, c, 's_q12_action', next_state=S_Q12_ACTION_DONE),
            pattern=f"^no_{S_Q12}$"
        )
    )

    context.user_data['current_influencer_state'] = {
        EP_Q6: EP_GET_INFLUENCER,
        NP_Q12: NP_GET_INFLUENCER,
        S_Q12: S_GET_INFLUENCER,
    }


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_cmd)],
        states=state_handlers,
        fallbacks=[
            CallbackQueryHandler(show_main_menu, pattern="^main_menu$"),
            CommandHandler("start", start_cmd),
            CommandHandler("cancel", cancel)
        ],
        per_message=False
    )

    application.add_handler(conv_handler)

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()





