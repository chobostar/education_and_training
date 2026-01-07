
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

### Six Leading Models
1. **OpenAI**: Known for GPT, their most famous model, along with the ChatGPT interface and the new 0101 preview.
2. **Anthropic**: OpenAI's competitor, features the Claude model in three versions: Haiku (smallest), Sonnet (medium, stronger than Opus), and Opus.
3. **Google Gemini**: A new model that replaced Bard and is used in Google search responses.
4. **Cohere**: A Canadian company leveraging the RAG technique to ensure expertise.
5. **Meta's LLaMA**: An open-source model available via Meta AI's website.
6. **Perplexity**: A search engine powered by AI and large language models, including its own model.

### Limitations of LLMs

1. **Limited Expertise**: Most lack PhD-level knowledge in specialized fields, though Claude 3.5 Sonnet excels in math, physics, and chemistry.
2. **Knowledge Cutoff**: Models can't access information beyond their training date (e.g., GPT cutoff: October last year).
3. **Hallucinations**: Can confidently provide incorrect answers without acknowledging uncertainty.

OpenAI Canvas feature enables interactive, collaborative coding sessions with GPT, allowing iterative code refinement.

- Claude 3.5 is currently one of the strongest large language models, excelling in thoughtful and insightful responses.
- - It demonstrates strong capabilities in coding, producing well-structured code artifacts.

- Claude is often favored for its succinct, charismatic, and safety-aligned answers.
- As LLM performance converges, factors like cost and rate limits will become key differentiators.

Trends:
- `Prompt Engineering -> Custom GPTs -> Copilots -> Agents`

Agentic AI represents a new trend where multiple LLMs collaborate autonomously, with memory and planning capabilities, to solve complex problems by dividing tasks among specialized agents.

