# Function to render the calculator answer inside an ASCII box
def render_boxed_answer(answer):
	answer_str = str(answer)
	width = len(answer_str) + 4
	print("+" + "-" * (width - 2) + "+")
	print(f"| {answer_str} |")
	print("+" + "-" * (width - 2) + "+")

# Function to render both the input expression and output answer inside a box
def render_boxed_expression(expression, answer):
	expr_str = f"Input: {expression}"
	answer_str = f"Output: {answer}"
	width = max(len(expr_str), len(answer_str)) + 4
	print("+" + "-" * (width - 2) + "+")
	print(f"| {expr_str.ljust(width - 4)} |")
	print(f"| {answer_str.ljust(width - 4)} |")
	print("+" + "-" * (width - 2) + "+")
