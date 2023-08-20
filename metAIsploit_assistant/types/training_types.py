from typing import List, Optional
from pydantic import BaseModel


class TrainingPromptModel(BaseModel):
    cve: str
    instruction: str
    input: str
    output: str


class TrainingPromptModelSet(BaseModel):
    training_set: List[TrainingPromptModel]


class TrainingFineTuneParamsModel(BaseModel):
    num_train_epochs: int
    learning_rate: float
    cutoff_len: int
    lora_r: int
    lora_alpha: int
    lora_dropout: float
    lora_target_models: List[str]
    train_on_inputs: bool
    group_by_length: bool
    save_steps: int
    save_total_limit: int
    logging_steps: int


class TrainingFineTuneInfoModel(BaseModel):
    hf_model_name: str
    load_from_hf: bool
    base_model: str
    prompt_template: str
