from telegram.ext import run_async

from NekoXRobot import dispatcher
from NekoXRobot.modules.disable import DisableAbleCommandHandler
from NekoXRobot.modules.helper_funcs.alternate import send_message
from NekoXRobot.modules.helper_funcs.chat_status import user_admin


@run_async
@dev_plus
def send(update, context):
    args = update.effective_message.text.split(None, 1)
    creply = args[1]
    send_message(update.effective_message, creply)


ADD_CCHAT_HANDLER = DisableAbleCommandHandler("snd", send)
dispatcher.add_handler(ADD_CCHAT_HANDLER)
__command_list__ = ["snd"]
__handlers__ = [ADD_CCHAT_HANDLER]
