from typing import Optional
from enum import StrEnum
from pydantic import BaseModel


class HackerModel(BaseModel):
    name: str
    url: str
    file_location: Optional[str]


class KnownModels(StrEnum):
    SNOOZY = "ggml-gpt4all-l13b-snoozy.bin"


class KnownModelUrls(StrEnum):
    SNOOZY = "http://gpt4all.io/models/ggml-gpt4all-l13b-snoozy.bin"


class OsOptions(StrEnum):
    WINDOWS = "windows"
    MAC = "mac"
    LINUX = "linux"
    KALI = "kali"


class SupportedScripts(StrEnum):
    BASH = "bash"
    PYTHON = "python"
    PIP = "pip"
    RUBY = "ruby"

    @classmethod
    def has_member(value) -> bool:
        return value in [
            SupportedScripts.BASH.value,
            SupportedScripts.PYTHON.value,
            SupportedScripts.RUBY.value,
            SupportedScripts.PIP.value,
        ]


class LlmFileOutput(BaseModel):
    file_type: SupportedScripts
    content: str


class BASE_MODELS:
    SNOOZY = HackerModel(
        name=KnownModels.SNOOZY.value,
        url=KnownModelUrls.SNOOZY.value,
        file_location=f"examples/models/{KnownModels.SNOOZY.value}",
    )
