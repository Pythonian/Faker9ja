"""This module provides the Degree mixin, which groups related methods for generating degree information using the DegreeProvider."""

import random

from fakernaija.providers.degree_provider import DegreeProvider


class Degree:
    """Methods for the DegreeProvider."""

    def __init__(self) -> None:
        """Initializes the Degree mixin and its provider."""
        self.degree_provider = DegreeProvider()
        self._used_degrees: set[str] = set()

    def degree(self, degree_type: str | None = None, initial: bool = False) -> str:
        """Generates a random degree or degree initial.

        Args:
            degree_type (str | None, optional): The type of degree to generate.
                                                Defaults to None (any degree type).
            initial (bool, optional): If True, returns the degree initial instead of the full name.
                                      Defaults to False.

        Returns:
            str: A random degree or degree initial.

        Example:
            .. code-block:: python

                >>> from fakernaija.faker import Faker
                >>> naija = Faker()

                >>> degree = naija.degree()
                >>> print(f"Random degree: {degree}")
                'Random degree: Bachelor of Science'

                >>> degree_initial = naija.degree(initial=True)
                >>> print(f"Random degree: {degree_initial}")
                'Random degree: B.Sc.'

                >>> degree = naija.degree(degree_type="undergraduate")
                >>> print(f"Random degree: {degree}")
                'Random degree: Bachelor of Science'

                >>> degree = naija.degree(degree_type="masters", initial=True)
                >>> print(f"Random degree: {degree}")
                'Random degree: M. Sc.'

        """
        if degree_type and degree_type not in ["undergraduate", "masters", "doctorate"]:
            msg = "Invalid degree_type. Must be one of 'undergraduate', 'masters', or 'doctorate'."
            raise ValueError(msg)

        if initial:
            degrees = self.degree_provider.get_degree_initials(degree_type)
        else:
            degrees = self.degree_provider.get_degrees(degree_type)
        degree = self._get_unique_value(degrees, self._used_degrees)
        self._used_degrees.add(degree)
        return degree

    def _get_unique_value(self, values: list[str], used_values: set[str]) -> str:
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
