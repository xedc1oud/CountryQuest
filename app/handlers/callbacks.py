import asyncio
import random
import os

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from data.requests import UserRequest, CountryRequest, EconomyRequest
from data.redis import RedisManager
from keyboards.inline import registry, customize, confirmation, economy_categories, population
from keyboards.pagination import profile
from keyboards.security import SecureKeyboard
from utils.states import Registry
from utils.helpers import flag_texture

user = Router()

# --------------------------------------------------------------------------------

@user.message(Command("country"))
async def cmdCountry(message: Message, session: AsyncSession, secure: SecureKeyboard):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)

    user = await userReq.get_user(message.from_user.id)
    group = message.chat.id

    if message.chat.type == "private":
        await message.reply(
            "<b>😩 Sigh... Country information is only available in groups. I don't even know what else to say...</b>"
        )
        return

    if not user:
        await message.reply(
            "<b>🫠 You're not even registered... Fine, maybe start with /start.</b>"
        )
        return

    country = await countryReq.get_country(uid=user.telegram, group=group)
    if not country:
        await message.reply(
            "<b>😔 It seems you haven't registered a country yet... Try creating one right now...</b>",
            reply_markup=await registry(secure, message.from_user.id)
        )
        return

    elif country and country.group != group:
        await message.reply(
            "<b>😔 It seems you don't have a country in this group... You'll have to create another one. Here's the button.</b>",
            reply_markup=await registry(secure, message.from_user.id)
        )
        return

    base_dir = Path(__file__).parent.parent
    try:
        photo = FSInputFile(f"{base_dir}/photos/{country.cid}.png")

        await message.reply_photo(
            photo=photo,
            caption=(
                "<b>🌍 Alright, here is your country...</b>\n\n"
                f"<b>🪧 Country name:</b> <i>{country.name}</i>\n"
                f"<b>👤 Country leader:</b> <i>{country.leader if country.leader else 'Not specified'}</i>\n"
                "<i>Hmm... who would've thought this would be so complicated.</i>"
            ),
            reply_markup=await profile(secure, message.from_user.id, page=0)
        )
    except:
        await message.reply_photo(
            "<b>🌍 Alright, here is your country...</b>\n\n"
            f"<b>🪧 Country name:</b> <i>{country.name}</i>\n"
            f"<b>👤 Country leader:</b> <i>{country.leader if country.leader else 'Not specified'}</i>\n"
            "<i>Hmm... who would've thought this would be so complicated.</i>",
            reply_markup=await profile(secure, message.from_user.id, page=0)
        )

@user.callback_query(F.data.startswith("profile_page_"))
async def navigate_profile(query: CallbackQuery, secure: SecureKeyboard):
    page = int(query.data.split("_")[-1])
    await query.message.edit_reply_markup(reply_markup=await profile(secure, query.from_user.id, page=page))
    await query.answer()

@user.callback_query(F.data.startswith("back"))
async def back_to_profile(query: CallbackQuery, secure: SecureKeyboard):
    await query.message.edit_reply_markup(reply_markup=await profile(secure, query.from_user.id, page=0))
    await query.answer()

@user.callback_query(F.data.startswith("customize"))
async def open_customize(query: CallbackQuery, secure: SecureKeyboard):
    await query.message.edit_reply_markup(reply_markup=await customize(secure, query.from_user.id))
    await query.answer()
    
@user.callback_query(F.data.startswith("delete"))
async def open_delete(query: CallbackQuery, session: AsyncSession, secure: SecureKeyboard):
    await query.message.reply(
        "<b>⚠ Are you sure you want to delete your country?</b>",
        reply_markup=await confirmation(secure, query.from_user.id)
    )
    await query.answer()
    
@user.callback_query(F.data.startswith("confirm"))
async def confirm_delete(query: CallbackQuery, session: AsyncSession, secure: SecureKeyboard):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    economyReq = EconomyRequest(session)
    
    user = await userReq.get_user(query.from_user.id)
    group = query.message.chat.id
    country = await countryReq.get_country(uid=user.telegram, group=group)
    base_dir = Path(__file__).parent.parent
    
    try:
        os.remove(f"{base_dir}/photos/{country.cid}.png")
        await countryReq.delete_country(cid=country.cid)
        await economyReq.delete_economy(cid=country.cid)
        await query.message.edit_text("<b>🗑 Your country has been successfully deleted.</b>")
        await query.answer()
    except:
        await query.answer()
    
