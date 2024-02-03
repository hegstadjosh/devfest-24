import os
import openai
from openai import OpenAI
import json
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import g4f

client = OpenAI()
GPT_MODEL = "gpt-3.5-turbo"

openai.api_key = "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"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    #
    # This function sends a chat completion request to the OpenAI API.

    # Parameters:
    # messages (list): A list of message objects. Each object should have a 'role' and 'content'.
    # tools (list, optional): A list of tools to be used. Defaults to None.
    # tool_choice (str, optional): The chosen tool. Defaults to None.
    # model (str, optional): The model to be used for the chat completion. Defaults to GPT_MODEL.

    # Returns:
    # dict: The response from the OpenAI API.
    # 

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    
def pretty_print_conversation(messages):
  """
  Prints a formatted conversation based on the provided messages.

  Parameters:
  - messages (list): A list of message objects representing the conversation.

  Returns:
  - None
  """

  role_to_color = {
    "system": "red",
    "user": "green",
    "assistant": "blue",
    "tool": "magenta",
  }

  for message in messages:
    if message["role"] == "system":
      print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "user":
      print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "assistant" and message.get("function_call"):
      print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
    elif message["role"] == "assistant" and not message.get("function_call"):
      print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
    elif message["role"] == "tool":
      print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

