# Evidence and Sources

Use supporting Markdown to connect a course's important claims to trustworthy material. A source note gives the learner and future sessions a short, readable account of why a claim appears in the course.

## Source Note

Create `sources/{slug}.md` with these sections:

```md
# {Source title}

## Source
{URL, path, paper identifier, or repository reference.}

## What It Supports
{The claim, behavior, definition, or example supported by the source.}

## Teaching Use
{How the course turns the source into an explanation, example, exercise, or comparison.}

## Scope
{The setting, audience, version, or conditions covered by the source.}
```

## Source Roles

Use plain labels when a distinction matters:

- `source`: directly supported by the cited material;
- `context`: surrounding history, terminology, or related work;
- `explanation`: a course reconstruction that makes the material learnable;
- `transfer`: guidance applied to a learner's system or goal.

Record the label beside the relevant claim or section. Keep a claim's source, teaching use, and scope visible to the author and concise for the learner.

## Positive Scope Language

Use sentences such as:

- "This source supports the documented interface."
- "This section reconstructs the mechanism for learning."
- "This comparison applies to the settings described in the source."
- "This transfer is useful when the learner's system has the same condition."

## Source Selection

Prefer the strongest available source for the claim. Use local code for repository behavior, the target paper for paper claims, official documentation for interfaces, and experiments for observed outcomes. Record gaps as open source questions that guide the next research step.
