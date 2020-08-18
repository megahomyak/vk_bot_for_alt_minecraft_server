USER_INFO_LINK = "https://vk.com/foaf.php?id={}"
USER_XML_ROOT_INDEX = 0
USER_XML_INFO_INDEX = 0
USER_XML_REGISTRATION_DATE_INDEX = 10

NOT_VALID_USERS_FILENAME = "not_valid_users.txt"
NOT_VALID_USERS_SEPARATOR = ","

NEW_MESSAGE_EVENT_NAME = "message_new"

VK_GROUP_TOKEN = ""
VK_GROUP_ID = 123

NICKNAME_REGEX = "[_[0-9][a-z][A-Z]]{3-16}"

COMMAND_ADD_NICKNAME = "/wl "

PAGE_NOT_VALID_MESSAGE = (
    "Эта страница невалидна, тебе нельзя попасть на "
    "сервер! (Я тому, кто написал ник {nickname})"
)
NICKNAME_ADDED_MESSAGE = "Никнейм {nickname} добавлен в белый список!"
NICKNAME_IS_NOT_VALID = "Никнейм {nickname} не валидный!"

VK_ERROR_MESSAGE = "Произошла ошибка при обработке команды {command}"
LOGGING_ERROR_MESSAGE = "Error {error} while processing command {command}"
LOGGING_NEW_MESSAGE = "Message from {peer_id}: {text}"
LOGGING_USER_SERVED = (
    "User {user_id} with request {command} served with {response}"
)
LOGGING_USER_NOT_SERVED = "User {user_id} with request {command} not served"

SERVER_ADDRESS = ""
SERVER_RCON_PASSWORD = ""

MAX_REGISTRATION_YEAR = 2019
