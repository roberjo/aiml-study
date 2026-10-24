---
name: draft-post
description: Draft the LinkedIn post for a week of the AI/ML study series from that week's notes, commits, and results. Use when the owner asks to draft, write, or revise a LinkedIn post for a week (e.g. "/draft-post w04").
---

Draft one LinkedIn post for the given week (argument like `w04`; default: the most recently modified `weeks/` folder).

1. **Gather the real material.**
   - `posts/README.md` (voice and format rules; follow them exactly) and the week's row in `posts/series-plan.md`.
   - The week's `weeks/wNN-*/README.md`, especially *Thoughts, Trade-offs, Mistakes, Lessons learned, Findings*.
   - `git log` for that week's commits, and the notebooks/write-up for actual metrics and results.
   - Earlier posts in `posts/` so this one doesn't repeat a hook or lesson.
2. **Never invent experiences.** Every mistake, number, and lesson must come from the notes, code, or results. If the README's capture sections are empty or too thin for a post, stop and ask the owner 3–4 pointed questions (What surprised you? What did you get wrong first? What did you trade away?) instead of drafting.
3. **Pick the story.** Use the planned angle only if the material supports it; otherwise choose the strongest real trade-off or mistake from the week and say why you switched.
4. **Write `posts/wNN-<slug>.md`** using the template in `posts/README.md`:
   - Give **two alternative hooks** above the body (labelled Hook A / Hook B) so the owner can pick.
   - 1,200–2,000 characters for the body; report the character count.
   - Project weeks (W9, W15, W19, W23): also outline the carousel slide by slide.
   - Fill in the First comment (repo link `https://github.com/roberjo/aiml-study` + path to the week) and the Visual (point at a specific chart or file that exists).
5. **Check before finishing.** No employer names, internal systems, or work data; no hype words from the banned list; no links in the body; claims match the repo. List anything the owner should verify or personalize.
