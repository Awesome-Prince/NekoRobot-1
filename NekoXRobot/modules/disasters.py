import html
import json
import os
from typing import Optional

from NekoXRobot import (DEV_USERS, OWNER_ID, DRAGONS, SUPPORT_CHAT, DEMONS,
                          TIGERS, WOLVES, dispatcher)
from NekoXRobot.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           whitelist_plus)
from NekoXRobot.modules.helper_funcs.extraction import extract_user
from NekoXRobot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'NekoXRobot/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
#disasters =
# """ Text here """

# do not async, not a handler
#def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("This member is already a A Rank Hunter")
        return ""

    if user_id in DEMONS:
        rt += "Requested HA to promote a B Rank Hunter to A Rank Hunter."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested HA to promote a D Rank Hunter to A Rank Hunter."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['sudos'].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Power Level {} to A Rank Hunter!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Requested HA to demote this A Rank Hunter to B Rank Hunter"
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("This user is already a B Rank Hunter.")
        return ""

    if user_id in WOLVES:
        rt += "Requested HA to promote this D Rank Hunter to B Rank Hunter"
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['supports'].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a B Rank Hunter!")

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a A Rank Hunter, Demoting to D Rank Hunter."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a B Rank Hunter, Demoting to D Rank Hunter."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("This user is already a D Rank Hunter.")
        return ""

    data['whitelists'].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a D Rank Hunter!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a A Rank Hunter, Demoting to C Rank Hunter."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a B Rank Hunter, Demoting to C Rank Hunter."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "This user is already a D Rank Hunter, Demoting to C Rank Hunter."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("This user is already a C Rank Hunter.")
        return ""

    data['tigers'].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a C Rank Hunter!"
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("Requested HA to demote this user to Civilian")
        DRAGONS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a A Rank Hunter!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("Requested HA to demote this user to Civilian")
        DEMONS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a B Rank Hunter!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("Demoting to normal user")
        WOLVES.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a D Rank Hunter!")
        return ""


@run_async
@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("Demoting to normal user")
        TIGERS.remove(user_id)
        data['tigers'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Tiger Disaster!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Known D Rank Hunters 🐺:</b>\n"
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>Known C Rank Hunters 🐯:</b>\n"
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known B Rank Hunters 👹:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>Known A Rank Hunters 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>S Rank Hunters ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands. 

 ╔ *List all special users:*
 ╠ `/aranks`*:* Lists all A Rank Hunters
 ╠ `/branks`*:* Lists all B Rank Hunters
 ╠ `/cranks`*:* Lists all C Rank Hunters
 ╠ `/dranks`*:* Lists all D Rank Hunters
 ╠ `/sranks`*:* Lists all S Rank Hunters
 ╠ `/addarank`*:* Adds a user to A Rank Hunter
 ╠ `/addbrank`*:* Adds a user to B Rank Hunter
 ╠ `/addcrank`*:* Adds a user to C Rank Hunter
 ╠ `/adddrank`*:* Adds a user to D Rank Hunter
 ╚ `Add dev doesnt exist, devs should know how to add themselves`

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Groups Info:*
 ╠ `/groups`*:* List the groups with Name, ID, members count as a txt
 ╠ `/leave <ID>`*:* Leave the group, ID must have hyphen
 ╠ `/stats`*:* Shows overall bot stats
 ╠ `/getchats`*:* Gets a list of group names the user has been seen in. Bot owner only
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Access control:* 
 ╠ `/ignore`*:* Blacklists a user from 
 ╠  using the bot entirely
 ╠ `/notice`*:* Removes user from blacklist
 ╚ `/ignoredlist`*:* Lists ignored users

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Prints modules and their names
 ╠ `/unload <name>`*:* Unloads module dynamically
 ╚ `/load <name>`*:* Loads module

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Global Bans:*
 ╠ `/gban user reason`*:* Globally bans a user
 ╚ `/ungban user reason`*:* Unbans the user from the global bans list

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to 
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot 

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rpunch user group`*:* Remote punch
 ╠ `/rmute user group`*:* Remote mute
 ╚ `/runmute user group`*:* Remote un-mute

 ╔ *Windows self hosted only:*
 ╠ `/reboot`*:* Restarts the bots service
 ╚ `/gitpull`*:* Pulls the repo and then restarts the bots service

 ╔ *Chatbot:* 
 ╚ `/listaichats`*:* Lists the chats the chatmode is enabled in
 
 ╔ *Debugging and Shell:* 
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/logs`*:* Run this in support group to get logs in pm
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Runs shell command
 ╠ `/shell`*:* Runs shell command
 ╠ `/clearlocals`*:* As the name goes
 ╠ `/dbcleanup`*:* Removes deleted accs and groups from db
 ╚ `/py`*:* Runs python code
 
 ╔ *Global Bans:*
 ╠ `/gban <id> <reason>`*:* Gbans the user, works by reply too
 ╠ `/ungban`*:* Ungbans the user, same usage as gban
 ╚ `/gbanlist`*:* Outputs a list of gbanned users

Visit @{SUPPORT_CHAT} for more information.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "addarank"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "addbrank"), addsupport)
TIGER_HANDLER = CommandHandler(("addtiger" , "addcrank"), addtiger)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "adddrank"), addwhitelist)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removearank"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removebrank"),
                                   removesupport)
UNTIGER_HANDLER = CommandHandler(("removetiger" , "removecrank"), removetiger)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removedrank"),
                                     removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "dranks"],
                                       whitelistlist)
TIGERLIST_HANDLER = CommandHandler(["tigers" , "cranks"], tigerlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "branks"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "aranks"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "sranks"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Ranks"
__handlers__ = [
    SUDO_HANDLER, SUPPORT_HANDLER, TIGER_HANDLER, WHITELIST_HANDLER,
    UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNTIGER_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, TIGERLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER
]
