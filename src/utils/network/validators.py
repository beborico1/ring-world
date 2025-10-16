# src/network/validators.py
"""Validation functions for network messages."""

from typing import Dict, Any
from ..settings import MOVE_PHASES, VALID_COLORS


def validate_move_data(move_data: Dict[str, Any], logger) -> bool:
    """Validate move data before sending."""
    required_fields = ["type", "position", "color", "phase"]
    if not all(field in move_data for field in required_fields):
        logger(f"Invalid move data: missing required fields - {move_data}")
        return False

    if not isinstance(move_data["position"], list) or len(move_data["position"]) != 2:
        logger(f"Invalid position format: {move_data['position']}")
        return False

    if not all(isinstance(x, (int, float)) for x in move_data["position"]):
        logger(f"Invalid position values: {move_data['position']}")
        return False

    if move_data["type"] != "move":
        logger(f"Invalid move type: {move_data['type']}")
        return False

    if move_data["phase"] not in MOVE_PHASES:
        logger(f"Invalid phase: {move_data['phase']}")
        return False

    if move_data["color"] not in VALID_COLORS:
        logger(f"Invalid color: {move_data['color']}")
        return False

    return True
