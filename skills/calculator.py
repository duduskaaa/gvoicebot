_WORD_TO_OP = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "multiplied by": "*",
    "divided by": "/",
    "over": "/",
}


def calculate(expression: str) -> str:
    text = expression.lower()
    for word, op in _WORD_TO_OP.items():
        text = text.replace(word, op)

    safe_expr = "".join(c for c in text if c in "0123456789+-*/.() ")
    if not safe_expr.strip():
        return "Could not parse the expression."

    try:
        result = eval(safe_expr)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"The result is {result}."
    except ZeroDivisionError:
        return "Cannot divide by zero."
    except Exception:
        return "Could not evaluate the expression. Please try again."
