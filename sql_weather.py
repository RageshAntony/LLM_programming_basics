import random

import openai
import json
from colorama import Fore


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": random.randint(10,99),
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in Boston in celsius?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location","unit"],
            },
        }
    ]
    OPENAI_API_KEY = "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"
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function

        function_name = response_message["function_call"]["name"]
        if function_name == "get_current_weather":
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = get_current_weather(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

            # Step 4: send the info on the function call and function response to GPT
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )  # get a new response from GPT where it can see the function response
            return second_response["choices"][0]["message"]["content"]

if __name__ == '__main__':
    print(Fore.MAGENTA + run_conversation())