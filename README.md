# 🌿 FocusForge

**Dump everything. Get one thing. Start a timer.**

FocusForge is a fully offline app for people whose brains freeze when they look at a long to-do list. You paste in your messy brain dump and get back **one** next action in big text, with a calm visual focus timer. The rest of the list stays hidden.

> Taskforge theme: *Work should fit people, not force people to fit the tool.*

---

## Project Story

Most productivity tools assume that if you can see all of your work, you can manage it. For many people with ADHD it works the other way around. Twenty tasks on one screen is twenty demands on your attention at once, and the result is often doing nothing at all.

We wanted a tool that adapts to how that brain works. Instead of asking you to sort, tag, prioritize and schedule (the exact executive-function work that's hard), FocusForge takes the raw mess and makes the decision for you. You see one task. You start. That's the whole product.

## Intended User

A **college student with ADHD**. Their week has assignments, emails to professors, bills, chores and errands all competing at once. They're capable and motivated, but when they open a long list they get stuck staring at it, reorganize it for the third time, and then close the laptop.

## The Barrier: Task Paralysis

Task paralysis is the freeze that happens when there are too many choices and none of them feels like an obvious first step. Common triggers:

- **Too many options.** Every visible task competes for attention.
- **Vague tasks.** "Work on the project" has no clear starting point.
- **Big tasks hiding small ones.** A huge essay makes the 2-minute "email the professor" invisible.
- **Choosing is itself a task.** Deciding what to do first uses up the energy needed to actually do it.

Traditional to-do apps make this worse: they show everything and leave the choosing to you.

## The Solution: FocusForge

1. **Brain Dump.** Paste anything: bullets, numbered lists, checkboxes, half-sentences.
2. **Forge My Next Step.** A local rule-based parser cleans each line and scores it:
   - Lines that **start with an action verb** get a boost ("email prof", "vacuum room"). Lines without one are never dropped; they just rank a little lower.
   - **Urgency words** (`today`, `ASAP`, `due`, `deadline`, `!`) push a task up.
   - **Quick-win verbs** (`email`, `call`, `pay`, `send`, `submit`) push a task up, since a small win builds momentum.
   - **Shorter tasks** score higher, because shorter usually means smaller.
   - **Vague, huge words** (`project`, `entire`, `everything`) push a task down.
3. **One task, in giant text,** with a short plain-English reason ("Picked because it's time-sensitive and it's a quick win").
4. **Focus Timer.** A calm circular countdown (5, 10, 15 or 25 minutes) built with plain HTML, CSS and JavaScript. Start, pause, reset.
5. **✅ Done / 🔁 Not this one.** "Done" shows the next task. "Not this one" moves the current task to the back of the queue, so you can skip it without guilt and without losing it.

### Run it

```bash
pip install streamlit
streamlit run app.py
```

The included `.streamlit/config.toml` turns off Streamlit's usage telemetry and binds the server to `localhost`, so nothing leaves your machine.

### Check the heuristic

```bash
python test_app.py   # prints "ok"
```

## Tools Used

- **Python 3** (standard library: `re`, `html`)
- **Streamlit** for the UI
- **Local heuristics:** hand-written keyword and verb scoring, no machine learning
- **Vanilla HTML/CSS/JS** for the timer (an SVG ring, no external libraries or CDNs)

## Limitations

- **Rule-based parser, not an LLM.** This was a deliberate choice: a brain dump can be very personal ("call therapist", "pay overdue rent"), and we wanted **100% offline privacy** with no API keys, no network calls and no data leaving the laptop. The trade-off is that the parser is only as smart as its word lists.
- **Fixed verb list.** Over 100 common school, chore and errand verbs are recognized. A task that starts with an unlisted verb is still kept, but it misses the "clear action" boost.
- **No real dates.** "Due Friday" isn't parsed as a date. Only urgency keywords count.
- **English only.**
- **No persistence.** Refreshing the page clears your list. This is on purpose for privacy, but it can be inconvenient.
- **The timer lives in the browser tab.** It resets if Streamlit reruns the page, for example when you change the timer length.

## What I Learned

- **Fewer choices is the feature.** The hardest design decision was what to *hide*. Showing the full ranked list "for transparency" felt helpful, but it brought the paralysis right back.
- **Explain the pick.** A short reason ("it's a quick win") makes people trust the choice instead of second-guessing it.
- **Skipping needs to feel safe.** "Not this one" sends a task to the back instead of deleting it. That was the difference between a tool that feels bossy and one that feels kind.
- **Simple heuristics go a long way.** Verb + urgency + size got the "obvious" pick right on most of the brain dumps we tried, with no model.
- **"Offline" takes checking.** Streamlit sends usage stats by default. Being truly local meant turning that off explicitly.

## AI Assistance Disclosure

This project was built with help from **Claude (Anthropic)**, an AI coding assistant. It helped draft `app.py` (the parsing heuristic, the Streamlit layout and the HTML/CSS/JS timer), the `test_app.py` self-check, and this README. I chose the concept, target user, constraints and design direction, and I reviewed, ran and tested the code. The app itself uses **no AI at runtime**: every decision it makes comes from transparent, local rules.
