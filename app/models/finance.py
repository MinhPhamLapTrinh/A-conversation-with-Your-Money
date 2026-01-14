from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict


class CategorySummary(BaseModel):
    # Category name
    category: str
    total: float
    # Frequency of transaction based on the category
    count: int


class FinancialReport(BaseModel):
    period_start: datetime
    period_end: datetime
    total_income: float
    total_expense: float
    net_savings: float
    top_spending_categories: List[CategorySummary]
    
    # This ensures the LLM gets a string representation of decimals 
    # to avoid JSON float parsing errors later
    model_config = ConfigDict(json_encoders={float: str})