import pandas as pd
from app.models.db.transaction_db import Transaction
from app.models.db.category_db import Category
from app.db.session import SessionDep
from app.models.finance import CategorySummary, FinancialReport
from sqlmodel import select, extract
from datetime import datetime
import calendar


class FinanceEngine:
    def __init__(self, db: SessionDep):
        self.db = db

    def generate_monthly_report(self, user_id, month, year) -> FinancialReport:
        query = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .where(extract("month", Transaction.occurred_at) == month)
            .where(extract("year", Transaction.occurred_at) == year)
        )

        # Load directly into pandas DataFrame
        df = pd.read_sql(query, self.db.bind)

        if df.empty:
            return self._empty_report(month, year)
        
        expense = df[df['direction'] == 'out']['amount'].sum()
        income = df[df['direction'] == 'in']['amount'].sum()
        net = income - expense
        
        print("-------DEBUG------ Total Expense: ", expense)
        print("-------DEBUG------ Total Income: ", income)

        # Group by categories
        expense_df = df[df['direction'] == 'out']
        print("-------DEBUG------ EXPENSE DF: ", expense_df)
        cat_group = expense_df.groupby('category_id')['amount'].agg(['sum', 'count']).reset_index()
        cat_group = cat_group.sort_values(by='sum', ascending=False)
        
        # Fetch category names and merge with grouped data
        category_query = select(Category).where(Category.user_id == user_id)
        categories_df = pd.read_sql(category_query, self.db.bind)
        print("-------DEBUG------ CATEGORIES DF: ", categories_df)
        cat_group = pd.merge(cat_group, categories_df, on='category_id', how='left')
        print("-------DEBUG------ CAT GROUP: \n", cat_group)

        # Structure Data
        top_categories = []
        for _, row in cat_group.iterrows():
            top_categories.append(CategorySummary(category=row['name'], total=row['sum'], count=row['count']))
        
        print("-------DEBUG------ TOP CATEGORIES: \n", top_categories)


        # Get the exact last day of the month
        _, last_day = calendar.monthrange(year, month)
        return FinancialReport(
            period_start=datetime(year, month, 1),
            period_end=datetime(year, month, last_day, 23, 59, 59),
            total_income=income,
            total_expense=expense,
            net_savings=net,
            top_spending_categories=top_categories
        )

    def _empty_report(self, month, year):
        return FinancialReport(
            period_start=datetime(year, month, 1),
            period_end=datetime(year, month, 1),
            total_income=0.0,
            total_expense=0.0,
            net_savings=0.0,
            top_spending_categories=[],
        )
