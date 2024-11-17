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

### Q-Learning

Q-Learning is a reinforcement learning algorithm that allows the agent to make optimal decisions based on learned state-action values.

#### Application in Splendor
- Models long-term strategies by learning the value of state-action pairs.
- Adapts dynamically to changing game conditions.

#### Key Benefits
- Enables self-learning and dynamic improvement.
- Effective for long-term reward maximization.

#### Limitations
- Requires a large number of iterations to converge.
- Struggles with high-dimensional state spaces.

---

### Breadth-First Search (BFS)

BFS is a graph traversal algorithm that explores all possible nodes layer by layer, guaranteeing the shortest path in unweighted graphs.

#### Application in Splendor
- Evaluates reachable states quickly to identify immediate gains.
- Useful for planning short-term actions, like resource collection.

#### Key Benefits
- Ensures the shortest path in unweighted scenarios.
- Efficient for shallow state trees.

#### Limitations
- Inefficient for deep or expansive search spaces.
- Limited by the complexity of Splendor’s game tree.

---

### Minimax Algorithm

The Minimax algorithm is a decision-making framework designed for adversarial games, optimizing for the best possible outcome against an opponent.

#### Application in Splendor
- Predicts and counters opponent moves.
- Utilizes heuristics to focus on relevant game states.

#### Key Benefits
- Robust against adversarial strategies.
- Ensures optimal defensive and offensive play.

#### Limitations
- Computationally intensive without optimizations.
- Performance degrades with deep state trees unless pruned.

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