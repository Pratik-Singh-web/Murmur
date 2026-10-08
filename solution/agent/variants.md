# Voice variants

Build the seller-fit agent once, test it, then **duplicate it twice** and change only Settings → Speakers & voice and speed. Keep prompt, variables, knowledge base and goal identical, because the outbound caller picks the variant per seller.

| Variant | Used for personas | Voice (pick in Sarvam; confirm availability) | Speed | Why |
|---|---|---|---|---|
| **Warm** | New seller, Service provider | Female, friendly (Simran / Ritu, Hinglish or Hindi support style) | 1.0× | Receptive, early-stage sellers respond to guidance and warmth |
| **Formal** | Established enterprise, Manufacturer | Male, mature (Aditya or similar) | 0.95× | Experienced owners hung up fastest on the generic pitch; calmer, respectful delivery |
| **Brisk** | Busy retailer, Trader/wholesaler | Female, energetic (Priya or similar) | 1.1× | Shop-counter sellers are time-poor; faster delivery respects that |

For each variant, set per-language voices (Settings → per starting language) for Tamil, Telugu, Kannada, Malayalam, Bengali, Odia and Assamese if Sarvam offers a suitable voice; otherwise leave the default.

After creating them, note each variant's **app_id** and **version** in `.env` (see `../service/.env.example`).

Judgement call, not evidence: no data shows which gender or voice converts better (VANI only ever used one). The mapping is a hypothesis we test with Sarvam Tests and later with a live A/B.
