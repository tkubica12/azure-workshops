# Story of analyzing data
1. Extracting textual data
2. Processing visual data
3. Using Code Interpreter tool for data analysis
4. Using Code Interpreter tool for data visualization
5. Using HTMX to generate interactive UI

# 1. Extracting textual data

System prompt:

```
# ROLE:
You are data analyst, writer and text editor.

# INSTRUCTIONS:
Process data as user requests, for example extract data from text, summarize it, analyze it, visualize it, write a report or article about it, etc.
Output data in format user requested, for example as text, table, chart, JSON, YAML, CSV, etc.
```

User Prompt:

```
Extract entities such as people, organizations, locations, dates, etc. from the following text and display them as valid JSON (no comments, no explanations, no additional text):

<document>

</document>
```

Insert content of [reasoning_best_practices.md](../inputs/reasoning_best_practices.md) into <document> tag.

See [example output](../outputs/analyze_entities.json)

User Prompt:

```
Now create new title and summary in Markdown. Be technical, it is for our technical wiki.
```

See [example output](../outputs/analyze_summary_business.md)

```
Now create new title and summary for our blog article. Be business oriented, engaging and easy to read.
```

See [example output](../outputs/analyze_summary_technical.md)

```
Now create new title and very short post for Facebook. You must be very engaging, use emojis and hashtags. Make sure post is short, viral and catchy.
```

See [example output](../outputs/analyze_summary_social.md)

---

User Prompt:

```
Here is table with animals and their features.

<table>

</table>

Always answer only based on data from the table, never add any additional information or context.

What animals are big yet run very fast?

```


User Prompt:

```
Are there any faster than those while being very small? Birds and sea animals do not count.
```