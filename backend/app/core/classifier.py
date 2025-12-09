def classify_message(text: str) -> str:
    text_lower = text.lower()

    categories = {
        "Laboral": [
            "despido", "contrato", "laboral", "nomina", "incapacidad",
            "erte", "seguridad social", "paro", "baja", "sindicato"
        ],
        "Fiscal": [
            "fiscal", "impuesto", "impuestos", "renta", "irpf",
            "iva", "tributacion", "hacienda", "declaracion"
        ],
        "Contable": [
            "contable", "contabilidad", "facturas", "balance",
            "asiento", "libro diario", "cierre contable"
        ],
        "Jurídico": [
            "juridico", "abogado", "denuncia", "juicio", "demanda",
            "contrato", "legal", "ley", "pleito", "herencia", "testamento"
        ],
    }

    # Recorremos las categorías en orden de prioridad
    for category, keywords in categories.items():
        for word in keywords:
            if word in text_lower:
                return category

    # Si no encuentra coincidencias, es general
    return "General"

