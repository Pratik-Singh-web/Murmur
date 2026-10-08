# Voice platform comparison for P4 (adaptive persona)

> Researched 8 Oct 2026. V = confirmed in docs, a vendor staff answer or source code; M = marketing or third-party claim; ? = not confirmed. Re-check before relying on any one line.

## Why look beyond the hosted Sarvam agent

P4's core feature is a persona that **adapts mid-call**. On Sarvam's hosted Voice Agents, voice (speaker) and pace are fixed per agent or per call. Only language, state and prompt variables can change mid-call ([sarvam-platform-notes](sarvam-platform-notes.md)). So the question is: which stack lets us switch **voice, pace and language live**, keeps Indic quality, and still counts as "built on Sarvam" for the hackathon?

**Hackathon constraint (deck):** solutions must be built on Sarvam (Saaras STT, Bulbul TTS, Sarvam LLM, Voice Agents) and the submission asks for a "Sarvam agent ID / live link". Dropping Sarvam entirely would cost points and may break the rules. The options below are judged with that in mind.

## Comparison

| Platform | Persona per call | Mid-call voice / pace / language | Indic quality | India telephony | Testing | Cost | Hackathon fit |
|---|---|---|---|---|---|---|---|
| **Sarvam Voice Agents (hosted)** | Voice per language; agent per call via `app_id` (V) | Language only (V); no voice or pace change (?) | Best Hindi evidence (below) | Rent via Vobiz or bring your own (V) | Test panel + AI-judged Tests (V) | Company access (free) | **Native**, gives an agent ID |
| **LiveKit Agents + Sarvam plugins** | Full control in code (V) | **Yes**: `SarvamTTS.update_options(speaker, pace, pitch, loudness, target_language_code)` in `livekit-plugins-sarvam` 1.8.5 (V, source code); STT `update_options(language, model)` (V); takes effect on the next utterance (V, LiveKit forum) | Same Sarvam models | Plivo and Exotel publish LiveKit SIP guides (V) | Code-based; no built-in simulator (?) | Free plan: 1,000 agent min + 1,000 SIP min (V) | Uses Sarvam STT/TTS/LLM; **no Sarvam agent ID** (live link instead) |
| **Pipecat + Sarvam** | Code (V) | `TTSUpdateSettingsFrame` changes voice mid-pipeline (V) | Same | Exotel/Plivo serializers (?) | None built in | Open source | Same as LiveKit |
| Vapi | Overrides per call (V) | Voice switch mid-call not supported; workaround is a Squads handoff (V, staff) | Third-party voices | Bring your own SIP (M) | ? | $0.05/min + pass-through (V) | Not Sarvam |
| Retell AI | Yes | Dynamic speed; node-level speed (V); no voice switch | Hindi, Tamil, Marathi only (V) | Twilio/Vonage | ? | ? | Not Sarvam |
| ElevenLabs Agents | Overrides (V) | Language-detection switches voice per language; multi-voice tags (V); docs also say language is fixed (conflict) | Lowest Hindi TTS WER in one small study | Bring your own SIP | Simulation tests (V) | ~$0.08/min (M) | Not Sarvam |
| Bolna (Indian) | Per-call language (V) | Voice + prompt per language, switched on request/detection (V); no tool-driven speed change | Uses Sarvam/Smallest/ElevenLabs | Plivo, Twilio, Vobiz (V) | ? | ₹5.5/min (V) | Can run Sarvam voices, but not Sarvam's platform |
| OpenAI gpt-realtime | Yes | Voice locked after first speech (V) | Indic weaker (?) | SIP | — | ? | Not Sarvam |
| Gemini Live, Cartesia, Bland, Smallest.ai | Yes | Not confirmed / no speed control found (?) | Mixed; Cartesia worst Hindi accent score in one study | Varies | ? | Varies | Not Sarvam |

## Indic speech quality evidence

