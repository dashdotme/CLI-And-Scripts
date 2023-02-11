#!/usr/bin/env python3

import argparse
import openai
import re
import os
from datetime import date

openai.api_key = os.environ["OPENAI_API_KEY"]

parser = argparse.ArgumentParser(
    prog="mygpt.py",
    description="A simple CLI for the OpenAI GPT3 API.",
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    "-t",
    "--type",
    type=str,
    default="create",
    help="""Definitions:
    - Completion (default): generates a completion based on the prompt
    - Code: completion for code prompts. Loops up to 5 times by default
    - Edit: adjusts a prompt based on the instruction 
    - Model: populates a datestamped file in ./gpt_model_lists/ with a json of the current model options""",
    choices=["completion", "code", "edit", "models"],
)

parser.add_argument(
    "-e",
    "--engine",
    type=str,
    default="text-davinci-003",
    help="""Most relevant:
    - text-davinci-003 (default): the default model
    - text-curie-001: a simpler/cheaper davinci
    - text-babbage-001: a much cheaper and faster text completion model
    - text-ada-001: the cheapest text completion model
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

args = parser.parse_args()

if args.type == "models":
    with open(
        "./gpt_model_lists/models_" + date.today().strftime("%Y-%m-%d") + ".json", "w"
    ) as f:
        f.write(str(openai.Model.list()))
    exit()

if len(args.prompt) == 0:
    print("If not using the model command, a prompt is required\n")
    parser.print_help()
    exit(2)

if len(args.prompt) == 1 and not re.match(r"^[\'\"\`]\s*$", args.prompt[0]):
    if not (os.path.isfile(args.prompt[0])):
        print("Single prompt args are parsed as files. Please give a valid file path.")
        exit()
    with open(args.prompt[0], "r") as f:
        args.prompt = f.read()

else:
    args.prompt = " ".join(args.prompt)

if args.type == "code":
    max_tokens = args.max_tokens

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=args.prompt,
        temperature=1,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=['"""'],
        echo=True,
    )

    while response.choices[0].finish_reason != "stop" and max_tokens < 1280:
        max_tokens += 256

        response = openai.Completion.create(
            model="code-davinci-002",
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


if args.type == "edit":
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
else:
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
