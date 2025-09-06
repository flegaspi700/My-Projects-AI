import sys
from dotenv import load_dotenv
from pkg.calculator import Calculator
from pkg.render import render_boxed_expression, render_boxed_answer

def main():
    load_dotenv()
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("No expression provided.")
        print("Usage: python main.py <expression>")
        print("Example: python main.py '2 + 2")
        sys.exit(1)


    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        render_boxed_expression(expression, result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()