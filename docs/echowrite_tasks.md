# 📋 EchoWrite — Task Breakdown

### Task 1: Source Ingestion
Implement ingestion for RSS + YouTube feeds.  
Store fetched items (title, summary, url, publishedAt).  
Handle retries and deduplication.

### Task 2: Trend Engine
Build scoring logic combining recency + keyword density.  
Return top N trending items for draft generation.

### Task 3: Voice Trainer
Extract tone descriptors from uploaded samples.  
Cache 3–5 top traits and expose via `getVoiceProfile`.

### Task 4: Newsletter Generator
Use LLM to generate newsletter from trends + style.  
Validate Markdown output and store in `Draft`.

### Task 5: Delivery
Schedule daily newsletter generation (08:00 AM local).  
Enable manual trigger route for on-demand draft.

### Task 6: Feedback
Implement `/api/feedback` endpoint.  
Capture thumbs-up/down and link to tone retraining.

### Task 7: Monitoring
Add `/api/health` route and structured logging.  
Track ingestion, generation, and delivery results.

### Task 8: Documentation
Add architecture diagram and finalize README.md.

