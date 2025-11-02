from aiogram.types import InlineKeyboardMarkup

from .security import SecureKeyboard

async def profile(secure: SecureKeyboard, user_id: int, page: int = 0) -> InlineKeyboardMarkup:
    categories = [
        ("💹 Economy", "economy"),
        ("❓ ???", "army"),
        ("❓ ???", "history"),
        ("❓ ???", "science"),
        ("❓ ???", "politics"),
        ("❓ ???", "administry"),
        ("❓ ???", "diplomacy"),
        ("🎨 Customization", "customize")
    ]
    
    items_per_page = 4
    start = page * items_per_page
    end = start + items_per_page
    current_categories = categories[start:end]
    
    buttons = []
    
    for text, callback in current_categories:
        buttons.append([(text, callback)])
    
    nav_row = []
    if page > 0:
        nav_row.append(("⬅️", f"profile_page_{page-1}"))
    if end < len(categories):
        nav_row.append(("➡️", f"profile_page_{page+1}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    keyboard = await secure.create_markup(buttons, user_id)
    
    return keyboard