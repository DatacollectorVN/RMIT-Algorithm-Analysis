map_symbols = {
    "(": ")",
    "[": "]",
    "{": "}",
}

def is_valid_parentheses(s: str) -> bool:
    stack = []
    for char in s:
        if char in map_symbols:
            stack.append(char)
        elif char in map_symbols.values():
            if not stack:
                return False
            stack_top = stack.pop()
            closed_symbol = map_symbols[stack_top]
            if closed_symbol != char:
                return False
    return not stack

if __name__ == "__main__":
    print(is_valid_parentheses("()"))
    print(is_valid_parentheses("()[]{}"))
    print(is_valid_parentheses("(]"))
    print(is_valid_parentheses("([)]"))
    print(is_valid_parentheses("{[]}"))