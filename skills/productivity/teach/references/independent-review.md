# Independent Review

Run an independent review when the user asks for review or when a multi-page or technical course carries a meaningful risk of drift. The reviewer receives raw course artifacts and a neutral task description.

## Review Prompt

```text
Read the supplied HTML and supporting Markdown as an independent course reviewer.
Report:

1. the course main line in three plain sentences;
2. the reader's likely starting point and first point of confusion;
3. the source support and scope for important claims;
4. terminology or structure drift across pages;
5. concrete repairs that improve learning or transfer.

Separate observations from teaching explanations and transfer guidance.
Use positive scope language. Return concise findings in Markdown.
```

## Review Result

Store an optional `review.md` with:

```md
# Course Review

## Main Line

## Reader Understanding

## Source Scope

## Structure and Terminology

## Repairs
```

Keep review findings as supporting material. The course pages remain written for the learner.
