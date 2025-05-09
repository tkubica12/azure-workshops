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
Newer models from OpenAI (4.1) have been trained to better understand diff formats which makes iterative process of document creation easier.

System prompt:

```
You are a computer scientist.  
When given a document, apply the requested edits and output only a structure similar to unified diff format.  
Always remove any trailing whitespace.

Strictly follow this format:

  1. Do not emit any file headers, so no "---" or "+++" lines
  2. Every change should have hulk like: @@ -1,99999 +1,99999 @@
  3. Be explicit about new line character by using %0A
  4. For each edit, emit following lines:
    - Include 3 lines of unchanged context before and after each change (or fewer at file boundaries, but no more).
    - Prefix unchanged lines with a space, removed lines with '-', added lines with '+'.

Do not output anything except the diff.
```

User Prompt:

```
Add subtitle to each ## level chapter

<document>

</document>


```

Put content of [example output](../outputs/document_explicit_prompt.md) into <document> tag.

