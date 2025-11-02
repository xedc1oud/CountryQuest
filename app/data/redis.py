from redis import asyncio as aioredis

from settings.config import settings

class RedisManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        redis_url = settings.redis.get_secret_value()
        self.redis = await aioredis.from_url(redis_url, decode_responses=True)

    async def set_button_owner(self, callback_id: str, user_id: int, ttl: int = 3600):
        await self.redis.set(callback_id, user_id, ex=ttl)

    async def get_button_owner(self, callback_id: str):
        owner = await self.redis.get(callback_id)
        if owner is not None:
            return int(owner)
        return None

    async def delete_button(self, callback_id: str):
        await self.redis.delete(callback_id)

    async def close(self):
        if self.redis:
            await self.redis.close()