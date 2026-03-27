from datetime import datetime
import uuid

class Expense:
    def __init__(self, amount, category, description="", date=None):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        expense = cls(data["amount"], data["category"], data["description"], data["date"])
        expense.id = data["id"]
        return expense

    def __str__(self):
        return f"{self.date} - {self.category}: ${self.amount:.2f} - {self.description}"