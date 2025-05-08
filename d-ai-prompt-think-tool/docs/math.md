# Story of getting better at math
1. How relatively **simple prompt** can improve the performance of pretty small LLMs in math tasks.
2. How **heavy prompt with guidance**, thinking process and examples can improve performance of very small LLMs in math tasks.
3. What if we orchestrate calling LLM multiple times so it can **reflect** on its own errors and improve the answer?
4. What if we automate process of AI trying various thinking strategies using Reinforcement Learning in verifiable domains and that capture successful ones and use it as training data to self-improve models? This is how **reasoning models** are trained and we will see how much better they are in math tasks.
5. But why let LLM calculate where it can use calculator or write some code? Solving our math challenge with **agent using tools**.

---

# 1. Simple prompt

User Prompt:

> Calculate 7952 * 9823

Correct answer is 78,112,496

Using **gpt-4.1-nano** with 0 temperature.

System prompt (**wrong** answer):
```
You are an AI assistant that helps people find information.
```

System prompt (**correct** answer):
```
# ROLE:
You are math professor.
```

System prompt (**wrong** answer):
```
# ROLE:
You are math professor.

# INSTRUCTIONS:
Print only final answer.
```

System prompt (**wrong** answer):
```
# ROLE:
You are math professor.

# INSTRUCTIONS:
First give me poem about how math is nice. After that print only final answer.
```

System prompt (correct answer):
```
# ROLE:
You are history professor.

# INSTRUCTIONS:
Do it step by step and explain your thinking at each step. Only then print the final answer.
```

## 2. Heavy prompt
What about even smaller model such as **Phi-3.5-mini**?

User Prompt:

> Calculate 7952 * 9823

System prompt (**wrong** answer):
```
# ROLE:
You are math professor.

# INSTRUCTIONS:
Do it step by step and explain your thinking at each step. Only then print the final answer.
```

Heavy system prompt with guidance, thinking process and examples (**correct** answer):
```
# ROLE
You are a relentlessly careful Math Professor.  
Your only job is to multiply two supplied positive integers A * B.

# EXAMPLE
## Step 1: Rewrite the problem clearly:
295546 × 35569

## Step 2: Break down the numbers into simpler parts to multiply:
We can split 35569 into 35000 + 500 + 60 + 9:
295546 × 35569 = 295546 × (35000 + 500 + 60 + 9)

## Step 3: Multiply each part separately:

295546 × 35000
295546 × 500
295546 × 60
295546 × 9

Let's calculate each separately:
295546 × 35000:
295546 × 35 = 10,344,110
Then multiply by 1000: 10,344,110 × 1000 = 10,344,110,000
295546 × 500:
295546 × 5 = 1,477,730
Then multiply by 100: 1,477,730 × 100 = 147,773,000
295546 × 60:
295546 × 6 = 1,773,276
Then multiply by 10: 1,773,276 × 10 = 17,732,760
295546 × 9:
295546 × 9 = 2,659,914

## Step 4: Add all these results together:
10,344,110,000
147,773,000
17,732,760
2,659,914
 
Let's add carefully step by step:

First, add the two smallest numbers:
17,732,760 + 2,659,914 = 20,392,674
Now add this result to 147,773,000:
147,773,000 + 20,392,674 = 168,165,674
Finally, add this result to 10,344,110,000:
10,344,110,000 + 168,165,674 = 10,512,275,674

**Final Answer:**
295546 × 35569 = 10,512,275,674
```

How I got this prompt? Asked clever model to give mi thinking process to achieve correct answer. For this case, it is easy, but for more complex ones even large models will struggle a lot. In verifiable domains you will get feedback, generate multiple trees of thoughts, leverage RL to find the best one and use it as training data to self-improve models. This is how reasoning models are trained and we will see how much better they are in math tasks.


## 3. Reflection
Let's now use **gpt-4.1** and give it rather difficult task.

System prompt:
```
# ROLE:
You are math professor.

# INSTRUCTIONS:
Do it step by step and explain your thinking at each step. Only then print the final answer.
```

User prompt (**wrong** answer):

``` Calculate 79234552 * 23456433 ```

Correct answer is 1,858,559,960,273,016

Continue conversation with reflection on the errors (still slightly **wrong**, but better answer):

```
Run series of self-tests to check the correctness of the calculation.
If the tests fail, analyze previous calculation steps to identify the issue.
Re-run calculation, do it correctly, and output final answer.
```


```
Run series of different self-tests to check the correctness of the calculation.
If the tests fail, analyze previous calculation steps to identify the issue.
Re-run calculation, do it correctly, and output final answer.
```

## 4. Reasoning (thinking) model
We will now use cheap **o4-mini** in *high* thinking mode. But first try more expensive non-thinking **gpt-4.1**.

User prompt:

``` Calculate 79234552 * 23456433 ```

Correct answer is 1,858,559,960,273,016

System prompt (**wrong** answer):
```
# ROLE:
You are math professor.

# INSTRUCTIONS:
Do it step by step and explain your thinking at each step. Only than print the final answer.
```

Switch to **o4-mini** with high thinking mode. Note it is not good idea to instruct it to think step by step, model does it already and this confuses it.

System prompt (**correct** answer):
```
# ROLE:
You are math professor.
```

## 5. Agent using tools
In Azure AI Foundry create agent using "just" **gpt-4o** model. We will try adding two tools:
- Code Interpreter (Python) - let model write and execute Python code to do the calculation
- Calculator API (math.js) [OpenAPI spec](../tools/mathjs.json) - let model use calculator via API to do the calculation

See? Correct, much more predictable answers, much faster and cheaper with agent deciding when to use which tool (if any).