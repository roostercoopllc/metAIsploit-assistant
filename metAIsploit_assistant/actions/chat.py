from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from metAIsploit_assistant.types import BASE_MODELS


def setup_model() -> LLMChain:
    # Callbacks support token-wise streaming
    callbacks = [StreamingStdOutCallbackHandler()]

    # If you want to use a custom model add the backend parameter
    # Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
    model_choice = input(
        """
                         Choose a model:
                         1. Snoozy (Nomadic.ai) [Default]: 
                         """
    )
    hacker_model = None
    if type(model_choice) is int:
        match model_choice:
            case 1:
                print("Using Snoozy Model")
                hacker_model = BASE_MODELS.SNOOZY
            case _:
                print("Using Default Model")
                hacker_model = BASE_MODELS.SNOOZY
    else:
        print("Choice was not a valid option")
        hacker_model = BASE_MODELS.SNOOZY

    llm = GPT4All(
        model=hacker_model.file_location,
        backend="gptj",
        callbacks=callbacks,
        verbose=True,
    )

    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    return LLMChain(prompt=prompt, llm=llm)


def perform_chat() -> None:
    prompt_text = None
    llm_chain = setup_model()

    while prompt_text != "exit":
        prompt_text = input("What do you want to know? (enter: exit to stop)")

        llm_chain.run_prompt(prompt_text)

    print("Happy Hacking")
