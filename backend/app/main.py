from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
# from app.api.v1 import auth, transactions, accounts, budget, goals, debt, policy, cloudinary

app = FastAPI(
    title="Ring-It API",
    description="Behavioral Finance Vault — Malaysian Compliance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Idempotency-Key"],
)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
# app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Accounts"])
# app.include_router(budget.router, prefix="/api/v1/budget", tags=["Budget"])
# app.include_router(goals.router, prefix="/api/v1/goals", tags=["Goals"])
# app.include_router(debt.router, prefix="/api/v1/debt", tags=["Debt"])
# app.include_router(policy.router, prefix="/api/v1/policy", tags=["Policy"])
# app.include_router(cloudinary.router, prefix="/api/v1/cloudinary", tags=["Cloudinary"])

@app.get("/health")
async def health_check():
    return {"status": "vault online", "version": "1.0.0"}