import os
from pathlib import Path
from typing import List
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
                LlmFileOutput(
                    file_type=SupportedScripts.PYTHON.value, content=parse[7:]
                )
            )
        elif SupportedScripts.PIP.value in parse[:10]:
            print("You will need to figure out the deps install stuff later")
            pass

        elif SupportedScripts.RUBY.value in parse[:10]:
            print("You will need to make this later")
            pass
    return scripts


def save_response_output_to_file(
    llm_resp: LlmFileOutput, filename: str, os_system: str
) -> None:
    write_loc = filename
    msf_root = os.environ.get("METASPLOIT_ROOT")
    if msf_root:
        write_loc = f"{msf_root}/modules/{os_system}/custom/{filename}"
        Path(write_loc).parent.mkdir(
            parents=True, exist_ok=True
        )
    with open(write_loc, "w") as fi:
        fi.write(llm_resp.content)
