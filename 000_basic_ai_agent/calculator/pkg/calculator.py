
# Simple Calculator class
class Calculator:
    def __init__(self):
        self.memory = 0

    def add(self, a, b):
        return a + b # Intentional bug: should be a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def evaluate(self, expression):
        """Evaluate an arithmetic expression using the instance's arithmetic methods.
        Supported: + - * / parentheses, unary minus, integers & floats.
        Routes operations through add/subtract/multiply/divide so intentional
        method bugs are reflected in the final result.
        """
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string")
        expr = expression.strip()
        if not expr:
            raise ValueError("Empty expression")

        import re
        token_pattern = re.compile(r"\s*([()+\-*/]|\d*\.\d+|\d+)")
        tokens = []
        i = 0
        last_was_op = True  # Start allows unary sign
        while i < len(expr):
            m = token_pattern.match(expr, i)
            if not m:
                raise ValueError("Invalid expression.")
            tok = m.group(1)
            i = m.end()
            # Handle unary minus / plus folding into number if followed by number
            if tok in ('+','-') and last_was_op:
                # Lookahead for a number
                m2 = token_pattern.match(expr, i)
                if m2:
                    possible = m2.group(1)
                    if re.fullmatch(r"\d*\.\d+|\d+", possible):
                        # merge sign with number
                        num = tok + possible
                        tokens.append(num)
                        i = m2.end()
                        last_was_op = False
                        continue
                # Unary operator not followed by number -> treat as 0 <op> expr
                tokens.append('0')
                tokens.append(tok)
                last_was_op = True
                continue
            tokens.append(tok)
            last_was_op = tok in ('+','-','*','/','(')

        # Shunting-yard to RPN
        precedence = {'+':1,'-':1,'*':2,'/':2}
        output = []
        stack = []
        for tok in tokens:
            if re.fullmatch(r"[+-]?\d*\.\d+|[+-]?\d+", tok):
                output.append(tok)
            elif tok in precedence:
                while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[tok]:
                    output.append(stack.pop())
                stack.append(tok)
            elif tok == '(':
                stack.append(tok)
            elif tok == ')':
                found = False
                while stack:
                    top = stack.pop()
                    if top == '(':
                        found = True
                        break
                    output.append(top)
                if not found:
                    raise ValueError("Mismatched parentheses")
            else:
                raise ValueError("Invalid token")
        while stack:
            top = stack.pop()
            if top in ('(',')'):
                raise ValueError("Mismatched parentheses")
            output.append(top)

        # Evaluate RPN using the instance methods
        eval_stack = []
        for tok in output:
            if tok in precedence:
                if len(eval_stack) < 2:
                    raise ValueError("Invalid expression")
                b = eval_stack.pop()
                a = eval_stack.pop()
                if tok == '+':
                    val = self.add(a,b)
                elif tok == '-':
                    val = self.subtract(a,b)
                elif tok == '*':
                    val = self.multiply(a,b)
                else:
                    # divide
                    try:
                        val = self.divide(a,b)
                    except ValueError as ve:
                        # Re-raise as ZeroDivisionError if appropriate
                        if 'zero' in str(ve).lower():
                            raise ZeroDivisionError("Division by zero.")
                        raise
                eval_stack.append(val)
            else:
                # number
                num = float(tok)
                # keep int type when applicable
                if num.is_integer():
                    num = int(num)
                eval_stack.append(num)

        if len(eval_stack) != 1:
            raise ValueError("Invalid expression")
        return eval_stack[0]
