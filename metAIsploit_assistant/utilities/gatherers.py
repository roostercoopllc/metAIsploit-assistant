import json
import os
import re
import requests
from time import time
from typing import Tuple, Optional, List
from metAIsploit_assistant.types.training_types import TrainingPromptModel
from bs4 import BeautifulSoup

CVE_RE = r"CVE-\d{4}-\d{4,7}"
MITRE_CVE_URL = "https://cve.mitre.org/cgi-bin/cvename.cgi"


def make_cve_url(cve_number: str) -> str:
    return f"{MITRE_CVE_URL}?name={cve_number}"


def get_cve_content(cve_number: str) -> str:
    return requests.get(make_cve_url(cve_number)).content


def get_generic_cve_writeup_content(url: str) -> str:
    return requests.get(url).content


def get_urls_from_mitre_cve_post(cve_str: str) -> List[str]:
    urls = []
    mitre_cve_content = get_cve_content(cve_str)
    cve_soup = BeautifulSoup(mitre_cve_content, "html.parser")
    for tag in cve_soup.find_all(["a"]):
        if "URL:" in str(tag):
            urls.append(tag["href"])
    return urls


def find_cve_in_input(prompt_input: str) -> Tuple[bool, Optional[str]]:
    cve_pattern = re.compile(CVE_RE)
    cve = cve_pattern.search(prompt_input)
    if cve:
        return True, cve.group(0)
    return False, None


def check_prompt_for_cve(prompt_input: str) -> str:
    cve_in_ask = find_cve_in_input(prompt_input)
    if cve_in_ask[0]:
        return cve_in_ask[1]
    return prompt_input


def get_prompt_model_from_msf(msf_module_file: str) -> Optional[TrainingPromptModel]:
    training_prompt = None
    with open(msf_module_file, "r") as fi:
        msf_module_content = fi.read()
        cve = find_cve_in_input(msf_module_content)
        if cve[0]:
            training_prompt = TrainingPromptModel(
                cve=cve[1], prompt="", response=msf_module_content, source=""
            )
    return training_prompt


def get_modules_for_cve() -> List[TrainingPromptModel]:
    msf_root = os.environ.get("METASPLOIT_INSTALL_ROOT")
    module_prompts = []
    if msf_root:
        msf_root = f"{msf_root}/modules"
    else:
        print(
            "No METASPLOIT_INSTALL_ROOT defined in env. Using /opt/metasploit-framework"
        )
        msf_root = "/opt/metasploit-framework/embedded/framework/modules"

    for root, dirs, files in os.walk(msf_root):
        for filename in files:
            prompt_model = get_prompt_model_from_msf(str(os.path.join(root, filename)))
            if prompt_model:
                module_prompts.append(prompt_model)
    return module_prompts


def write_generic_prompt_list(cve_str: str, msf_module_for_cve: str) -> List[dict]:
    prompts = [
        {
            "cve": cve_str,
            "prompt": f"Write a metasploit modules for {cve_str}",
            "response": msf_module_for_cve,
            "source": "Generic Generation",
        },
        {
            "cve": cve_str,
            "prompt": f"Write a metasploit modules for the {cve_str}",
            "response": msf_module_for_cve,
            "source": "Generic Generation",
        },
        {
            "cve": cve_str,
            "prompt": f"Write a metasploit modules for the vulnerabilty {cve_str}",
            "response": msf_module_for_cve,
            "source": "Generic Generation",
        },
    ]

    return prompts


def get_full_prompt_list_for_msf() -> List[dict]:
    prompt_list = []
    # find module from location
    start_time = time()
    msf_modules = get_modules_for_cve()
    for msf_module in msf_modules:
        print(f"Creating Generics for {msf_module.cve}")
        # generate prompts from msf
        prompt_list = prompt_list + write_generic_prompt_list(
            msf_module.cve, msf_module.response
        )
        print(f"Gathering urls for {msf_module.cve}")
        # search for mitre cves
        urls_list = get_urls_from_mitre_cve_post(msf_module.cve)
        for url in urls_list:
            try:
                prompt_model = TrainingPromptModel(
                    cve=msf_module.cve,
                    prompt=f"Create a Metasploit module based off of the following research: {requests.get(url, timeout=10).content}",
                    response=f"The Metasploit modules for {msf_module.cve} can be written like this: ```rb\n{msf_module.response}\n```\n\nThe file must be saved in the `modules` directory of the metasploit. Generally using the folloiwng format <msf root>/modules/<os>/<service>/<exploit_name>.rb",
                    source=url,
                )
                prompt_list.append(dict(prompt_model))
            except Exception as e:
                print(e)

    print(
        f"Completed prompt generation. Total {len(msf_modules)} modules generated {len(prompt_list)} total prompts in {time() - start_time}"
    )
    save_to_file = input("Do you want to save the output to a file? (y/n): ")
    if save_to_file == "y" or save_to_file == "yes" or save_to_file == "":
        file_location = input(
            "Save File Location? (Default Location: ./datasets/metasploit-prompts.json): "
        )
        if file_location == "":
            file_location = "datasets/metasploit-prompts.json"
        with open(file_location, "w") as fi:
            json.dump(prompt_list, fi)
    return prompt_list
