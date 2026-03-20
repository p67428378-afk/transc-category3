from core.config import settings

def categorize_transaction(description: str) -> str:
    """Placeholder for LLM-based transaction categorization."""
    # In a real application, this would involve calling an LLM API
    # using settings.LLM_API_KEY and processing the description.
    # For now, we'll use a simple rule-based categorization.
    description_lower = description.lower()
    if "starbucks" in description_lower or "cafe" in description_lower:
        return "Food"
    elif "rent" in description_lower:
        return "Rent"
    elif "electricity" in description_lower or "water" in description_lower:
        return "Utilities"
    else:
        return "Miscellaneous"
