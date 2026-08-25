---
name: to-questionnaire
description: Turn a decision you cannot answer alone into a questionnaire for the person who can.
argument-hint: "Who will answer, and what do you need to learn or decide?"
disable-model-invocation: true
---

# To Questionnaire

Turn a knowledge gap the user cannot close alone into a Markdown questionnaire
for one informed person to complete asynchronously or during a meeting.

**Grill the send, not the subject.** Interview the user only about information
they can supply: who will receive the questionnaire and what must come back. The
document's questions then target the gap between what the recipient knows and
what the user needs.

The questionnaire is the only artifact this skill owns. Product specifications,
ADRs, issues, Wayfinder state, and `.codex/agents/` remain with their existing
workflows. Complete this interview directly without invoking another skill.

## 1. Identify the recipient

Ask for the recipient's role, relevant expertise, and relationship to the user
in one exchange. Use information already supplied in the arguments or
conversation instead of asking for it again.

Complete this step when the recipient and the knowledge they hold are clear
enough to set the questionnaire's context, vocabulary, and tone.

## 2. Define what must come back

Ask for the concrete facts, decisions, constraints, or judgments the user needs
from this person. Express the result as outcomes: what the user must be able to
decide or do after reading the answers.

Complete this step when every required outcome is named and no requested answer
depends on knowledge the recipient is unlikely to hold.

## 3. Write the questionnaire

Write `to-questionnaire-<slug>.md` in the current directory, using a short slug
derived from the topic. Order questions by decision value because an async
questionnaire may receive only one pass. Group them under `##` headings when
there are more than a handful.

Every question covers one idea and has an answer stub directly beneath it. Add
a one-line _Why this matters_ only when the question could be misread or invite
a superficial answer.

Complete this step when the file exists and every outcome from step 2 is covered
by a question. Report the path.

## Document structure

Use this template:

<questionnaire-template>

# <Questionnaire title>

**Purpose:** <why this questionnaire exists and the decision riding on it>

- **From:** <the user>
- **To:** <the recipient>
- **How your answers will be used:** <where the answers go>

## Context

<One paragraph that gives the recipient enough context to answer well.>

## How to answer

<Deadline and concrete effort guidance. State that partial answers, uncertainty,
and "I don't know" are useful.>

## <Theme heading>

### What load is the system expected to handle at launch?

_Why this matters: it determines whether capacity must be provisioned now or
can be deferred._

>

## Anything else?

<Anything important that the questionnaire did not ask?>

</questionnaire-template>
