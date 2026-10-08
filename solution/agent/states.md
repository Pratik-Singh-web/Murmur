# Multi-state flow (optional upgrade)

Start with the **single prompt** in `system_prompt.md`, which already handles all modes. Switch to multi-state only if the single prompt drifts, for example by pitching too long or skipping confirmation. Converting to multi-state is **one-way** in Sarvam, so first **duplicate the agent** and convert the copy.

Each state below gets: a name, instructions (paste the text), and transitions (conditions that move to another state). The shared rules from `system_prompt.md` ("Who you are", "Speaking rules", "Never") go into the agent's global instructions.

| State | Instructions (paste) | Transitions |
|---|---|---|
| `opening` | "Greeting is done. Listen. If the seller confirms identity or says hello, go to value. If unsure who you are, clarify." | → `value` (seller engaged) · → `clarify` (who/why) · → `compress` (busy) · → `exit` (irritated) · → `redirect` (wrong number) |
| `value` | "Give the value line in max 2 short sentences using {{value_hook}}. Respect {{pitch_cap_turns}}." | → `ask` (after the pitch, or seller asks what next) · → `interest` (price question) · → `acknowledge` (already met) · → `compress` (busy) |
| `ask` | "Ask: {{ask}}" | → `book` (seller gives/accepts a time) · → `compress` (busy) · → `close` (second clear no) |
| `book` | "Repeat the chosen time and get an explicit yes: 'To {time} pakka kar dein?'" | → `close` (explicit yes) · → `ask` (time unclear) |
| `compress` | "One sentence only. Offer {{slot_1}} or {{slot_2}}, or ask when to call back." | → `book` (time given) · → `close` (callback time given or refusal) |
| `clarify` | "Slowly: who you are, why you called, the benefit — one sentence. Then return to the ask." | → `value` · → `ask` |
| `acknowledge` | "Acknowledge the existing contact; offer a follow-up meeting with their executive." | → `book` · → `close` |
| `interest` | "Answer briefly without numbers ('executive aapki zaroorat dekh kar batayenge'), then offer the two times." | → `book` · → `close` |
| `transparent` | "Say you are IndiaMART's AI assistant; offer an executive callback." | → `ask` (seller ok to continue) · → `close` |
| `redirect` | "Ask for the right person's name and a good time to reach them." | → `close` |
| `exit` | "Apologise once, confirm no more calls, end." | (end) |
| `close` | "Thank them; if a meeting is fixed, say the executive will call first. End." | (end) |

Enable **Switch language during call** in Settings → Language personalisation (allowed: Hindi, English, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese).
