# 🏔️ Hill Climbing Game - Human vs AI

A competitive climbing game that demonstrates three different AI strategies in action: **Heuristic Search**, **Adversarial Search**, and **Fuzzy Logic**.

## 🎯 Game Objectives

- Race to the top of a climbing wall against an AI opponent
- Avoid obstacles that can block your progress
- Learn how different AI strategies make decisions
- Experience dynamic AI behavior that adapts to game situations

## 🤖 AI Strategies Demonstrated

### 1. Heuristic Search
- **Purpose**: Evaluates the best path based on current position
- **Logic**: Chooses paths with the least obstacles and shortest distance to top
- **Formula**: `Score = (1/distance_to_top) - (obstacle_count × 0.3)`

### 2. Adversarial Search
- **Purpose**: Predicts and blocks opponent moves
- **Logic**: 
  - Predicts player's best heuristic move
  - Positions AI to block if behind
  - Continues optimal path if ahead
- **Condition**: Blocks when `|ai_col - player_col| ≤ 1` and `ai_row ≥ player_row`

### 3. Fuzzy Logic
- **Purpose**: Dynamic risk assessment based on game phase
- **Game Phases**:
  - **Early** (< 33% turns): High risk, aggressive moves
  - **Mid** (33-66% turns): Medium risk, balanced approach
  - **Late** (> 66% turns): Low risk, conservative moves
- **Risk Levels**: Adjusts obstacle penalties and speed bonuses

## 🎮 How to Play

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Controls
- **1/2/3**: Move left/straight/right
- **H**: Switch to Heuristic Search AI
- **A**: Switch to Adversarial Search AI  
- **F**: Switch to Fuzzy Logic AI
- **R**: Restart game
- **P**: Toggle AI strategy panel
- **ESC**: Quit game

### Game Rules
1. **Setup**: Both players start at the bottom of a climbing wall
2. **Turns**: Players take turns selecting a path and moving up
3. **Obstacles**: Red obstacles block progress and cause you to skip a turn
4. **Winning**: First player to reach the top wins
5. **Strategy**: Choose paths with fewer obstacles for better progress

## 🖥️ UI Features

### Main Game View
- **Climbing Wall**: Visual grid showing obstacles and player positions
- **Player Indicators**: 👤 (Human) and 🤖 (AI)
- **Obstacles**: Red squares with ⚠️ symbols
- **Finish Line**: Green line at the top

### AI Strategy Panel
- Shows current AI strategy and decision reasoning
- Displays move evaluations and scores
- Explains why the AI chose a particular move
- Updates in real-time during gameplay

### Game Statistics
- Move counts for both players
- Obstacles hit by each player
- Current leader and distance ahead

## 🧠 Educational Value

This game demonstrates key AI concepts:

1. **Search Algorithms**: How AI evaluates multiple options
2. **Adversarial Intelligence**: How AI predicts and counters opponents
3. **Fuzzy Logic**: How AI makes decisions with uncertainty
4. **Game Theory**: Strategic decision making in competitive environments
5. **Heuristics**: Using rules of thumb to make quick decisions

## 🏗️ Technical Architecture

### Core Components
- **GameState**: Manages wall generation, positions, and game rules
- **AIStrategies**: Implements the three AI decision-making algorithms
- **GameUI**: PyGame-based graphical interface
- **AIAgent**: Coordinates AI strategies and decision making

### Key Algorithms
```python
# Heuristic Search
score = (1/distance_to_top) - (obstacles_ahead × 0.3)

# Adversarial Search  
if can_block and not ai_ahead:
    move = blocking_move_with_best_heuristic_score()

# Fuzzy Logic
risk_adjustment = obstacles_ahead × risk_weight
final_score = base_score + risk_adjustment + speed_bonus
```

## 🎯 Game Features

- **Dynamic Wall Generation**: Random obstacles with guaranteed winning paths
- **Multiple AI Strategies**: Switch between different AI approaches
- **Educational Panel**: Learn how AI makes decisions
- **Real-time Statistics**: Track game progress and performance
- **Visual Feedback**: Clear indication of moves, obstacles, and positions

## 🔧 Customization

You can modify the game by adjusting:
- **Wall Size**: Change `height` and `width` in `GameState`
- **Obstacle Density**: Modify `obstacle_density` parameter
- **AI Parameters**: Adjust scoring weights in `AIStrategies`
- **Visual Style**: Customize colors and symbols in `GameUI`

## 📚 Related Projects

- [Hill Climb Racing AI](https://github.com/Code-Bullet/Hill-Climb-Racing-AI)
- [Checkers with Minimax](https://github.com/cpappas18/checkers)
- [EasyAI Framework](https://github.com/Zulko/easyAI)

## 🤝 Contributing

Feel free to contribute improvements:
- Add new AI strategies
- Enhance the UI
- Improve game balance
- Add new features

## 📄 License

This project is open source and available under the MIT License.
