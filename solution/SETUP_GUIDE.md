# Setup guide — run the seller-fit persona agent end to end

Follow the steps in order. Each step says **what to do** and **why**. Steps marked 🧑 need you, either in the Sarvam console or on your Mac. Steps marked 🤖 I can do for you once you share the result.

Time: about 2–3 hours the first time.

---

## What you will have at the end

- **3 Sarvam agents** (Warm, Formal, Brisk). One prompt, three voices and speeds.
- **1 baseline agent** that copies today's VANI. Needed to prove ours is better.
- A **persona engine** that turns any seller row into a persona card.
- A **service** that receives call results and decides the next attempt.
- **34 test scenarios** run on both agents, plus a **score table**.

```
seller row ──► persona engine ──► persona card ──► Sarvam agent (variant by voice)
                                                     │
                     score table ◄── webhook service ◄┘ (call result)
```

---

## Step 1 🧑 — Run the code on your Mac (10 min)

```bash
cd ~/Desktop/Murmur/solution
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python tests/test_core.py                     # should print "all tests passed"
python persona_engine/build_cards.py --sellers persona_engine/synthetic_sellers.csv --out out
cat out/summary.txt
head -c 600 out/cards.jsonl
```

**Why:** it proves the persona rules work before you touch Sarvam. `out/cards.jsonl` has one persona card per seller. Each card holds the opener, tone, time slots and voice variant the agent will receive. Read two or three cards; if a line sounds wrong, edit `persona_engine/playbook.yaml` and run again. The playbook is where you tune the personas, with no code changes needed.

Optional: run it on the real seller file (output stays on your Mac, git-ignored):
```bash
python persona_engine/build_cards.py --sellers "../Persona Files/Seller-Fit Adaptive Voice Persona - Dataset 1 of 3/ps07_seller_files_part1.csv" --limit 5000 --out out/real
cat out/real/summary.txt     # expect roughly: new 31%, established 25%, trader 14%, retailer 13%, manufacturer 10%, service 8%
```
**Why:** this checks that the persona mix matches the data analysis.

---

## Step 2 🧑 — Get into Sarvam and collect your IDs (10 min)

1. Open **indus.sarvam.ai** and sign in with the company access.
2. Find and note, in `solution/.env` (copy `.env.example` to `.env` first):
   - **Org ID** and **Workspace ID**: usually in the URL or Settings.
   - **API key**: Settings → API keys. The API key header is `X-API-Key` (already set in `.env.example`).

**Why:** `service/dial.py` needs these to place calls through Sarvam's outbound API. Never commit `.env`, because it holds your key (git already ignores it).

---

## Step 3 🧑 — Build the main agent: "Murmur – Warm" (45 min)

In Sarvam: **Build → Agents → Create from scratch**. Name it `Murmur – Warm`.

| # | Where in Sarvam | What to do | Why |
|---|---|---|---|
| 3.1 | **Variables** tab | Create every input variable in `agent/variables.md` with its default value. Turn **"send to LLM" off** for `seller_glid`, `voice_variant`, `language`. | The persona card arrives as these variables. The defaults let you test without real calls. Hidden variables stay out of the prompt. |
| 3.2 | **Instructions → Greeting** | Put just the `opener` variable chip. | The first sentence becomes persona-specific. 28% of today's calls end in 10 seconds, so the opener matters most. |
| 3.3 | **Instructions → Prompt** | Paste `agent/system_prompt.md` (from "Who you are" down). Replace each `{{name}}` with the matching variable chip. | This is the persona brain: tone, short turns, the booking rules and the 7 live-adaptation modes. |
| 3.4 | **Settings → Language personalisation** | Starting language Hindi; turn **Switch language during call** on; allow Hindi, English, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese. | Sellers switch language; the agent must follow. The starting language per seller comes from the card. |
| 3.5 | **Settings → Speakers & voice** | Pick a friendly female Hindi/Hinglish voice (e.g. Simran or Ritu), speed **1.0**. Try Bulbul v4 if listed. If available, set a voice per starting language for Tamil, Telugu and others. | Warm persona = new sellers and service providers. |
| 3.6 | **Knowledge** | Upload `agent/knowledge_base.md`. | Stops the agent inventing prices or claims. It answers "is it free?" and "can it be online?" from facts. |
| 3.7 | **Variables → Output** | Create the output variables in `agent/variables.md` (`call_outcome` as Enum, etc.). | Sarvam extracts the result after each call; our service and scoring read it. |
| 3.8 | **Goal** | Successful when `call_outcome` equals `meeting_fixed`. | Sarvam analytics then shows the success rate per agent and per voice. |
| 3.9 | **Save / commit a version** | Commit the version. | The outbound API calls a committed version (`app_version`). |

### Check it in the test panel (15 min)
Open **Test agent → Voice** (browser mic). Override variables if the panel allows, or keep the defaults. Do these four short calls:

| You say | Good agent behaviour |
|---|---|
| "Haan ji boliye" → then "theek hai, shaam ko" | Short value line → offers 2 times → repeats your time and asks "pakka?" |
| "Abhi busy hoon" | ONE sentence, offers a time immediately |
| "Aap bot ho kya?" | Says honestly it is IndiaMART's AI assistant, offers a human |
| "Baar baar call mat karo" | Apologises once, says no more calls, ends |

If it lectures or pitches after "busy", tighten the "Speaking rules" in the prompt (e.g. "max 15 words per turn") and commit again.
**Why:** it's 10× faster to fix behaviour here than after phone calls.

---

## Step 4 🧑 — Make the other two voice variants (15 min)

