from enum import Enum


class CreateCustomTemplateEnum(Enum):
    ERROR = "error"
    ACCESS_DENIED = "access_denied"


class DownloadEmptyTemplateEnum(Enum):
    ERROR = "error"
    ACCESS_DENIED = "access_denied"
    NOT_FOUND = "not_found"
