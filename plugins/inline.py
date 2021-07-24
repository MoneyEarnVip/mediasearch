import logging
from urllib.parse import quote

from pyrogram import Client, emoji, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument

from utils import get_search_results, is_subscribed
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

sample_msg = f"""

〽️ Powered By @T2Links

Share and Support us❤️
🎯 Join Now ☞ [Tamil Hd Movies](t.me/tamil_latest_films)
"""  



    
@Client.on_inline_query(filters.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):
    """Show search results for given inline query"""

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to subscribe my channel to use the bot',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        disallowed_characters = "._!"
    for character in disallowed_characters:
        username = file.file_name
        username = username.replace(character, " ")
        caption = f"<code>{username}</code> {sample_msg}"
    if caption is None:
        caption = f"<code>{file.file_name}</code> {sample_msg}"
    results.append(
        InlineQueryResultCachedDocument(
            title=file.file_name,
            file_id=file.file_id,
            caption=f"<code>{username}</code> {sample_msg}",
            description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
            reply_markup=reply_markup))
    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results"
        if string:
            switch_pm_text += f" for {string}"

        await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
    else:

        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('Search again', switch_inline_query_current_chat=query),
            InlineKeyboardButton('More Bots', url='https://t.me/subin_works/122')
        ]
        ]
    return InlineKeyboardMarkup(buttons)


def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

