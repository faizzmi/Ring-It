from pydantic import BaseModel

class LedgerSummaryResponse(BaseModel):
    netWorth: float
    netWorthDelta: float
    dsr: float
    dsrStatus: str      # "healthy" | "good" | "danger" | "critical"
    dsrLabel: str       # "Healthy" | "Good" | "Danger Zone" | "Critical"
    dsrMessage: str     # human-readable advice
    income: float
    expenses: float
    savings: float
    incomeTrend: float
    expenseTrend: float
    savingsTrend: float

    class Config:
        from_attributes = True