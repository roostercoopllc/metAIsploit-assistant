import os
from typing import List, Optional
from metAIsploit_assistant.types import SupportedScripts, LlmFileOutput


def has_script_in_response(llm_resp: str) -> bool:
    return "```" in llm_resp


def splice_out_file(llm_resp: str) -> List[LlmFileOutput]:
    parsed = llm_resp.split("```")
    scripts = []
    for parse in parsed:
        if SupportedScripts.BASH.value in parse[:10]:
            scripts.append(
                LlmFileOutput(file_type=SupportedScripts.BASH.value, content=parse[5:])
            )
        elif SupportedScripts.PYTHON.value in parse[:10]:
            scripts.append(
                LlmFileOutput(file_type=SupportedScripts.PYTHON.value, content=parse[7:])
            )
        elif SupportedScripts.PIP.value in parse[:10]:
            print("You will need to figure out the deps install stuff later")
            pass

        elif SupportedScripts.RUBY.value in parse[:10]:
            print("You will need to make this later")
            pass
    return scripts


def save_response_output_to_file(
    llm_resp: LlmFileOutput, filename: str
) -> None:
    if llm_resp.file_type == SupportedScripts.BASH.value:
        filename = f"{filename}.sh"
    if llm_resp.file_type == SupportedScripts.PYTHON.value:
        filename = f"{filename}.py"
    with open(filename, "w") as fi:
        fi.write(llm_resp.content)
