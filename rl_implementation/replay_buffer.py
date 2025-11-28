"""
ReplayBuffer: Experience replay for DQN
Stores transitions and samples random batches for training
"""

import random
import numpy as np
from collections import deque


class ReplayBuffer:
    """
    Fixed-size buffer to store experience tuples (s, a, r, s', done)
    """

    def __init__(self, capacity):
        """
        Args:
            capacity: Maximum number of transitions to store
        """
        self.buffer = deque(maxlen=capacity)
        self.capacity = capacity

    def push(self, state, action, reward, next_state, done):
        """
        Add a new transition to the buffer

        Args:
            state: Current state (np.array)
            action: Action taken (int)
            reward: Reward received (float)
            next_state: Next state (np.array)
            done: Whether episode ended (bool)
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """
        Sample a random batch of transitions

        Args:
            batch_size: Number of transitions to sample

        Returns:
            Tuple of (states, actions, rewards, next_states, dones)
            Each as np.array with batch dimension
        """
        batch = random.sample(self.buffer, batch_size)

        states = np.array([t[0] for t in batch], dtype=np.float32)
        actions = np.array([t[1] for t in batch], dtype=np.int64)
        rewards = np.array([t[2] for t in batch], dtype=np.float32)
        next_states = np.array([t[3] for t in batch], dtype=np.float32)
        dones = np.array([t[4] for t in batch], dtype=np.float32)

        return states, actions, rewards, next_states, dones

    def __len__(self):
        """Return current size of buffer"""
        return len(self.buffer)

    def clear(self):
        """Clear all transitions from buffer"""
        self.buffer.clear()


class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay (optional enhancement)
    Samples important transitions more frequently based on TD error
    """

    def __init__(self, capacity, alpha=0.6):
        """
        Args:
            capacity: Maximum number of transitions to store
            alpha: How much prioritization to use (0 = uniform, 1 = fully prioritized)
        """
        self.buffer = deque(maxlen=capacity)
        self.priorities = deque(maxlen=capacity)
        self.capacity = capacity
        self.alpha = alpha
        self.max_priority = 1.0

    def push(self, state, action, reward, next_state, done):
        """Add transition with maximum priority"""
        self.buffer.append((state, action, reward, next_state, done))
        self.priorities.append(self.max_priority)

    def sample(self, batch_size, beta=0.4):
        """
        Sample batch with prioritization

        Args:
            batch_size: Number of transitions to sample
            beta: Importance sampling weight (0 = no correction, 1 = full correction)

        Returns:
            Tuple of (states, actions, rewards, next_states, dones, indices, weights)
        """
        # Convert priorities to probabilities
        priorities = np.array(self.priorities, dtype=np.float32)
        probs = priorities ** self.alpha
        probs /= probs.sum()

        # Sample indices based on priorities
        indices = np.random.choice(len(self.buffer), batch_size, p=probs, replace=False)

        # Compute importance sampling weights
        total = len(self.buffer)
        weights = (total * probs[indices]) ** (-beta)
        weights /= weights.max()  # Normalize for stability

        # Extract transitions
        batch = [self.buffer[idx] for idx in indices]
        states = np.array([t[0] for t in batch], dtype=np.float32)
        actions = np.array([t[1] for t in batch], dtype=np.int64)
        rewards = np.array([t[2] for t in batch], dtype=np.float32)
        next_states = np.array([t[3] for t in batch], dtype=np.float32)
        dones = np.array([t[4] for t in batch], dtype=np.float32)

        return states, actions, rewards, next_states, dones, indices, weights

    def update_priorities(self, indices, priorities):
        """
        Update priorities for sampled transitions

        Args:
            indices: Indices of transitions to update
            priorities: New priorities (e.g., TD errors)
        """
        for idx, priority in zip(indices, priorities):
            self.priorities[idx] = priority
            self.max_priority = max(self.max_priority, priority)

    def __len__(self):
        """Return current size of buffer"""
        return len(self.buffer)

    def clear(self):
        """Clear all transitions and priorities"""
        self.buffer.clear()
        self.priorities.clear()
        self.max_priority = 1.0
