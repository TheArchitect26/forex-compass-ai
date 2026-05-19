"""Reinforcement Learning Engine — stub for Stable-Baselines3 PPO agent.

Wire a `gymnasium.Env` over historical OHLCV and train PPO to learn
when to *issue* signals (not when to trade — execution stays human).
"""
from __future__ import annotations

STUB = """\
Implement:
1. ForexSignalEnv(gym.Env): obs = technical features, action = {hold, signal_long, signal_short}.
2. Reward = realized R-multiple of the signal (read from journal).
3. PPO('MlpPolicy', env).learn(total_timesteps=...).
4. Save under /app/models/ppo_signal.zip and load in signal_intelligence.
"""


def status() -> dict:
    return {"implemented": False, "notes": STUB}
