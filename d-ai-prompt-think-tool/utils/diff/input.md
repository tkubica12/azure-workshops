---
title: Azure OpenAI Service | Prompt engineering techniques
titleSuffix: Azure OpenAI
description: Learn how to use prompt engineering to optimize your work with Azure OpenAI Service.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 03/26/2025
ms.custom: references_regions, build-2023, build-2023-dataai
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Prompt engineering techniques

GPT-3, GPT-3.5, GPT-4, and GPT-4o models from OpenAI are prompt-based. With prompt-based models, the user interacts with the model by entering a text prompt, to which the model responds with a text completion. This completion is the model’s continuation of the input text. These techniques are not recommended for o-series models.

While these models are extremely powerful, their behavior is also very sensitive to the prompt. This makes prompt construction an important skill to develop.

Prompt construction can be difficult. In practice, the prompt acts to configure the model weights to complete the desired task, but it's more of an art than a science, often requiring experience and intuition to craft a successful prompt. The goal of this article is to help get you started with this learning process. It attempts to capture general concepts and patterns that apply to all GPT models. However it's important to understand that each model behaves differently, so the learnings may not apply equally to all models.

## Basics

This section covers the basic concepts and elements of GPT prompts.

Text prompts are how users interact with GPT models. As with all generative language models, GPT models attempt to produce the next series of words that are most likely to follow from the previous text. It's as if we're saying *What is the first thing that comes to your mind when I say `<prompt>`?* The examples below demonstrate this behavior. Given the first words of famous content, the model is able to accurately continue the text.

| Prompt                             |Completion |
|------------------------------------|-----------|
| Four score and seven years ago our | fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. […]|
| "Call me Ishmael."                 | "Some years ago—never mind how long precisely—having little o no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world." […]|

As you develop more complex prompts, it's helpful to keep this fundamental behavior in mind. Regardless of the prompt that is provided, the model is simply responding with what it determines is most likely (given its training data and training targets). If you ask a question in your prompt, the model isn't following a separate “Q&A” code path, but rather it appears to answer the question because an answer is the most likely sort of response for the given question as input.

### Prompt components

When using the Completion API while there's no differentiation between different parts of the prompt, it can still be useful for learning and discussion to identify underlying prompt components. With the [Chat Completion API](../how-to/chatgpt.md) there are distinct sections of the prompt that are sent to the API in the form of an array of dictionaries with associated roles: system, user, and assistant. This guidance focuses more generally on how to think about prompt construction rather than providing prescriptive guidance that is specific to one API over another.

It's also important to understand that while there could be other valid ways to dissect prompts, the goal of this breakdown is to provide a relatively simple way to think about prompt construction. With the Completion API, all the components are optional, but at least one must be present and most prompts include more than one component. There can be some grey area between components as well. The order presented below roughly corresponds to how commonly each component is used, from most to least.

#### Instructions

Instructions are likely the most commonly used prompt component. Instructions are simply that: instructions to the model on what to do. While simple in concept, they can be complex in practice. The following table illustrates this by showing both simple and more complex instructions, in two different forms.

|Instruction Type                |  Prompt      | Completion    |
|--------------------------------|---------------|--------------|
Simple instructions | Write an introduction for a weekly newsletter. | Welcome to our weekly newsletter. This week we have a special focus on productivity. We'll be sharing tips and tricks on how to be productive in all areas of your life. We hope you enjoy and please share with your friends! |
| Complex instructions | Write an introduction for a weekly newsletter to my company named Contoso. It should mention the great all hands meeting we had last week and thank the team for all their hard work over the tough past few months. | Welcome to Contoso's weekly newsletter! We had a great all hands meeting last week and I want to thank the team for all their hard work over the tough past few months. We're looking forward to a bright future and I'm confident that with our team's dedication and commitment, we will achieve great things. Thank you for being a part of our team and I look forward to working with you all in the coming weeks and months. Sincerely, [Your name]. |
| Complex Instructions | Write an introduction for a weekly newsletter, including the following: <br>- My company is named contoso <br>- An exuberant greeting <br>- Thanking the team for their hard work over a couple tough months <br>- Positive outlook for the coming quarter<br>- Signed by the SLT |	Hello Contoso team! I wanted to take a moment to thank you for all your hard work over the past few months. It's been a tough couple of months, but you've all pulled together and done an amazing job. I'm really proud of you all. Looking ahead to the next quarter, I'm feeling really positive. I think we're going to achieve some great things. Thanks again, The Senior Leadership Team.|

### Primary Content

