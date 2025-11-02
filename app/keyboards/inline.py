from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .security import SecureKeyboard

async def customize(secure: SecureKeyboard, user_id: int) -> InlineKeyboardMarkup:
    keyboard = await secure.create_markup([
        [("🏳 Change flag", "flag")],
        [("🧹 Delete country", "delete")],
        [("🔙 Back", "back")]
    ], user_id)
    
    return keyboard

async def registry(secure: SecureKeyboard, user_id: int) -> InlineKeyboardMarkup:
    keyboard = await secure.create_markup([
        [("🪖 Create country", "create")]
    ], user_id)
    
    return keyboard

async def confirmation(secure: SecureKeyboard, user_id: int) -> InlineKeyboardMarkup:
    keyboard = await secure.create_markup([
        [("✅ Confirm", "confirm")],
        [("❌ Cancel", "cancel")]
    ], user_id)
    
    return keyboard

async def economy_categories(secure: SecureKeyboard, user_id: int) -> InlineKeyboardMarkup:
    keyboard = await secure.create_markup([
        [("👥 Population", "population")],
        [("📦 Regulations", "regulations")],
        [("📈 Budget", "budget")],
        [("🏭 Enterprises", "enterprises")],
        [("🏢 Private business", "business")],
        [("🔙 Back", "profile_page_0")]
    ], user_id)
    
    return keyboard

async def population(secure: SecureKeyboard, user_id: int) -> InlineKeyboardMarkup:
    keyboard = await secure.create_markup([
        [("👥 Population Rule", "rule_population")],
        [("👷‍♂️ Work Force", "workforce")],
        [("🛂 Migration Policy", "migration_policy")]
    ], user_id)
    
    return keyboard