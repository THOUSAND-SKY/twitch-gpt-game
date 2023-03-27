import re
import textwrap


def truncate_wrap(text, width):
    new_lines = []
    for line in text.split("\n"):
        l = textwrap.fill(line, width=width,
                          replace_whitespace=False, drop_whitespace=False)
        new_lines.append(l)
    return "\n".join(new_lines)


def max_lines(text, n):
    return "\n".join(text.split("\n")[-n:])


def text_square(text, width, height):
    return max_lines(truncate_wrap(text, width), height)


def test_text_square():
    ai_completion = """You  find yourself in a holding cell. The walls are made of thick concrete and there's only one door. You can hear growls and moans on the other side. You notice a small hole on the ceiling, maybe big enough to climb through. What do you do?

    Option 1: Check the door for a way to open it quietly and peek through to assess the situation.
    Option 2: Check the door for a way to open it quietly and peek through to assess the situation.
    Option 3: Climb the hole in the ceiling to try to escape.
    Option 4: Yell as loud as you can for help."""

    new_var = text_square(ai_completion, 100, 3)
    # print(new_var)
    assert new_var == """    Option 2: Check the door for a way to open it quietly and peek through to assess the situation.
    Option 3: Climb the hole in the ceiling to try to escape.
    Option 4: Yell as loud as you can for help."""

    comp = """abcdefg
"""
    new_var1 = text_square(comp, 3, 5)
    # print(new_var1)
    assert new_var1 == """abc
def
g
"""


def split_words_with_whitespace(text):
    ws = re.findall(r'\s*\S+', text)
    return ws, len(ws)


def test_split_words_with_whitespace():
    v, _ = split_words_with_whitespace("What do you do?")
    assert v[-1] == " do?"


def sentences(words):
    return re.findall(r'[^,.:?!;\n]*.', words)


if __name__ == '__main__':
    test_text_square()
    test_split_words_with_whitespace()
    print("All tests passed!")
