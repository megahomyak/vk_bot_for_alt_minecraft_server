import random

from simple_avk import SimpleAVK


class VKWorker(SimpleAVK):

    async def reply(self, peer_id: int, text: str) -> None:
        await self.call_method(
            "messages.send",
            {
                "message": text,
                "random_id": random.randint(-1_000_000, 1_000_000),
                "peer_id": peer_id
            }
        )

    async def get_page_info(self, page_id: int) -> dict:
        users_info = await self.call_method(
            "users.get",
            {
                "user_ids": str(page_id)
            }
        )
        return users_info[0]