@user.callback_query(F.data.startswith("cancel"))
async def cancel_delete(query: CallbackQuery, secure: SecureKeyboard):
    await query.message.edit_text("<b>❌ Country deletion canceled.</b>")
    await query.answer()
    
# --------------------------------------------------------------------------------

@user.callback_query(F.data.startswith("flag"))
async def cmdFlag(query: CallbackQuery, state: FSMContext):
    await state.set_state(Registry.change_flag)
    await query.message.reply(
        "<b>🏳 Okay... send the new flag for your country. I don't know if it'll look any better, but let's try.</b>"
    )
    await query.answer()
    

@user.message(Registry.change_flag, F.photo)
async def cmdFlag_procces(message: Message, session: AsyncSession, state: FSMContext, bot: Bot, secure: SecureKeyboard):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    
    group = message.chat.id
    user = await userReq.get_user(message.from_user.id)
    country = await countryReq.get_country(uid=user.telegram, group=group)
    if user:
        if country:
            photo = message.photo[-1]
            file_id = photo.file_id
                
            base_dir = Path(__file__).parent.parent
            photos_dir = base_dir / "photos"
            original_photo_path = photos_dir / "1.jpg"
                
            await bot.download(file_id, original_photo_path)
                
            await flag_texture(
                cid=country.cid,
                input_image_path=original_photo_path
            )
                
            try:
                os.remove(original_photo_path)
            except:
                pass
                
            await message.reply("<b>🏳 Okay, the flag has been updated. I hope you're satisfied...</b>")
            await state.clear()
            await asyncio.sleep(0.5)
            await message.reply_photo(
                photo=file_id,
                caption=(
                    "<b>🌍 Here is your country...</b>\n\n"
                    f"<b>🪧 Country name:</b> <i>{country.name}</i>\n"
                    f"<b>👤 Country leader:</b> <i>{country.leader if country.leader else 'Not specified, as usual'}</i>\n"
                    "<i>Yes... sometimes I just want to walk away and forget about all of this.</i>"
                ),
                reply_markup=await profile(secure, message.from_user.id, page=0)
            )
        else:
            await message.reply(
                "<b>❗ It seems you don't have a country. And yes, that's unfortunate...</b>"
            )
    else:
        await message.reply(
            "<b>❗ It seems you don't have a country. And yes, that's unfortunate...</b>"
        )

# --------------------------------------------------------------------------------       
            
@user.callback_query(F.data.startswith("create"))
async def cmdCreate(query: CallbackQuery, session: AsyncSession, state: FSMContext, secure: SecureKeyboard):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    
    user = await userReq.get_user(query.from_user.id)
    group = query.message.chat.id
    
    if query.message.chat.type == "private":
        await query.message.edit_text(
            "<b>😩 Creating a country is only available in groups... I don't even know what else to say.</b>"
        )
        await query.answer()
        return
    else:
        if user:
            country = await countryReq.get_country(uid=user.telegram, group=group)
            if not country:
                await query.message.edit_text("<b>🪖 Are you kidding?... You already have a country</b>")
            
            await state.set_state(Registry.name)
            await query.message.edit_text(
                "<b>🪖 Alright... what will your country be called? Hurry up.</b>"
            )
            await query.answer()
        else:
            pass
    
    
@user.message(Registry.name)
async def cmdCreate_procces(message: Message, session: AsyncSession, state: FSMContext):
    userReq = UserRequest(session)
    
    user = await userReq.get_user(message.from_user.id)
    if user:
        country_name = message.text
        if len(country_name) > 30:
            await message.reply(
                "<b>❌ Country name too long. Maximum 30 characters. Please try again...</b>"
            )
            return
        
        await message.reply(
            "<b>🪖 Okay... now send your country's flag. Pick something at least decent.</b>"
        )
        await state.update_data(name=country_name)
        await state.set_state(Registry.flag)
        
        
