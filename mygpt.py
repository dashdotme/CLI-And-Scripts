#!/usr/bin/env python3

import argparse
import openai
import re
import os
from datetime import date

openai.api_key = os.environ["OPENAI_API_KEY"]

parser = argparse.ArgumentParser(
    prog="mygpt.py",
    description="A simple CLI for the OpenAI GPT3.X API.",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-t",
    "--type",
    type=str,
    default="create",
    help="""Definitions:
    - Chat (default): interactive, ongoing mode. '|?' to submit your current query (can be multiline)
    - Completion: generates a completion based on the prompt
    - Code: completion for code prompts. Loops up to 5 times by default
    - Edit: adjusts a prompt based on the instruction 
    - Model: populates a datestamped file in ./gpt_model_lists/ with a json of the current model options""",
    choices=["completion", "code", "edit", "models"],
)

parser.add_argument(
    "-e",
    "--engine",
    type=str,
    default="gpt-3.5-turbo",
    help="""Most relevant:
    - gpt-3.5-turbo (default): the (current) best model. Auto-updated
    - gpt-3.5-turbo-0301: Snapshot of March 1, 2023 GPT3.5 model.
    - text-davinci-003: expensive, with less fine tuning, but runs faster
    - code-davinci-002: optimized for code completion, with a larger (8001) token limit
See https://platform.openai.com/docs/models for more info.""",
)

parser.add_argument(
    "-i",
    "--instruction",
    type=str,
    default="Fix the errors in this statement.",
    help="""Tells the model what to change for edit type requests. 
Defaults to 'Fix the errors in this statement.'""",
)

parser.add_argument(
    "-m",
    "--max_tokens",
    type=int,
    default="256",
    help="""The base maximum number of tokens used per request. Defaults to 256. 
This, along with the engine (model) used, limits cost per request.""",
)

parser.add_argument("prompt", nargs="*", type=str)

# TODO: encapsulate this, and pass around the args in each function call
args = parser.parse_args()

def main():
    if len(os.sys.argv) < 2:
        chatmode()

    if args.type == "models":
        modelsmode()

    if len(args.prompt) == 1 and not re.match(r"^[\'\"\`]\s*$", args.prompt[0]):
        if not (os.path.isfile(args.prompt[0])):
            print(
                "Single prompt args are parsed as files. Please give a valid file path.")
            exit()
        with open(args.prompt[0], "r") as f:
            args.prompt = f.read()

    else:
        args.prompt = " ".join(args.prompt)

    if args.type == "code":
        codemode()

    if args.type == "edit":
        editmode()
    
    if args.type == "completion":
        completionmode()

    chatmode()

def modelsmode():
    with open(
        "./gpt_model_lists/models_" + date.today().strftime("%Y-%m-%d") + ".json", "w"
    ) as f:
        f.write(str(openai.Model.list()))
    exit()


def codemode():
    max_tokens = args.max_tokens

    response = openai.Completion.create(
        model=args.engine,
        prompt=args.prompt,
        temperature=1,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=['"""'],
        echo=True,
    )

    while response.choices[0].finish_reason != "stop" and max_tokens < 8001:
        max_tokens += 1000

        response = openai.Completion.create(
            model=args.engine,
            prompt=response.choices[0].text,
            temperature=1,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=['"""'],
            echo=False,
        )

    print(response.choices[0].text)
    exit()

# probably don't use this anymore; chat mode is better
def editmode():
    if args.instruction == "":
        print("Edit type requires an instruction")
        exit()
    args.engine = (
        "text-davinci-edit-001" if args.engine == "text-davinci-003" else args.engine
    )

    print(
        f"""Amending the prompt 
    {args.prompt}
using the instruction 
    {args.instruction}
and the model "{args.engine}"
    """
    )
    response = openai.Edit.create(
        model=args.engine,
        input=args.prompt,
        instruction=args.instruction,
    )
    print(response.choices[0].text)
    exit()


def completionmode():
    response = openai.Completion.create(
        model=args.engine,
        prompt=args.prompt,
        temperature=0,
        max_tokens=args.max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=['"""'],
        echo=True,
    )
    print(response.choices[0].text)
    exit()

def read_message():
    next_msg = []
    looping = True
    while looping:
        next_line = input()
        if '|?' in next_line:
            next_line.replace('|?', '')
            looping = False
        next_msg.append(next_line)


# see www.haihai.ai/chatgpt-api for walkthrough & further inspiration
# 
def chatmode():
    messages = []
    system_msg = input("What sort of bot do you need?\n")
    messages.append({"role": "system", "content": system_msg})

    print("")
    while input != "exit()":
        next_msg = []
        print("Me:")
        while True:
            next_line = input()
            if '|?' in next_line:
                next_msg.append(next_line.replace('|?', ''))
                break
            next_msg.append(next_line)

        message = "\n".join(next_msg)
        messages.append({"role": "user", "content": message})
        print("\nChatGPT is thinking...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("\nChatGPT:" + reply + "\n")
    exit()

if __name__ == "__main__":
    main()