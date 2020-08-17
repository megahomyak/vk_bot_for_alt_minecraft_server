import asyncrcon


class RConWorker:

    def __init__(self, rcon_client: asyncrcon.AsyncRCON) -> None:
        self.rcon_client = rcon_client

    async def add_nickname_to_whitelist(self, nickname: str) -> None:
        await self.rcon_client.open_connection()
        await self.rcon_client.command(f'whitelist add {nickname}')
        await self.rcon_client.close()
