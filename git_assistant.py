# git assistant trained with commands from http://guides.beanstalkapp.com/version-control/common-git-commands.html

# common imports
import json
import openai
import yaml
import os
from gpt import GPT
from gpt import Example


def get_config(config_file):
    ''' open config file with name config_file that contains parameters
    for this module and return Python object

    Args:
        config_file: filename containing config parameters

    Returns:
        config: Python dictionary with config parms from config file - dictionary

    '''
    current_path = os.getcwd()
    print("current directory is: " + current_path)

    path_to_yaml = os.path.join(current_path, config_file)
    print("path_to_yaml " + path_to_yaml)
    try:
        with open(path_to_yaml, 'r') as c_file:
            config = yaml.safe_load(c_file)
        return config
    except Exception as error:
        print('Error reading the config file '+error)
       
  
def get_input():
    ''' prompt user for input on the command line
    
    Returns:
        input_string: input entered by the user

    '''
    try:
        # input("Type something to test this out: ")
        input_string = input("what do you want git to do? ")
    except Exception as error:
        print('ERROR', error)
    else:
        return input_string
    
def main():
    ''' main function for module 
    - get gpt_key - note that you will need to provide your own key 
    - once you have access to the GPT-3 beta you can find the key under "Secret" here https://beta.openai.com/developer-quickstart
    - initialize GPT object
    - provide examples of English text with corresponding git commands
    - prompt user for input text descriptions and output GPT-3's translation of the text description into git commands
    '''
    print("Welcome to the Git assistant")
    # ingest config file
    config = get_config('gpt_assistant_config.yml')
    # initialize GPT-3 env
    openai.api_key = config['general']['gpt_key']
    gpt = GPT(engine=config['general']['gpt_engine'],
          temperature=config['general']['gpt_temperature'],
          max_tokens=config['general']['gpt_max_tokens'])
    # provide GPT-3 with a set of examples of English text / git command pairs
    gpt.add_example(Example('initialize a git repository', 'git init'))
    gpt.add_example(Example('add file foo to the staging area for git', 'git add foo'))
    gpt.add_example(Example('add all files in the current directory to the staging area for git', 'git add .'))
    gpt.add_example(Example('record the changes made to the files to a local repository', 'git commit -m "commit message"'))
    gpt.add_example(Example('return the current state of the repository', 'git status'))
    gpt.add_example(Example('Clone the remote repository https://github.com/ryanmark1867/webview_rasa_example','git clone https://github.com/ryanmark1867/webview_rasa_example'))
    gpt.add_example(Example('remove file foo from the staging area', 'git rm -f foo'))
    gpt.add_example(Example('show the chronological commit history for a repository', 'git log'))
    # loop to prompt for text description of what you want to do
    input_request = get_input()
    while input_request != config['general']['stop_string']: 
        output = gpt.submit_request(input_request)
        print("git command is:")
        print(output.choices[0].text)
        input_request = get_input()




if __name__ == "__main__":
    main()