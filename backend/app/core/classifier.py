def classify_message(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["despido", "contrato", "laboral"]):
        return "Laboral"
    if any(word in text_lower for word in ["herencia", "testamento"]):
        return "Herencias"
    if any(word in text_lower for word in ["fiscal", "impuestos", "renta"]):
        return "Fiscal"

    return "General"
