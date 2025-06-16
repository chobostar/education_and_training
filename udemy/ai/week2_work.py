import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai
import gradio as gr
import time

load_dotenv(override=True)

# Initialize API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None
if google_api_key:
    genai.configure(api_key=google_api_key)

# Available models
MODELS = {
    "GPT-4o": {"provider": "openai", "model": "gpt-4o"},
    "GPT-4o Mini": {"provider": "openai", "model": "gpt-4o-mini"},
    "Claude 3.5 Sonnet": {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
    "Claude 3 Haiku": {"provider": "anthropic", "model": "claude-3-haiku-20240307"},
    "Gemini 1.5 Pro": {"provider": "google", "model": "gemini-1.5-pro"},
    "Gemini 1.5 Flash": {"provider": "google", "model": "gemini-1.5-flash"}
}

system_message = "You are a technical assistant for LLM engineering student. "
system_message += "Give short, accurate answers, no more than 3-5 sentences. "
system_message += "Always be accurate. If you don't know the answer, say so."

def get_current_weather(latitude, longitude):
    """Get current weather data using latitude and longitude"""
    print(f"Tool get_current_weather called for lat: {latitude}, lon: {longitude}")

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        current_weather = data.get("current_weather", {})

        return {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "temperature": current_weather.get("temperature"),
            "temperature_unit": data.get("current_weather_units", {}).get("temperature", "°C"),
            "windspeed": current_weather.get("windspeed"),
            "windspeed_unit": data.get("current_weather_units", {}).get("windspeed", "km/h"),
            "wind_direction": current_weather.get("winddirection"),
            "weather_code": current_weather.get("weathercode"),
            "is_day": current_weather.get("is_day"),
            "time": current_weather.get("time")
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

# OpenAI/Anthropic style tool definition
weather_function_openai = {
    "name": "get_current_weather",
    "description": "Get the current weather for a specific location using latitude and longitude coordinates. Use this when someone asks about weather conditions for a city or location.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "The latitude coordinate of the location"
            },
            "longitude": {
                "type": "number",
                "description": "The longitude coordinate of the location"
            }
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    }
}

# Google Gemini style tool definition
weather_function_gemini = {
    "function_declarations": [
        {
            "name": "get_current_weather",
            "description": "Get the current weather for a specific location using latitude and longitude coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "The latitude coordinate of the location"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The longitude coordinate of the location"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
    ]
}

def handle_openai_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    latitude = arguments.get('latitude')
    longitude = arguments.get('longitude')
    weather_data = get_current_weather(latitude, longitude)
    response = {
        "role": "tool",
        "content": json.dumps(weather_data),
        "tool_call_id": tool_call.id
    }
    return response

def handle_anthropic_tool_call(tool_use):
    latitude = tool_use.input.get('latitude')
    longitude = tool_use.input.get('longitude')
    weather_data = get_current_weather(latitude, longitude)
    response = {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(weather_data)
            }
        ]
    }
    return response

def handle_gemini_tool_call(function_call):
    latitude = function_call.args.get('latitude')
    longitude = function_call.args.get('longitude')
    weather_data = get_current_weather(latitude, longitude)
    return weather_data

