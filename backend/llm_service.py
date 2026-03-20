async def categorize_transaction(description: str) -> str:
    """Mocks an LLM service for categorizing transactions."""
    description_lower = description.lower()
    if "starbucks" in description_lower or "cafe" in description_lower:
        return "Food"
    elif "rent" in description_lower or "landlord" in description_lower:
        return "Rent"
    elif "electricity" in description_lower or "water bill" in description_lower:
        return "Utilities"
    elif "salary" in description_lower or "payroll" in description_lower:
        return "Income"
    else:
        return "Miscellaneous"
