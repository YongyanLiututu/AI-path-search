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
1. **Strategic Depth**: Combines short-term planning, long-term learning, and adversarial reasoning.
2. **Dynamic Adaptation**: Adjusts strategies dynamically based on game progress and opponent actions.
3. **Scalable Framework**: Modular design supports easy integration of additional techniques or improvements.

### Combined Limitations
1. **State-Space Complexity**: Handling large state spaces remains challenging despite heuristic and neural network optimizations.
2. **Computation Overhead**: Hybrid strategies require careful balancing of computational resources and response time.
3. **Parameter Sensitivity**: Effective performance depends on hyperparameter tuning (e.g., learning rates, exploration probabilities, heuristic weights).

---

## 6. How to Run the Project

Follow these steps to execute the Splendor agent:

### Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>


### 
# This README serves as a comprehensive guide to understanding, setting up, and running the Splendor Autonomous Agent project. Contributions and suggestions for improvement are always welcome!
=======
```

### AI-path-search
Splendor Autonomous Agent  An intelligent agent designed to autonomously play the board game Splendor using advanced AI techniques, including Q-Learning, Breadth-First Search (BFS), and the Minimax algorithm. This project showcases strategic decision-making and adaptability in a competitive game environment.
>>>>>>> ad009635de0f3570debdb34a71f4f70539aef461



# 中文版：

# Splendor 自动化代理 - 项目概述

欢迎来到 Splendor 自动化代理项目！本项目旨在构建一个能够自主玩 **Splendor** 桌游的智能代理。目标是开发一个使用高级技术进行战略决策的竞争性 AI 系统。

---

## 目录

1. [项目概述](#项目概述)
2. [文件结构](#文件结构)
3. [安装与先决条件](#安装与先决条件)
4. [使用的算法](#使用的算法)
    - [Q-Learning](#q-learning-基于神经网络的函数近似)
    - [广度优先搜索 (BFS)](#广度优先搜索-bfs-与-a-启发式结合)
    - [极小极大算法 (Minimax)](#极小极大算法-与蒙特卡洛方法和-alpha-beta剪枝结合)
5. [优缺点分析](#优缺点分析)
6. [如何运行项目](#如何运行项目)

---

## 1. 项目概述

Splendor 是一款资源管理类的策略游戏，玩家需要通过收集资源、购买卡片并赚取积分来竞争胜利。本项目的目标是通过以下 AI 算法设计一个能够自主玩游戏的智能代理：

1. **Q-Learning**：通过奖励动态学习策略。
2. **广度优先搜索 (BFS)**：确定最优的短期路径。
3. **极小极大算法 (Minimax)**：评估对手策略并制定最优应对方案。

通过结合这些方法，代理能够平衡即时奖励、长期目标和防御性策略，以优于对手的表现完成游戏。

---

## 2. 文件结构

项目的文件组织如下：

|-- agents/ |-- myAgent.py # 智能代理的主要实现 |-- wiki-template/ # 项目文档模板 |-- docker/ # Docker 配置文件 |-- README.md # 项目概述与说明 |-- Splendor/ # 游戏相关资源与设置 |-- requirements.txt # Python 依赖列表

### 关键组件

- **`agents/myAgent.py`**：Splendor AI 代理的核心实现。
- **`docker/`**：用于设置可复现运行环境的脚本。
- **`requirements.txt`**：所需 Python 库的列表。

---

## 3. 安装与先决条件

### 软件要求

1. **Python 3.8 或更高版本**
2. **Docker**（可选，用于一致性运行）
3. 推荐的 IDE：**Visual Studio Code** 或 **PyCharm**

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone <repository_url>
   cd <repository_directory>

```
2. 安装 Python 依赖：
```bash
    复制代码
    pip install -r requirements.txt
```
3. （可选）设置 Docker：
```bash
    复制代码
    cd docker
    docker-compose up
```

## 4. 使用的算法

---

### 1. Q-Learning 基于神经网络的函数近似

Q-Learning 是一种强化学习算法，代理通过学习状态-动作对的价值来决策。本项目使用 **深度神经网络** 替代传统的 Q 表，从而扩展到复杂、高维的状态空间。

### 在 Splendor 中的应用
- 将游戏状态（如资源、卡片、对手进度）编码为特征向量。
- 使用 **Bellman 方程** 更新 Q 值：
  \[
  Q(s, a) \gets Q(s, a) + \alpha \big[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \big]
  \]
  其中 \(s\) 是当前状态，\(a\) 是动作，\(r\) 是奖励，\(\gamma\) 是折扣因子。
