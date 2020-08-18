import asyncio
import functools
import logging

import aiohttp
from asyncrcon import AsyncRCON

import constants
import utils
from rcon_worker import RConWorker
from vk_page_validators import VKPageValidators
from vk_worker import VKWorker

logging.basicConfig(
    filename="bot_errors.log",
    format="%(asctime)s | %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG
)


class MainLogic:

    def __init__(
            self, vk_worker: VKWorker,
            vk_page_validators: VKPageValidators,
            rcon_worker: RConWorker) -> None:
        self.vk_worker = vk_worker
        self.vk_page_validators = vk_page_validators
        self.rcon_worker = rcon_worker
        with open(constants.NOT_VALID_USERS_FILENAME, "r") as f:
            not_valid_users: str = f.read()
            self.ids_of_not_valid_users = [
                int(user_id.strip())
                for user_id in not_valid_users.split(
                    constants.NOT_VALID_USERS_SEPARATOR
                )
            ]

    def save_not_valid_users_list(self):
        with open(constants.NOT_VALID_USERS_FILENAME, "w") as f:
            f.write(", ".join(map(str, self.ids_of_not_valid_users)))

    async def handle_message(self, message_info: dict) -> None:
        peer_id = message_info["peer_id"]
        text = message_info["text"]
        from_id = message_info["from_id"]
        logging.info(
            constants.LOGGING_NEW_MESSAGE.format(
                peer_id=peer_id,
                text=text
            )
        )
        text_for_user = await self.check_command(message_info)
        if text_for_user:
            logging.info(
                constants.LOGGING_USER_SERVED.format(
                    user_id=from_id,
                    command=text,
                    response=text_for_user
                )
            )
            await self.vk_worker.reply(
                peer_id,
                text_for_user
            )
        else:
            logging.info(
                constants.LOGGING_USER_NOT_SERVED.format(
                    user_id=from_id,
                    command=text
                )
            )

    async def check_command(self, message_info: dict) -> str:
        text = message_info["text"]
        if text.startswith(constants.COMMAND_ADD_NICKNAME):
            nickname = text[len(constants.COMMAND_ADD_NICKNAME):]
            if utils.validate_nickname(nickname):
                from_id = message_info["from_id"]
                if from_id in self.ids_of_not_valid_users:
                    return constants.PAGE_NOT_VALID_MESSAGE.format(nickname)
                sender_page_info = await self.vk_worker.get_page_info(
                    from_id
                )
                if await self.vk_page_validators.checks_facade(
                    sender_page_info
                ):
                    return constants.NICKNAME_ADDED_MESSAGE.format(nickname)
                else:
                    return constants.PAGE_NOT_VALID_MESSAGE.format(nickname)
            else:
                return constants.NICKNAME_IS_NOT_VALID.format(nickname)

    async def coroutine_done_callback(
            self, future: asyncio.Future, peer_id: int, text: str):
        future_exception = future.exception()
        if future_exception:
            logging.error(
                constants.LOGGING_ERROR_MESSAGE.format(
                    error=str(future_exception),
                    command=text
                )
            )
            await self.vk_worker.reply(
                peer_id, constants.VK_ERROR_MESSAGE.format(command=text)
            )

    async def start(self):
        async for event in self.vk_worker.listen():
            if event["type"] == constants.NEW_MESSAGE_EVENT_NAME:
                msg_info = event["object"]["message"]
                asyncio.gather(
                    self.handle_message(msg_info)
                ).add_done_callback(
                    functools.partial(
                        self.coroutine_done_callback,
                        msg_info["peer_id"], msg_info["text"]
                    )
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
