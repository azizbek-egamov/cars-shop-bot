import aiogram
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F
from aiogram.filters import Command
from config import TOKEN
from sql import add_information, user_info, delete
from aiogram.utils.keyboard import InlineKeyboardBuilder
from button import menu, cars_shop
from random import randint
from aiogram.utils.deep_linking import create_start_link, decode_payload

import requests
url = requests.get("https://code.visualcoder.ru/json/cars.json").json()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


def process_message(message):

    text = message.text
    cid = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    full_name = message.chat.full_name
    username = message.chat.username
    is_premium = message.from_user.is_premium

    return {
        "text": text,
        "cid": cid,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "username": username,
        "is_premium": is_premium,
    }

@dp.message(Command("start"))
async def cmd_start(message: Message):
    msg = process_message(message)
    if len(message.text.split()) > 1:
        refid = message.text.split()[1]
        await bot.send_message(
            chat_id=refid,
            text="<b>📳 Sizda yangi taklif mavjud!</b>",
            parse_mode='html')
    await bot.send_message(
        chat_id=msg["cid"],
        text = f"<b>👋 Salom {msg["full_name"]}</b>",
        reply_markup = menu,
        parse_mode = ParseMode.HTML)
    
@dp.callback_query(F.data == "back")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(
        text=f"Salom {callback.from_user.full_name}",
        reply_markup=menu
    )
    
@dp.message(Command("ref"))
async def referral(message: Message):
    link = await create_start_link(bot,str(f"user-{message.from_user.id}"))
    await message.answer(
        text = f"Bu sizning referal havolangiz: {link}"
    )
    
    
@dp.callback_query(F.data == "shop")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(
        text = "Bizdagi berndlar ro'yhati",
        reply_markup=cars_shop.as_markup()
    )
    
@dp.callback_query(F.data.startswith("brend-"))
async def callbacks_num(callback: CallbackQuery):
    action = callback.data.split("-")
    br = action[1]
    btn = InlineKeyboardBuilder()
    for i in url:
        if i["brend"] == br:
            btn.add(InlineKeyboardButton(text=f"{i['model']}", callback_data=f"model-{br}-{i["model"]}"))
    btn.add(InlineKeyboardButton(text="Orqaga", callback_data="shop"))
    btn.adjust(2)
    await callback.message.answer(
        text="Mashinalar ro'yhati",
        reply_markup=btn.as_markup()
    )    

@dp.callback_query(F.data.startswith("model-"))
async def callbacks_num(callback: CallbackQuery):
    action = callback.data.split("-")
    br = action[1]
    md = action[2]
    for i in url:
        if i["brend"] == br and i["model"] == md:
            keys = InlineKeyboardMarkup(
                inline_keyboard = [
                    [InlineKeyboardButton(text = "🚘 Savatga qo'shish", callback_data=f"ok-{br}-{md}"), InlineKeyboardButton(text = "Orqaga", callback_data=f"brend-{br}")],
                ]
            )
            await callback.message.answer_photo(photo=f"{i['rasm']}", caption=f"Mashina haqida ma'lumotlar:\n\n Brend: {i["brend"]}\nModel: {i["model"]}\nTezlik: {i["tezkorlik"]}\nNarxi: {i["narx"]}$\n\n✅ Savatga qo'shishni istasangiz pastdagi '✅ Savatga qo'shish' tugmasini bosing", reply_markup=keys)
            break
        
@dp.callback_query(F.data.startswith("ok-"))
async def callbacks_num(callback: CallbackQuery):
    action = callback.data.split("-")
    br = action[1]
    md = action[2]
    rand = randint(111111111, 999999999)
    for i in url:
        if i["brend"] == br and i["model"] == md:
            add_information(callback.from_user.id, rand, i["brend"], i["model"], i["narx"], i["rasm"])
    await callback.message.answer(
        text="Mashina savarga qo'shildi",
    )
    
@dp.callback_query(F.data == "savat")
async def send_random_value(callback: CallbackQuery):
    get_auto = user_info(callback.from_user.id)
    if get_auto != False:
        btn = InlineKeyboardBuilder()
        for i in get_auto:
            btn.add(InlineKeyboardButton(text=f"🗑 {list(i)[3]} {list(i)[4]}", callback_data=f"delete-{list(i)[2]}"))
        btn.add(InlineKeyboardButton(text="Orqaga", callback_data="back"))
        btn.adjust(2)
        await callback.message.answer(
            text = "✅ Savatingizdagi mashinalar to'plami. Xozirda buyurtma berolmaysiz, lekin savatdan mashinani olib tashlashingiz mumkin.",
            reply_markup=btn.as_markup())
    else:
        await callback.message.answer("😐 Savatingizda avtomabillar yo'q")
    
@dp.callback_query(F.data.startswith("delete-"))
async def callbacks_num(callback: CallbackQuery):
    action = callback.data.split("-")
    print(action)
    br = action[1]
    try:
        delete(br)
        await callback.message.answer(
            text="✅ Mashina muvaffaqiyatli olib tashlandi",
        )
    except:
        await callback.message.answer(
            text="😐 Mashinani olib tashlashda hatolik yuz berdi.",
        )
        
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Dastur yakunlandi")
