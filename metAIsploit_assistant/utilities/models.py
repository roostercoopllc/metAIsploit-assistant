import os
from typing import List
from pathlib import Path
from tqdm import tqdm
import requests
from metAIsploit_assistant.types import BASE_MODELS, HackerModel


def get_models_inventory() -> None:
    for llm_model in BASE_MODELS.get_model_inventory():
        print("Making default Directories")
        Path(llm_model.file_location).parent.mkdir(parents=True, exist_ok=True)

        print("Requesting download for the model")
        response = requests.get(llm_model.url, stream=True)
        print("Saving response to file")
        with open(llm_model.file_location, "wb") as fi:
            for chunk in tqdm(response.iter_content(chunk_size=8192)):
                if chunk:
                    fi.write(chunk)


def get_available_models() -> List[HackerModel]:
    available_models = []
    for llm_model in BASE_MODELS.get_model_inventory():
        if os.path.exists(llm_model.file_location):
            available_models.append(llm_model)
    return available_models


def model_choices_prompt() -> str:
    promp_str = "Choose a model:\n"
    model_list = get_available_models()
    for _ in range(len(model_list)):
        promp_str = promp_str + f"{_}) {model_list[_].choice_name}: \n"
    return promp_str


def model_selection(llm_model_choice: int) -> HackerModel:
    return get_available_models[llm_model_choice]
