from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


class SiftfulSyntaxError(Exception):
    pass


class Lexer:
    """A compact tokenizer for SIFTFUL statements and expressions."""

    def tokenize_line(self, text: str, line_no: int) -> List[Token]:
        if text is None:
            return []

        text = text.strip()
        if not text:
            return []

        tokens: List[Token] = []
        i = 0
        column = 1

        while i < len(text):
            ch = text[i]

            if ch.isspace():
                i += 1
                column += 1
                continue

            if ch in "(){}[],:;":
                tokens.append(Token(ch, ch, line_no, column))
                i += 1
                column += 1
                continue

            if ch in "+-*/%":
                tokens.append(Token("OP", ch, line_no, column))
                i += 1
                column += 1
                continue

            if ch in "=<>!":
                if i + 1 < len(text) and text[i:i + 2] in {"==", "!=", ">=", "<="}:
                    tokens.append(Token("OP", text[i:i + 2], line_no, column))
                    i += 2
                    column += 2
                else:
                    tokens.append(Token("OP", ch, line_no, column))
                    i += 1
                    column += 1
                continue

            if ch in "'\"":
                quote = ch
                start = i
                i += 1
                column += 1
                value_chars = []
                while i < len(text):
                    current = text[i]
                    if current == "\\":
                        if i + 1 < len(text):
                            value_chars.append(text[i + 1])
                            i += 2
                            column += 2
                            continue
                    if current == quote:
                        i += 1
                        column += 1
                        break
                    value_chars.append(current)
                    i += 1
                    column += 1
                else:
                    raise SiftfulSyntaxError(f"Unterminated string literal on line {line_no}.")

                tokens.append(Token("STRING", "".join(value_chars), line_no, start))
                continue

            if ch.isdigit() or (ch == "." and i + 1 < len(text) and text[i + 1].isdigit()):
                start = i
                seen_dot = ch == "."
                i += 1
                column += 1
                while i < len(text) and (text[i].isdigit() or (text[i] == "." and not seen_dot)):
                    if text[i] == ".":
                        seen_dot = True
                    i += 1
                    column += 1
                tokens.append(Token("NUMBER", text[start:i], line_no, start))
                continue

            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                column += 1
                while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                    i += 1
                    column += 1
                value = text[start:i]
                if value in {"true", "false"}:
                    tokens.append(Token("BOOLEAN", value, line_no, start))
                elif value in {"and", "or", "not"}:
                    tokens.append(Token("LOGIC", value, line_no, start))
                else:
                    tokens.append(Token("IDENT", value, line_no, start))
                continue

            if ch == ".":
                tokens.append(Token("DOT", ".", line_no, column))
                i += 1
                column += 1
                continue

            raise SiftfulSyntaxError(f"Unexpected character '{ch}' on line {line_no}.")

        return tokens
