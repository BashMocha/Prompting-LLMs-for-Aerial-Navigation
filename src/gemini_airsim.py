import google.generativeai as genai
import re
import argparse
from airsim_wrapper import *
import math
import numpy as np
import os
import json
import time

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
    parser.add_argument("--model", type=str, default="gemini-1.5-pro")
    args = parser.parse_args()

    with open("config.json", "r") as f:
        config = json.load(f)

    print("Initializing Gemini...")
    genai.configure(api_key=config["GEMINI_API_KEY"])
    
    with open(args.sysprompt, "r") as f:
        sysprompt = f.read()

    chat_history = [
        {
            "role": "user",
            "parts": [
                {
                    "text": sysprompt
                }
            ],
        },
        {
            "role": "user",
            "parts": [
                {
                    "text": "move 10 units up"
                }
            ],
        },
        {
            "role": "model",
            "parts": [
                {
                    "text": """```python
aw.fly_to([aw.get_drone_position()[0], aw.get_drone_position()[1], aw.get_drone_position()[2]+10])
```

This code uses the `fly_to()` function to move the drone to a new position that is 10 units up from the current position. It does this by getting the current position of the drone using `get_drone_position()` and then creating a new list with the same X and Y coordinates, but with the Z coordinate increased by 10. The drone will then fly to this new position using `fly_to()`."""
                }
            ],
        }
    ]
    model = args.model
    model = genai.GenerativeModel(model)
    chat = model.start_chat(history=chat_history)
    print(f"Done.")

    print(f"Initializing AirSim...")
    aw = AirSimWrapper()
    print(f"Done.")

    with open(args.prompt, "r") as f:
        prompt = f.read()
    _, chat_history = ask(prompt, chat, chat_history)

    print("Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands.")
    aw.client.startRecording()

    while True:
        question = input(colors.YELLOW + "AirSim> " + colors.ENDC)

        if question == "!quit" or question == "!exit":
            write_chat_history(args.model, args.testname, chat_history)
            aw.client.stopRecording()
            break

        if question == "!clear":
            os.system("cls")
            continue

        response, chat_history = ask(question, chat, chat_history)

        print(f"\n{response}\n")

        code = extract_python_code(response)
        if code is not None:
            print("Please wait while I run the code in AirSim...")
            exec(extract_python_code(response))
            print("Done!\n")

def ask(prompt, chat, chat_history):
    response = chat.send_message(prompt, safety_settings={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL' : 'BLOCK_NONE',
        'DANGEROUS' : 'BLOCK_NONE'})
    
    chat_history.append(response.candidates[0].content.parts[0].text)
    return response.candidates[0].content.parts[0].text, chat_history
        
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
    path = os.path.join("../chats/gemini/", filename)
    
    with open(path, "w") as f:
        for log in chat_history:
            f.write(f"{log['role']}: \n{log['parts'][0]['text']}\n")
            f.write("\n<------>\n\n")


if __name__ == '__main__':
    main()
