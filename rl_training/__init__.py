"""
rl_training
===========

Utilities, environments, and learning agents for the Random Number Texas Hold'Em
project. This package is intentionally self-contained so training code can run
without modifying the primary `pokerplayer.py` entrypoint used by the grader.
"""

from . import utils, poker_env, evaluate  # noqa: F401  (re-export for convenience)

__all__ = ["utils", "poker_env", "evaluate"]
