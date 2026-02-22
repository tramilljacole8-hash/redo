"""
redo.py - Efficient undo/redo stack implementation in Python.

Provides a CommandHistory class that manages undo and redo operations
using two stacks (collections.deque) for O(1) push/pop performance.
"""

from collections import deque


class Command:
    """Represents a reversible command with execute and undo callables."""

    def __init__(self, execute, undo, description=""):
        self._execute = execute
        self._undo = undo
        self.description = description

    def execute(self):
        self._execute()

    def undo(self):
        self._undo()


class CommandHistory:
    """
    Manages a history of executed commands supporting undo and redo.

    Uses two deques for O(1) amortised push/pop on both ends.
    An optional *maxlen* argument caps memory usage by discarding the
    oldest undoable commands when the limit is exceeded.
    """

    def __init__(self, maxlen=None):
        self._undo_stack = deque(maxlen=maxlen)
        self._redo_stack = deque()

    # ------------------------------------------------------------------
    # Core interface
    # ------------------------------------------------------------------

    def execute(self, command):
        """Execute *command* and push it onto the undo stack."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        """Undo the most-recently executed command.

        Returns the undone :class:`Command`, or ``None`` if there is
        nothing to undo.
        """
        if not self._undo_stack:
            return None
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return command

    def redo(self):
        """Re-execute the most-recently undone command.

        Returns the re-executed :class:`Command`, or ``None`` if there
        is nothing to redo.
        """
        if not self._redo_stack:
            return None
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return command

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    def can_undo(self):
        """Return ``True`` if there is at least one command to undo."""
        return bool(self._undo_stack)

    def can_redo(self):
        """Return ``True`` if there is at least one command to redo."""
        return bool(self._redo_stack)

    def clear(self):
        """Clear both stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    @property
    def undo_count(self):
        """Number of commands available to undo."""
        return len(self._undo_stack)

    @property
    def redo_count(self):
        """Number of commands available to redo."""
        return len(self._redo_stack)
