from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import requests
cars_url = requests.get("https://code.visualcoder.ru/json/cars.json").json()

menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "🚘 Sotuv bo'limi", callback_data="shop"), InlineKeyboardButton(text = "💥 Savat", callback_data="savat")],
        [InlineKeyboardButton(text = "🤵 Administrator", url="https://t.me/visualcoderuz")],
    ]
)

cars = list()
for i in cars_url:
    cars.append(i['brend'])

cars2 = list()
for i in set(cars):
    cars2.append(i)
    
cars_shop = InlineKeyboardBuilder()
for i in sorted(cars2):
    cars_shop.add(InlineKeyboardButton(text = f"{i}", callback_data = f"brend-{i}"))
cars_shop.add(InlineKeyboardButton(text="Orqaga", callback_data="back"))
cars_shop.adjust(2)

# cars_shop = InlineKeyboardMarkup(
#     inline_keyboard = [
#         [InlineKeyboardButton(text=f"{cars2[0]}", callback_data=f"brend-{cars2[0]}"), InlineKeyboardButton(text=f"{cars2[1]}", callback_data=f"brend-{cars2[1]}")],
#         [InlineKeyboardButton(text=f"{cars2[2]}", callback_data=f"brend-{cars2[2]}"), InlineKeyboardButton(text=f"{cars2[3]}", callback_data=f"brend-{cars2[3]}")],
#         [InlineKeyboardButton(text=f"{cars2[4]}", callback_data=f"brend-{cars2[4]}"), InlineKeyboardButton(text="Orqaga", callback_data="back")],
#     ]
# )

