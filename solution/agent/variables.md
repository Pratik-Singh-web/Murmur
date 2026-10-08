# Agent variables (Sarvam → Agent → Variables)

Create these exactly. **Input variables** are filled per call from the campaign CSV / outbound API (`agent_variables`). **Output variables** are extracted by Sarvam after the call and arrive in the webhook.

## Input variables

| Name | Default (for test panel) | Send to LLM? | Filled from |
|---|---|---|---|
| `seller_glid` | 900000010 | **No** (only for joining results) | card |
| `persona_id` | established_enterprise | Yes | card |
| `persona_label` | Established enterprise | Yes | card |
| `voice_variant` | formal | No | card (used to pick the agent variant) |
| `language` | Hindi | No | card (also passed as `initial_language_name`) |
| `agent_name` | Aditya | Yes | card |
| `address` | ji | Yes | card |
| `company` | Shree Balaji Packaging | Yes | card |
| `category` | Corrugated Box | Yes | card |
| `city` | Ahmedabad | Yes | card |
| `tone` | Respectful, concise, business-value first. | Yes | card |
| `formality` | high | Yes | card |
| `pitch_cap_turns` | 2 | Yes | card |
| `opener` | Namaste ji, IndiaMART se Aditya. … | Yes | card → used as the **Greeting** |
| `value_hook` | aapki listing par jo enquiries … | Yes | card |
| `ask` | Kya is hafte 15 minute ki meeting … | Yes | card |
| `slot_1` | kal subah 11 baje | Yes | card |
| `slot_2` | kal shaam 4 baje | Yes | card |
| `avoid` | long IndiaMART introduction; … | Yes | card |
| `attempt_no` | 1 | Yes | card |
| `attempt_note` | Normal persona opener. | Yes | card |
| `flag_note` | (empty) | Yes | card |

**Greeting:** set the agent's Greeting to just the `{{opener}}` variable chip. That makes the first sentence persona-specific (the first 10 seconds decide 28% of calls).

## Output variables (extracted after the call)

| Name | Type | Values / extraction prompt |
|---|---|---|
| `call_outcome` | Enum | `meeting_fixed`, `callback_scheduled`, `not_interested`, `already_in_touch`, `do_not_call`, `wrong_contact`, `dropped_early`, `other`. Prompt: "Final result of the call. meeting_fixed only if the seller explicitly agreed to a specific meeting time." |
| `meeting_time` | String | "Meeting date/time the seller explicitly agreed to, else empty." |
| `callback_time` | String | "Time the seller asked to be called back, else empty." |
| `signals_seen` | String | "Comma-separated list from: busy, confused, already_met, price, bot_question, irritated, wrong_contact, language_switch. Empty if none." |
| `final_language` | String | "Language the seller mostly used." |
| `seller_sentiment` | Enum | `positive`, `neutral`, `negative` |

## Goal (Sarvam → Goal / "Successful when")

`call_outcome` **equals** `meeting_fixed`
