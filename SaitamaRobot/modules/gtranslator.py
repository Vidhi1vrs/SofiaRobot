from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from gpytranslate import SyncTranslator


trans = SyncTranslator()


def translate(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    reply_msg = message.reply_to_message
    if not reply_msg:
        message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Translated from {source} to {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    message.reply_text(reply, parse_mode=ParseMode.HTML)


def languages(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "Click on the button below to see the list of supported language codes.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Language codes",
                        url="https://telegra.ph/Lang-Codes-03-19-3",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )


__help__ = """
• `/tr` or `/tl` (language code) as reply to a long message
*Example:*
  `/tr en`*:* translates something to english
  `/tr hi//en`*:* translates hindi to english
• `/lang `*:* Get a list of languages supported 
"""


TRANSLATE_HANDLER = DisableAbleCommandHandler(["tr", "tl"], translate)
LANGUAGE_HANDLER = DisableAbleCommandHandler(["lang"], languages)

dispatcher.add_handler(TRANSLATE_HANDLER)
dispatcher.add_handler(LANGUAGE_HANDLER)

__mod_name__ = "Translator"
__command_list__ = ["tr", "tl", "lang"]
__handlers__ = [TRANSLATE_HANDLER, LANGUAGE_HANDLER]
