from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from data.requests import GroupRequest

class GroupStatusMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message):
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id
            
        bot = data.get('bot')
        session = data.get('session')
        admins = await bot.get_chat_administrators(chat_id)
        owner = next((a.user for a in admins if a.status == "creator"), None)
        if session:
            try:
                if event.chat.type == "private":
                    return await handler(event, data)
                else:
                    groupReq = GroupRequest(session)
                    group = await groupReq.get_group(chat_id)
                    
                    await groupReq.update(gid=chat_id, name=event.chat.title if event.chat.title else "No Name", owner=owner.id)
                    
                    if not group:
                        await groupReq.add_group(
                            gid=chat_id,
                            name=event.chat.title if event.chat.title else "No Name",
                            owner=owner.id
                        )
            except Exception as e:
                print(f"GroupStatusMiddleware error: {e}")        
            
            
        return await handler(event, data)