import uuid

from aiogram import BaseMiddleware, types

from data.redis import RedisManager
from keyboards.security import SecureKeyboard


class SecureButtonMiddleware(BaseMiddleware):
    def __init__(self, redis_manager: RedisManager, ttl: int = 3600):
        self.redis_manager = redis_manager
        self.ttl = ttl
        self.secure_keyboard = SecureKeyboard(redis_manager, ttl)
        super().__init__()

    async def __call__(self, handler, event, data):
        
        data["secure"] = self.secure_keyboard
        
        if isinstance(event, types.CallbackQuery):
            callback_id = event.data
            if callback_id:
                owner_id = await self.redis_manager.get_button_owner(callback_id)
                if owner_id is None:
                    await event.answer("❌ This button is not valid.", show_alert=True)
                    return
                if int(owner_id) != event.from_user.id:
                    await event.answer("❌ This button is not for you!", show_alert=True)
                    return
                
                if ":" in callback_id:
                    original_callback = callback_id.split(":")[0]
                    object.__setattr__(event, 'data', original_callback)
        
        result = await handler(event, data)
        return result