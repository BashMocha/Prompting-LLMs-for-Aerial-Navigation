import re
import argparse
from airsim_wrapper import *
import math
import numpy as np
import os
import json
import time
import anthropic

class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="../prompts/airsim_basic.txt")
    parser.add_argument("--sysprompt", type=str, default="../system_prompts/airsim_basic.txt")
    parser.add_argument("--testname", type=str, default="third_test")
    parser.add_argument("--model", type=str, default="claude-3-opus-20240229")
    args = parser.parse_args()

    with open("config.json", "r") as f:
        config = json.load(f)
    
    print("Initializing Claude...")
    model = args.model
    client = anthropic.Anthropic(api_key=config['CLAUDE_API_KEY'],)

    with open(args.sysprompt, "r") as f:
        sysprompt = f.read()
    
    chat_history = [
        {
            "role": "user",
            "content": "move 10 units up"
        },
        {
            "role": "assistant",
            "content": """```python
    aw.fly_to([aw.get_drone_position()[0], aw.get_drone_position()[1], aw.get_drone_position()[2]+10])
    ```

    This code uses the `fly_to()` function to move the drone to a new position that is 10 units up from the current position. It does this by getting the current position of the drone using `get_drone_position()` and then creating a new list with the same X and Y coordinates, but with the Z coordinate increased by 10. The drone will then fly to this new position using `fly_to()`."""
        }
    ]
    print("Done.")

    print("Initializing AirSim...")
    aw = AirSimWrapper()
    print("Done.")

    with open(args.prompt, "r") as f:
        prompt = f.read()
    _, chat_history = ask(prompt, client, sysprompt, model, chat_history)

    print("Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands.")
    aw.client.startRecording()

    while True:
        question = input(colors.YELLOW + "AirSim> " + colors.ENDC)

        if question == "!quit" or question == "!exit":
            aw.client.stopRecording()
            write_chat_history(model, args.testname, chat_history)
            break

        if question == "!clear":
            os.system("cls")
            continue

        response, chat_history = ask(question, client, sysprompt, model, chat_history)

        print(f"\n{response}\n")

        code = extract_python_code(response)
        if code is not None:
            print("Please wait while I run the code in AirSim...")
            exec(extract_python_code(response))
            print("Done!\n")    

def ask(prompt, client, sysprompt, model, chat_history):
    chat_history.append({"role": "user", "content": prompt})
    #print(chat_history)
    response = client.messages.create(
        model = model,
        max_tokens = 2048,
        system = sysprompt,
        messages = chat_history
    )
    #print(response.content[0].text)
    chat_history.append({"role": "assistant", "content": response.content[0].text})
    return chat_history[-1]["content"], chat_history

def extract_python_code(content):
    code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)
    code_blocks = code_block_regex.findall(content)

    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None

def write_chat_history(model_name, test_name, chat_history):
    filename = model_name + "-" + test_name + ".txt"
    path = os.path.join("../chats/claude/", filename)
    
    with open(path, "w") as f:
        for log in chat_history:
            f.write(f"{log['role']}: \n{log['content']}\n")
            f.write("\n<------>\n\n")


if __name__ == '__main__':
    main()