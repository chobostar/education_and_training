import openai
import json
from datetime import datetime

# Initialize OpenAI client
client = openai.OpenAI(api_key="your-api-key-here")

# Define tool functions
def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    # Mock weather data - in real implementation, call weather API
    weather_data = {
        "New York": {"temperature": 22, "condition": "sunny"},
        "London": {"temperature": 15, "condition": "cloudy"},
        "Tokyo": {"temperature": 28, "condition": "rainy"}
    }

    location_weather = weather_data.get(location, {"temperature": 20, "condition": "unknown"})
    return {
        "location": location,
        "temperature": location_weather["temperature"],
        "unit": unit,
        "condition": location_weather["condition"]
    }

def calculate_math(expression):
    """Safely calculate mathematical expressions"""
    try:
        # Simple calculator - in production, use safer evaluation
        result = eval(expression.replace("^", "**"))
        return {"expression": expression, "result": result}
    except:
        return {"expression": expression, "result": "Error: Invalid expression"}

# Define tools for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. New York, London"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Calculate mathematical expressions",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate, e.g. '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def run_conversation(user_prompt):
    # Step 1: Send conversation and available functions to the model
    messages = [{"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # Let model decide when to use tools
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 2: Check if the model wants to call a function
    if tool_calls:
        # Extend conversation with assistant's reply
        messages.append(response_message)

        # Step 3: Call the function(s)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Call the appropriate function
            if function_name == "get_current_weather":
                function_response = get_current_weather(
                    location=function_args.get("location"),
                    unit=function_args.get("unit", "celsius")
                )
            elif function_name == "calculate_math":
                function_response = calculate_math(
                    expression=function_args.get("expression")
                )

            # Add function response to conversation
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response)
            })

        # Step 4: Get final response from model
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return second_response.choices[0].message.content

    return response_message.content

# Example usage
if __name__ == "__main__":
    # Test weather tool
    print("=== Weather Query ===")
    result1 = run_conversation("What's the weather like in New York?")
    print(result1)

    print("\n=== Math Calculation ===")
    result2 = run_conversation("Calculate 15 * 7 + 25")
    print(result2)

    print("\n=== Combined Query ===")
    result3 = run_conversation("What's the weather in London and calculate 100 / 4?")
    print(result3)