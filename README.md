# ReverseSaaS

ReverseSaaS analyzes any startup URL by crawling, detecting technology, generating AI insights, predicting architecture, estimating costs, and exporting a professional report.

## Tech Stack

- Frontend: Next.js 15, TypeScript, TailwindCSS, shadcn/ui, Framer Motion
- Backend: FastAPI, Python
- Database: PostgreSQL + Prisma
- AI: Google Gemini API
- Scraping: Playwright

## Project Structure

```
apps/
  api/        # FastAPI backend
  web/        # Next.js frontend
reversesaas_landing_page/  # Original UI reference
reversesaas_analysis_dashboard/
reversesaas_ai_core_scanning/
```

## Requirements

- Node.js 20+
- Python 3.11+
- PostgreSQL 16+
- Playwright browsers

## Local Setup

### 1) Environment variables

Copy the sample env file and update values:

```
cp .env.example .env
```

### 2) Backend setup

```
cd apps/api
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m prisma generate
python -m prisma migrate dev --name init
python -m playwright install
uvicorn app.main:app --reload
```

### 3) Frontend setup

```
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000

## Docker

```
docker compose up --build
```

The web UI runs at http://localhost:3000 and the API at http://localhost:8000.

## Production Deployment (Vercel + Railway)

### Railway (API)

1) Create a new Railway service from this repo.
2) Railway will use [railway.toml](railway.toml) to build with the API Dockerfile.
3) Set environment variables:

```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>?schema=public
GEMINI_API_KEY=your_gemini_api_key
PLAYWRIGHT_HEADLESS=true
ALLOWED_ORIGINS=https://your-vercel-domain
```

The API container runs `prisma migrate deploy` automatically via [apps/api/start.sh](apps/api/start.sh).

### Vercel (Web)

1) Create a Vercel project from this repo.
2) The repo includes [vercel.json](vercel.json) for monorepo builds.
3) Set environment variables:

```
API_URL=https://your-railway-api-domain
```

Deploy. The web app will proxy API calls through Next.js route handlers.

## API Endpoints

- `POST /analyze`
- `GET /analysis/{id}`
- `GET /technology/{id}`
- `GET /competitors/{id}`
- `GET /costs/{id}`
- `GET /analysis/{id}/report`

## Notes

- `prisma generate` is required before running the API.
- Playwright requires browser binaries (`python -m playwright install`).
- Set `GEMINI_API_KEY` for full AI insights.
