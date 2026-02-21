"""
skills/calculator.py — Калькулятор
"""

def calculate(expression: str) -> str:
    """
    Вычисляет математическое выражение.
    Пример: "5 + 3" → "Результат: 8"
    """
    try:
        # Убираем всё кроме цифр и операторов
        safe_expr = "".join(c for c in expression if c in "0123456789+-*/.() ")
        if not safe_expr.strip():
            return "Не удалось распознать выражение."
        result = eval(safe_expr)
        # Убираем лишние нули у целых чисел
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"Результат: {result}"
    except Exception:
        return "Не удалось вычислить выражение. Попробуйте ещё раз."
