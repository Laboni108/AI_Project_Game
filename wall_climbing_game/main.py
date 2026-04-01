import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from game_ui_tk import HillClimbingGameTk
except ImportError:
    print("Error: game_ui_tk.py not found. Make sure all files are in the same directory.")
    sys.exit(1)

def main():
    """Main entry point for the Hill Climbing game."""
    print("=" * 60)
    print("HILL CLIMBING GAME - HUMAN vs AI")
    print("=" * 60)
    print()
    print("Game Objectives:")
    print("• Race to the top of the climbing wall")
    print("• Avoid obstacles that block your progress")
    print("• Watch the AI use different strategies to compete")
    print()
    print("Controls:")
    print("• 1/2/3: Move left/straight/right")
    print("• H/A/F: Switch AI strategy (Heuristic/Adversarial/Fuzzy)")
    print("• R: Restart game")
    print()
    print("AI Strategies:")
    print("• Heuristic Search: Evaluates paths based on obstacles")
    print("• Adversarial Search: Predicts and blocks your moves")
    print("• Fuzzy Logic: Dynamic risk assessment")
    print()
    print("Starting game...")
    print("=" * 60)
    
    try:
        # Create and run the game
        game = HillClimbingGameTk()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"\nError running game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