`Transformers`:
**1. Attention Mechanism**
- Models can "pay attention" to different parts of input text
- Self-attention allows each word to consider all other words in context
- Captures relationships and dependencies between tokens [[1]](https://rpradeepmenon.medium.com/introduction-to-large-language-models-and-the-transformer-architecture-534408ed7e61)

**2. Architecture**
- **Encoder**: Processes and understands input
- **Decoder**: Generates output text
- **Multi-head attention**: Multiple attention mechanisms working in parallel
- **Feed-forward networks**: Process information between attention layers [[4]](https://www.truefoundry.com/blog/transformer-architecture)

### How They Work
1. **Tokenization**: Text → numerical tokens
2. **Embeddings**: Convert tokens to vectors
3. **Positional encoding**: Add position information
4. **Attention layers**: Calculate importance of each token
5. **Output**: Generate next token probabilities [[7]](https://www.ibm.com/think/topics/transformer-model)


`Weights`:
- LLMs are defined by the number of parameters, also called `weights`, which control their output.
- `weights` representing the levers adjusted during training to improve predictions.
- Traditional machine learning models typically have between 20 and 200 parameters, whereas LLMs have millions to trillions of parameters.
- The scale of parameters in LLMs has grown exponentially from GPT-1's 117 million to frontier models with around 10 trillion parameters.

`Tokens`:
- Basic units in language models (characters → words → subword chunks)
- GPT uses subword tokenization for optimal balance
- 1 token ≈ 4 chars or 0.75 words in English

### Рекомендации
- Для сложных задач лучше использовать английский
- Для простых вопросов разница в качестве минимальна
- Учитывать разницу в стоимости при масштабировании

Context Windows:
- Maximum tokens an LLM can process at once
- Limited by: Model architecture and parameters
- **ChatGPT approach**: Resubmits entire conversation history each time
- **Longer chats**: Need more context window space to maintain coherence

### Context Window Recommendations
**For Users:**
- **Keep conversations focused** - start new chats for different topics
- **Summarize long discussions** when hitting limits
- **Be concise** in prompts to save token space
- **Use system messages** efficiently for instructions

**For Developers:**
- **Choose models** with appropriate context size for your use case
- **Implement conversation pruning** (keep recent + important messages)
- **Cache/summarize** old context instead of keeping everything
- **Monitor token usage** to optimize costs

**Model Selection:**
- **GPT-4**: 8K-32K tokens (varies by version)
- **Claude**: Up to 200K tokens
- **Gemini**: Up to 1M tokens
- Consider **cost vs context size** trade-offs

**Pro Tip**: Longer context ≠ always better - models can lose focus in very long contexts.

### API vs Chat Interface Costs
**API Pricing:**
- Pay per token (input + output)
- Low individual costs, high at scale
- Requires minimum credit ($5+)

**Chat Interfaces:**
- Monthly subscription
- Rate limits, no per-call charges
- Fixed cost regardless of usage

### Recommendations
**Use Chat Interface when:**
- Personal/occasional use
- Predictable monthly usage
- Learning/experimenting

**Use API when:**
- Building applications
- Bulk processing
- Need programmatic access
- Variable usage patterns

LLM Leaderboard:
https://www.vellum.ai/llm-leaderboard


Пример минимально полезной агента:
- инициализация OpenAI библиотек и токена
- распарсить html по URL, например используя python BeautifulSoup
- использовать технику `Structured Outputs`:
- - ```
    link_system_prompt = "You are provided with a list of links found on a webpage. \
   You are able to decide which of the links would be most relevant to include in a brochure about the company, \
   such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
   link_system_prompt += "You should respond in JSON as in this example:"
   link_system_prompt += """
   {
   "links": [
   {"type": "about page", "url": "https://full.url/goes/here/about"},
   {"type": "careers page": "url": "https://another.full.url/careers"}
   ]
   }
   """
    ```
- Их смешать с обычными контектом и передать в LLM с новыми намерениями
- Получить результат

Код который рисует брошуру и добавляет ссылки: https://github.com/ed-donner/llm_engineering/blob/main/week1/day5.ipynb

Еще пример из ДЗ: https://github.com/ed-donner/llm_engineering/blob/main/week1/solutions/week1%20SOLUTION.ipynb

Setup multiple LLMs by retrieving keys:
- For OpenAI, visit https://openai.com/api/  
- For Anthropic, visit https://console.anthropic.com/  
- For Google, visit https://ai.google.dev/gemini-api

There is example code of 2 LLMs conversation: https://github.com/ed-donner/llm_engineering/blob/main/week2/day1.ipynb

## Gradio

**Gradio** is a Python library for rapidly building ML user interfaces with minimal coding effort.

**Key Features:**
- Quick UI prototyping without front-end expertise
- Seamless Hugging Face integration
- Perfect for LLM applications (GPT, Claude, Gemini)
- Any Python function can serve as backend
- Share interfaces locally or via public URLs
- Code runs on local machine while interface is accessible remotely

**Use Cases:**
- Demo ML models
- Create interactive web apps
- Prototype AI interfaces
- Share models with non-technical users

**Interface Options:**
- Clean UI (flagging can be disabled)
- Local or public sharing
- Works with any Python function or LLM wrapper


(This can reveal the "training cut off", or the most recent date in the training data)
> message_gpt("What is today's date?")


example code with UI for Assistant: https://github.com/ed-donner/llm_engineering/blob/main/week2/day2.ipynb

https://www.promptingguide.ai/

## AI Tools with LLMs

### What Are Tools?
**Tools** enable LLMs to connect with external functions, extending their capabilities beyond text generation. They provide access to databases, APIs, calculators, and other external resources.

### How Tools Work
1. **Define functions** available to the LLM (inputs, outputs, usage conditions)
2. **Inform the LLM** about available tools
3. **LLM decides** whether to respond directly or request a tool
4. **Execute the tool** and return results to LLM
5. **LLM generates** enhanced response using tool output

### Common Use Cases

| Use Case | Example | Benefit |
| --- | --- | --- |
| **Fetching Data** | Database lookups | Added knowledge |
| **Taking Actions** | Booking meetings, purchasing | Real-world operations |
| **Calculations** | Math operations | Improved accuracy |
| **UI Modifications** | Interface changes | Dynamic interactions |

### Tools vs. Structured JSON
- **Tools**: Integrated solution for complex workflows
- **JSON Responses**: Simpler approach where LLM returns structured data indicating desired actions
- **Choice depends on**: Complexity and integration requirements

### Key Benefits
- **Dynamic context**: LLMs request information as needed
- **Enhanced capabilities**: Access to real-time data and external functions
- **Structured workflow**: Organized way to extend LLM functionality
- **Richer responses**: Combines LLM reasoning with external data/actions

**Bottom Line**: Tools transform LLMs from text generators into intelligent agents capable of interacting with external systems and performing complex tasks.

See the example: [week2_ai_gerenated_tool_example.py](week2_ai_gerenated_tool_example.py)
See the other example: https://github.com/ed-donner/llm_engineering/blob/main/week2/day4.ipynb


Agents:
- autonomous
- goal-oriented
- task specific

### Multimodel AI
 **Multimodal AI** refers to artificial intelligence systems that can process, understand, and generate content across multiple types of data modalities or formats simultaneously:
- **Text** - Natural language processing and generation
- **Images** - Computer vision and image analysis
- **Audio** - Speech recognition and audio processing
- **Video** - Moving image analysis and understanding
- **Sensors** - Data from various IoT devices and sensors
- **Code** - Programming languages and structured data

### Multimodel AI: How It Works
Multimodal AI systems typically:
1. **Process multiple inputs** - Can simultaneously analyze text, images, audio, etc.
2. **Cross-modal understanding** - Understand relationships between different types of data
3. **Unified representations** - Convert different modalities into shared internal representations
4. **Generate multimodal outputs** - Can produce responses in various formats

### Multimodel AI: Benefits
- **Richer Understanding** - More comprehensive analysis by combining multiple data sources
- **Better Context** - Enhanced decision-making through cross-modal information
- **More Natural Interaction** - Interfaces that work more like human perception
- **Improved Accuracy** - Multiple modalities can validate and enhance each other

Домашка week2: [week2_work.py](week2_work.py)
- взаимодействие с несколькими LLM
- использование tools

## Hugging Face
https://huggingface.co/
- Hugging Face is a comprehensive open-source platform offering over 800,000 models, 200,000 datasets, and Spaces for app deployment.
- The platform supports libraries like Transformers, Datasets, Hub, Peft, TRL, and Accelerate to facilitate efficient model training and deployment.
- Spaces enable sharing of Gradio and Streamlit apps on Hugging Face cloud infrastructure.
- Advanced techniques such as parameter efficient fine tuning (PEFT) and reinforcement learning (TRL) are integral for customizing and improving language models.

`Google Colab`:
- Google Colab provides a cloud-based Jupyter notebook environment accessible with a Google account.

https://colab.research.google.com/

examoles for colab: https://colab.research.google.com/drive/1DjcrYDZldAXKJ08x1uYIVCtItoLPk1Wr?usp=sharing

### Key Takeaways
- Google Colab enables easy access to powerful cloud GPUs for AI model execution.
- The Flux model is a top trending open-source text-to-image generation model from Black Forest.
- Users can prompt models with creative inputs to generate unique AI-generated images.
- Mastery of Hugging Face and Google Colab prepares users to run open-source AI models effectively.

### Key Takeaways
- Hugging Face Transformers offers two API levels: high-level pipelines for quick inference and low-level APIs for detailed customization and training.
- Pipelines enable performing common AI tasks like sentiment analysis, classification, named entity recognition, question answering, summarization, and translation with minimal code.
- Text, image, and audio generation can also be accomplished simply using pipelines.
- The Hugging Face hub provides easy access to pre-trained models and datasets for rapid AI development.

Pipelines demo:
https://colab.research.google.com/drive/1aMaEw8A56xs0bRM4lu8z7ou18jqyybGm?usp=sharing
- Hugging Face's Transformers library offers a high-level pipeline API for easy inference across various AI tasks.
- Pipelines support tasks such as sentiment analysis, named entity recognition, question answering, summarization, translation, zero-shot classification, text generation, image generation, and text-to-speech.

# Mastering RAG

### The Big Idea: Vector Embeddings
- Vector: A set of numbers (coordinates in multi-dimensional space) representing the meaning of a text.
- Role in RAG: Enables "fuzzy lookup"—finding relevant context based on semantic similarity rather than just keyword matching.

### Two Types of LLMs
- Auto-Regressive Models (e.g., GPT, Claude): Trained to predict the next token. They are primarily text generators.
- Encoder / Embedding Models (e.g., BERT, MiniLM): Process the entire input to produce a single vector representation. They are used for classification and search.

### Tokens vs. Vectors
- Tokens (Input): Simple numeric IDs for text fragments created by a tokenizer. They serve as the raw input the model can "read."
- Vectors (Output): Advanced numeric representations produced by the model. They capture relationships and deep semantic meaning.

**Key takeaway**: Tokens are the simple inputs; vectors are the intelligent, model-generated outputs that capture essence and intent.

--

### Meaning as a Point in Space
- Proximity = Similarity: In vector space, concepts with similar meanings are located close to each other.
- Example: "Flight prices from JFK to Heathrow" and "Cost of tickets from New York to London" will have vectors very near each other, despite using different words.

### Vector Arithmetic
Meaning can be manipulated mathematically, proving that vectors capture the underlying structure of concepts:
- `King - Man + Woman ≈ Queen`
- `Paris - France + England ≈ London`

### Evolution: From Words to Context
- **word2vec**: An older algorithm that mapped individual words to vectors.
- Modern Encoders: Map entire sentences, paragraphs, or abstract concepts (like a person's career path) to vectors while preserving context.

### Technical Metric
- Cosine Similarity: The standard technical method used to measure how "close" or similar two vectors are in high-dimensional space.

**Summary**: Vector embeddings allow us to calculate the similarity of ideas mathematically, independent of the specific phrasing used.

---

### The RAG Workflow
1. Vectorization: Both the user's question and the knowledge base are converted into vectors using an Encoder model.
2. Semantic Search: Instead of matching keywords (e.g., "Heathrow"), the system searches a Vector Data Store for coordinates with the closest meaning (e.g., "London Airport").
3. Context Injection: The system retrieves the relevant natural language text (not numbers) and adds it to the prompt.
4. Generation: The Autoregressive LLM receives the context and the question to generate a factual response.

### Key Distinctions
- Encoder vs. LLM: The encoder is a separate tool used only for the search phase. The LLM only receives and generates human language.
- Fuzzy Lookup: RAG is powerful because it understands concepts even when specific words don't match exactly.

### The Reality of RAG
- Empirical Practice: RAG is often described as a series of "hacks" and experiments. Finding the most relevant context requires trial, error, and practical tools like LangChain and Chroma.

**Summary**: RAG uses an encoder to find the "meaningful" context in a vector database and feeds that context to an LLM to ensure accurate, grounded answers.

---

# Vector Databases

- https://github.com/langchain-ai/langchain
  - framework for building agents and LLM-powered applications. It helps you chain together interoperable components and third-party integrations to simplify AI application development
  - https://docs.langchain.com/oss/python/langchain/overview
  - load out knowledge base:
    - read documents in all folders
    - divide into chunks
    - vectorize and store

https://github.com/chroma-core/chroma  - Open-source search and retrieval database for AI applications.
