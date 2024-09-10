# tokenizer

""" 
break character stream into tokens, provide a token stream 
"""

import re

patterns = [
    ["\\(", "("],
    ["\\)", ")"],
    ["\\+", "+"],
    ["\\-", "-"],
    ["\\*", "*"],
    ["\\/", "/"],
    ["(\\d+\\.\\d*)|(\\d*\\.\\d+)|(\\d+)", "number"],
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])


def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break
        assert match
        token = {
            "tag": tag,
            "value": match.group(0),
            "position": position,
        }
        tokens.append(token)
        # print(position)
        position = match.end()
        # print(len(characters))
    for token in tokens:
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    return tokens


def test_simple_tokens():
    # print("testing simple tokens")
    # assert tokenize("+") == [{"tag": "+", "value": "+", "position": 0}]
    # assert tokenize("-") == [{"tag": "-", "value": "-", "position": 0}]
    i = 0
    for char in "+-*/()":
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i
    for characters in ["+", "-"]:
        tokens = tokenize(characters)
        assert tokens[0]["tag"] == characters
        assert tokens[0]["value"] == characters
    for number in ["123.45", "1.", ".1", "123"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
        assert tokens[0]["value"] == float(number)

    testString ='+-*/()'
    tokens = tokenize(testString)
    for i in range(len(testString)):
        assert tokens[i]["tag"] == testString[i]
        assert tokens[i]["value"] == testString[i]
        assert tokens[i]["position"] == i



if __name__ == "__main__":
    test_simple_tokens()
    print("done.")
