"""FocusForge: paste a messy brain dump, get ONE next action and a timer. 100% offline."""
import html
import re

import streamlit as st

ACTION_VERBS = {
    # admin / school
    "apply", "ask", "attend", "book", "call", "cancel", "check", "confirm", "contact", "draft",
    "edit", "email", "file", "fill", "finish", "find", "follow", "join", "learn", "list", "log",
    "meet", "memorize", "message", "outline", "pay", "plan", "practice", "prepare", "print",
    "proofread", "read", "register", "remind", "renew", "reply", "request", "research", "respond",
    "revise", "review", "rsvp", "schedule", "send", "sign", "start", "study", "submit", "text",
    "update", "upload", "watch", "write", "zoom",
    # chores / home
    "bake", "clean", "clear", "cook", "declutter", "dishes", "dust", "empty", "feed", "fold",
    "hang", "iron", "laundry", "make", "mop", "organize", "pack", "put", "recycle", "scrub",
    "shower", "sort", "sweep", "tidy", "trash", "unpack", "vacuum", "walk", "wash", "water", "wipe",
    # errands / life
    "backup", "borrow", "buy", "charge", "collect", "deposit", "do", "download", "drop", "fix",
    "get", "go", "grab", "install", "mail", "move", "order", "pick", "refill", "repair", "replace",
    "return", "sell", "ship", "shop", "take", "transfer", "try", "visit", "withdraw",
}
URGENT_WORDS = {"urgent", "asap", "today", "tonight", "now", "due", "deadline", "tomorrow", "overdue", "exam"}
QUICK_WORDS = {"call", "email", "text", "reply", "pay", "send", "book", "print", "submit",
               "sign", "message", "renew", "cancel", "order", "quick", "charge", "water", "feed"}
VAGUE_WORDS = {"project", "everything", "life", "figure", "entire", "whole", "all", "someday", "eventually"}
FILLER = re.compile(r"^(i\s+)?(need|have|got|want)\s+to\s+|^(must|should|remember\s+to|todo:?)\s+", re.I)
BULLET = re.compile(r"^(\s*([-*•>]|\d+[.)]|\[\s?[xX ]?\s?\]))+\s*")


def clean(line):
    return FILLER.sub("", BULLET.sub("", line).strip()).strip()


def score(task):
    """Return (score, reasons). A leading verb is a bonus, never a requirement."""
    words = re.findall(r"[a-z']+", task.lower())
    s, why = 0.0, []
    if words and words[0] in ACTION_VERBS:
        s += 3
        why.append("it starts with a clear action")
    if URGENT_WORDS & set(words) or "!" in task:
        s += 4
        why.append("it's time-sensitive")
    if QUICK_WORDS & set(words):
        s += 2
        why.append("it's a quick win")
    s += max(0, 8 - len(words)) * 0.5  # shorter = smaller = easier to start
    if VAGUE_WORDS & set(words):
        s -= 3
    return s, why or ["it's on your list and it's a fine place to start"]


def rank(dump):
    """All tasks best-first; ties keep the order you typed them. Nothing is dropped."""
    tasks = [t for t in (clean(l) for l in dump.splitlines()) if t]
    return [(t, score(t)[1]) for t in sorted(tasks, key=lambda t: -score(t)[0])]