**Duplicate** `Murmur – Warm` twice:
- `Murmur – Formal`: mature male voice (e.g. Aditya), speed **0.95**.
- `Murmur – Brisk`: energetic female voice (e.g. Priya), speed **1.1**.

Change **only** the voice and speed (see `agent/variants.md`), then commit each. Copy each agent's **app_id** and **version** into `.env`.

**Why:** Sarvam fixes voice and speed for the whole call, so the persona's sound has to be chosen before dialling. The dialler picks the variant from the card. The prompt stays identical, so only the voice differs between them.

---

## Step 5 🧑 — Make the baseline agent (10 min)

Create `Murmur – Baseline` from `agent/baseline_agent.md`. Use the same output variables and goal. Commit and copy its app_id into `.env` (`SARVAM_APP_ID_BASELINE`).

**Why:** without a "before", you can't show improvement. The baseline copies today's single-persona VANI script, so the comparison is fair.

---

## Step 6 🧑 + 🤖 — Run the test scenarios on both agents (45 min)

```bash
python eval/make_scenarios.py      # 34 scenarios → eval/scenarios.csv
```

In Sarvam: **Tests** → create a test suite. For each row of `eval/scenarios.csv`:
- **Simulated user / scenario** = the `simulated_seller` text
- **Pass criteria / judge** = the `pass_criteria` text
- **Variables** = the values in `variables_json` (if the test lets you set variables)

Run the suite on `Murmur – Warm` (for warm personas), `Formal` and `Brisk` as matching. Then run the same suite on `Murmur – Baseline`. Use **3 runs per case**.

Record the results in `eval/test_results.csv`:
```
scenario_id,agent_label,passed,outcome
new_seller__busy,baseline,0,dropped_early
new_seller__busy,seller_fit,1,callback_scheduled
```
Then:
```bash
python eval/score.py --tests eval/test_results.csv
```
**Why:** this is the evidence. Pass rates per behaviour (busy, price, irritated, and so on) for baseline vs ours show where the persona and adaptation help. Send me the CSV or a screenshot (🤖) and I'll turn it into the results table and the approach-note text.

> If Sarvam Tests can't be bulk-created on your plan, create the 10 most important ones by hand: the busy and receptive rows for each persona, plus `edge__bot_question` and `edge__tamil`.

---

## Step 7 🧑 — Real phone call with results flowing back (30 min)

1. **Phone number:** in Sarvam **Telephony**, rent a number or connect the provided one. Note the **connection ID** and **agent phone number** in `.env`. On a trial, also whitelist your own mobile.
   *Why:* outbound calls need a caller number and connection.
2. **Start the service:**
   ```bash
   export $(grep -v '^#' .env | xargs)
   uvicorn service.app:app --port 8000
   ```
3. **Open a tunnel** in a second terminal: `ngrok http 8000` (or `cloudflared tunnel --url http://localhost:8000`). Put the https URL in `.env` as `MURMUR_PUBLIC_URL`.
   *Why:* Sarvam's servers must be able to reach your laptop to deliver the call result.
4. **Dry run, then call yourself:**
   ```bash
   python persona_engine/build_cards.py --sellers persona_engine/synthetic_sellers.csv --out out
   python -m service.dial --card-glid 900000032 --phone +91<your number> --dry-run   # check the payload
   python -m service.dial --card-glid 900000032 --phone +91<your number>            # busy-retailer persona, Brisk voice
   python -m service.dial --card-glid 900000010 --phone +91<your number>            # established, Formal voice
   python -m service.dial --card-glid 900000010 --phone +91<your number> --baseline # same seller, baseline agent
   ```
5. After each call: `curl "http://localhost:8000/results?token=$MURMUR_TOKEN"` and `python eval/score.py --db out/murmur.db`.

**Why:** this proves the full loop: the persona card selects the voice, the agent adapts, Sarvam sends the result, and the service decides the next attempt. These calls are also your demo recordings.

---

## Step 8 (optional) 🧑 — Mid-call `adapt` tool

Only if the agent misses signals using the prompt alone. In Sarvam **Tools → API tool**:
- POST `{MURMUR_PUBLIC_URL}/tools/adapt`, header `X-Murmur-Token: <token>`, body `{"utterance": "<seller's last sentence>"}`
- **Save reply into variables:** `mode` → `adapt_mode`, `guidance` → `adapt_guidance`
- Add to the prompt: "If you are unsure what the seller means, call the adapt tool and follow `{{adapt_guidance}}`."

**Why:** a deterministic second opinion for tricky turns. It costs a little latency, so it's optional.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Outbound API returns 401/403 | Wrong key or header name: check `SARVAM_AUTH_HEADER` against the Sarvam API-keys page |
| 422 from outbound API | A variable name in `.env`/payload doesn't exist in the agent, or the version isn't committed |
| No webhook arrives | Tunnel not running, wrong URL, or token mismatch: check the uvicorn log |
| Agent reads the card out loud | In the prompt, make sure the variables sit inside "The seller you are talking to" as instructions, not as speech |
| Agent pitches too long | Lower `pitch_cap_turns` in `playbook.yaml`, add "max 15 words per turn", commit a new version |
| Language doesn't switch | Turn on "Switch language during call" and add the language to the allowed list |

---

## What to send me after each step

- After Step 3: anything Sarvam didn't accept (a field name, a limit). I'll adjust the files.
- After Step 6: `eval/test_results.csv` or screenshots. I'll build the results table and analysis.
- After Step 7: `python eval/score.py --db out/murmur.db` output plus one transcript. I'll tune the prompt and playbook.
