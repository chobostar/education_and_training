## LLM Parameters
### **Core Generation Parameters**

| Parameter | Range | Default | Description |
| --- | --- | --- | --- |
| **temperature** | 0.0 - 2.0 | 1.0 | Controls randomness/creativity. Lower = more focused, higher = more creative [[1]](https://www.analyticsvidhya.com/blog/2024/10/llm-parameters/) |
| **max_tokens** | 1 - model limit | varies | Maximum number of tokens to generate [[3]](https://mehmetozkaya.medium.com/llm-settings-explained-temperature-max-tokens-stop-sequences-top-p-frequency-penalty-and-04a9df257378) |

### **Sampling Parameters**

| Parameter | Range | Default | Description |
| --- | --- | --- | --- |
| **top_p** | 0.0 - 1.0 | 1.0 | Nucleus sampling - only considers tokens with cumulative probability up to p [[2]](https://www.promptingguide.ai/introduction/settings) |
| **top_k** | 1 - vocab size | 50 | Only considers top k most likely tokens for sampling [[7]](https://aviralrma.medium.com/understanding-llm-parameters-c2db4b07f0ee) |

### **Repetition Control Parameters**

| Parameter | Range | Default | Description |
| --- | --- | --- | --- |
| **frequency_penalty** | -2.0 to 2.0 | 0.0 | Penalizes tokens based on frequency in generated text [[2]](https://www.promptingguide.ai/introduction/settings) |
| **presence_penalty** | -2.0 to 2.0 | 0.0 | Penalizes tokens that already appeared, encouraging topic diversity [[2]](https://www.promptingguide.ai/introduction/settings) |
| **repetition_penalty** | 0.1 - 2.0 | 1.0 | Penalizes repeated phrases (Hugging Face models) [[4]](https://www.cyberseo.net/blog/comprehensive-guide-to-understanding-key-gpt-model-parameters/) |

### **Control Parameters**

| Parameter | Range | Default | Description |
| --- | --- | --- | --- |
| **stop_sequences** | strings/array | None | Sequences that halt generation when encountered [[3]](https://mehmetozkaya.medium.com/llm-settings-explained-temperature-max-tokens-stop-sequences-top-p-frequency-penalty-and-04a9df257378) |
| **seed** | integer | None | Ensures reproducible outputs when set [[1]](https://argilla-io.github.io/distilabel/1.4.1/api/llm/llm_gallery/) |
| **logit_bias** | token_id: -100 to 100 | None | Adjusts likelihood of specific tokens being generated [[7]](https://aviralrma.medium.com/understanding-llm-parameters-c2db4b07f0ee) |

### **Usage Examples by Scenario** [[6]](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683)

| Use Case | Temperature | Top_p | Description |
| --- | --- | --- | --- |
| **Code Generation** | 0.2 | 0.1 | Precise, conventional code |
| **Creative Writing** | 0.8-1.2 | 0.9 | Imaginative, diverse content |
| **Technical Documentation** | 0.1-0.3 | 0.1 | Factual, consistent information |
| **Conversational AI** | 0.7 | 0.8 | Natural, engaging responses |
| **Data Analysis** | 0.1 | 0.1 | Accurate, deterministic output |

### **Best Practices**
1. **Don't adjust both frequency_penalty and presence_penalty simultaneously** [[2]](https://www.promptingguide.ai/introduction/settings)
2. **Use temperature OR top_p, not both at extreme values**
3. **Start with default values and adjust incrementally**
4. **Lower temperature for factual tasks, higher for creative tasks** [[5]](https://learnprompting.org/blog/llm-parameters?srsltid=AfmBOooX1_dSagIEExH1vYHrZn2ceWOizt9DKgIwC6kGyHi4yctbzULD)

### **Parameter Interactions**
- **Temperature + Top_p**: Temperature applies first, then top_p filters the results
- **Penalties**: Frequency looks at token count, presence looks at token existence
- **Seed**: Only works when temperature = 0 or other deterministic settings are used