- **STT, independent (code published):** Trelis "Tara" Hindi benchmark. Mean WER Sarvam Saaras-v3 12.3 vs ElevenLabs Scribe-v2 13.8; phone audio 23.0 vs 26.9; spontaneous speech 15.3 vs 27.5; conversational Hinglish 11.3 vs 12.4. Scribe was better on read code-mixed speech. Google, Deepgram and OpenAI were not tested. <https://huggingface.co/Trelis/tara>
- **TTS, independent but tiny (10 utterances):** Hindi accent score (lower is better): Sarvam 211.8, ElevenLabs v3 227.5, Indic Parler 248.4, Cartesia Sonic-3 267.4. ElevenLabs had the lowest Hindi WER. All systems struggle with Tamil/Telugu retroflex sounds. <https://arxiv.org/abs/2604.25476>
- **TTS, vendor-run (not independent):** Caller Digital — Bulbul MOS 4.2–4.5 vs ElevenLabs 3.7–4.2, Google 3.5–3.9; code-mixing Bulbul ahead. <https://caller.digital/blog/indic-tts-benchmark-bulbul-elevenlabs-sarvam-google-ai4bharat-2026>
- Conclusion: **no evidence that another vendor beats Sarvam on Hindi/Hinglish phone speech**; Sarvam is at least competitive and probably best for our sellers.

## Verdict

**Keep Sarvam models. Choose the orchestration layer by how much live switching we want.**

| Option | What we get | Cost / risk | Verdict |
|---|---|---|---|
| A. Hosted Sarvam agent only | Agent ID, telephony, tests in hours; persona chosen before the call; live tone + language adaptation | No audible voice/pace change mid-call | Safe baseline |
| **B. LiveKit Agents + Sarvam STT/TTS/LLM** | True mid-call voice, pace and language switch via a `set_persona` tool → the strongest "adaptive persona" demo | ~4–6 h extra setup; we own latency and turn-taking; no Sarvam agent ID | **Primary for the demo**, if organisers accept it as "built on Sarvam" |
| C. Non-Sarvam platform (Vapi, Retell, ElevenLabs …) | Polished tooling | Breaks the Sarvam requirement; weaker or unproven Indic quality; Vapi/OpenAI can't switch voice mid-call | **Reject** |

**Recommended: B + a thin A.**
- Build the adaptive agent on LiveKit with Sarvam plugins: Saaras v4 STT, Bulbul v3 TTS, Sarvam-105b LLM.
- In parallel, keep a minimal hosted Sarvam agent (same prompt, persona via variables). It satisfies the "agent ID" item, serves as the fallback, and acts as the "before" in the demo.
- Ask the organisers at 10:30 whether a LiveKit build on Sarvam models satisfies the submission. If not, A becomes primary and B becomes a recorded stretch demo.

## Day-1 checks before committing to B

1. `pip install "livekit-agents[sarvam]"`. Then confirm that `tts.update_options(speaker=..., pace=...)` mid-session changes the **next** utterance on a live room (the source code supports it; behaviour on an already open stream is not verified).
2. Confirm that Bulbul v3 speaker names are compatible with the plugin's speaker list (the plugin validates model–speaker compatibility).
3. Measure turn latency on web (target < 1.2 s), using the docs' advice: `turn_detection="stt"`, low endpointing delay.
4. Phone demo only if it's quick (Plivo/Exotel SIP into LiveKit); otherwise demo over the web.

## Sources

- LiveKit Sarvam TTS plugin: <https://docs.livekit.io/agents/models/tts/sarvam.md>; source: PyPI `livekit-plugins-sarvam` 1.8.5 (`tts.py` `update_options`)
- LiveKit TTS switching: <https://community.livekit.io/t/how-to-switch-tts-during-agent-runtime/105>
- LiveKit pricing: <https://livekit.com/pricing>
- Pipecat service settings: <https://docs.pipecat.ai/pipecat/fundamentals/service-settings>
- Vapi voice switch (support): <https://support.vapi.ai/t/33037144/switch-assistant-voice-during-call>
- OpenAI realtime voice lock: <https://developers.openai.com/api/docs/guides/realtime-conversations>
- ElevenLabs language detection: <https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/language-detection>
- Bolna multilingual config: <https://www.bolna.ai/docs/customizations/multilingual-config-reference.md>
- Retell changelog: <https://www.retellai.com/changelog/chatgpt-app-dynamic-voice-speed-a-b-testing-and-more>
- Plivo + LiveKit: <https://www.plivo.com/livekit/> · Exotel + LiveKit: <https://exotel.com/blog/production-architecture-low-latency-voice-ai-exotel-livekit/>
