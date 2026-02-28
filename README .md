<div align="center">

```
██████╗ ██╗███╗   ██╗ ██████╗       ██╗████████╗
██╔══██╗██║████╗  ██║██╔════╝       ██║╚══██╔══╝
██████╔╝██║██╔██╗ ██║██║  ███╗█████╗██║   ██║   
██╔══██╗██║██║╚██╗██║██║   ██║╚════╝██║   ██║   
██║  ██║██║██║ ╚████║╚██████╔╝      ██║   ██║   
╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝       ╚═╝   ╚═╝   
```

**`// sovereign theme · obsidian vault · oxblood ledger`**

[![CI Pipeline](https://img.shields.io/github/actions/workflow/status/ringit-my/ring-it/ci.yml?branch=main&label=CI%20Pipeline&style=flat-square&color=800020)](https://github.com/ringit-my/ring-it/actions)
[![Coverage](https://img.shields.io/badge/coverage->90%25-4CAF50?style=flat-square)](https://codecov.io/gh/ringit-my/ring-it)
[![Vuln Scan](https://img.shields.io/badge/vuln%20scan-passing-4CAF50?style=flat-square)](https://github.com/ringit-my/ring-it/security)
[![Python](https://img.shields.io/badge/python-3.12+-E0E0E0?style=flat-square&logo=python)](https://python.org)
[![Vue](https://img.shields.io/badge/vue-3.4+-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/fastapi-0.110+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-800020?style=flat-square)](LICENSE)
[![IEEE SRS](https://img.shields.io/badge/IEEE-830--1998%20SRS-gold?style=flat-square)](docs/RING-IT-SRS-001-v1.0.docx)
[![IEEE SDD](https://img.shields.io/badge/IEEE-1016--2009%20SDD-gold?style=flat-square)](docs/RING-IT-SDD-001-v1.0.docx)

</div>

---

## Mission

> *"You do not rise to the level of your goals. You fall to the level of your systems."*
> — **James Clear**, Atomic Habits

Ring-It is not a budgeting app. It is a **behavioral architecture for wealth accumulation**.

Built on the intersection of **behavioral finance psychology** and **Malaysian financial regulatory compliance**, Ring-It is engineered to make good financial habits effortless and bad ones deliberately difficult. Every design decision — from the dark industrial Sovereign UI that frames your finances as a serious vault, to the mandatory justification friction before impulsive purchases — is intentional.

The three core behavioral levers:

| Principle | Ring-It Implementation |
|-----------|----------------------|
| **Friction by Design** | "Want" purchases >RM 50 require a typed Justification Note before saving |
| **Immediate Reward** | Every saving logs a 10-year compounding projection instantly |
| **Habit Anchoring** | Daily Gauge resets at midnight — the fresh-start effect on repeat |

This is your financial operating system. Not a tracker. A system.

---

## Tech Stack

```
ring-it/
├── backend/           # FastAPI (Python 3.12+)
│   ├── Pydantic v2    # Strict-mode request validation (no float, only Decimal)
│   ├── SQLAlchemy 2   # Async ORM + Alembic migrations
│   ├── PostgreSQL      # Double-Entry Bookkeeping schema (Supabase)
│   └── APScheduler    # Annual policy migration cron (Jan 1st)
│
├── frontend/          # Vue.js 3 (Composition API + TypeScript)
│   ├── Pinia          # Strict TypeScript state management
│   ├── Vuetify 3      # Sovereign theme (#080808 / #800020)
│   ├── Tailwind CSS   # Utility-class layout system
│   └── Cloudinary     # Encrypted receipt vault (signed upload)
│
├── security/
│   ├── JWT/OAuth2     # RS256 asymmetric signing
│   ├── AES-256-GCM    # Field-level encryption (PDPA 2010)
│   ├── WebAuthn       # W3C Level 2 biometric auth
│   └── BNM RMIT       # Rate limiting + idempotency keys
│
└── docs/
    ├── SRS v1.0       # IEEE 830-1998 (11 modules, 8 diagrams)
    └── SDD v1.0       # IEEE 1016-2009 (FastAPI + Vue.js architecture)
```

### Core Dependencies

**Backend**
```toml
[tool.poetry.dependencies]
python          = "^3.12"
fastapi         = "^0.110.0"
pydantic        = {version = "^2.6.0", extras = ["email"]}
sqlalchemy      = "^2.0.0"
asyncpg         = "^0.29.0"          # Async PostgreSQL driver
alembic         = "^1.13.0"
python-jose     = "^3.3.0"           # JWT (RS256)
cryptography    = "^42.0.0"          # AES-256-GCM
passlib         = {version="^1.7.4", extras=["bcrypt"]}
slowapi         = "^0.1.9"           # Rate limiting (BNM RMIT)
cloudinary      = "^1.39.0"
apscheduler     = "^3.10.0"
supabase        = "^2.0.0"
```

**Frontend**
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vuetify": "^3.5.0",
    "pinia": "^2.1.0",
    "@vueuse/core": "^10.9.0",
    "tailwindcss": "^3.4.0",
    "axios": "^1.6.0",
    "decimal.js": "^10.4.3"
  }
}
```

---

## Sovereign Theme

The Ring-It UI is governed by the **Sovereign** Vuetify theme. No pastels. No gradients. No shadows.

```typescript
// plugins/vuetify.ts
const sovereign: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#080808',  // Deepest Obsidian — the void behind your wealth
    surface:    '#121214',  // Matte Iron — the vault surface
    primary:    '#800020',  // Flat Oxblood Red — your financial weapon
    secondary:  '#757575',  // Muted Gunmetal — supporting information
    accent:     '#E0E0E0',  // Platinum Silver — highlights
    error:      '#B00020',  // Deep Crimson — NO-BUY / danger
    success:    '#4CAF50',  // Vault Green — BUY / safe
    warning:    '#FB8C00',  // Forge Orange — caution / yellow DSR
  }
}
```

> Every component uses `flat: true`, `elevation: 0`, and `rounded: 'sm'` — machined-corner precision, not rounded consumer-app friendliness.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENT  Vue.js 3 · Pinia · Vuetify Sovereign · TypeScript   │
└──────────────────────┬──────────────────────────────────────┘
           HTTPS / TLS 1.3 · JWT Bearer Token
┌──────────────────────▼──────────────────────────────────────┐
│  API GATEWAY  FastAPI · CORS · Rate Limiter · JWT Verify     │
├─────────────────────────────────────────────────────────────┤
│  BUSINESS LOGIC  LedgerSvc · DebtNettingEngine · ZakatEng   │
├─────────────────────────────────────────────────────────────┤
│  DATA LAYER  PostgreSQL (Supabase) · RLS · DEB Schema        │
└──────────────────────┬──────────────────────────────────────┘
          ┌────────────┴────────────┐
   Live Forex API           Cloudinary Receipt Vault
  (150+ currencies)      (AES-encrypted · 7yr retention)
```

> **Note:** LHDN, EPF, Zakat, and OCR are handled **entirely internally** — no third-party government APIs. All constants are manually maintained by the Admin in versioned Policy Config JSON files.

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL (or Supabase project)
- Cloudinary account

### Backend
```bash
cd backend
cp .env.example .env          # Fill in your secrets
poetry install
alembic upgrade head          # Run DB migrations
uvicorn app.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
cp .env.example .env.local    # Set VITE_API_BASE_URL etc.
npm install
npm run dev
# App: http://localhost:5173
```

### Docker (Full Stack)
```bash
docker compose up --build
# Backend: :8000  |  Frontend: :5173  |  DB: :5432
```

---

## Project Structure

```
ring-it/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI factory + middleware
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic Settings
│   │   │   ├── security.py      # JWT + OAuth2
│   │   │   ├── encryption.py    # AES-256-GCM
│   │   │   ├── rate_limit.py    # slowapi BNM RMIT
│   │   │   └── scheduler.py     # APScheduler policy cron
│   │   ├── api/v1/              # FastAPI routers
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic v2 request/response
│   │   ├── services/            # Business logic layer
│   │   └── repositories/        # DB access layer
│   ├── alembic/                 # DB migrations
│   └── tests/                   # pytest (>90% coverage)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VaultDashboard.vue
│   │   │   ├── QuickLogModal.vue
│   │   │   ├── DSRCalculator.vue
│   │   │   └── AIAdvisorWidget.vue
│   │   ├── pages/
│   │   │   ├── landingPage.vue
│   │   ├── stores/
│   │   │   ├── useTransactionStore.ts
│   │   │   ├── useAccountStore.ts
│   │   │   └── useBudgetStore.ts
│   │   ├── types/               # TypeScript interfaces
│   │   └── plugins/
│   │       └── vuetify.ts       # Sovereign theme
│   └── tests/                   # Vitest unit tests

```

---

## Malaysian Compliance

| Framework | Implementation |
|-----------|---------------|
| **PDPA 2010 (Act 709)** | AES-256-GCM field encryption · RLS data isolation · 7yr receipt retention |
| **LHDN 2026/2027** | Internal Policy Config JSON · Admin-maintained tax relief caps |
| **EPF RIA** | Internal benchmarking (RM 390K / 650K / 1.3M) · No EPF API |
| **BNM RMIT** | Rate limiting (100 req/min) · Idempotency keys · Audit trail · Input validation |
| **Zakat** | Internal Nisab calculation · bi-annual Admin update · No Zakat API |

---

## Contributing

### Branching Strategy (GitHub Flow)

```
main          ← Production only. Protected. 2 reviewers required.
  └─ develop  ← Integration branch
       ├─ feature/RIT-{id}-{description}
       ├─ fix/RIT-{id}-{description}
       └─ hotfix/RIT-{id}-{description}  → merges to main + develop
```

### Conventional Commits

All commits **must** follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org). `commitlint` is enforced via husky.

```bash
# Valid commit formats:
feat(ledger): implement double-entry bookkeeping engine
fix(dsr): handle zero net-income edge case
docs(api): add Pydantic schema documentation
test(auth): add JWT expiry edge case coverage
chore(deps): upgrade Pydantic to v2.6.1
refactor(stores): migrate to strict TypeScript interfaces
perf(db): add covering index on ledger_entries
security(middleware): enforce rate limiting on auth routes
```

```bash
# Types: feat | fix | docs | test | chore | refactor | perf | security | ci | build
# Scope: ledger | dsr | auth | budget | goals | policy | stores | api | db | ui | ci
```

### Pull Request Checklist

```markdown
## PR Checklist
- [ ] feat/fix follows Conventional Commits format
- [ ] Unit tests added/updated — coverage remains >90%
- [ ] TypeScript strict mode passes (`vue-tsc --noEmit`)
- [ ] Pydantic v2 strict mode — no floats, only Decimal for amounts
- [ ] No secrets committed (pre-commit hook: `detect-secrets`)
- [ ] API changes reflected in Pydantic schemas
- [ ] DB changes have Alembic migration
- [ ] PR title follows: `type(scope): description`
```

---

## CI/CD Pipeline

```
Push / PR to develop or main
         │
    ┌────▼──────────────────────────────────────────┐
    │  STAGE 1: Code Quality                         │
    │  ├─ ruff check (Python linting)                │
    │  ├─ mypy --strict (type checking)              │
    │  ├─ vue-tsc --noEmit (TS checking)             │
    │  └─ eslint (Vue/TS linting)                    │
    └────┬──────────────────────────────────────────┘
         │
    ┌────▼──────────────────────────────────────────┐
    │  STAGE 2: Tests                                │
    │  ├─ pytest --cov --cov-fail-under=90 ✓        │
    │  └─ vitest run --coverage ✓                    │
    └────┬──────────────────────────────────────────┘
         │
    ┌────▼──────────────────────────────────────────┐
    │  STAGE 3: Security Scanning                    │
    │  ├─ pip-audit (Python CVE scan) ✓              │
    │  ├─ npm audit --audit-level=high ✓             │
    │  └─ trivy image (container scan) ✓             │
    └────┬──────────────────────────────────────────┘
         │ (main branch only)
    ┌────▼──────────────────────────────────────────┐
    │  STAGE 4: Deploy                               │
    │  ├─ Backend → Railway (Docker container)       │
    │  └─ Frontend → Vercel (static + SSR)           │
    └───────────────────────────────────────────────┘
```

| Badge | Status |
|-------|--------|
| CI Pipeline | `<!-- CI_BADGE_PLACEHOLDER -->` |
| Test Coverage | `<!-- COVERAGE_BADGE_PLACEHOLDER -->` |
| Vulnerability Scan | `<!-- VULN_SCAN_BADGE_PLACEHOLDER -->` |
| Deployment | `<!-- DEPLOY_BADGE_PLACEHOLDER -->` |

---

## Documentation

| Document | Standard | Version | Link |
|----------|----------|---------|------|
| Software Requirements Specification | IEEE 830-1998 | v1.0 | [SRS →](docs/RING-IT-SRS-001-v1.0.docx) |
| Software Design Document | IEEE 1016-2009 | v1.0 | [SDD →](docs/RING-IT-SDD-001-v1.0.docx) |
| API Reference | OpenAPI 3.1 | Auto-generated | `/docs` (FastAPI) |
| ADR Log | MADR Format | Ongoing | [ADRs →](docs/adr/) |

---

## License

MIT © 2026 Ring-It Malaysia. See [LICENSE](LICENSE).

---

<div align="center">

**`// the vault is open. the ledger awaits.`**

`#080808` · `#800020` · `#E0E0E0`

</div>
