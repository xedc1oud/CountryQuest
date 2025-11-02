import uuid

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.redis import RedisManager

class SecureKeyboard:
    def __init__(self, redis_manager: RedisManager, ttl: int = 3600):
        self.redis_manager = redis_manager
        self.ttl = ttl
    
    async def create_button(self, text: str, callback_data: str, user_id: int) -> InlineKeyboardButton:
        """Create a secure button."""
        secure_id = f"{callback_data}:{uuid.uuid4().hex[:8]}"
        await self.redis_manager.set_button_owner(secure_id, user_id, ttl=self.ttl)
        return InlineKeyboardButton(text=text, callback_data=secure_id)
    
    async def create_markup(self, buttons: list, user_id: int) -> InlineKeyboardMarkup:
        """
        Create keyboard for list of buttons.
        buttons: [[("Текст", "callback"), ...], ...]
        """
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for text, callback_data in row:
                button = await self.create_button(text, callback_data, user_id)
                keyboard_row.append(button)
            keyboard.append(keyboard_row)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)