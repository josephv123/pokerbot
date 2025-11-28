"""
DQN Agent: Dueling Double DQN with target network
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random

from replay_buffer import ReplayBuffer
from config import *


class DuelingQNetwork(nn.Module):
    """
    Dueling DQN architecture:
    - Shared feature extraction
    - Separate value and advantage streams
    - Q(s,a) = V(s) + (A(s,a) - mean(A(s,a)))
    """

    def __init__(self, state_dim=STATE_DIM, action_dim=ACTION_DIM,
                 hidden_dim=HIDDEN_DIM, value_hidden=VALUE_HIDDEN,
                 advantage_hidden=ADVANTAGE_HIDDEN):
        super(DuelingQNetwork, self).__init__()

        # Shared feature extraction
        self.feature = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )

        # Value stream: V(s)
        self.value_stream = nn.Sequential(
            nn.Linear(hidden_dim, value_hidden),
            nn.ReLU(),
            nn.Linear(value_hidden, 1)
        )

        # Advantage stream: A(s,a)
        self.advantage_stream = nn.Sequential(
            nn.Linear(hidden_dim, advantage_hidden),
            nn.ReLU(),
            nn.Linear(advantage_hidden, action_dim)
        )

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        """He initialization for ReLU networks"""
        if isinstance(module, nn.Linear):
            nn.init.kaiming_normal_(module.weight, mode='fan_in', nonlinearity='relu')
            if module.bias is not None:
                nn.init.constant_(module.bias, 0)

    def forward(self, state):
        """
        Forward pass

        Args:
            state: (batch, state_dim) or (state_dim,)

        Returns:
            q_values: (batch, action_dim) or (action_dim,)
        """
        # Shared features
        features = self.feature(state)

        # Value and advantages
        value = self.value_stream(features)
        advantages = self.advantage_stream(features)

        # Dueling aggregation: Q(s,a) = V(s) + (A(s,a) - mean(A))
        q_values = value + (advantages - advantages.mean(dim=-1, keepdim=True))

        return q_values


class DQNAgent:
    """
    Double DQN agent with dueling architecture and experience replay
    """

    def __init__(self, state_dim=STATE_DIM, action_dim=ACTION_DIM,
                 lr=LR, gamma=GAMMA, tau=TAU, buffer_size=BUFFER_SIZE,
                 device=None):
        """
        Args:
            state_dim: Dimension of state space
            action_dim: Number of discrete actions
            lr: Learning rate
            gamma: Discount factor
            tau: Soft update parameter for target network
            buffer_size: Replay buffer capacity
            device: torch device (cpu or cuda)
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.tau = tau

        # Device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device

        # Networks
        self.q_network = DuelingQNetwork(state_dim, action_dim).to(self.device)
        self.target_network = DuelingQNetwork(state_dim, action_dim).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()  # Target network always in eval mode

        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr,
                                     weight_decay=WEIGHT_DECAY)

        # Replay buffer
        self.buffer = ReplayBuffer(buffer_size)

        # Exploration
        self.epsilon = EPSILON_START

        # Training stats
        self.total_steps = 0
        self.training_steps = 0

    def act(self, state, valid_actions_mask=None, epsilon=None):
        """
        Select action using epsilon-greedy policy

        Args:
            state: Current state (np.array of shape (state_dim,))
            valid_actions_mask: Boolean mask of valid actions (np.array of shape (action_dim,))
            epsilon: Exploration rate (if None, uses self.epsilon)

        Returns:
            action: Selected action index
        """
        if epsilon is None:
            epsilon = self.epsilon

        # Epsilon-greedy exploration
        if random.random() < epsilon:
            # Random action from valid actions
            if valid_actions_mask is not None:
                valid_actions = np.where(valid_actions_mask)[0]
                return random.choice(valid_actions)
            else:
                return random.randint(0, self.action_dim - 1)
        else:
            # Greedy action
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.q_network(state_tensor).cpu().numpy()[0]

                # Mask invalid actions
                if valid_actions_mask is not None:
                    q_values[~valid_actions_mask] = -float('inf')

                return int(np.argmax(q_values))

    def step(self, state, action, reward, next_state, done):
        """
        Store transition and train if ready

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode ended
        """
        # Store in replay buffer
        self.buffer.push(state, action, reward, next_state, done)
        self.total_steps += 1

    def learn(self, batch_size=BATCH_SIZE):
        """
        Sample batch and update Q-network using Double DQN

        Args:
            batch_size: Size of batch to sample

        Returns:
            loss: Training loss (float) or None if not enough samples
        """
        if len(self.buffer) < batch_size:
            return None

        # Sample batch
        states, actions, rewards, next_states, dones = self.buffer.sample(batch_size)

        # Convert to tensors
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        # Current Q values: Q(s, a)
        q_values = self.q_network(states).gather(1, actions)

        # Double DQN: use online network to select action, target network to evaluate
        with torch.no_grad():
            # Select best actions using online network
            next_actions = self.q_network(next_states).argmax(1, keepdim=True)
            # Evaluate using target network
            next_q_values = self.target_network(next_states).gather(1, next_actions)
            # Compute targets: r + γ * Q_target(s', argmax_a Q_online(s', a))
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values

        # Huber loss (smooth L1) - more robust than MSE
        loss = F.smooth_l1_loss(q_values, target_q_values)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), max_norm=10.0)
        self.optimizer.step()

        self.training_steps += 1

        return loss.item()

    def update_target_network(self, tau=None):
        """
        Soft update of target network: θ_target = τ*θ_online + (1-τ)*θ_target

        Args:
            tau: Update rate (if None, uses self.tau)
        """
        if tau is None:
            tau = self.tau

        for target_param, param in zip(self.target_network.parameters(),
                                        self.q_network.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)

    def decay_epsilon(self, decay_rate=EPSILON_DECAY):
        """Decay exploration rate"""
        self.epsilon = max(EPSILON_END, self.epsilon * decay_rate)

    def save(self, filepath):
        """Save model weights"""
        torch.save({
            'q_network': self.q_network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'total_steps': self.total_steps,
            'training_steps': self.training_steps
        }, filepath)

    def load(self, filepath):
        """Load model weights"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network'])
        self.target_network.load_state_dict(checkpoint['target_network'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint.get('epsilon', EPSILON_END)
        self.total_steps = checkpoint.get('total_steps', 0)
        self.training_steps = checkpoint.get('training_steps', 0)

    def set_eval_mode(self):
        """Set network to evaluation mode"""
        self.q_network.eval()

    def set_train_mode(self):
        """Set network to training mode"""
        self.q_network.train()

    def get_q_values(self, state):
        """
        Get Q-values for a state (for debugging/visualization)

        Args:
            state: State array

        Returns:
            q_values: Array of Q-values for each action
        """
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.q_network(state_tensor).cpu().numpy()[0]
        return q_values