def chat_streaming(message, history, selected_model):
    model_config = MODELS.get(selected_model)
    if not model_config:
        yield "Error: Invalid model selection"
        return

    provider = model_config["provider"]
    model_name = model_config["model"]

    # Convert history to the correct format
    if provider == "openai":
        messages = [{"role": "system", "content": system_message}]
        for human_msg, assistant_msg in history:
            messages.append({"role": "user", "content": human_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": message})

        yield from handle_openai_chat(messages, model_name)

    elif provider == "anthropic":
        messages = []
        for human_msg, assistant_msg in history:
            messages.append({"role": "user", "content": human_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": message})

        yield from handle_anthropic_chat(messages, model_name)

    elif provider == "google":
        # Convert history for Gemini
        chat_history = []
        for human_msg, assistant_msg in history:
            chat_history.append({"role": "user", "parts": [human_msg]})
            if assistant_msg:
                chat_history.append({"role": "model", "parts": [assistant_msg]})

        yield from handle_gemini_chat(chat_history, message, model_name)

def handle_openai_chat(messages, model_name):
    try:
        if not openai_client:
            yield "Error: OpenAI API key not configured"
            return

        # First, check if we need to make a tool call
        initial_response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=[{"type": "function", "function": weather_function_openai}],
            stream=False
        )

        # Handle tool calls if needed
        if initial_response.choices[0].finish_reason == "tool_calls":
            message_with_tool_call = initial_response.choices[0].message
            tool_response = handle_openai_tool_call(message_with_tool_call)
            messages.append(message_with_tool_call)
            messages.append(tool_response)

            # Now stream the final response
            stream = openai_client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True
            )
        else:
            # Stream the direct response
            stream = openai_client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=[{"type": "function", "function": weather_function_openai}],
                stream=True
            )

        # Yield streaming response
        partial_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                partial_message += chunk.choices[0].delta.content
                yield partial_message

    except Exception as e:
        yield f"Error: {str(e)}"

def handle_anthropic_chat(messages, model_name):
    try:
        if not anthropic_client:
            yield "Error: Anthropic API key not configured"
            return

        # First, check if we need to make a tool call
        initial_response = anthropic_client.messages.create(
            model=model_name,
            max_tokens=1000,
            system=system_message,
            messages=messages,
            tools=[{
                "name": "get_current_weather",
                "description": "Get the current weather for a specific location using latitude and longitude coordinates",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number", "description": "The latitude coordinate"},
                        "longitude": {"type": "number", "description": "The longitude coordinate"}
                    },
                    "required": ["latitude", "longitude"]
                }
            }]
        )

        # Handle tool calls if needed
        if initial_response.stop_reason == "tool_use":
            tool_use = None
            for content in initial_response.content:
                if content.type == "tool_use":
                    tool_use = content
                    break

            if tool_use:
                messages.append({"role": "assistant", "content": initial_response.content})
                tool_response = handle_anthropic_tool_call(tool_use)
                messages.append(tool_response)

                # Get final response with streaming
                with anthropic_client.messages.stream(
                        model=model_name,
                        max_tokens=1000,
                        system=system_message,
                        messages=messages
                ) as stream:
                    partial_message = ""
                    for text in stream.text_stream:
                        partial_message += text
                        yield partial_message
            else:
                yield initial_response.content[0].text
        else:
            yield initial_response.content[0].text

    except Exception as e:
        yield f"Error: {str(e)}"

def handle_gemini_chat(chat_history, message, model_name):
    try:
        if not google_api_key:
            yield "Error: Google API key not configured"
            return

        model = genai.GenerativeModel(
            model_name=model_name,
            tools=[weather_function_gemini],
            system_instruction=system_message
        )

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(message)

        # Check if there are function calls
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            weather_data = handle_gemini_tool_call(function_call)

            # Send function response back
            function_response = genai.protos.Part(
                function_response=genai.protos.FunctionResponse(
                    name="get_current_weather",
                    response={"result": weather_data}
                )
            )

            response = chat.send_message([function_response])

        yield response.text

    except Exception as e:
        yield f"Error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Multi-LLM Chat with Weather Tool") as demo:
    gr.Markdown("# Multi-LLM Chat with Weather Tool")
    gr.Markdown("Select a model and ask about weather in any city! The assistant will get real-time weather data.")

    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=list(MODELS.keys()),
            value="GPT-4o Mini",
            label="Select Model",
            interactive=True
        )

    chatbot = gr.Chatbot(
        label="Chat",
        height=400,
        show_copy_button=True
    )

    msg = gr.Textbox(
        label="Message",
        placeholder="Try asking: 'What's the weather like in Tokyo?'",
        lines=2,
        max_lines=5
    )

    with gr.Row():
        submit_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear Chat")
        stop_btn = gr.Button("Stop", variant="stop")

    def respond(message, chat_history, model):
        if not message.strip():
            return "", chat_history

        # Add user message to history immediately
        chat_history.append((message, ""))
        yield "", chat_history

        # Stream the bot response
        for partial_response in chat_streaming(message, chat_history[:-1], model):
            chat_history[-1] = (message, partial_response)
            yield "", chat_history

    def clear_chat():
        return [], ""

    def stop_generation():
        return

    # Event handlers
    submit_event = submit_btn.click(
        respond,
        inputs=[msg, chatbot, model_dropdown],
        outputs=[msg, chatbot]
    )

    msg_event = msg.submit(
        respond,
        inputs=[msg, chatbot, model_dropdown],
        outputs=[msg, chatbot]
    )

    clear_btn.click(
        clear_chat,
        outputs=[chatbot, msg]
    )

    stop_btn.click(
        stop_generation,
        cancels=[submit_event, msg_event]
    )

if __name__ == "__main__":
    demo.launch(share=False, debug=True)