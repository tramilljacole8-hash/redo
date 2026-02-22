"""Tests for redo.py"""

import unittest
from redo import Command, CommandHistory


class TestCommand(unittest.TestCase):
    def test_execute_calls_execute_callable(self):
        log = []
        cmd = Command(lambda: log.append("exec"), lambda: log.append("undo"))
        cmd.execute()
        self.assertEqual(log, ["exec"])

    def test_undo_calls_undo_callable(self):
        log = []
        cmd = Command(lambda: log.append("exec"), lambda: log.append("undo"))
        cmd.undo()
        self.assertEqual(log, ["undo"])

    def test_description(self):
        cmd = Command(lambda: None, lambda: None, description="my cmd")
        self.assertEqual(cmd.description, "my cmd")


class TestCommandHistory(unittest.TestCase):
    def _make_counter_command(self, counter, key):
        """Return a Command that increments counter[key] on execute and decrements on undo."""
        def execute():
            counter[key] = counter.get(key, 0) + 1

        def undo():
            counter[key] -= 1

        return Command(execute, undo, description=key)

    # ------------------------------------------------------------------
    # Basic execute / undo / redo
    # ------------------------------------------------------------------

    def test_execute_runs_command(self):
        state = {}
        history = CommandHistory()
        history.execute(self._make_counter_command(state, "a"))
        self.assertEqual(state["a"], 1)

    def test_undo_reverses_command(self):
        state = {}
        history = CommandHistory()
        history.execute(self._make_counter_command(state, "a"))
        history.undo()
        self.assertEqual(state["a"], 0)

    def test_redo_reapplies_command(self):
        state = {}
        history = CommandHistory()
        history.execute(self._make_counter_command(state, "a"))
        history.undo()
        history.redo()
        self.assertEqual(state["a"], 1)

    def test_undo_returns_command(self):
        history = CommandHistory()
        cmd = Command(lambda: None, lambda: None)
        history.execute(cmd)
        self.assertIs(history.undo(), cmd)

    def test_redo_returns_command(self):
        history = CommandHistory()
        cmd = Command(lambda: None, lambda: None)
        history.execute(cmd)
        history.undo()
        self.assertIs(history.redo(), cmd)

    # ------------------------------------------------------------------
    # Edge cases: nothing to undo / redo
    # ------------------------------------------------------------------

    def test_undo_empty_returns_none(self):
        self.assertIsNone(CommandHistory().undo())

    def test_redo_empty_returns_none(self):
        self.assertIsNone(CommandHistory().redo())

    # ------------------------------------------------------------------
    # New execute clears redo stack
    # ------------------------------------------------------------------

    def test_new_execute_clears_redo(self):
        state = {}
        history = CommandHistory()
        history.execute(self._make_counter_command(state, "a"))
        history.undo()
        # Executing a new command should discard the pending redo
        history.execute(self._make_counter_command(state, "b"))
        self.assertFalse(history.can_redo())
        self.assertEqual(history.redo_count, 0)

    # ------------------------------------------------------------------
    # can_undo / can_redo / counts
    # ------------------------------------------------------------------

    def test_can_undo_false_initially(self):
        self.assertFalse(CommandHistory().can_undo())

    def test_can_redo_false_initially(self):
        self.assertFalse(CommandHistory().can_redo())

    def test_can_undo_true_after_execute(self):
        history = CommandHistory()
        history.execute(Command(lambda: None, lambda: None))
        self.assertTrue(history.can_undo())

    def test_can_redo_true_after_undo(self):
        history = CommandHistory()
        history.execute(Command(lambda: None, lambda: None))
        history.undo()
        self.assertTrue(history.can_redo())

    def test_counts(self):
        history = CommandHistory()
        history.execute(Command(lambda: None, lambda: None))
        history.execute(Command(lambda: None, lambda: None))
        self.assertEqual(history.undo_count, 2)
        history.undo()
        self.assertEqual(history.undo_count, 1)
        self.assertEqual(history.redo_count, 1)

    # ------------------------------------------------------------------
    # clear
    # ------------------------------------------------------------------

    def test_clear_resets_both_stacks(self):
        history = CommandHistory()
        history.execute(Command(lambda: None, lambda: None))
        history.undo()
        history.clear()
        self.assertFalse(history.can_undo())
        self.assertFalse(history.can_redo())

    # ------------------------------------------------------------------
    # maxlen caps undo history
    # ------------------------------------------------------------------

    def test_maxlen_limits_undo_stack(self):
        history = CommandHistory(maxlen=3)
        for _ in range(5):
            history.execute(Command(lambda: None, lambda: None))
        self.assertEqual(history.undo_count, 3)

    # ------------------------------------------------------------------
    # Multiple undo / redo cycles
    # ------------------------------------------------------------------

    def test_multiple_undo_redo_cycles(self):
        state = {"value": 0}

        def make_add(n):
            return Command(
                lambda n=n: state.__setitem__("value", state["value"] + n),
                lambda n=n: state.__setitem__("value", state["value"] - n),
            )

        history = CommandHistory()
        history.execute(make_add(1))   # value = 1
        history.execute(make_add(2))   # value = 3
        history.execute(make_add(4))   # value = 7

        history.undo()                 # value = 3
        self.assertEqual(state["value"], 3)
        history.undo()                 # value = 1
        self.assertEqual(state["value"], 1)
        history.redo()                 # value = 3
        self.assertEqual(state["value"], 3)
        history.redo()                 # value = 7
        self.assertEqual(state["value"], 7)


if __name__ == "__main__":
    unittest.main()
