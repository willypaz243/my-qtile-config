import json
import os
from typing import TypedDict


class Colors(TypedDict):
    bg: str
    fg: str
    selection: str
    red: str
    green: str
    yellow: str
    blue: str
    magenta: str
    cyan: str


def load_colors(theme: str) -> Colors:
    colors_path = os.path.join(os.path.dirname(__file__), "assets/colors.json")
    with open(colors_path, "r") as f:
        colors: Colors = json.loads(f.read())[theme]
    return colors
