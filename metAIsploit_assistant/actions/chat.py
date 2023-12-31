from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from metAIsploit_assistant.types import BASE_MODELS
from metAIsploit_assistant.utilities.formatters import (
    has_script_in_response,
    splice_out_file,
    save_response_output_to_file,
)
from metAIsploit_assistant.utilities.models import (
    get_available_models,
    model_choices_prompt,
    model_selection,
)


def setup_model() -> LLMChain:
    # Callbacks support token-wise streaming
    callbacks = [StreamingStdOutCallbackHandler()]

    # If you want to use a custom model add the backend parameter
    # Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
    model_choice = input(model_choices_prompt())
    hacker_model = None
    if type(model_choice) is int and model_choice < len(get_available_models()):
        hacker_model = model_selection(model_choice)
    else:
        print("Choice was not a valid option. Defaulting to Snoozy.")
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
        prompt_text = input("\nWhat do you want to know? (enter: exit to stop): ")
        if prompt_text != "exit":
            llm_response = llm_chain.run(prompt_text)
            if has_script_in_response(llm_response):
                script_cut_out = splice_out_file(llm_response)
                for cut_out in script_cut_out:
                    save_to_file = input(
                        f"\nWould you like to save the {cut_out.file_type} script to a file? (y/n)"
                    )
                    if save_to_file == "y" or save_to_file == "yes":
                        os_system = input("System Type: (windows/mac/linux): ")
                        save_filename = input(
                            f"""\n{cut_out.content}\nWhere would you like to save the file (file endings will be added automatically)? (default: <METASPLOIT_ROOT>/modules/linux/custom/default_output.py) """
                        )
                        if save_filename == "":
                            save_filename = "default_output.py"
                        save_response_output_to_file(cut_out, save_filename, os_system)

    print("\nHappy Hacking!")
