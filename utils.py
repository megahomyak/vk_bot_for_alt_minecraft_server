import re

import constants


def validate_nickname(nickname: str) -> bool:
    return bool(re.match(constants.NICKNAME_REGEX, nickname))
