# Learning State

Read this file only when the Course Contract's `learning-state` field is true. It defines the persistent workspace a returning learner's course maintains across sessions: `MISSION.md`, `RESOURCES.md`, `GLOSSARY.md`, and `learning-records/`.

## Mission

`MISSION.md` records the learner's purpose and drives source, example, exercise, and module choices. Keep one concise mission per workspace; update it when the learner's goal changes.

```md
# Mission: {Topic}

## Why
{The concrete change this learning enables in the learner's work or life.}

## Success Looks Like
- {An observable capability}
- {Another observable capability}

## Constraints
- {Time, experience, tools, or preferences}

## Current Scope
- {The subject covered by this workspace}
- {The adjacent subject reserved for later}
```

## Resources

`RESOURCES.md` is the curated source list for the course. Prefer primary sources, official documentation, trusted experts, peer-reviewed work, and high-signal communities. Annotate every source with its contribution and use case, and record community preferences for future sessions.

```md
# {Topic} Resources

## Knowledge

- [Source title](https://example.com)
  Covers: {the concepts, evidence, or procedures it supports}
  Use when: {the course situation that calls for it}

## Wisdom

- [Community or local resource](https://example.com)
  Offers: {the practical perspective it contributes}
  Use when: {the situation that calls for it}

## Source Gaps

- {A mission-relevant topic that needs a trusted source}
```

## Glossary

`GLOSSARY.md` is the course's stable vocabulary. Add a term after the learner can use it correctly in an explanation or exercise.

```md
# {Topic} Glossary

{One or two sentences describing the vocabulary.}

## Terms

**Term**:
One or two sentences defining what the term is.
Use: {the preferred context or phrase}
```

Apply these rules:

- choose one preferred term when several aliases exist;
- use glossary terms inside later definitions;
- group terms when useful clusters appear;
- record a local meaning when a term has several common meanings;
- revise definitions as the learner's understanding becomes more precise.

## Learning Records

Learning records preserve demonstrated understanding, useful prior knowledge, corrected misconceptions, and changes to the learner's goal. Store them in `learning-records/` as `0001-slug.md`, `0002-slug.md`, and so on.

```md
# {Short title}

{What the learner established and how it changes the next teaching step.}
```

Add `Evidence` when a question, exercise, or explanation demonstrates the understanding. Add `Implications` when the record changes the course path. Mark an older record as superseded when later understanding replaces it. Create a record when the learner demonstrates a non-trivial capability, shares relevant prior knowledge, corrects a misconception, or changes the mission.
