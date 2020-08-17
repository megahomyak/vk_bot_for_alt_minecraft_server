import xml.etree.ElementTree as XMLElementTree

import aiohttp

import constants


class VKPageValidators:

    def __init__(self, aiohttp_session: aiohttp.ClientSession):
        self.aiohttp_session = aiohttp_session

    async def checks_facade(self, vk_page_info: dict) -> bool:
        return all(
            [
                await self.check_registration_date(
                    int(vk_page_info["id"])
                )
            ]
        )

    async def check_registration_date(self, vk_page_id: int) -> bool:
        user_info_req = await self.aiohttp_session.get(
            constants.USER_INFO_LINK.format(vk_page_id)
        )
        user_info_xml = await user_info_req.text()
        xml_root = XMLElementTree.fromstring(user_info_xml)
        registration_date: str = (
            xml_root
            [constants.USER_XML_ROOT_INDEX]
            [constants.USER_INFO_LINK]
            [constants.USER_XML_REGISTRATION_DATE_INDEX]
        ).text
        registration_year = int(registration_date.split("-")[0])
        return registration_year <= constants.MAX_REGISTRATION_YEAR
