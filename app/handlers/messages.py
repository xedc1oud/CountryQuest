import asyncio
import random

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.requests import UserRequest, CountryRequest, GroupRequest

user = Router()

@user.message(CommandStart())
async def cmdStart(message: Message, session: AsyncSession):
    userReq = UserRequest(session)
    
    user = await userReq.get_user(message.from_user.id)
    if not user:
        await userReq.add_user(
            telegram=message.from_user.id,
            username=message.from_user.username,
            name=message.from_user.first_name
        )
        await message.reply(f"<b>🪖 H-hello... Well, let's get started.</b>")
    else:
        await userReq.update(
            telegram=message.from_user.id,
            username=message.from_user.username,
            name=user.name if user.name else message.from_user.first_name
        )
        emoji = ['😣', '😫', '🪖', '😪', '😴', '🤕', '🫩']
        await message.reply(f"<b>{random.choice(emoji)} {user.name}, is that you?.. I'm re-checking the data...</b>")
        

@user.message(F.text.startswith("Country") | F.text.startswith("country"))
async def cmdQuiz(message: Message):
    text_lower = message.text.lower()
    question_part = text_lower[len("country"):].strip()
    
    responses = {
        "how are you": [
            "Sigh... trying to stay afloat... but my strength is fading.",
            "These questions again... I'm just trying not to fall asleep.",
            "Commander Country... I remember, but it doesn't change much...",
            "I... Suomi... Sisu... Protokol... it's all... fragments.",
            "Winter War... these memories again... I'm tired.",
            "Trying to piece together who I was... but it's difficult.",
            "I'm... sort of alive... but my memory... is unclear.",
            "Almost no energy... but I try to understand something.",
            "It seems there was someone who helped me... Protocol...",
            "I try to remember, but the details slip away...",
            "I'm just... trying to work... even if it barely makes sense."
        ],
        "what are you doing": [
            "Nothing special... just trying to survive.",
            "Someone removed my abilities... and I'm still trying to remember myself...",
            "Requested data... they remain silent... as always.",
            "Country... Who am I?.. I don't know... tired of thinking about it.",
            "Just trying to understand what's happening... and why it's so hard.",
            "I'm restoring memory... piece by piece... slowly.",
            "It seems there used to be a combat protocol... now only fragments.",
            "Trying to recall the Protocol... that person... they were nearby...",
            "Sometimes thoughts get tangled... hard to pull myself together.",
            "Doing what I can... while I have the strength...",
            "I'm just trying to understand... who I was and who I became."
        ]
    }

    emoji = ['😩', '😫', '🪖', '😪', '😴', '🥱', '😔', '🥀', '🩹', '🫠']

    if message.from_user.id == 6700061194:
        await message.reply(
            f"<b>{random.choice(emoji)} General Protocol?.. Help me... I'm trying to remember... I have almost no strength...</b>"
        )
    elif "how are you" in question_part:
        await message.reply(f"<b>{random.choice(emoji)} {random.choice(responses['how are you'])}</b>")
    elif "what are you doing" in question_part:
        await message.reply(f"<b>{random.choice(emoji)} {random.choice(responses['what are you doing'])}</b>")
    else:
        pass


@user.message(Command("profile"))
async def cmdProfile(message: Message, session: AsyncSession):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    groupReq = GroupRequest(session)

    user = await userReq.get_user(message.from_user.id)
    if user:
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
        
        group_id = message.chat.id
        group = await groupReq.get_group(group_id)
        country = await countryReq.get_country(user.id, group_id)
        created_date = user.created_at
        formatted_date = f"{created_date.day} {months[created_date.month - 1]} {created_date.year} at {created_date.strftime('%H:%M')}"
        
        match user.telegram:
            case owner if owner == group.owner:
                text = "\n\n<b>👨‍💼 You are the owner of this chat!</b>"
            case admin if admin in group.admins:
                text = "\n\n<b>🛡️ You are an administrator of this chat!</b>"
            case _:
                text = ""
        
        await message.reply(
            f"<b>👤 You again?.. Fine, checking the archive...</b>\n\n"
            f"<b>💬 Nickname:</b> <i>{user.name if user.name else 'Not specified'}</i>\n"
            f"<b>🌍 Country:</b> <i>{country.name if country else 'Not specified'}</i>\n"
            f"<b>📅 Registered:</b> <i>{formatted_date}</i>\n"
            f"<b>🆔 ID:</b> <code>{user.id}</code>\n"
            f"<b>🤵🏼‍♂️ Admin level:</b> <i>{user.admin}</i>"
            f"{text}"
        )
    else:
        pass


@user.message(Command("nick"))
async def cmdNick(message: Message, session: AsyncSession, command: CommandObject):
    userReq = UserRequest(session)
    
    user = await userReq.get_user(message.from_user.id)
    if user:
        if command.args:
            new_nick = command.args.strip()
            if len(new_nick) > 30:
                await message.reply(
                    "<b>❌ Nickname too long. Maximum 30 characters. Please try again...</b>"
                )
                return
            
            result = await userReq.update(telegram=message.from_user.id, name=new_nick)                      
            await message.reply(f"<b>✅ Nickname changed to:</b> <i>{new_nick}</i>")
        else:
            await message.reply(
                "<b>❌ You didn't provide a nickname. Use the command like this:</b>\n\n<code>/nick YourNewNick</code>"
            )
    else:
        pass


@user.message(Command("clear"))
async def cmdClear(message: Message, state: FSMContext):
    await state.clear()
    await message.reply(
        "<b>🗑️ Your temporary data has been cleared. I don't even know why you need this...</b>"
    )
