
# First steps

ollama.com

```bash
$ curl -fsSL https://ollama.com/install.sh | sh
```

```
ollama run llama3.2 
```

then able to chat:

use help:
```
$ ollama --help
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command
```
logs:
```
journalctl -xe -u ollama
```

Вопросы:
- насколько локально происходит испольнение? он может работать без интернета?
- насколько требователен к ресурсам? есть ли локальная память?


Course repo: https://github.com/ed-donner/llm_engineering

Install anaconda:
- https://github.com/ed-donner/llm_engineering/blob/main/SETUP-linux.pdf
```
alias conda_setup="eval $(/home/kiril/anaconda3/bin/conda shell.bash hook)"
```

```
cd <project>
conda env create -f environment.yml
```

```
#
# To activate this environment, use
#
#     $ conda activate llms
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```

This will open the browser:
```
jupyter lab
```

get OpenAI token, it might need 10$ credits.

pass Notebook: https://github.com/ed-donner/llm_engineering/tree/main/week1

Пример обращений:
```
import openai

response = openai.ChatCompletion.create(
    model="gpt-4", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do neural networks work in simple terms?"}
    ],
    temperature=0.7,        # Adjust creativity
    max_tokens=100,         # Limit response length
    top_p=0.95,             # Nucleus sampling
    frequency_penalty=0.0,  # Avoid repetition
    presence_penalty=0.6    # Encourage new ideas/topics
)

print(response['choices'][0]['message']['content'])
```

### Different Ways to Use Language Models
1. **Chat Interfaces**:
   Interact through web-based UIs (e.g., ChatGPT) with models managed entirely in the cloud by the provider.
2. **Cloud APIs**:
   Call models programmatically via an API (like OpenAI's API). Pay per request, useful for app integration.
3. **Managed AI Cloud Services**:
   Use big providers like Amazon Bedrock, Google Vertex AI, or Azure ML, which host and manage models on their infrastructure.
4. **Running Models Locally**:
   Use and run models on your local machine or remote servers. Two options:
    - **Framework-Based**: Use libraries (e.g., Hugging Face) for full control (e.g., tokenization, execution).
    - **Optimized Code**: Use tools like `llama.cpp` (optimized for performance but less control).
