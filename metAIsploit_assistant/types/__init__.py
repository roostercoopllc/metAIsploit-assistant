from typing import Optional
from enum import Enum
from pydantic import BaseModel


class HackerModel(BaseModel):
    name: str
    url: str
    file_location: Optional[str]


class KnownModels(Enum):
    SNOOZY = "ggml-gpt4all-l13b-snoozy.bin"


class KnownModelUrls(Enum):
    SNOOZY = "http://gpt4all.io/models/ggml-gpt4all-l13b-snoozy.bin"


class BASE_MODELS:
    SNOOZY = HackerModel(
        name=KnownModels.SNOOZY.value,
        url=KnownModelUrls.SNOOZY.value,
        file_location=f"examples/models/{KnownModels.SNOOZY.value}",
    )
