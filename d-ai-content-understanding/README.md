# Foundry Content Understanding
Video example

Go throw commands in `configure.http`. Save results into `results.json`.

You can than ask GitHub Copilot to give you nice report in Markdown based on this.

```markdown
Write and run Python script that will implement the following.

Take outputs in `results.json` from video analysis tools and create nice structured Markdown from it to visualize those results. You MUST include every item in JSON with its original name and value without any interpretation on your side. Your task is to visualize this JSON in some structured way using markdown constructs including links and tables, but do to summarize or interpret anything. If field do not have any value, include it anyway and say so (NA or null).
- There is "markdown" field - this is inner markdown that MUST be covered in 4-backtick (````markdown)
- Segments should not be markdown chapter, just simply do bold segment <number> and provide list of key/value pairs there
- Scenes should be chapter, simply add scenes from segments as single "scenes table" that will be part of segment
- transcriptPhrases should be visualized as markdown of table
- KeyFrameTimesMs and cameraShotTimesMs should be list
- Do not make `Markdown` and `Fields` section a chapter, simply continue as part of `Content` chapter
- Output to results.md
```