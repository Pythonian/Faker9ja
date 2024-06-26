"""Utility file that provides functions to load json files and validate its data structure."""

import json
import random
from pathlib import Path
from typing import Any


def load_json(file_path: str | Path, required_keys: list[str]) -> list[dict[str, Any]]:
    """Load data from a JSON file and validate its structure.

    Args:
        file_path (str | Path): The path to the JSON file.
        required_keys (list[str]): The keys that each entry in the JSON data must have.

    Returns:
        list[dict[str, Any]]: The data loaded from the JSON file.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        ValueError: If the JSON data is invalid or missing required keys.
    """
    try:
        with Path(file_path).open(encoding="utf-8") as file:
            data = json.load(file)
            validate_json_structure(data, required_keys)
            return data
    except FileNotFoundError:
        msg = f"File not found: {file_path}"
        raise FileNotFoundError(msg) from None
    except json.JSONDecodeError as exc:
        msg = f"Error decoding JSON from file: {file_path}"
        raise ValueError(msg) from exc


def validate_json_structure(
    data: list[dict[str, Any]],
    required_keys: list[str],
) -> None:
    """Validate the structure of the JSON data.

    Args:
        data (list[dict[str, Any]]): The JSON data to validate.
        required_keys (list[str]): The keys that each entry in the JSON data must have.

    Raises:
        ValueError: If any entry is missing a required key or contains extra keys.
    """
    for entry in data:
        entry_keys = set(entry.keys())
        required_keys_set = set(required_keys)

        missing_keys = required_keys_set - entry_keys
        invalid_keys = entry_keys - required_keys_set

        if missing_keys:
            msg = f"Missing keys {missing_keys} in entry: {entry}"
            raise ValueError(msg)
        if invalid_keys:
            msg = f"Invalid keys {invalid_keys} in entry: {entry}"
            raise ValueError(msg)


def get_unique_value(values: list[str], used_values: set[str]) -> str:
    """Helper method to get a unique value from a list of values.

    Ensures the generated value is unique within the session by:
        * Checking available values against used values.
        * Resetting used values if all options are exhausted.

    Args:
        values (list[str]): The list of possible values.
        used_values (set[str]): The set of values that have already been used.

    Returns:
        str: A unique value from the list.
    """
    # Calculate the set difference to find values that have not been used
    available_values = set(values) - used_values

    # If no values are available, reset the used values set
    if not available_values:
        used_values.clear()
        available_values = set(values)

    # Return a randomly chosen value from the available values
    return random.choice(list(available_values))
