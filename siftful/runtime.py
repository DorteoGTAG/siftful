from __future__ import annotations

import ast
import re
from typing import Any, List, Optional, Tuple

from .lexer import Lexer, SiftfulSyntaxError


class Parser:
    """Parses a small subset of SIFTFUL into executable statement dictionaries."""

    def __init__(self) -> None:
        self.lexer = Lexer()

    @staticmethod
    def _strip_comment(line: str) -> str:
        if "#" in line:
            return line.split("#", 1)[0]
        return line

    def parse(self, source: str) -> List[dict]:
        if not source or not source.strip():
            return []

        lines = source.splitlines()
        statements: List[dict] = []
        index = 0

        while index < len(lines):
            raw = self._strip_comment(lines[index])
            if not raw.strip():
                index += 1
                continue

            line = raw.strip()
            if line.startswith("if.inst"):
                condition, index, then_block, else_block = self._parse_if_block(lines, index)
                statements.append({
                    "type": "if",
                    "condition": condition,
                    "then": then_block,
                    "else": else_block,
                })
                continue

            if line.startswith("else.inst"):
                raise SiftfulSyntaxError("Unexpected else without a matching if.")

            statements.append(self._parse_statement(line))
            index += 1

        return statements

    def _parse_if_block(self, lines: List[str], index: int) -> Tuple[str, int, List[dict], List[dict]]:
        line = self._strip_comment(lines[index]).strip()
        match = re.match(r"^if\.inst\((.*)\)\s*(?:\{)?\s*$", line)
        if not match:
            raise SiftfulSyntaxError(f"Invalid if statement: {line}")

        condition = match.group(1).strip()
        idx = index + 1
        then_block: List[dict] = []
        else_block: List[dict] = []

        while idx < len(lines):
            current = self._strip_comment(lines[idx]).strip()
            if not current:
                idx += 1
                continue
            if current.startswith("}"):
                idx += 1
                break
            if current.startswith("else.inst"):
                break
            then_block.append(self._parse_statement(current))
            idx += 1

        while idx < len(lines):
            current = self._strip_comment(lines[idx]).strip()
            if not current:
                idx += 1
                continue
            if current.startswith("else.inst"):
                match_else = re.match(r"^else\.inst\(\)\s*(?:\{)?\s*$", current)
                if not match_else:
                    raise SiftfulSyntaxError(f"Invalid else statement: {current}")
                idx += 1
                while idx < len(lines):
                    current_else = self._strip_comment(lines[idx]).strip()
                    if not current_else:
                        idx += 1
                        continue
                    if current_else == "}":
                        idx += 1
                        break
                    else_block.append(self._parse_statement(current_else))
                    idx += 1
                break
            if current == "}":
                idx += 1
                break
            break

        return condition, idx, then_block, else_block

    def _parse_statement(self, line: str) -> dict:
        if not line:
            raise SiftfulSyntaxError("Empty statement.")

        if line.startswith("print.inst"):
            args = self._extract_call_arguments(line, "print.inst")
            return {"type": "print", "value": args[0] if args else ""}

        if line.startswith("new.varible"):
            arg = self._extract_call_arguments(line, "new.varible")
            if len(arg) != 1:
                raise SiftfulSyntaxError("new.varible expects exactly one argument.")
            return {"type": "new_var", "name": arg[0]}

        if line.startswith("game.title"):
            return {"type": "game_set", "field": "title", "value": self._extract_call_arguments(line, "game.title")[0]}

        if line.startswith("game.player"):
            return {"type": "game_set", "field": "player", "value": self._extract_call_arguments(line, "game.player")[0]}

        if line.startswith("game.win"):
            return {"type": "game_win", "value": self._extract_call_arguments(line, "game.win")[0]}

        if line.startswith("game.lose"):
            return {"type": "game_lose", "value": self._extract_call_arguments(line, "game.lose")[0]}

        if line.startswith("game.score"):
            if "=" in line:
                left, right = line.split("=", 1)
                return {"type": "assign", "target": left.strip(), "value": right.strip()}

        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*(\+=|-=|\*=|/=)\s*.+$", line):
            target, op, expr = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*(\+=|-=|\*=|/=)\s*(.+)$", line).groups()
            return {"type": "compound_assign", "target": target, "op": op, "value": expr.strip()}

        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*=\s*.+$", line):
            target, expr = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$", line).groups()
            return {"type": "assign", "target": target, "value": expr.strip()}

        if re.match(r"^game\.score\s*[:=].+$", line):
            left, right = line.split("=", 1)
            return {"type": "assign", "target": left.strip(), "value": right.strip()}

        raise SiftfulSyntaxError(f"Unsupported statement: {line}")

    def _extract_call_arguments(self, line: str, function_name: str) -> List[str]:
        pattern = rf"^{re.escape(function_name)}\((.*)\)$"
        match = re.match(pattern, line.strip())
        if not match:
            raise SiftfulSyntaxError(f"Invalid call syntax: {line}")
        args_text = match.group(1).strip()
        if not args_text:
            return []
        # Keep simple comma-separated parsing only.
        return [part.strip() for part in args_text.split(",")]

    def parse_expression(self, text: str) -> ast.AST:
        sanitized = self._normalize_expression(text)
        return ast.parse(sanitized, mode="eval").body

    def _normalize_expression(self, expr: str) -> str:
        expr = expr.strip()
        expr = expr.replace("true", "True").replace("false", "False")
        expr = expr.replace("&&", " and ").replace("||", " or ")
        # Fix simple SIFTFUL comparisons like `score > 50` is already valid Python syntax.
        return expr
