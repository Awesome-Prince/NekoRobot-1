# Simple lyrics module using tswift by @TheRealPhoenix

from tswift import Song

from telegram import Bot, Update, Message, Chat
from telegram.ext import CallbackContext, run_async

from NekoXRobot import dispatcher
from NekoXRobot.modules.disable import DisableAbleCommandHandler
from NekoXRobot.modules.helper_funcs.alternate import typing_action


@run_async
@typing_action
def lyrics(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    msg = update.effective_message
    query = " ".join(args)
    song = ""
    if not query:
        msg.reply_text("You haven't specified which song to look for!")
        return
    else:
        song = Song.find_song(query)
        if song:
            if song.lyrics:
                reply = song.format()
            else:
                reply = "Couldn't find any lyrics for that song!"
        else:
            reply = "Song not found!"
        if len(reply) > 4090:
            with open("lyrics.txt", 'w') as f:
                f.write(f"{reply}\n\n\nOwO UwU OmO")
            with open("lyrics.txt", 'rb') as f:
                msg.reply_document(document=f,
                caption="Message length exceeded max limit! Sending as a text file.")
        else:
            msg.reply_text(reply)

            
__help__ = """
 Want to get the lyrics of your favorite songs straight from the app? This module is perfect for that!
*Available commands:*
 - /lyrics <song>: returns the lyrics of that song.
 You can either enter just the song name or both the artist and song name.
"""

__mod_name__ = "Lyrics"



LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)

dispatcher.add_handler(LYRICS_HANDLER)