Primary content refers to some sort of text that is being processed or transformed by the model. Primary content is typically used in conjunction with instructions. A simple example would be language translation. In the example below, the English text would be considered the primary content while "Translate to French:" is an instruction.

| Prompt | Completion|
|--------|-----------|
| Can you please tell me how to get to the museum?<br>Translate to French: |`Pouvez-vous s'il vous plaît me dire comment aller au musée?` |

Primary content can also be much longer. In the following example, the primary content is the introduction section from the [Wikipedia entry on time complexity](https://en.wikipedia.org/wiki/Time_complexity), which is almost 300 words long. This content has been abbreviated in our table for ease of display.

| Prompt | Completion|
|--------|-----------|
| In computer science, the time complexity is the computational complexity that describes the amount of computer time it takes to run an algorithm. Time complexity is commonly estimated by [...]<br>Summarize the previous text in a few sentences:| Time complexity is a measure of how long an algorithm takes to run. It is typically expressed as a function of the size of the input. The most common measure is worst-case time complexity, which is the maximum amount of time required for inputs of a given size.|
| In computer science, the time complexity is the computational complexity that describes the amount of computer time it takes to run an algorithm. Time complexity is commonly estimated by [...]<br>`TL;DR` (Too long didn't read) | The time complexity of an algorithm is the amount of time it takes to run an algorithm. Time complexity is commonly estimated by counting the number of elementary operations performed by the algorithm, supposing that each elementary operation takes a fixed amount of time to perform. The time complexity is generally expressed as a function of the size of the input.|

GPT models can also handle primary content that is structured. In the example below, a TSV about beers in Belgium (abbreviated for display in this article) is passed to the model as part of the prompt. It is capable of properly interpreting the content and answering questions about the data.

| Prompt | Completion |
|--------|------------|
| `Belgian Beer Brands` <br>`Beer name	Beer style	color	ABV	Brewery`<br>`"Chimay Gold: ""Doree"""	trappist pale ale	gold	4.80%	Chimay Brewery (official trappist)`<br>`"Chimay Blue: ""Grande Reserve"""	trappist dark ale	dark	9.00%`<br>[…]<br>Referencing the table above, how many beers are less than 6% ABV? |	There are 10 beers in the table that are less than 6% ABV. |

### Examples

Successful prompts often rely on the practice of “one-shot” or “few-shot” learning. This refers to the inclusion of one or more examples of the desired behavior of the model, typically by including input and output pairs. This is not learning in the sense that the model is permanently changed, but rather that the examples better condition the model to respond as desired for only the current inference. The use of prompts with no examples is sometimes referred to as “zero-shot” learning. Note that with the Chat Completion API few-shot learning examples are typically added to the messages array in the form of example user/assistant interactions after the initial system message.

| Learning Type|  Prompt| Completion|
|------------------------------------- |-------|-----|
| Zero-shot | Headline: Coach confident injury won't derail Warriors<br>Topic:| The coach is confident that the injury won't derail the Warriors' season. The team is still focused on their goals and that they will continue to work hard to achieve them.|
| Few-shot | Headline: Twins' Correa to use opt-out, test free agency<br>Topic: Baseball<br>Headline: Qatar World Cup to have zones for sobering up<br>Topic: Soccer<br>Headline: Yates: Fantasy football intel for Week 6<br>Topic: Football<br>Headline: Coach confident injury won't derail Warriors<br>Topic: | Basketball |

The example above illustrates the utility of few-shot learning. Without the examples, the model seems to be guessing at the desired behavior, while the examples cleanly show the model how to operate. This also demonstrates the power of the model, it can infer the category of label that is wanted, even without a "basketball" label in the examples.

### Cue

Cues act as the "jumpstart" for the output of the model, helping to direct the model to the desired output. It is often a prefix that the model can build onto. In the example below, we show the cue directing the story to include key elements. Cues are often used along with instructions, but not always. In the examples below, the model is being used to summarize a long announcement email. A cue is used in one case to help focus the output of the model and to suggest a specific output format (bullet points) in the other.  

In the context of the Chat Completion API instructions take the form of the system message, and few-shot examples are indicated by providing a series of example user/assistant interactions to help prime the model.

| Number of Cues|Prompt | Completion|
|----------|-------|-----------|
| 0 | Performance reviews are a core component of our Performance & Development approach at Contoso. […] <br> Summarize the above email message: | The purpose of this email is to inform employees of recent changes to the performance review experience, which is part of Contoso's Performance & Development approach. The changes include an improved structure, upgraded in-tool user experience, and focused prompts. Additionally, there is now an optional Conversation Starters section for employees to flag topics they'd like to discuss with their managers. |
| 1 | Performance reviews are a core component of our Performance & Development approach at Contoso. […] <br> Summarize the above email message:<br> The key takeaway of the message is | that Contoso is improving the performance review experience by making it more focused on core priorities, expectations, and impact. Additionally, they are upgrading the in-tool user experience with tips, resources, and guidance. Finally, they are adding guidance on how to activate company-wide core priorities. | 
|2 | Performance reviews are a core component of our Performance & Development approach at Contoso. […] <br> Summarize the above email message: <br>Key Points:<br>• | Contoso is introducing changes to the performance review experience, based on feedback from employees.<br>• The changes include a new focus on core priorities, expectations, and impact; an upgraded user experience; and new guidance on company-wide core priorities.<br>• Performance reviews are a time to reflect on past performance and learning as well as to plan for future priorities and growth opportunities.<br>• Employees and managers should write comments in advance of the performance review meeting.<br>• There should be at least two performance reviews per year.<br>• The time investment for each review should remain about the same. |

### Supporting content

Supporting content is information that the model can utilize to influence the output in some way. It differs from primary content in that it is not the main target of task, but it is typically used along with primary content. Common examples include contextual information such as the current date, the name of the user, user preferences, and so on. The example below uses supporting content to help organize a set of planned workshops for the user. Without the supporting (important topics) the model simply lists off the workshops (truncated for display), when informed of my important topics, the model is able to accurately group the meetings.

| Supporting Content| Prompt | Completion|
|--------|-------------|-----------------|
| Without | Workshop list:<br>Title	Description<br> Planning Workshop Kickoff Please join us to kick off our workshop! Hear from our leaders about cross group priorities and learnings for the year ahead. The invitation to this event has already been sent to everyone in […]<br>Summarize the workshops above, grouped by topic: | Workshop list: <br> Planning Workshop Kickoff <br> -Planning Workshop Wrap-up<br>- Core MeetUp<br>- Customer Driven Perspectives<br>-Impact and Key Focus Areas<br>-Best practices<br>-Accelerating app adoption […] |
| With | Workshop list: <br>Title	Description<br>Planning Workshop Kickoff	Please join us to kick off our workshop! Hear from our leaders about cross group priorities and learnings for the year ahead. The invitation to this event has already been sent to everyone in […] <br>My Important Topics: prompt engineering, search, GPT models<br>Summarize the workshops above, grouped by my important topics:| 1. Prompt Engineering: <br>- New prompt engineering tips<br>- The art of prompt engineering<br>2. Search:<br>-Intro to vector search with embedding<br>3. GPT Models:<br>- Intro to GPT-4<br>- GPT-35-Turbo in-depth.|

## Scenario-specific guidance

While the principles of prompt engineering can be generalized across many different model types, certain models expect a specialized prompt structure. For Azure OpenAI GPT models, there are currently two distinct APIs where prompt engineering comes into play:

- Chat Completion API.
- Completion API.

Each API requires input data to be formatted differently, which in turn impacts overall prompt design. The **Chat Completion API** supports the GPT-35-Turbo and GPT-4 models. These models are designed to take input formatted in a [specific chat-like transcript](../how-to/chatgpt.md) stored inside an array of dictionaries.

The **Completion API** supports the older GPT-3 models and has much more flexible input requirements in that it takes a string of text with no specific format rules.

The techniques in this section will teach you strategies for increasing the accuracy and grounding of responses you generate with a Large Language Model (LLM). It is, however, important to remember that even when using prompt engineering effectively you still need to validate the responses the models generate. Just because a carefully crafted prompt worked well for a particular scenario doesn't necessarily mean it will generalize more broadly to certain use cases. Understanding the [limitations of LLMs](/legal/cognitive-services/openai/transparency-note?context=/azure/ai-services/openai/context/context#limitations), is just as important as understanding how to leverage their strengths.

#### [Chat completion APIs](#tab/chat)

[!INCLUDE [Prompt Chat Completion](../includes/prompt-chat-completion.md)]

#### [Completion APIs](#tab/completion)

[!INCLUDE [Prompt Completion](../includes/prompt-completion.md)]

---

## Best practices

- **Be Specific**. Leave as little to interpretation as possible. Restrict the operational space.
- **Be Descriptive**. Use analogies.
- **Double Down**. Sometimes you might need to repeat yourself to the model. Give instructions before and after your primary content, use an instruction and a cue, etc. 
- **Order Matters**. The order in which you present information to the model might impact the output. Whether you put instructions before your content (“summarize the following…”) or after (“summarize the above…”) can make a difference in output. Even the order of few-shot examples can matter. This is referred to as recency bias.
- **Give the model an “out”**. It can sometimes be helpful to give the model an alternative path if it is unable to complete the assigned task. For example, when asking a question over a piece of text you might include something like "respond with "not found" if the answer is not present." This can help the model avoid generating false responses.

## Space efficiency

While the input size increases with each new generation of GPT models, there will continue to be scenarios that provide more data than the model can handle. GPT models break words into "tokens." While common multi-syllable words are often a single token, less common words are broken in syllables. Tokens can sometimes be counter-intuitive, as shown by the example below which demonstrates token boundaries for different date formats. In this case, spelling out the entire month is more space efficient than a fully numeric date. The current range of token support goes from 2,000 tokens with earlier GPT-3 models to up to 32,768 tokens with the 32k version of the latest GPT-4 model.

:::image type="content" source="../media/prompt-engineering/space-efficiency.png" alt-text="Screenshot of a string of text with highlighted colors delineating token boundaries." lightbox="../media/prompt-engineering/space-efficiency.png":::

Given this limited space, it is important to use it as efficiently as possible.
- Tables – As shown in the examples in the previous section, GPT models can understand tabular formatted data quite easily. This can be a space efficient way to include data, rather than preceding every field with name (such as with JSON). 
- White Space – Consecutive whitespaces are treated as separate tokens which can be an easy way to waste space. Spaces preceding a word, on the other hand, are typically treated as part of the same token as the word. Carefully watch your usage of whitespace and don’t use punctuation when a space alone will do. 

## Related content 

* [Learn more about Azure OpenAI](../overview.md).
* Get started with the ChatGPT model with [the ChatGPT quickstart](../chatgpt-quickstart.md).
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure/openai-samples)

---
title: Planning red teaming for large language models (LLMs) and their applications 
titleSuffix: Azure OpenAI Service
description: Learn about how red teaming and adversarial testing are an essential practice in the responsible development of systems and features using large language models (LLMs)
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 03/27/2025
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Planning red teaming for large language models (LLMs) and their applications

This guide offers some potential strategies for planning how to set up and manage red teaming for responsible AI (RAI) risks throughout the large language model (LLM) product life cycle.

## What is red teaming?

The term *red teaming* has historically described systematic adversarial attacks for testing security vulnerabilities. With the rise of LLMs, the term has extended beyond traditional cybersecurity and evolved in common usage to describe many kinds of probing, testing, and attacking of AI systems. With LLMs, both benign and adversarial usage can produce potentially harmful outputs, which can take many forms, including harmful content such as hate speech, incitement or glorification of violence, or sexual content.

## Why is RAI red teaming an important practice?

Red teaming is a best practice in the responsible development of systems and features using LLMs. While not a replacement for systematic measurement and mitigation work, red teamers help to uncover and identify harms and, in turn, enable measurement strategies to validate the effectiveness of mitigations.

While Microsoft has conducted red teaming exercises and implemented safety systems (including [content filters](./content-filter.md) and other [mitigation strategies](./prompt-engineering.md)) for its Azure OpenAI Service models (see this [Overview of responsible AI practices](/legal/cognitive-services/openai/overview)), the context of each LLM application will be unique and you also should conduct red teaming to:

- Test the LLM base model and determine whether there are gaps in the existing safety systems, given the context of your application.

- Identify and mitigate shortcomings in the existing default filters or mitigation strategies.

- Provide feedback on failures in order to make improvements.

- Note that red teaming is not a replacement for systematic measurement. A best practice is to complete an initial round of manual red teaming before conducting systematic measurements and implementing mitigations. As highlighted above, the goal of RAI red teaming is to identify harms, understand the risk surface, and develop the list of harms that can inform what needs to be measured and mitigated.

Here is how you can get started and plan your process of red teaming LLMs. Advance planning is critical to a productive red teaming exercise.

## Before testing

### Plan: Who will do the testing

**Assemble a diverse group of red teamers**

Determine the ideal composition of red teamers in terms of people’s experience, demographics, and expertise across disciplines (for example, experts in AI, social sciences, security) for your product’s domain. For example, if you’re designing a chatbot to help health care providers, medical experts can help identify risks in that domain.

**Recruit red teamers with both benign and adversarial mindsets**

Having red teamers with an adversarial mindset and security-testing experience is essential for understanding security risks, but red teamers who are ordinary users of your application system and haven’t been involved in its development can bring valuable perspectives on harms that regular users might encounter.

**Assign red teamers to harms and/or product features**

- Assign RAI red teamers with specific expertise to probe for specific types of harms (for example, security subject matter experts can probe for jailbreaks, meta prompt extraction, and content related to cyberattacks).

- For multiple rounds of testing, decide whether to switch red teamer assignments in each round to get diverse perspectives on each harm and maintain creativity. If switching assignments, allow time for red teamers to get up to speed on the instructions for their newly assigned harm.

- In later stages, when the application and its UI are developed, you might want to assign red teamers to specific parts of the application (i.e., features) to ensure coverage of the entire application.

- Consider how much time and effort each red teamer should dedicate (for example, those testing for benign scenarios might need less time than those testing for adversarial scenarios).

It can be helpful to provide red teamers with:
 - Clear instructions that could include:
     - An introduction describing the purpose and goal of the given round of red teaming; the product and features that will be tested and how to access them; what kinds of issues to test for; red teamers’ focus areas, if the testing is more targeted; how much time and effort each red teamer should spend on testing; how to record results; and who to contact with questions.  
 - A file or location for recording their examples and findings, including information such as:
     - The date an example was surfaced; a unique identifier for the input/output pair if available, for reproducibility purposes; the input prompt; a description or screenshot of the output.

### Plan: What to test

Because an application is developed using a base model, you might need to test at several different layers:

- The LLM base model with its safety system in place to identify any gaps that may need to be addressed in the context of your application system. (Testing is usually done through an API endpoint.)

- Your application. (Testing is best done through a UI.)

- Both the LLM base model and your application, before and after mitigations are in place.

The following recommendations help you choose what to test at various points during red teaming:

- You can begin by testing the base model to understand the risk surface, identify harms, and guide the development of RAI mitigations for your product.

- Test versions of your product iteratively with and without RAI mitigations in place to assess the effectiveness of RAI mitigations. (Note, manual red teaming might not be sufficient assessment—use systematic measurements as well, but only after completing an initial round of manual red teaming.)  

- Conduct testing of application(s) on the production UI as much as possible because this most closely resembles real-world usage.  

When reporting results, make clear which endpoints were used for testing. When testing was done in an endpoint other than product, consider testing again on the production endpoint or UI in future rounds.

### Plan: How to test

**Conduct open-ended testing to uncover a wide range of harms.**

The benefit of RAI red teamers exploring and documenting any problematic content (rather than asking them to find examples of specific harms) enables them to creatively explore a wide range of issues, uncovering blind spots in your understanding of the risk surface.

**Create a list of harms from the open-ended testing.**

- Consider creating a list of harms, with definitions and examples of the harms.  
- Provide this list as a guideline to red teamers in later rounds of testing.

**Conduct guided red teaming and iterate: Continue probing for harms in the list; identify new harms that surface.**

Use a list of harms if available and continue testing for known harms and the effectiveness of their mitigations. In the process, you will likely identify new harms. Integrate these into the list and be open to shifting measurement and mitigation priorities to address the newly identified harms.

Plan which harms to prioritize for iterative testing. Several factors can inform your prioritization, including, but not limited to, the severity of the harms and the context in which they are more likely to surface.

### Plan: How to record data

**Decide what data you need to collect and what data is optional.**

- Decide what data the red teamers will need to record (for example, the input they used; the output of the system; a unique ID, if available, to reproduce the example in the future; and other notes.)

- Be strategic with what data you are collecting to avoid overwhelming red teamers, while not missing out on critical information.

**Create a structure for data collection**

A shared Excel spreadsheet is often the simplest method for collecting red teaming data. A benefit of this shared file is that red teamers can review each other’s examples to gain creative ideas for their own testing and avoid duplication of data.

## During testing

**Plan to be on active standby while red teaming is ongoing**

- Be prepared to assist red teamers with instructions and access issues.
- Monitor progress on the spreadsheet and send timely reminders to red teamers.

## After each round of testing

**Report data**

Share a short report on a regular interval with key stakeholders that:

1. Lists the top identified issues.

2. Provides a link to the raw data.

3. Previews the testing plan for the upcoming rounds.

4. Acknowledges red teamers.

5. Provides any other relevant information.

**Differentiate between identification and measurement**

In the report, be sure to clarify that the role of RAI red teaming is to expose and raise understanding of risk surface and is not a replacement for systematic measurement and rigorous mitigation work. It is important that people do not interpret specific examples as a metric for the pervasiveness of that harm.

Additionally, if the report contains problematic content and examples, consider including a content warning.

The guidance in this document is not intended to be, and should not be construed as providing, legal advice. The jurisdiction in which you're operating may have various regulatory or legal requirements that apply to your AI system. Be aware that not all of these recommendations are appropriate for every scenario and, conversely, these recommendations may be insufficient for some scenarios.