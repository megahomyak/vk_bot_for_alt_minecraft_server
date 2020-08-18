import asyncio

import aiohttp
from asyncrcon import AsyncRCON

import constants
import utils
from vk_worker import VKWorker
from rcon_worker import RConWorker
from vk_page_validators import VKPageValidators


class MainLogic:

    def __init__(
            self, vk_worker: VKWorker,
            vk_page_validators: VKPageValidators,
            rcon_worker: RConWorker) -> None:
        self.vk_worker = vk_worker
        self.vk_page_validators = vk_page_validators
        self.rcon_worker = rcon_worker
        with open("not_valid_users.txt", "r") as f:
            not_valid_users: str = f.read()
            self.ids_of_not_valid_users = [
                int(user_id.strip())
                for user_id in not_valid_users.split(",")
            ]

    def save_not_valid_users_list(self):
        with open("not_valid_users.txt", "w") as f:
            f.write(", ".join(map(str, self.ids_of_not_valid_users)))

    async def start(self):
        async for message_info in self.vk_worker.listen():
            peer_id = message_info["peer_id"]
            text = message_info["text"]
            if text.startswith(constants.COMMAND_ADD_NICKNAME):
                nickname = text[len(constants.COMMAND_ADD_NICKNAME):]
                if utils.validate_nickname(nickname):
                    from_id = message_info["from_id"]
                    if from_id in self.ids_of_not_valid_users:
                        await self.vk_worker.reply(
                            peer_id,
                            constants.PAGE_NOT_VALID_MESSAGE.format(nickname)
                        )
                    else:
                        sender_page_info = await self.vk_worker.get_page_info(
                            from_id
                        )
                        if await self.vk_page_validators.checks_facade(
                            sender_page_info
                        ):
                            await self.vk_worker.reply(
                                peer_id,
                                constants.NICKNAME_ADDED_MESSAGE.format(
                                    nickname
                                )
                            )
                        else:
                            await self.vk_worker.reply(
                                peer_id,
                                constants.PAGE_NOT_VALID_MESSAGE
                            )
                else:
                    await self.vk_worker.reply(
                        peer_id,
                        constants.NICKNAME_IS_NOT_VALID.format(nickname)
                    )


if __name__ == '__main__':
    # noinspection PyShadowingNames
    # because I throw outer event_loop into this function
    async def main(event_loop: asyncio.AbstractEventLoop):
        async with aiohttp.ClientSession(loop=event_loop) as aiohttp_session:
            main_logic = MainLogic(
                VKWorker(
                    aiohttp_session,
                    constants.VK_GROUP_TOKEN,
                    constants.VK_GROUP_ID
                ),
                VKPageValidators(
                    aiohttp_session
                ),
                RConWorker(
                    AsyncRCON(
                        constants.SERVER_ADDRESS,
                        constants.SERVER_RCON_PASSWORD
                    )
                )
            )
        await main_logic.start()
    event_loop = asyncio.get_event_loop()
    main(event_loop)
