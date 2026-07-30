"""Lightweight Dependency Registry for Engine Subsystem.

Provides typed dependency registration, lookup, duplicate prevention, and lifecycle ownership.
Governed by 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

from typing import Any, TypeVar

from profileforge.engine.exceptions import DependencyError

T = TypeVar("T")


class DependencyRegistry:
    """Registry managing application service and subsystem instances."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}
        self._types: dict[type[Any], Any] = {}

    def register(self, name: str, instance: Any, instance_type: type[Any] | None = None) -> None:
        """Register a dependency instance by unique string name and optional type.

        Args:
            name: Unique string identifier for the dependency.
            instance: Dependency instance object.
            instance_type: Optional explicit type class.

        Raises:
            DependencyError: If a dependency with the same name or type is already registered.
        """
        if not name or not name.strip():
            raise DependencyError("Dependency name cannot be empty.")

        if name in self._services:
            raise DependencyError(f"Dependency with name '{name}' is already registered.")

        target_type = instance_type or type(instance)
        if target_type in self._types:
            raise DependencyError(
                f"Dependency of type '{target_type.__name__}' is already registered."
            )

        self._services[name] = instance
        self._types[target_type] = instance

    def get(self, name: str) -> Any:
        """Retrieve registered dependency instance by name.

        Args:
            name: Registered name.

        Returns:
            Dependency instance object.

        Raises:
            DependencyError: If dependency is not found.
        """
        if name not in self._services:
            raise DependencyError(f"No registered dependency found with name '{name}'.")
        return self._services[name]

    def get_by_type(self, target_type: type[T]) -> T:
        """Retrieve registered dependency instance by type class.

        Args:
            target_type: Expected class type.

        Returns:
            Dependency instance object.

        Raises:
            DependencyError: If dependency of specified type is not found.
        """
        if target_type not in self._types:
            raise DependencyError(
                f"No registered dependency found of type '{target_type.__name__}'."
            )
        instance = self._types[target_type]
        if not isinstance(instance, target_type):
            raise DependencyError(
                f"Registered dependency is not an instance of '{target_type.__name__}'."
            )
        return instance

    def has(self, name: str) -> bool:
        """Check if a dependency is registered by name."""
        return name in self._services

    def has_type(self, target_type: type[Any]) -> bool:
        """Check if a dependency is registered by type."""
        return target_type in self._types

    def clear(self) -> None:
        """Clear all registered dependencies and release instances."""
        self._services.clear()
        self._types.clear()

    @property
    def registered_names(self) -> list[str]:
        """Return list of all registered dependency names."""
        return list(self._services.keys())
