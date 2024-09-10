"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""
"""
    simple_expression = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
"""

from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens

def parse_expression(tokens):
    return parse_simple_expression(tokens)

def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
    }
    # pprint(ast)

    tokens = tokenize("-(2+-(3))")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {
            "tag": "+",
            "left": {
                "position": 2,
                "tag": "number",
                "value": 2,
            },
            "right": {
                "tag": "negate",
                "value": {
                    "position": 6,
                    "tag": "number",
                    "value": 3,
                },
            },
        },
    }


def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))

    #testing factor = simple expression
    for s in ["(3+(2-4))", "300", "-(3+(2-4))"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)

    #added code to fix bug
    while len(tokens) > 0 and tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    #term can be a factor.

    #testing when term = factor
    for s in ["100", "(100+100)", "-(100+100)"]:
        assert parse_term(tokenize(s))==parse_factor(tokenize(s))

    #term can be a factor * factor
    tokens=tokenize("100*3")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {"position": 0, "tag": "number", "value": 100},
        "right": {"position": 4, "tag": "number", "value": 3},
    }

    #term can be a factor/factor
    tokens=tokenize("10/5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "/",
        "left": {"position": 0, "tag": "number", "value": 10},
        "right": {"position": 3, "tag": "number", "value": 5},
    }


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    #modified line because an expression can be a term or a term +/- term
    while len(tokens) > 0 and tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression")
    #expression can be a term
    
    #testing when expression is a term
    for s in ["1", "(1+3)", "-(1+-4)", "3*5", "3/(2-1)"]:
        tokens = tokenize(s)
        assert parse_expression(tokens) == parse_term(tokens)
    

    #testing when expression is term +/- term
    tokens = tokenize("3+4")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "+",
        "left": {"position": 0, "tag": "number", "value": 3},
        "right": {"position": 2, "tag": "number", "value": 4},
    }

    tokens = tokenize("4-3")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "-",
        "left": {"position": 0, "tag": "number", "value": 4},
        "right": {"position": 2, "tag": "number", "value": 3},
    }


if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    print("done")
