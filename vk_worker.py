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
