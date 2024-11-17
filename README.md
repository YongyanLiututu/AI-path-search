<<<<<<< HEAD
# Splendor Autonomous Agent - Project Overview

Welcome to the Splendor Autonomous Agent project! This project focuses on building an intelligent agent capable of playing the **Splendor** board game autonomously. The goal is to develop a competitive AI that uses advanced techniques for strategic decision-making.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [Setup and Prerequisites](#setup-and-prerequisites)
4. [Techniques Used](#techniques-used)
    - [Q-Learning](#q-learning)
    - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
    - [Minimax Algorithm](#minimax-algorithm)
5. [Advantages and Limitations](#advantages-and-limitations)
6. [How to Run the Project](#how-to-run-the-project)

---

## 1. Project Overview

Splendor is a strategic resource-management game where players compete to collect resources, purchase cards, and earn points. This project focuses on designing an autonomous agent to play Splendor by integrating the following AI techniques:

1. **Q-Learning**: Enables the agent to learn strategies dynamically through rewards.
2. **Breadth-First Search (BFS)**: Identifies optimal short-term paths.
3. **Minimax Algorithm**: Evaluates opponent strategies and ensures optimal counteractions.

By combining these methods, the agent balances immediate rewards, long-term goals, and defensive strategies to outperform opponents.

---

## 2. File Structure

The repository is structured as follows:

|-- agents/ |-- myAgent.py # Main implementation of the AI agent |-- wiki-template/ # Template for project documentation |-- docker/ # Docker setup files for environment replication |-- README.md # Project overview and instructions |-- Splendor/ # Game-specific resources and settings |-- requirements.txt # Python dependencies



### Key Components

- **`agents/myAgent.py`**: Core implementation of the Splendor AI agent.
- **`docker/`**: Scripts for setting up a replicable execution environment.
- **`requirements.txt`**: Lists all required Python libraries.

---

## 3. Setup and Prerequisites

### Software Requirements

1. **Python 3.8 or higher**
2. **Docker** (optional, for consistent execution)
3. Recommended IDE: **Visual Studio Code** or **PyCharm**

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. Install Python dependencies:
   pip install -r requirements.txt
3. (Optional) Set up Docker:
   cd docker
   docker-compose up


## 4. Techniques Used

### 1. Q-Learning with Neural Network-Based Function Approximation

Q-Learning is a reinforcement learning algorithm where the agent learns the value of state-action pairs. In this project, **deep neural networks** replace the Q-table, enabling scalability to complex and high-dimensional state spaces.

#### Application in Splendor
- Encodes game states (e.g., resources, cards, opponent progress) into a feature vector.
- Updates Q-values using the **Bellman Equation**:
  \[
  Q(s, a) \gets Q(s, a) + \alpha \big[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \big]
  \]
  where \(s\) is the current state, \(a\) is the action, \(r\) is the reward, and \(\gamma\) is the discount factor.
- Trains a **Deep Q-Network (DQN)** to approximate Q-values for continuous action spaces.

#### Advanced Enhancements
1. **Experience Replay**: Stores transitions \((s, a, r, s')\) in a buffer to break correlation between consecutive samples, improving convergence.
2. **Target Network**: A secondary network is periodically updated to stabilize Q-value estimates.
3. **Reward Shaping**: Tailored rewards encourage actions aligned with Splendor-specific goals, such as purchasing high-value cards or reserving critical resources.

#### Advantages
- Can handle complex, multi-dimensional state spaces.
- Learns dynamic strategies by observing the opponent’s actions over time.

#### Limitations
- Computationally intensive during training, requiring GPU acceleration for efficiency.
- May overfit to specific scenarios if exploration-exploitation tradeoff is not well-tuned.

---

### 2. Breadth-First Search (BFS) with A* Heuristic Integration

While standard BFS explores all possible states layer by layer, this project enhances it with **A*-like heuristics** to prioritize exploration of promising game states.

#### Application in Splendor
- Finds optimal sequences of actions to maximize **short-term resource efficiency** (e.g., collecting gems or purchasing cards).
- Integrates heuristic estimates, such as:
  \[
  h(n) = \text{resource deficit to purchase next card}
  \]
  where \(h(n)\) estimates the effort required to transition to a desired game state.

#### Advanced Enhancements
1. **Multi-Objective Heuristics**: Incorporates multiple factors, such as card value, resource efficiency, and opponent interference likelihood.
2. **Adaptive Pruning**: Dynamically excludes low-probability states based on Splendor-specific thresholds (e.g., impractical resource combinations).

#### Advantages
- Ensures fast identification of short-term optimal paths.
- Guarantees completeness (finds a solution if it exists).

#### Limitations
- Computationally expensive for deeply nested states without effective pruning.
- Limited to local optimization; lacks consideration for long-term strategies.

---

### 3. Minimax Algorithm with Monte Carlo Rollouts and Alpha-Beta Pruning

The Minimax algorithm is extended with **Monte Carlo rollouts** and **Alpha-Beta Pruning** to optimize adversarial decision-making.

#### Application in Splendor
- Simulates opponent behavior by evaluating the game tree:
  \[
  \text{Value}(s) = \max_a \min_b \big( \text{Utility}(s, a, b) \big)
  \]
  where \(a\) and \(b\) represent actions for the agent and opponent, respectively.
- Evaluates game states using a **utility function**:
  \[
  U(s) = \text{points gained} + w_1 \cdot \text{resource balance} - w_2 \cdot \text{opponent advantage}
  \]

#### Advanced Enhancements
1. **Monte Carlo Rollouts**: Simulates random plays beyond the depth limit to approximate future outcomes.
2. **Alpha-Beta Pruning**: Reduces the number of explored branches by skipping irrelevant states:
   \[
   \text{if } \alpha \geq \beta \text{, prune the branch.}
   \]
3. **Opponent Modeling**: Dynamically adjusts the opponent's utility based on observed tendencies (e.g., aggressive vs. defensive playstyles).

#### Advantages
- Provides robust planning in adversarial scenarios.
- Balances defensive and offensive strategies effectively.

#### Limitations
- Highly dependent on the depth of the search and quality of utility functions.
- Computationally expensive without heuristic-based pruning.

---

### 4. Hybrid Strategy: Combining Q-Learning, BFS, and Minimax

To address the diverse challenges of Splendor, the agent employs a **hybrid strategy** that integrates these techniques:
- **Q-Learning** drives long-term strategy by learning optimal policies from experience.
- **BFS with Heuristics** ensures short-term efficiency for immediate gains.
- **Minimax with Rollouts** enables robust responses to opponent moves in adversarial scenarios.

#### Dynamic Role Assignment
1. **Opening Moves**: BFS identifies optimal resource collection paths to establish an early advantage.
2. **Mid-Game Strategy**: Q-Learning refines strategies based on evolving game conditions.
3. **Late-Game Defense**: Minimax counters opponent strategies, ensuring optimal endgame performance.

---

## 5. Advantages and Limitations

### Combined Advantages
1. **Comprehensive Strategy**: Integrating Q-Learning, BFS, and Minimax ensures a balance between long-term planning and immediate action.
2. **Adaptability**: Q-Learning enables dynamic learning, while BFS and Minimax provide robust planning.
3. **Scalability**: Modular design allows for future enhancements.

### Combined Limitations
1. **State-Space Complexity**: Large state spaces can hinder BFS and Q-Learning performance.
2. **Computational Overhead**: Minimax’s efficiency is constrained without advanced optimizations like Alpha-Beta Pruning.
3. **Parameter Sensitivity**: Q-Learning requires careful tuning for optimal performance.

---

## 6. How to Run the Project

Follow these steps to execute the Splendor agent:

### Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>

# This README serves as a comprehensive guide to understanding, setting up, and running the Splendor Autonomous Agent project. Contributions and suggestions for improvement are always welcome!
=======
# AI-path-search
Splendor Autonomous Agent  An intelligent agent designed to autonomously play the board game Splendor using advanced AI techniques, including Q-Learning, Breadth-First Search (BFS), and the Minimax algorithm. This project showcases strategic decision-making and adaptability in a competitive game environment.
>>>>>>> ad009635de0f3570debdb34a71f4f70539aef461