- 训练一个 **深度 Q 网络 (DQN)** 以近似连续动作空间的 Q 值。

### 高级优化
1. **经验回放 (Experience Replay)**：存储转移 \((s, a, r, s')\)，打破连续样本的相关性，提高收敛速度。
2. **目标网络 (Target Network)**：使用独立的目标网络稳定 Q 值估计。
3. **奖励设计 (Reward Shaping)**：设计针对 Splendor 目标（如购买高价值卡片）的奖励函数。

### 优点
- 可处理复杂的多维状态空间。
- 通过观察对手动作学习动态策略。

### 缺点
- 训练过程中计算量大，需要 GPU 加速以提高效率。
- 如果探索与利用的平衡调节不当，可能会过拟合特定场景。

---

### 2. 广度优先搜索 (BFS) 与 A* 启发式结合

标准 BFS 按层探索所有可能状态。本项目结合了 **A* 启发式**，优先探索更有前景的游戏状态。

#### 在 Splendor 中的应用
- 找到优化行动序列以最大化 **短期资源效率**（例如收集宝石或购买卡片）。
- 集成启发式估计，如：
  \[
  h(n) = \text{购买下一张卡片所需资源缺口}
  \]
  \(h(n)\) 估算从当前状态转移到目标状态所需的努力。

#### 高级优化
1. **多目标启发式 (Multi-Objective Heuristics)**：综合考虑卡片价值、资源效率和对手干扰概率。
2. **动态剪枝 (Adaptive Pruning)**：基于 Splendor 特定阈值（如不切实际的资源组合）排除低概率状态。

#### 优点
- 快速识别短期最优路径。
- 保证完整性（如果有解，必能找到）。

#### 缺点
- 对于深层嵌套状态计算开销大。
- 局限于局部优化，无法考虑长期策略。

---

### 3. 极小极大算法 与蒙特卡洛方法和 Alpha-Beta 剪枝结合

极小极大算法扩展了 **蒙特卡洛方法** 和 **Alpha-Beta 剪枝**，用于优化对抗性决策。

#### 在 Splendor 中的应用
- 通过评估游戏树模拟对手行为：
  \[
  \text{Value}(s) = \max_a \min_b \big( \text{Utility}(s, a, b) \big)
  \]
  其中 \(a\) 和 \(b\) 分别表示代理和对手的动作。
- 使用 **效用函数** 评估游戏状态：
  \[
  U(s) = \text{获得的积分} + w_1 \cdot \text{资源平衡} - w_2 \cdot \text{对手优势}
  \]

#### 高级优化
1. **蒙特卡洛方法 (Monte Carlo Rollouts)**：在搜索深度限制之外模拟随机玩法，估计未来结果。
2. **Alpha-Beta 剪枝**：通过跳过无关状态减少探索分支：
 如果 $ \alpha \geq \beta $，剪枝此分支。

3. **对手建模 (Opponent Modeling)**：根据观察动态调整对手的效用（例如进攻型与防守型玩法）。

#### 优点
- 在对抗场景中提供稳健的规划。
- 有效平衡防守与进攻策略。

#### 缺点
- 高度依赖搜索深度和效用函数的质量。
- 如果没有启发式剪枝，计算成本较高。

---

## 4. 混合策略：结合 Q-Learning、BFS 和 Minimax

为应对 Splendor 的多样性挑战，代理采用 **混合策略**：

- **Q-Learning** 提供基于经验的长期策略。
- **BFS 启发式** 确保即时收益最大化。
- **Minimax** 提供对抗场景下的强力防御与应对。

### 动态角色分配
1. **开局阶段**：BFS 确定最佳资源收集路径，建立早期优势。
2. **中期策略**：Q-Learning 基于不断变化的游戏条件优化策略。
3. **终局防御**：Minimax 应对对手策略，确保最优的结束表现。

---

## 5. 优缺点分析

### 综合优点
1. **战略深度**：结合短期规划、长期学习与对抗性推理。
2. **动态适应**：根据游戏进程和对手动作动态调整策略。
3. **可扩展框架**：模块化设计支持额外技术或改进的轻松集成。

### 综合缺点
1. **状态空间复杂度**：尽管有优化，仍难以完全解决大状态空间问题。
2. **计算开销**：混合策略需要平衡计算资源和响应时间。
3. **参数敏感性**：算法性能依赖于超参数调节（如学习率、探索概率、启发式权重）。
