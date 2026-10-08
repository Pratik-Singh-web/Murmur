# Sarvam platform notes

> Checked 8 Oct 2026 against docs.sarvam.ai. Re-verify on Day 1 with the Sarvam team; the platform changes weekly.

## Agent building

- Agents are built at **indus.sarvam.ai → Build → Agents**, either from a prompt ("Genie" drafts it) or from scratch, then configured on a visual **Canvas**.
- **Instructions** tab: Greeting (opening line, can include variables) + system prompt.
- Agents can have tools, knowledge, states and evaluation criteria.
- **Settings → Language personalisation:** starting language, "Switch language during call", allowed languages. **Speakers & voice:** voice selection; since 9 Sep a different voice can map to each starting language (chosen at call start).

## Variables

- **System variables** (read-only): `current_date`, `current_time`, `current_datetime`, `current_day`, `start_datetime`, `language_name`.
- **Agent variables** (ours): input (name + default) or output (type String/Enum + extraction prompt).
- Ways to fill input variables per call:
  - **Inbound:** telephony metadata (caller phone).
  - **On-start hook:** an API call at call start; response fields map into agent variables before the agent speaks.
  - **Outbound campaign:** CSV columns → variables.
  - **Outbound API:** `agent_variables` map in the request (see below).
- Each input variable has a toggle for whether it is sent to the LLM (off = available to tools only).
- **Tools can read and write variables mid-call**; API tools have "Save reply into variables".
- **Output variables** are extracted by the LLM after the call and sent via the on-end hook.
- Call goal: a "Successful when" rule on a variable scores each call.
- Not documented: size limits for variables; exact field names for the on-start hook response.

## Outbound API

`POST https://apps.sarvam.ai/api/outbounds/v1/orgs/{org_id}/workspaces/{workspace_id}/outbounds`

Body: `app_config` (`app_id`, `app_version`, `connection_config` {`connection_id`, `agent_phone_number`}, `agent_variables`, `app_overrides` {`initial_bot_message`, `initial_state_name`, `initial_language_name`}), `user_config` {`user_phone_number`}, `webhook_config` {`url`, `metadata`}. Returns `attempt_id`. Auth header not stated on the page — check API key setup.

## Webhooks (call completion)

Inbound (since 2 Sep) and outbound (since 20 Aug) deployments send an event when each call ends. Payload fields: `app_id`, `app_version`, `deployment_id`, `interaction_id`, `user_phone_number`, `agent_phone_number`, `duration`, `final_agent_variables`, `output_agent_variables`, `start_datetime`, `end_datetime`, `interaction_transcript[]` (`role`, `en_text`, `indic_text`), `metadata`.

No separate start-of-call webhook — the on-start hook plays that role.

## Tools

- Built-in API tools and data-validation tools.
- **Call-context variables in API tools** (20 Aug): caller phone, transcript, interaction ID, call length.
- **Code tools** (15 Aug): upload a Python file to define custom tools — access on request.
- **Call transfer** (2 Sep): hand off to a human, another number or SIP trunk.

## Models (latest)

| Area | Model | Note |
|---|---|---|
| STT | `saaras:v4` | GA on Voice Agents 2 Sep; Realtime API 3 Sep; keyterm prompting on REST/Batch 15 Sep |
| TTS | Bulbul v3, **Bulbul v4** | v4 on Voice Agents since 6 Oct |
| LLM | `sarvam-105b` | `sarvam-30b` deprecated (18 Aug); GLM-5.3, Gemma 4 31B in beta |

## Channels

- **Phone:** bring your own telephony (Twilio, Plivo, Exotel, Vobiz guides) or rent numbers from Sarvam; inbound and outbound campaigns.
- **Slack:** connect via Cowork (23 Sep).
- **Web chat / WhatsApp:** not documented → bring our own if a problem needs a second channel.

## Gaps that matter for our candidates

| Gap | Affects | Plan |
|---|---|---|
| No chat/WhatsApp channel | P2 | Own web chat on Sarvam LLM; ask Sarvam on Day 1 |
| No mid-call voice/pace/pitch change | P4 | Tone/language switch on hosted agent, or code-first build; ask on Day 1 |
| Multi-agent not available | P4 | Multi-state agent |
| Hook response field names undocumented | All | Confirm on Day 1 |

## Sources

- [Voice Agents quickstart](https://docs.sarvam.ai/conversations/quickstart)
- [Release notes](https://docs.sarvam.ai/conversations/releases)
- [Variables & Personalization](https://docs.sarvam.ai/conversations/build/variables-personalization)
- [Instant outbound API](https://docs.sarvam.ai/conversations/api/instant-outbound/create)
- [Webhook payload](https://docs.sarvam.ai/conversations/api/deployments/webhooks/webhook-payload)

## Persona-specific capabilities (checked 8 Oct 2026, for P4)

| Capability | Status | Source |
|---|---|---|
| Voices | Bulbul v3: 37 speakers (23 male, 14 female, e.g. Shubh, Aditya, Rohan, Ritu, Priya, Simran, Kavya); Bulbul v4 (on Voice Agents since 6 Oct) adds descriptive voices such as "Ritu – Hindi Support Agent", "Simran – Hinglish Support Agent", "Pooja – Gujarati Conversational" | `/api-reference/text-to-speech/convert`, `/conversations/build/voice-language` |
| Voice per starting language | Yes; fixed for the whole call even if the caller switches language | `/changelog/2026/9/9` |
| Speed / pitch | Agent-level sliders. The Python SDK's `text_to_speech_config.speech_settings` (pace 0.85–2.0, pitch −0.5–0.5) is per session, but it is documented only on PyPI | `/conversations/build/voice-language`, PyPI `sarvam-conv-ai-sdk` |
| Per-call overrides (outbound API / campaign contact) | `app_overrides`: `initial_bot_message`, `initial_state_name`, `initial_language_name`; plus `agent_variables`. No voice/pace field | `/conversations/api/instant-outbound/create` |
| Agent per call | Yes: `app_id` + `app_version` on every outbound call → one agent variant per voice/pace | same |
| Change voice mid-call | **Not documented** | — |
| Change language mid-call | Yes: auto switch, built-in language tool, `context.change_language()` in code tools | `/conversations/build/tools/core-tools` |
| Multi-state | Per-state instructions, tools and transitions; no per-state voice; marked as an older paradigm to be replaced by multi-agent (not yet available) | `/conversations/build/states-conversation-flow` |
| Tools write variables mid-call | Yes ("Save reply into variables"; `context.set_agent_variable()` in code tools, which are available on request) | `/conversations/build/tools/https-tool` |
| Testing | Test panel (browser voice, chat, whitelisted phone) with speaker/language/variable override; **Tests** = AI-simulated user + AI judge, repeat runs, REST API | `/conversations/build/tests` |
| Analytics | Goals analytics includes "TTS voice × goal rate" | `/conversations/monitor/agent-analytics/goals` |
| Limits | Campaigns: 10 concurrent; Bulbul v3 Starter 30 req/min; code tools and workflows enterprise/on request | `/api/getting-started/ratelimits` |

Implication: pick voice and pace **before** the call (agent variant), and adapt tone, script, state and language **during** it. Real mid-call voice switching would need a LiveKit/Pipecat pipeline on the raw Saaras/Bulbul APIs (kept as a stretch goal).
