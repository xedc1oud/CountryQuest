import time

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Tuple, List, Optional, Set

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, interval: int = 10, whitelist: Optional[Set[int]] = None):
        super().__init__()
        self.limit = limit
        self.interval = interval
        self.whitelist = whitelist or set()
        self.storage: Dict[Tuple[int,int], List[float]] = {}

    async def __call__(self, handler, event, data):
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        chat_id = event.chat.id

        if user_id in self.whitelist or event.from_user.is_bot:
            return await handler(event, data)

        now = time.time()
        key = (chat_id, user_id)
        timestamps = [t for t in self.storage.get(key, []) if now - t < self.interval]
        timestamps.append(now)
        self.storage[key] = timestamps

        if len(timestamps) > self.limit:
            try:
                await event.delete()
                await event.answer("⚠️ Please, don't spam messages", show_alert=True)
            except:
                pass
            return

        return await handler(event, data)