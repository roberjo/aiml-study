# LinkedIn series: building an AI/ML program in public

One post per assignment (24 posts, kickoff + W1–W23). Audience: **tech professionals**,
meaning engineers, architects and engineering leaders who know software but are weighing how deep to go on ML.
They want the **thinking**: trade-offs, mistakes, lessons. Not tutorials, not hype.

- **Series plan:** [series-plan.md](series-plan.md), with the angle and planned format for every week
- **Drafting:** run `/draft-post wNN` in Claude Code. It reads the week's README, commits and code, and drafts
  `posts/wNN-slug.md` using the rules below.

## The pipeline: capture → draft → post

1. **Capture (during the week).** The week's `README.md` has four headings that feed the post:
   *Thoughts · Trade-offs · Mistakes · Lessons learned*. Jot raw notes there as they happen; a
   mistake written down on Tuesday is worth ten reconstructed on Sunday.
2. **Draft (Sunday).** `/draft-post wNN` turns those notes and the actual results into a draft.
   It never invents an experience. If the notes are thin, it asks.
3. **Edit (you).** Rewrite at least the hook and closing line in your own words.
4. **Post (Tue–Thu morning).** Link to the repo goes in the **first comment**, not the body.
5. **Log it.** Fill in the post's front matter (`posted:` date and URL) and commit.

## Voice

- First person, specific, plain. Write like explaining to a sharp colleague over coffee.
- **Numbers over adjectives.** "PR-AUC went from 0.71 to 0.84" beats "huge improvement".
- **Show the trade-off, not just the choice.** What you gave up is the interesting part.
- **Admit the mistake fully.** What you did, why it seemed right, what it cost, what you do now.
- Opinions are fine; label them as yours. Don't pretend to certainty you don't have.
- No hype words: *game-changer, revolutionary, unlock, dive in, delve, leverage, in today's fast-paced world*.
- No emoji bullets, and go easy on em dashes. Both read as AI-written to this audience.
- Never mention employer names, internal systems, or anything from work. Public data only, same as the repo.

## Format rules

| Element | Rule |
|---|---|
| Hook | First 2 lines (~200 chars) must earn the "…see more" click. A surprising number, a mistake, or a contrarian claim |
| Length | 1,200–2,000 characters for text posts |
| Structure | One idea per short paragraph; blank lines between; arrows (→) or numbers for lists |
| Visual | Attach one when possible: a chart from the notebook, a diagram, or a screenshot of the app |
| Project weeks | **Carousel** (PDF, 6–10 slides): problem → data → approach → result → what failed → lesson |
| Close | One genuine question to the audience. Never "Thoughts?" alone |
| Links | None in the body. Repo or write-up link goes in the first comment |
| Hashtags | 3–5 at the end. Rotate from: #MachineLearning #AI #GenerativeAI #DataScience #MLOps #LearningInPublic #SoftwareEngineering #AIEngineering |

## Post file template

```markdown
---
week: W04
title: Linear regression, three ways
format: text | carousel | image
status: draft | ready | posted
posted:            # YYYY-MM-DD
url:               # LinkedIn post URL
---

<post body>

---
**First comment:** <repo or write-up link + one line of context>
**Visual:** <what to attach>
```
