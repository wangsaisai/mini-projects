from __future__ import annotations
import os
import sys
from dataclasses import dataclass
from textwrap import dedent
from httpx import AsyncClient

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider


SYSTEM_PROMPT = dedent(
    """\
    You are a professional developer specializing in shell commands.
    Your task is to generate the correct shell commands based on the 
    user's request.
    IMPORTANT: ALWAYS USE THE SAME LANGUAGE AS THE USER PROMPT IN 
    YOUR RESPONSE.
     Process:
    1. Think Aloud: Use the `think` function to explain your reasoning. 
    Justify why you chose a particular command, considering efficiency,
    safety, and best practices.
    2. Provide the Final Command: Use the `answer` function to present
    the final shell command concisely.
"""
)


@dataclass
class Answer:
    success: bool
    cmd: str | None
    failure: str | None

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# set up proxy if needed.
# export http_proxy=http://127.0.0.1:1087;export https_proxy=http://127.0.0.1:1087;
custom_http_client = AsyncClient(timeout=30)
agent = Agent(
    model=GeminiModel("gemini-2.0-flash", provider=GoogleGLAProvider(api_key=GOOGLE_API_KEY, http_client=custom_http_client)),
    system_prompt=SYSTEM_PROMPT,
    result_type=Answer,
)


@agent.tool_plain
def think(s: str) -> None:
    """Communicate your thought process to the user.
    Args:
        s (str): A description of your reasoning or decision-making process.
    """
    print(f"(AI Thinking): {s}\n")


@agent.tool_plain
def answer(success: bool, cmd: str | None, failure: str | None) -> Answer:
    """Provide the final shell command or explain why it couldn't be generated.
    Args:
        success (bool): Indicates whether a shell command was successfully generated.
        cmd (str | None): The generated shell command if `success` is True.
            It must be a single-line command. If `success` is False, this should be None.
        failure (str | None): If `success` is False, provide a reason why the command
            could not be generated. If `success` is True, this should be None.
    Returns:
        Answer: A structured response that will be processed for the user.
    """
    return Answer(success, cmd, failure)


def main() -> None:
    user_prompt = "".join(sys.argv[1:])
    if len(user_prompt) == 0:
        print("No prompts")
        sys.exit(1)

    resp = agent.run_sync(user_prompt)
    answer = resp.data
    if answer.success and answer.cmd is not None:
        print(f"(AI Answer): {answer.cmd}")
        y_or_n = input("Execute? Y/N: ")
        if y_or_n in ["y", "Y"]:
            os.system(answer.cmd)
    else:
        print(f"(AI Answer): {answer.failure}")
        print("Generate failed")


if __name__ == "__main__":
    main()
