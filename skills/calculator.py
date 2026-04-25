from skills.base import Skill

_WORD_TO_OP = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "multiplied by": "*",
    "divided by": "/",
    "over": "/",
}


class CalculatorSkill(Skill):
    keywords = ["calculate", "compute", "how much is", "what is", "equals"]

    def execute(self, text: str) -> str:
        expr = text.lower()
        for word, op in _WORD_TO_OP.items():
            expr = expr.replace(word, op)
        safe = "".join(c for c in expr if c in "0123456789+-*/.() ")
        if not safe.strip():
            return "Could not parse the expression."
        try:
            result = eval(safe)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return f"The result is {result}."
        except ZeroDivisionError:
            return "Cannot divide by zero."
        except Exception:
            return "Could not evaluate the expression. Please try again."