@user.message(Registry.flag, F.photo)
async def cmdCreate_procces2(message: Message, state: FSMContext):      
        photo = message.photo[-1]
        file_id = photo.file_id
        await message.reply(
            "<b>🪖 Great... Now provide the name of your country's leader. Yes, we have to do this again.</b>"
        )
        await state.set_state(Registry.leader)
        await state.update_data(flag=file_id)
        
        
@user.message(Registry.leader)
async def cmdCreate_procces3(message: Message, session: AsyncSession, state: FSMContext, bot: Bot):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    economyReq = EconomyRequest(session)
    
    user = await userReq.get_user(message.from_user.id)
    if user:
        
        leader_name = message.text
        if len(leader_name) > 30:
            await message.reply(
                "<b>❌ Leader name too long. Maximum 30 characters. Please try again...</b>"
            )
            return
        
        await state.update_data(leader=leader_name)
        data = await state.get_data()
        
        country_id = random.randint(0, 9999)
        group_id = message.chat.id
        
        await countryReq.add_country(
            cid=country_id,
            uid=user.telegram,
            name=data.get('name'),
            leader=data.get('leader'),
            group=group_id
        )
        await economyReq.add_economy(cid=country_id)
        country = await countryReq.get_country(country_id, group_id)
        
        photo = data.get('flag')
        base_dir = Path(__file__).parent.parent
        photos_dir = base_dir / "photos"
        original_photo_path = photos_dir / "1.jpg"
        
        await bot.download(photo, original_photo_path)
        
        await flag_texture(
            cid=country_id,
            input_image_path=original_photo_path
        )
        
        try:
            os.remove(original_photo_path)
        except:
            pass
        
        await message.reply(
            "<b>🪖 Alright, congratulations... Your state has been created. Maybe this is the best thing you've ever done...</b>"
        )
        await state.clear()

# --------------------------------------------------------------------------------

@user.callback_query(F.data.startswith("economy"))
async def cmdEconomy(query: CallbackQuery, session: AsyncSession, secure: SecureKeyboard):
    await query.message.edit_reply_markup(reply_markup=await economy_categories(secure, query.from_user.id))
    await query.answer()
    
@user.callback_query(F.data.startswith("population"))
async def cmdPopulation(query: CallbackQuery, session: AsyncSession, secure: SecureKeyboard):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    economyReq = EconomyRequest(session)
    
    user = await userReq.get_user(query.from_user.id)
    group = query.message.chat.id
    country = await countryReq.get_country(uid=user.telegram, group=group)
    economy = await economyReq.get_economy(cid=country.cid)
    
    await query.message.reply(
        "<b>📊 Here is the population information of your state...</b>\n\n"
        f"<b>👥 Your state's population is {economy.population} thousand people</b>\n"
        f"<b>👶 Birth rate in your state is about {economy.birth} {'child' if economy.birth <= 4.0 else 'children'} per family\n"
        f"<b>👷‍♂️ The labor force in your state is {economy.labor} thousand people</b>\n"
        f"<b>📉 The unemployment rate in your state is {economy.unemployment}%</b>\n"
        f"<b>📉 The poverty rate in your state is {economy.poverty}%</b>\n"
        f"<b>🌍 The migration rate in your state is {economy.migration}%</b>\n"
        f"<b>🎫 Migrants make up {economy.reverse}% of your population</b>",
        reply_markup=await population(secure, query.from_user.id)
    )
    await query.answer()
    
@user.callback_query(F.data.startswith("rule_population"))
async def cmdRulePopulation(query: CallbackQuery, session: AsyncSession):
    userReq = UserRequest(session)
    countryReq = CountryRequest(session)
    economyReq = EconomyRequest(session)
    
    user = await userReq.get_user(query.from_user.id)
    group = query.message.chat.id
    country = await countryReq.get_country(uid=user.telegram, group=group)
    economy = await economyReq.get_economy(cid=country.cid)
    
    await query.message.reply()
    await query.answer()
