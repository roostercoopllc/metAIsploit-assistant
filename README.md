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

```sh
pip install poetry
git clone https://github.com/roostercoopllc/metAIsploit-assistant
cd metAIsploit-assistant
poetry install
# If you don't have the model downloaded
poetry run demo
# if you do have the model downloaded
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

## Create / Update Datasets model training
`Create Initial Datasets`
* *Labels*
  * Attempted Automated Labeling:
  * Manual Labeling:

* *Training*
  * Transfer Learning:
  * Scoring / Performance:

* *Saving Model*
  * Saving Models:

## Ways to contribute
1. Label Data
2. Create Quality of Life to code
3. Write wiki documents

## FAQs
1. [What are the Metasploit Python Module Guidelines?](https://docs.metasploit.com/docs/development/developing-modules/external-modules/writing-external-python-modules.html)

## References
1. [Big thanks to Nomic AI and the gpt4all project](https://github.com/nomic-ai/gpt4all)
2. [Big thanks to Metasploit Framework by Rapid 7](https://github.com/rapid7/metasploit-framework)
3. [Huggingface Dataset for Metasploit Prompts](https://huggingface.co/datasets/icantiemyshoe/cve-to-metasploit-module) 