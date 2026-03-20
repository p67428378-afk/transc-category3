import random

class LLMCategorizationService:
    def __init__(self):
        self.categories = ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Salary", "Miscellaneous"]

    def categorize_transaction(self, description: str) -> str:
        # Simulate LLM categorization
        # In a real scenario, this would involve an API call to an LLM
        # For now, we'll use some basic keyword matching and random assignment

        description_lower = description.lower()

        if "starbucks" in description_lower or "cafe" in description_lower or "restaurant" in description_lower:
            return "Food"
        elif "rent" in description_lower or "landlord" in description_lower:
            return "Rent"
        elif "electricity" in description_lower or "water" in description_lower or "internet" in description_lower:
            return "Utilities"
        elif "bus" in description_lower or "train" in description_lower or "uber" in description_lower:
            return "Transport"
        elif "cinema" in description_lower or "concert" in description_lower:
            return "Entertainment"
        elif "salary" in description_lower or "payroll" in description_lower:
            return "Salary"
        else:
            return random.choice(self.categories)

llm_service = LLMCategorizationService()
