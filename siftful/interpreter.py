from __future__ import annotations

from typing import Any, Dict, List


class SiftfulRuntime:
    def __init__(self) -> None:
        self.variables: Dict[str, Any] = {}
        self.game: Dict[str, Any] = {
            "title": "",
            "player": "",
            "score": 0,
            "win_message": "",
            "lose_message": "",
        }
        self.output: List[str] = []

    def new_variable(self, name: str) -> None:
        if name in self.variables:
            return
        self.variables[name] = 0

    def assign(self, name: str, value: Any) -> None:
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        if name not in self.variables:
            raise NameError(f"Variable '{name}' is not defined.")
        return self.variables[name]

    def print_value(self, value: Any) -> None:
        self.output.append(str(value))

    def set_game(self, field: str, value: Any) -> None:
        self.game[field] = value

    def set_game_score(self, value: Any) -> None:
        self.game["score"] = value

    def get_value(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        if name in self.game:
            return self.game[name]
        raise NameError(f"Unknown symbol '{name}'.")
