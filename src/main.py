from sys import argv
from .Lexer import Lexer

parenthesis = 0


def parse(tokens):
    parsed = []
    i = 0
    while i < len(tokens):
        if tokens[i][0] == "OPEN":
            inner, length = parse(tokens[i + 1:])
            parsed.append(inner)
            i += length
        elif tokens[i][0] == "CLOSE":
            return parsed, i + 1
        elif tokens[i][0] == "DOTS":
            i += 1
            continue
        else:
            parsed.append(tokens[i])
        i += 1
    return parsed, i


def compute_sum(tokens):
    result = 0
    i = 0
    while i < len(tokens):
        if type(tokens[i]) == list:
            inner, length = compute([tokens[i]])
            inner = inner[1: -1] if inner[0] == '(' else inner
            inner_sum = 0
            for j in inner:
                if type(j) == tuple and j[0] == "NUMBER":
                    inner_sum += int(j[1])
                elif type(j) == str and j.isdigit():
                    inner_sum += int(j)
            result += inner_sum
        elif tokens[i][0] == "NUMBER":
            result += int(tokens[i][1])
        i += 1
    return result, i


def compute_cc(tokens):
    atoms = 0
    result = []
    i = 0

    while i < len(tokens):
        if type(tokens[i]) == list:
            inner, length = compute([tokens[i]])
            inner = inner[1: -1] if inner[0] == '(' else inner
            result += inner
        elif tokens[i][0] == "NUMBER":
            result.append(tokens[i][1])
            atoms += 1
        elif tokens[i][0] == "EMPTY_LIST" and atoms:
            result.append('()')

        i += 1
    return result, i


def compute_lambda(tokens):

    global parenthesis
    argument = tokens[1]
    not_replaceable = False
    body = []
    i = 2
    while i < len(tokens) - 1:
        if tokens[i][0] == "LAMBDA" and tokens[i + 1][0] == "ID":
            body.append(tokens[i])
            body.append(tokens[i + 1])
            if tokens[i + 1] == argument:
                not_replaceable = True
            i += 2
        else:
            if type(tokens[i]) == list or tokens[i][0] in ("ID", "NUMBER"):
                body.append(tokens[i])
                i += 1
                break
    parenthesis = 1 if type(body[0]) == list else 0
    value = tokens[i:] if len(tokens) - i > 1 else tokens[i]

    if not_replaceable:
        return body

    result = solve_lambda(value, argument, body)
    return result


def solve_lambda(value, argument, body):
    result = []
    i = 0
    while i < len(body):
        if type(body[i]) == list:
            inner = solve_lambda(value, argument, body[i])
            result.append(inner)
        elif body[i] == argument and body[i - 1][0] != "LAMBDA":
            if type(value) == list and value[0][0] == "LAMBDA":
                result += value
            else:
                result.append(value)
        else:
            result.append(body[i])
        i += 1
    return result


def compute(tokens):
    result = []
    i = 0
    last_op = ""
    while i < len(tokens):
        if type(tokens[i]) == list:
            inner, last_op = compute(tokens[i])
            if last_op == "lambda":
                del tokens[i]
                tokens = inner + tokens
            else:
                result += inner
                i += 1
        elif tokens[i][0] == "NUMBER":
            last_op = "number"
            result.append(tokens[i][1])
            i += 1
        elif tokens[i][0] == "EMPTY_LIST":
            last_op = "empty"
            result.append('()')
            i += 1
        elif tokens[i][0] == "SUM":
            last_op = "sum"
            if tokens[i + 1][0][0] in ("LAMBDA", "CONCAT", "SUM"):
                inner = compute(tokens[i + 1])[0]
                tokens[i + 1] = ('NUMBER', str(inner[0])) if tokens[i + 1][0][0] == "SUM" else inner
            else:
                sum, length = compute_sum(tokens[i + 1])
                result.append(str(sum))
                i += length + 1
        elif tokens[i][0] == "CONCAT":
            last_op = "concat"
            concat, length = compute_cc(tokens[i + 1])
            result += ['('] + concat + [')']
            i += length + 1
        elif tokens[i][0] == "LAMBDA":
            last_op = "lambda"
            inner = compute_lambda(tokens)
            return inner, last_op

    if result[0] == '(' or last_op == "sum":
        return result, last_op

    return ['('] + result + [')'], last_op


def check_parenthesis(tokens):
    stack = []
    for i, token in enumerate(tokens):
        if token[0] == "OPEN":
            stack.append(i)
        elif token[0] == "CLOSE":
            if not stack:
                return [i]
            else:
                stack.pop()
    return stack


def main():
    if len(argv) != 2:
        return

    filename = argv[1]
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    str_ = ''.join(lines)
    spec = [
        ("EMPTY_LIST", "()"),
        ("OPEN", "("),
        ("CLOSE", ")"),
        ("SPACE", "\\ "),
        ("NEWLINE", "\n"),
        ("TAB", "\t"),
        ("NUMBER", "[0-9]+"),
        ("SUM", "\\+"),
        ("CONCAT", "\\+\\+"),
        ("LAMBDA", "lambda"),
        ("DOTS", ":"),
        ("ID", "([a-z]|[A-Z])+")
    ]
    lexer = Lexer(spec)
    tokens = lexer.lex(str_)

    if tokens[0][0] == '':
        print("ERROR:", tokens[0][1])
        return

    stack = check_parenthesis(tokens)
    if stack:
        print("ERROR: parenthesis mismatch at postion", stack[-1] + 1)
        return

    tokens = [token for token in tokens if token[0] not in ["SPACE", "TAB", "NEWLINE"]]

    parsed = parse(tokens)[0]
    result, last_op = compute(parsed)

    if parenthesis == 1 and len(result) > 3:
        result = ['('] + result + [')']
    elif len(result) == 3 and last_op != "concat":
        result = result[1: -1]

    print(" ".join(result))


if __name__ == '__main__':
    main()