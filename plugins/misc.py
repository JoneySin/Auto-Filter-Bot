import os
from info import ADMINS
from speedtest import Speedtest, ConfigRetrievalError
from pyrogram import Client, filters, enums
from utils import get_size
from datetime import datetime
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
import logging


@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    replied_to_msg = bool(message.reply_to_message)
    if replied_to_msg:
        return await message.reply_text(f"""The forwarded message channel {replied_to_msg.chat.title}'s id is, <code>{replied_to_msg.chat.id}</code>.""")
    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text(f'🦹 User ID: <code>{message.from_user.id}</code>')

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply_text(f'👪 Group ID: <code>{message.chat.id}</code>')

    elif chat_type == enums.ChatType.CHANNEL:
        await message.reply_text(f'📣 Channel ID: <code>{message.chat.id}</code>')


@Client.on_message(filters.command('speedtest') & filters.user(ADMINS))
async def speedtest(client, message):
    #from - https://github.com/weebzone/WZML-X/blob/master/bot/modules/speedtest.py
    msg = await message.reply_text("Initiating Speedtest...")
    try:
        speed = Speedtest()
    except ConfigRetrievalError:
        await msg.edit("Can't connect to Server at the Moment, Try Again Later !")
        return
    speed.get_best_server()
    speed.download()
    speed.upload()
    speed.results.share()
    result = speed.results.dict()
    photo = result['share']
    text = f'''
➲ <b>SPEEDTEST INFO</b>
┠ <b>Upload:</b> <code>{get_size(result['upload'])}/s</code>
┠ <b>Download:</b>  <code>{get_size(result['download'])}/s</code>
┠ <b>Ping:</b> <code>{result['ping']} ms</code>
┠ <b>Time:</b> <code>{datetime.strptime(result['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")}</code>
┠ <b>Data Sent:</b> <code>{get_size(int(result['bytes_sent']))}</code>
┖ <b>Data Received:</b> <code>{get_size(int(result['bytes_received']))}</code>

➲ <b>SPEEDTEST SERVER</b>
┠ <b>Name:</b> <code>{result['server']['name']}</code>
┠ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
┠ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
┠ <b>Latency:</b> <code>{result['server']['latency']}</code>
┠ <b>Latitude:</b> <code>{result['server']['lat']}</code>
┖ <b>Longitude:</b> <code>{result['server']['lon']}</code>

➲ <b>CLIENT DETAILS</b>
┠ <b>IP Address:</b> <code>{result['client']['ip']}</code>
┠ <b>Latitude:</b> <code>{result['client']['lat']}</code>
┠ <b>Longitude:</b> <code>{result['client']['lon']}</code>
┠ <b>Country:</b> <code>{result['client']['country']}</code>
┠ <b>ISP:</b> <code>{result['client']['isp']}</code>
┖ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    await message.reply_photo(photo=photo, caption=text)
    await msg.delete()
