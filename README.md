# Content Crew

Multi-brand AI content pipeline. Each brand has a niche profile and one or more channels
(TikTok, Instagram, YouTube, Facebook). A crew of four agents hands a short video from topic
to platform-ready posts, and nothing moves forward without human approval.

Scout (topics) -> Writer (script) -> Designer (thumbnail and shots) -> Publisher (per-platform posts) -> queue -> results

## What works today
- Accounts, brands in different niches, several channels per brand
- Full agent pipeline with approve / redo-with-note at every stage, editable captions
- Scheduling with a per-channel daily cap (default 3), cancel, "publish due" button
- Simulated publishing (provider `dryrun`) and manual results entry per post
- Per-user AI usage counter
- Demo mode without an API key; real Claude output with `ANTHROPIC_API_KEY`

## Not built yet
- Real posting. Add a provider in `publisher.py` that calls a posting service whose app already
  has platform approvals (TikTok only allows public API posts from audited apps; Instagram
  needs a Business account). Keep the `(channel, post) -> {"external_id": ...}` contract.
- Video generation, automatic analytics collection, billing, background scheduler.

## Run locally
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000, create an account, add a brand and a channel, start a run.

Set `ANTHROPIC_API_KEY` (see `.env.example`) for real agents. Tests: `python -m pytest`.

## Deploy
`gunicorn wsgi:app` behind HTTPS. Set `SECRET_KEY`. SQLite lives in `instance/`; back it up
or move to Postgres before running real customers.
