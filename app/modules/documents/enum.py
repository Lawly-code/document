from enum import Enum


class DocumentUpdateEnum(Enum):
    NOT_FOUND = "not_found"


class ImproveTextEnum(Enum):
    ERROR = "error"


class GenerateDocumentEnum(Enum):
    ERROR = "error"
    NOT_FOUND = "not_found"
    GENERATE_SUCCESS = "generate_success"
