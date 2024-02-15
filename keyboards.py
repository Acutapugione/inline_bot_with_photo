from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def keyboard()->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="<-", callback_data="prev")
    builder.button(text="->", callback_data="next")
    builder.adjust(2)
    return builder.as_markup()