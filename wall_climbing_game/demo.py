#!/usr/bin/env python3
"""
Demo script to showcase the Hill Climbing Game AI strategies
without requiring the GUI. Perfect for testing and understanding
how the AI makes decisions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from ai_strategies import AIAgent

def print_wall(game_state):
    """Print the climbing wall in ASCII format."""
    print("\n" + "="*50)
    print("CLIMBING WALL")
    print("="*50)
    print("🏁 FINISH LINE")
    
    for row in range(game_state.height):
        line = ""
        for col in range(game_state.width):
            if game_state.wall[row, col] == 1:
                line += "⚠️ "
            elif game_state.player_pos == (row, col):
                line += "👤 "
            elif game_state.ai_pos == (row, col):
                line += "🤖 "
            else:
                line += "⬜ "
        print(f"Row {row:2d}: {line}")
    
    print("🏔️  BOTTOM")
    print("="*50)

def demo_ai_strategies():
    """Demonstrate all three AI strategies."""
    print("🏔️  HILL CLIMBING GAME - AI STRATEGY DEMO")
    print("="*60)
    
    # Create game state
    game_state = GameState(height=15, width=5, obstacle_density=0.25)
    ai_agent = AIAgent(game_state)
    
    print_wall(game_state)
    
    strategies = ["heuristic", "adversarial", "fuzzy"]
    strategy_names = ["Heuristic Search", "Adversarial Search", "Fuzzy Logic"]
    
    for i, (strategy, name) in enumerate(zip(strategies, strategy_names)):
        print(f"\n🤖 TESTING {name.upper()}")
        print("-" * 40)
        
        # Make AI move
        move, decision = ai_agent.make_move(strategy)
        
        print(f"AI Position: Row {game_state.ai_pos[0]}, Col {game_state.ai_pos[1]}")
        print(f"Player Position: Row {game_state.player_pos[0]}, Col {game_state.player_pos[1]}")
        print(f"Selected Move: {move} ({'Left' if move == 0 else 'Straight' if move == 1 else 'Right'})")
        print(f"Strategy: {decision.get('strategy', 'Unknown')}")
        print(f"Reasoning: {decision.get('reasoning', 'No reasoning provided')}")
        
        # Show strategy-specific details
        if strategy == "heuristic" and 'scores' in decision:
            print("\nMove Evaluations:")
            for move_num, info in decision['scores'].items():
                move_name = ['Left', 'Straight', 'Right'][move_num]
                print(f"  {move_name}: Score {info['score']:.2f}, Obstacles: {info['obstacles_ahead']}")
        
        elif strategy == "adversarial" and 'predicted_player_move' in decision:
            print(f"\nAdversarial Analysis:")
            print(f"  Predicted Player Move: {decision['predicted_player_move']}")
            print(f"  Can Block: {decision.get('can_block', False)}")
            print(f"  Sub-strategy: {decision.get('sub_strategy', 'Unknown')}")
        
        elif strategy == "fuzzy" and 'game_phase' in decision:
            print(f"\nFuzzy Logic Analysis:")
            print(f"  Game Phase: {decision.get('game_phase', 'Unknown')}")
            print(f"  Risk Level: {decision.get('risk_level', 'Unknown')}")
            print(f"  AI Ahead: {decision.get('is_ai_ahead', False)}")
            print(f"  Leader Distance: {decision.get('leader_distance', 0)}")
        
        print("-" * 40)

def simulate_game():
    """Simulate a short game to show strategy differences."""
    print("\n🎮 SIMULATING A SHORT GAME")
    print("="*60)
    
    game_state = GameState(height=10, width=3, obstacle_density=0.3)
    ai_agent = AIAgent(game_state)
    
    print_wall(game_state)
    
    # Simulate a few turns
    for turn in range(5):
        print(f"\n--- TURN {turn + 1} ---")
        
        # Player move (simulate random)
        import random
        player_moves = game_state.get_available_moves(game_state.player_pos)
        player_move = random.choice(player_moves)
        game_state.move_player(player_move)
        print(f"Player moves: {'Left' if player_move == 0 else 'Straight' if player_move == 1 else 'Right'}")
        
        if game_state.game_over:
            print(f"🎉 Game Over! Winner: {game_state.winner}")
            break
        
        # AI move with different strategies
        strategy = ["heuristic", "adversarial", "fuzzy"][turn % 3]
        ai_move, decision = ai_agent.make_move(strategy)
        game_state.move_ai(ai_move)
        print(f"AI moves: {'Left' if ai_move == 0 else 'Straight' if ai_move == 1 else 'Right'} (Strategy: {strategy})")
        
        if game_state.game_over:
            print(f"🎉 Game Over! Winner: {game_state.winner}")
            break
        
        game_state.turn_counter += 1
    
    print_wall(game_state)
    print(f"\nFinal Stats:")
    print(f"  Player Moves: {game_state.player_moves}")
    print(f"  AI Moves: {game_state.ai_moves}")
    print(f"  Player Obstacles Hit: {game_state.player_obstacles_hit}")
    print(f"  AI Obstacles Hit: {game_state.ai_obstacles_hit}")

if __name__ == "__main__":
    try:
        demo_ai_strategies()
        simulate_game()
        print("\n✅ Demo completed successfully!")
        print("Run 'python main.py' to play the full game with GUI!")
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        sys.exit(1)
