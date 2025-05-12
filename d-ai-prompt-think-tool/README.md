# AI Demo - from prompting to thinking to tool use
In this demo we will touch prompt engineering, reasoning, multi-step orchestration and tool use, but not as separate topics, but as a **story** of how to get better at certain tasks.

## Story of getting better at math
See [full guide](./docs/math.md) for more details.

1. [How relatively **simple prompt** can improve the performance of pretty small LLMs in math tasks.](./docs/math.md#1-simple-prompt)
2. [How **heavy prompt with guidance**, thinking process and examples can improve performance of very small LLMs in math tasks.](./docs/math.md#2-heavy-prompt)
3. [What if we orchestrate calling LLM multiple times so it can **reflect** on its own errors and improve the answer?](./docs/math.md#3-reflection)
4. [What if we automate process of AI trying various thinking strategies using Reinforcement Learning in verifiable domains and that capture successful ones and use it as training data to self-improve models? This is how **reasoning models** are trained and we will see how much better they are at math tasks.](./docs/math.md#4-reasoning-thinking-model)
5. [But why let LLM calculate where it can use calculator or write some code? Let's go solving our math challenge with **agent using tools**.](./docs/math.md#5-agent-using-tools)

## Story of writing insightful documents
See [full guide](./docs/creating_documents.md) for more details.

1. [How being very **explicit** in prompt will help you get what you want?](./docs/creating_documents.md#1-being-explicit-about-what-you-want)
2. [**Iterations** over document - from copy paste or "print it all" to using diffs.](./docs/creating_documents.md#2-iterations-over-document)
3. [Adding **context** always helps and why your site should have llms.txt file.](./docs/creating_documents.md#3-adding-context)
4. [Using **tools** to retrieve context automatically.](./docs/creating_documents.md#4-using-tools-to-retrieve-context-automatically)
5. [Iterate over tools either orchestrated, multi-agent or preferably while thinking - this is how **deep research** works and goes WAY beyond just reasoning models.](./docs/creating_documents.md#5-iterate-over-tools-either-orchestrated-or-while-thinking---this-how-deep-research-works)

## Story of analyzing data
See [full guide](./docs/analyzing_data.md) for more details.

1. [Extracting **textual** data](./docs/analyzing_data.md#1-extracting-textual-data)
2. [Processing **visual** data](./docs/analyzing_data.md#2-processing-visual-data)
3. [Using Code Interpreter tool for **data analysis***](./docs/analyzing_data.md#3-using-code-interpreter-tool-for-data-analysis)
4. [Using Code Interpreter tool for **data visualization**](./docs/analyzing_data.md#4-using-code-interpreter-tool-for-data-visualization)

## Resources
- [ShumerPrompt](https://shumerprompt.com/)
- [How to prompt reasoning models effectively](https://platform.openai.com/docs/guides/reasoning-best-practices#how-to-prompt-reasoning-models-effectively)
- [GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)