TIMER_HTML = """
<div id="w" style="font-family:system-ui,sans-serif;text-align:center;color:#3b4a5a">
  <svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="Focus timer">
    <circle cx="110" cy="110" r="96" stroke="#e3ebf3" stroke-width="14" fill="none"/>
    <circle id="ring" cx="110" cy="110" r="96" stroke="#7fb3a3" stroke-width="14" fill="none"
      stroke-linecap="round" transform="rotate(-90 110 110)"
      stroke-dasharray="603.2" stroke-dashoffset="0" style="transition:stroke-dashoffset 1s linear"/>
    <text id="t" x="110" y="122" text-anchor="middle" font-size="40" fill="#3b4a5a">__MM__:00</text>
  </svg>
  <div>
    <button id="go" style="__BTN__">Start</button>
    <button id="rs" style="__BTN__;background:#eef2f6;color:#3b4a5a">Reset</button>
  </div>
  <p id="msg" style="margin-top:10px;font-size:15px" aria-live="polite"></p>
</div>
<script>
const total = __MM__ * 60, C = 603.2;
let left = total, id = null;
const t = document.getElementById('t'), ring = document.getElementById('ring'),
      go = document.getElementById('go'), msg = document.getElementById('msg');
function draw() {
  t.textContent = String(Math.floor(left / 60)).padStart(2, '0') + ':' + String(left % 60).padStart(2, '0');
  ring.style.strokeDashoffset = C * (1 - left / total);
}
go.onclick = () => {
  if (id) { clearInterval(id); id = null; go.textContent = 'Resume'; return; }
  go.textContent = 'Pause'; msg.textContent = 'Just this one thing. You got it.';
  id = setInterval(() => {
    left--; draw();
    if (left <= 0) { clearInterval(id); id = null; go.textContent = 'Start';
      left = total; msg.textContent = 'Time! Take a breath. Done, or another round?'; }
  }, 1000);
};
document.getElementById('rs').onclick = () => {
  clearInterval(id); id = null; left = total; go.textContent = 'Start'; msg.textContent = ''; draw();
};
</script>
"""
BTN = ("border:none;border-radius:999px;padding:10px 26px;margin:0 6px;font-size:16px;"
       "background:#7fb3a3;color:white;cursor:pointer")


def main():
    st.set_page_config(page_title="FocusForge", page_icon="🌿", layout="centered")
    st.markdown("""
    <style>
      .stApp { background: #f6f8fb; }
      .stApp h1 { color: #2c3e50 !important; }
      .one-task { font-size: clamp(2rem, 6vw, 3.4rem); font-weight: 700; line-height: 1.2;
                  color: #2c3e50; text-align: center; padding: 2.2rem 1rem;
                  background: white; border-radius: 24px; box-shadow: 0 6px 24px rgba(0,0,0,.06); }
      .why { text-align: center; color: #6b7c8d; margin-top: .8rem; }
    </style>""", unsafe_allow_html=True)

    st.title("🌿 FocusForge")
    st.caption("Dump everything. We'll hand you just one thing. Nothing leaves your computer.")

    ss = st.session_state
    ss.setdefault("queue", [])
    ss.setdefault("idx", 0)
    ss.setdefault("done", 0)

    dump = st.text_area("Brain dump", height=200,
                        placeholder="- finish history essay\n- email prof about extension ASAP\n- laundry\n- pay phone bill today")
    if st.button("🔨 Forge My Next Step", type="primary", use_container_width=True):
        ss.queue, ss.idx = rank(dump), 0
        if not ss.queue:
            st.info("Your dump is empty. Even one line is enough.")

    if ss.queue and ss.idx < len(ss.queue):
        task, why = ss.queue[ss.idx]
        st.markdown(f"<div class='one-task'>{html.escape(task)}</div>"
                    f"<div class='why'>Picked because {' and '.join(why)}.</div>", unsafe_allow_html=True)
        st.write("")
        c1, c2 = st.columns(2)
        if c1.button("✅ Done!", use_container_width=True):
            ss.idx += 1
            ss.done += 1
            st.rerun()
        if c2.button("🔁 Not this one", use_container_width=True):
            ss.queue.append(ss.queue.pop(ss.idx))  # send to back, never lose it
            st.rerun()

        mins = st.select_slider("Focus timer (minutes)", [5, 10, 15, 25], value=15)
        st.iframe(TIMER_HTML.replace("__MM__", str(mins)).replace("__BTN__", BTN), height=330)
    elif ss.queue:
        st.balloons()
        st.success(f"You cleared all {ss.done}. That's real. Go rest.")


if __name__ == "__main__":
    main()
