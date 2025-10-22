# 🧩 Product Requirements Document — EchoWrite

## 🩶 Tagline  
### *Crafting clarity from the chatter.*

---

## 1. Overview
**EchoWrite** is an AI-powered **content curation and newsletter drafting assistant** that listens to the “echo” of the web — aggregating insights, detecting trends, and producing ready-to-send newsletters in the creator’s authentic voice.

It reduces a creator’s daily 2–3-hour research and writing cycle to **under 20 minutes**, empowering consistent, engaging content delivery.

---

## 2. Problem Statement
Creators and agencies waste hours researching and writing, while maintaining consistent tone remains a challenge.  
EchoWrite automates curation and writing — transforming raw feeds into high-quality, personalized newsletters.

---

## 3. Goals & Success Metrics

| Goal | Target |
|------|---------|
| Reduce newsletter creation time | < 20 minutes |
| Draft acceptance rate | ≥ 70 % |
| Engagement uplift (open / CTR) | ≥ 2× baseline |
| Automated draft generation time | Daily 8 AM (local) |

---

## 4. Core Use Cases

| Role | Need | Outcome |
|------|------|----------|
| Independent Creator | Wants curated, tone-matched daily drafts | Consistency and saved time |
| Agency Manager | Manages multiple client newsletters | Scalable workflow per brand |
| Marketing Team | Needs daily trend intelligence | Real-time insight capture |

---

## 5. Functional Requirements

### 5.1 Source Aggregation
- Supports multiple input sources:  
  - RSS / newsletter feeds  
  - YouTube channel RSS  
  - Twitter / X handles or hashtags  
- Stores metadata: title, summary, link, timestamp.

### 5.2 Trend Engine
- Assigns each fetched item a *trend score* via:  
  - Recency decay  
  - Keyword frequency spikes  
- Selects top N items in 48-hour window for draft generation.

### 5.3 Style Trainer
- Accepts 5–20 text samples (newsletters, blogs, posts).  
- Extracts writing traits (tone, rhythm, humor etc.).  
- Builds a reusable *voice profile* for each creator.

### 5.4 Newsletter Generator
- Uses AI to generate Markdown newsletters from trending items + user style.  
- Structure:  
  1. Intro paragraph  
  2. **Top Picks** (3–5 bullets + summaries)  
  3. **Trends to Watch** (3 quick insights)  
  4. Closing call-to-action  
- Validates word limit, grammar, link integrity.

### 5.5 Delivery
- Sends the generated draft every morning (08:00 local) via email or stores in dashboard.  
- Manual “Generate Now” option for ad-hoc creation.

### 5.6 Feedback Loop
- Captures 👍 / 👎 reactions or notes per draft.  
- Uses feedback to refine source weighting and tone adaptation.

### 5.7 Dashboard (optional)
- Manage sources, upload samples, view drafts and review feedback.

---

## 6. Non-Functional Requirements
- Modular services for ingestion, trend analysis, generation, delivery and feedback.  
- Secure credentials & isolated user data.  
- Structured logging + analytics integration.  
- Configurable cron-based scheduling.  
- Deployment ready for scale (multi-tenant).

---

## 7. Conceptual Data Model
```json
{
  "user": {
    "id": "u123",
    "email": "creator@echowrite.ai",
    "voiceTraits": ["friendly", "insightful", "witty"]
  },
  "sources": [
    { "id": "s1", "type": "rss", "handle": "https://feeds.feed.com/tech" },
    { "id": "s2", "type": "youtube", "handle": "@TechGuru" }
  ],
  "items": [
    {
      "id": "i1",
      "sourceId": "s1",
      "title": "AI Startups Boom",
      "url": "https://technews/ai-boom",
      "summary": "Investments doubled in 2025.",
      "score": 0.92
    }
  ],
  "draft": {
    "id": "d1",
    "bodyMd": "## Top Picks ...",
    "sentAt": "2025-10-15T02:30:00Z",
    "accepted": true
  },
  "feedback": { "draftId": "d1", "reaction": "👍" }
}
```

---

## 8. System Flow
1. Ingest new items from configured sources.  
2. Score and rank items by trend level.  
3. Generate newsletter using LLM + style profile.  
4. Deliver at 08:00 AM (local) or on-demand.  
5. Capture feedback to refine future tone and relevance.  
6. Repeat daily.

---

## 9. Future Expansion
- Multi-language generation  
- Social media post generator (LinkedIn / X)  
- Auto-publishing to Beehiiv / Substack  
- Analytics dashboard for performance tracking  

---

## 10. Implementation Plan (4-Hour Build)

### Hour 1 — Setup & Data Foundations
- Create entities: User, Source, Item, StyleSample, Draft, Feedback.  
- Implement ingestion for RSS + YouTube feeds.  
- Seed initial data and verify persistence.

### Hour 2 — Trend & Style Modules
- Build scoring algorithm for trend ranking.  
- Add style extraction and caching of voice traits.  
- Merge both for `generationInput` JSON.

### Hour 3 — Generation & Delivery
- Generate newsletter via LLM prompt (Markdown).  
- Validate length, structure and links.  
- Send email draft (or print preview).  
- Optional: automate via scheduler.

### Hour 4 — Feedback & Hardening
- Implement feedback endpoint and storage.  
- Add logging and error capture.  
- Full pipeline test (ingest → analyze → generate → send → feedback).

---

## 11. Deliverables
- End-to-end working MVP  
- Architecture diagram + PRD (this file)  
- Example generated newsletter  
- Demo walkthrough (optional)

---

## 12. Task Breakdown

### Task 1 — Source Ingestion
- Build ingestion service for RSS + YouTube.  
- Store items with title, summary, url, publishedAt.  
- Handle deduplication, retries and logging.

### Task 2 — Trend Engine
- Implement scoring function (recency + keyword frequency).  
- Expose helper `getTopTrendingItems(userId)`.

### Task 3 — Style Trainer
- Parse uploaded text samples.  
- Extract 3–5 tone descriptors (e.g. witty, analytical).  
- Store and expose `getVoiceProfile(userId)`.

### Task 4 — Newsletter Generator
- Combine top items + voice profile into prompt.  
- Generate Markdown newsletter (Intro, Top Picks, Trends, Closing).  
- Validate and persist as Draft.

### Task 5 — Delivery
- Schedule daily generation + send (08:00 local).  
- Implement manual “Generate Now” route.  
- Record delivery logs.

### Task 6 — Feedback Loop
- Capture 👍 / 👎 per draft.  
- Link feedback to future tone refinement.  
- Create `/api/feedback` endpoint.

### Task 7 — Monitoring & Health
- Add basic logging and `/api/health` endpoint.  
- Include error capture and activity metrics.

### Task 8 — Documentation & Diagram
- Produce architecture diagram (Sources → Trend Engine → Generator → Delivery → Feedback).  
- Update README and setup guide.

---

**End of PRD**

