# MetAIsploit Assistant
This project is a study into generating POC / Exploits for the metasploit framework using LLMs.

Assumptions of the project:
1. Metasploit framework has a well defined outcome for a module.
2. The modules have metadata required for each module that would make labeling easier and more consistent.
3. The modules can be broken down into various utilities that (assumed to be similar to defined classes).
3. Most modules are associated with CVE research that can lead to robust prompt generation.

*Success Criteria for Project*: Utilize the commandline chat prompt to generate a guide for install, and usage of a module that can be saved directly into the metasploit framework using a previously unseen CVE.

## Quick Use
For a quick demo on how this is used please run the following commands (assuming you have the pre-reqs installed).

Setup
```sh
pip install poetry
git clone https://github.com/roostercoopllc/metAIsploit-assistant -r
cd metAIsploit-assistant
poetry install
# (Optional) This will download the snoozy binary by default
poetry run init
```

```sh
# If you don't have the snoozy model downloaded
poetry run demo
# if you do have the snoozy model downloaded
poetry run prompt-demo
```

You can run the script interactively by running the following commands:
```sh
export METASPLOIT_ROOT=<your metasploit root>
# Update the .env with your MSF root
poetry run chat
```

*Note* Depending on your hardware you are running this on, this might take a little while to return the response.

## Install / Setup
This project uses poetry to generate manage dependencies and attempts to keep the project clean (we will see for how long)

You can use this module through the poetry commands outlined in the `pyproject.toml`.

However, it is intended to eventually be available through the `msfconsole` to where you can use a digital assistant without needing to start a different terminal and keep the same session alive. 

### Requirements
* python 3.11
* Metasploit-Framework
* git-lfs
* And the below pip packages managed by poetry

Development Setup
```sh
poetry install
```

## Simple Usage
To run the chat interactively 
```sh
poetry run chat
```

You can then chat with the model and generate responses. When those responses find code snippets, the script will ask if you wanted to save each individual code snippet. 

## (TO-DO) Create / Update Datasets model training
`Create Initial Datasets`
* *Labels*
  * Attempted Automated Labeling:
    
    There are two scripts that attempt to make the prompt dataset. These prompts are based off of a collection of the writeups on cves from the mitre collection of cves. They will associate the metasploit modules with ever one of the complete write ups housed in the the mitre datahouse. 

    The prompts for training are the entire white paper and an additional prompt of the phrase `write a metasploit module for cve-xxxx-yyyyy`.
     
    - Automated Labeling will take the CVE code and attempt to search it on the cve database on the MITRE repository for CVEs. It will then search the URLs of the CVE references and create prompts that associate with the Metasploit module the cve goes with. 
    *Note*: Hopeuflly this will create mroe variance on what kind of description of the CVEs will generate a valid module.
  * Manual Labeling:

* *Training*
  * Transfer Learning:
  * Scoring / Performance:

* *Saving Model*
  * Saving Models:

## (TO-DO) Ways to contribute
1. Label Data
2. Create Quality of Life to code
3. Write wiki documents

## FAQs
1. [What are the Metasploit Python Module Guidelines?](https://docs.metasploit.com/docs/development/developing-modules/external-modules/writing-external-python-modules.html)
2. [What do you to to train a model?](https://huggingface.co/blog/how-to-train)

## References
1. [Big thanks to Nomic AI and the gpt4all project](https://github.com/nomic-ai/gpt4all)
2. [Big thanks to Metasploit Framework by Rapid 7](https://github.com/rapid7/metasploit-framework)
3. [Huggingface Dataset for Metasploit Prompts](https://huggingface.co/datasets/icantiemyshoe/cve-to-metasploit-module) 
4. [LLaMA Retraining Evaluation](https://github.com/zetavg/LLaMA-LoRA-Tuner)
5. [GPT4All Prompt Dataset](https://huggingface.co/datasets/nomic-ai/gpt4all-j-prompt-generations)
6. [Base Model used for the gpt4all models](https://github.com/kingoflolz/mesh-transformer-jax)
7. [Training nomic](https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-training/README.md)
8. [Command Stagers](https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-use-command-stagers.html)