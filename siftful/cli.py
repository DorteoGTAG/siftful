from __future__ import annotations

import ast
import re
from typing import Any, Dict, List, Optional

from .parser import Parser, SiftfulSyntaxError
from .runtime import SiftfulRuntime


class SiftfulInterpreter:
    def __init__(self, runtime: Optional[SiftfulRuntime] = None) -> None:
        self.runtime = runtime or SiftfulRuntime()
        self.parser = Parser()

    def run(self, source: str) -> List[str]:
        statements = self.parser.parse(source)
        for statement in statements:
            self.execute_statement(statement)
        return self.runtime.output

    def execute_statement(self, statement: Dict[str, Any]) -> None:
        kind = statement.get("type")

        if kind == "print":
            self.runtime.print_value(self.evaluate_value(statement.get("value", "")))
            return

        if kind == "new_var":
            self.runtime.new_variable(statement["name"])
            return

        if kind == "assign":
            target = statement["target"]
            value = self.evaluate_value(statement["value"])
            if target == "game.score":
                self.runtime.set_game_score(value)
            else:
                self.runtime.assign(target, value)
            return

        if kind == "compound_assign":
            target = statement["target"]
            base = self.runtime.get_variable(target)
            expr = self.evaluate_value(statement["value"])
            op = statement["op"]
            if op == "+=":
                result = base + expr
            elif op == "-=":
                result = base - expr
            elif op == "*=":
                result = base * expr
            elif op == "/=":
                result = base / expr
            else:
                raise SiftfulSyntaxError(f"Unsupported operator: {op}")
            self.runtime.assign(target, result)
            return

        if kind == "if":
            condition_result = self.evaluate_condition(statement["condition"])
            if condition_result:
                for sub in statement.get("then", []):
                    self.execute_statement(sub)
            else:
                for sub in statement.get("else", []):
                    self.execute_statement(sub)
            return

        if kind == "game_set":
            self.runtime.set_game(statement["field"], self.evaluate_value(statement["value"]))
            return

        if kind == "game_win":
            self.runtime.set_game("win_message", self.evaluate_value(statement["value"]))
            self.runtime.print_value(self.evaluate_value(statement["value"]))
            return

        if kind == "game_lose":
            self.runtime.set_game("lose_message", self.evaluate_value(statement["value"]))
            self.runtime.print_value(self.evaluate_value(statement["value"]))
            return

        raise SiftfulSyntaxError(f"Unknown statement type: {kind}")

    def evaluate_value(self, value: Any) -> Any:
        if isinstance(value, (int, float, bool, str)):
            return value

        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                return value[1:-1]
            if value.startswith("'") and value.endswith("'"):
                return value[1:-1]
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
            if re.fullmatch(r"[0-9]+", value):
                return int(value)
            if re.fullmatch(r"[0-9]+\.[0-9]+", value):
                return float(value)
            if value in self.runtime.variables:
                return self.runtime.variables[value]
            if value in self.runtime.game:
                return self.runtime.game[value]
            return value

        raise SiftfulSyntaxError(f"Unsupported value: {value!r}")

    def evaluate_condition(self, condition: str) -> bool:
        expr = condition.strip()
        expr = expr.replace("true", "True").replace("false", "False")
        namespace = {**self.runtime.variables, **self.runtime.game}
        try:
            return bool(eval(expr, {"__builtins__": {}}, namespace))
        except Exception as exc:
            raise SiftfulSyntaxError(f"Invalid condition: {condition}") from exc
