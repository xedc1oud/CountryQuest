from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from data.requests import UserRequest

class UserStatusMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message):
            user_id = event.from_user.id
            username = event.from_user.username
            name = event.from_user.first_name
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            username = event.from_user.username
            name = event.from_user.first_name
            
        session = data.get('session')
        if session:
            try:
                userReq = UserRequest(session)
                user = await userReq.get_user(user_id)
                if user:
                    await userReq.update(telegram=user_id, username=username)
                else:
                    await userReq.add_user(telegram=user_id, username=username, name=name)
            except:
                pass        
            
            
        return await handler(event, data)