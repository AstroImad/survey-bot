# survey-bot

A lightweight, extensible bot for creating and running surveys in chat platforms or web. Designed for simple deployment, customizable survey flows, and easy integration with storage backends.

## Features
- Create single- and multi-question surveys
- Support for multiple question types: text, multiple-choice, rating
- Persistence with pluggable storage (SQLite by default)
- Webhook or polling modes for chat platform integration
- Export survey results as CSV or JSON
- Simple configuration via environment variables

## Requirements
- Node.js 18+ or Python 3.10+ (choose implementation)
- Docker (optional)
- SQLite (default) or another supported database

## Quickstart (Node.js example)
Install dependencies:
```bash
git clone <repo-url>
cd survey-bot
npm install
```

Set environment variables (example):
```bash
cp .env.example .env
# Edit .env: PORT=3000, DATABASE_URL=sqlite://./data.db, BOT_TOKEN=...
```

Run locally:
```bash
npm start
```

## Docker
Build and run:
```bash
docker build -t survey-bot .
docker run -e BOT_TOKEN=... -p 3000:3000 survey-bot
```

## Configuration
Key environment variables:
- PORT — HTTP port (default: 3000)
- DATABASE_URL — connection string for storage
- BOT_TOKEN — token for chat platform (if applicable)
- BASE_URL — public URL for webhooks

## Usage
- Create a new survey via the admin API or CLI
- Publish survey and share link or trigger via chat command
- Collect responses and export results from the admin endpoint

Example API call to create a survey (JSON):
```http
POST /api/surveys
Content-Type: application/json

{
    "title": "Customer Feedback",
    "questions": [
        {"type": "rating", "text": "Rate your experience (1-5)"},
        {"type": "text", "text": "What can we improve?"}
    ]
}
```

## Development
- Run linters and tests:
```bash
npm run lint
npm test
```
- Use environment `.env.development` for local development
- Add database migrations as features evolve

## Contributing
- Fork the repo, create a feature branch, and open a pull request
- Follow existing code style and include tests for new behavior
- Refer to CONTRIBUTING.md for detailed guidelines

## License
MIT License — see LICENSE file for details

## Contact
Report issues via repository issue tracker. Include reproduction steps and logs for faster triage.