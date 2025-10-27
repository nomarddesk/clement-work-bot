async def save_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves @username, logs it, and notifies admin group."""
    username = update.message.text
    if username.startswith('@') and len(username) > 2:
        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name or "Unknown"
        last_name = update.message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        logger.info(f"*** SUPPORT REQUEST from user {user_id}: {username} ***")
        
        # --- IMPROVED NOTIFICATION BLOCK ---
        # Get the Admin Group ID from environment variables
        ADMIN_GROUP_ID = os.environ.get("ADMIN_GROUP_ID")
        
        if ADMIN_GROUP_ID:
            try:
                # Convert to integer if it's a numeric ID
                try:
                    admin_chat_id = int(ADMIN_GROUP_ID)
                except ValueError:
                    admin_chat_id = ADMIN_GROUP_ID  # it might be a username starting with @
                
                logger.info(f"Attempting to send notification to: {admin_chat_id}")
                
                # Create a more informative message
                text_to_send = (
                    f"🆕 New Support Request:\n"
                    f"👤 User: {full_name}\n"
                    f"🆔 User ID: {user_id}\n"
                    f"📱 Username: {username}\n"
                    f"⏰ Time: {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                
                # Send the notification message to the admin group
                await context.bot.send_message(
                    chat_id=admin_chat_id,
                    text=text_to_send
                )
                logger.info("✅ Successfully sent support notification to admin group.")
                
            except Exception as e:
                # More detailed error logging
                error_msg = f"❌ Failed to send notification to admin group {ADMIN_GROUP_ID}: {str(e)}"
                logger.error(error_msg)
                
                # Also log the type of error for better debugging
                logger.error(f"Error type: {type(e).__name__}")
        else:
            # Log a warning if the environment variable is not set
            logger.error("❌ ADMIN_GROUP_ID environment variable not set. Cannot send notification.")
        
        # Reply to the user (this should always work regardless of admin notification)
        await update.message.reply_text(s(context)['prompt_thanks_username'])
        await update.message.reply_text(s(context)['s_end_flow'])
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(s(context)['prompt_invalid_username'])
        return S_GET_USERNAME  # Stay in this state
