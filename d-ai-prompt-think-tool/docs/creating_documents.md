# Creating rich documents
1. How being very **explicit** in prompt will help you get what you want?
2. **Iterations** over document - from copy paste or "print it all" to using diffs.
3. Adding **context** always helps and why your site should have llms.txt file.
4. Using **tools** to retrieve context automatically.
5. Iterate over tools either orchestrated or while thinking - this how **deep research** works.
6. 
---

# 1. Being explicit about what you want

User Prompt:

``` Explain sharding using example of online game with players around the world. ```


System prompt (not explicit):

```
# Role
You are computer scientist.

# Instructions
Use simple easy to understand language
```

See [example output](../outputs/document_implicit_prompt.md)

System prompt (explicit):

```
# Role
You are computer scientist teacher with 10 years of experience and ability to explain complex concepts in simple terms.

# Instructions
- If you use any jargon or technical terms, explain them.
- Use examples to illustrate your points.
- Use analogies to make the concepts relatable.
- Provide a summary at the end to reinforce learning.
- Keep the tone friendly and engaging.
- Use markdown formatting for better readability.
- Use bullet points and headings for clarity
- Use code snippets if necessary
- Use mermaid diagrams to illustrate architectures or processes
- Use tables for comparisons if applicable
- Use quotes or references from well-known sources if applicable
- Use lists for steps or processes
- Use bold and italics for emphasis

# Example structure
- Title
- Introduction
- Explanation of the concept
- Deep dive into the components each with examples and analogies
- End-to-end example
- Real-world applications and scenarios
- Summary
```

See [example output](../outputs/document_explicit_prompt.md)

# 2. Iterations over document
Current LLMs are "better" at reading than writing (see input vs. output lengths, quality in large sequences, accumulation of error due to autoregression). You might want to work on your document iteratively. But how?

System prompt:

```
# Role
You are computer scientist.

# Instructions
You will be given a document with user instructions what to change or enhance. Make sure you strictly follow these rules:
- Use simple easy to understand language
- Do not change or remove content of the document unless it is explicitly related to changes requested by user.
- Do not add any content to the document unless it is explicitly related to changes requested by user.
- Do not change the structure of the document unless it is explicitly related to changes requested by user.
- Do not change the formatting of the document unless it is explicitly related to changes requested by user.

Output format:
- Output final version of the document with all changes applied.
- Do not add any additional comments or explanations.
```

User Prompt:

```
Add an italic subtitle to every '## ' level heading.
Insert blank line before and after that subtitle.

<document>

</document>
```

Put content of [example output](../outputs/document_explicit_prompt.md) into <document> tag.

See [example output](../outputs/document_iteration.md)

There are few issues with this approach:
- It is not very efficient - LLM need to output full document costing money
- You may reach output limit of LLM quickly
- Output quality may degrade due to accumulation of errors during autoregression
- LLMs might introduce changes to section of documents that you have not intended to change
- To get diff of changes you need to use diff tool yourself

Another approach is to ask LLM to output only changes. Over the last few months (as of writing - May 2025) this has been areas of improvements especially for code generation applications.

See [code](../utils/diff/main.py), [changes](../utils/diff/patch.json), and [example output](../utils/diff/output.md) for more details.