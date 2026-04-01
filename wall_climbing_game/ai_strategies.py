import random
from typing import Tuple, List, Dict, Optional
from game_state import GameState

class AIStrategies:
    """Implements the three AI strategies: Heuristic Search, Adversarial Search, and Fuzzy Logic."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        
    def heuristic_search(self, ai_position: Tuple[int, int]) -> Tuple[int, Dict]:
        """
        Heuristic Search: Evaluate paths based on obstacles and distance to top.
        Returns: (best_move, decision_info)
        """
        available_moves = self.game_state.get_available_moves(ai_position)
        scores = {}
        
        for move in available_moves:
            # Calculate new position after move
            row, col = ai_position
            new_col = self._get_new_column(col, move)
            new_row = max(0, row - 1)
            new_pos = (new_row, new_col)
            
            # Skip if obstacle at destination
            if self.game_state.wall[new_row, new_col] == 1:
                scores[move] = {
                    'score': -10,  # Very low score for obstacle
                    'distance_to_top': self.game_state.get_distance_to_top(new_pos),
                    'obstacles_ahead': 1,
                    'obstacle_density': 1.0
                }
                continue
            
            # Calculate distance to top from new position
            distance_to_top = self.game_state.get_distance_to_top(new_pos)
            
            # Count obstacles in path ahead
            obstacles_ahead = self.game_state.get_obstacles_ahead(new_pos, 1)  # Look straight ahead
            
            # Calculate obstacle density
            path_length = min(5, distance_to_top)
            obstacle_density = obstacles_ahead / max(1, path_length)
            
            # Heuristic score: prioritize shorter distance and fewer obstacles
            distance_score = 1.0 / max(1, distance_to_top)
            obstacle_penalty = obstacles_ahead * 0.3
            
            score = distance_score - obstacle_penalty
            scores[move] = {
                'score': score,
                'distance_to_top': distance_to_top,
                'obstacles_ahead': obstacles_ahead,
                'obstacle_density': obstacle_density
            }
        
        # Choose move with highest score
        if scores:
            best_move = max(scores.keys(), key=lambda m: scores[m]['score'])
        else:
            best_move = 1  # Default to center move
            
        decision_info = {
            'strategy': 'Heuristic Search',
            'scores': scores,
            'selected_move': best_move,
            'reasoning': f"Chose move {best_move} with score {scores.get(best_move, {}).get('score', 0):.2f}"
        }
        
        return best_move, decision_info
    
    def adversarial_search(self, ai_position: Tuple[int, int], player_position: Tuple[int, int]) -> Tuple[int, Dict]:
        """
        Adversarial Search: Predict player's move and potentially block them.
        Returns: (best_move, decision_info)
        """
        # Predict player's best heuristic move
        player_moves = self.game_state.get_available_moves(player_position)
        player_scores = {}
        
        for move in player_moves:
            row, col = player_position
            new_col = self._get_new_column(col, move)
            new_row = max(0, row - 1)
            
            # Skip if obstacle
            if self.game_state.wall[new_row, new_col] == 1:
                player_scores[move] = -10
                continue
                
            obstacles_ahead = self.game_state.get_obstacles_ahead((new_row, new_col), 1)
            distance_to_top = new_row  # Distance is the row index
            
            distance_score = 1.0 / max(1, distance_to_top)
            obstacle_penalty = obstacles_ahead * 0.3
            player_scores[move] = distance_score - obstacle_penalty
        
        if player_scores:
            predicted_player_move = max(player_scores.keys(), key=lambda m: player_scores[m])
        else:
            predicted_player_move = 1
            
        # Calculate player's predicted new position
        player_row, player_col = player_position
        player_new_col = self._get_new_column(player_col, predicted_player_move)
        player_new_row = max(0, player_row - 1)
        player_new_pos = (player_new_row, player_new_col)
        
        # Check if AI can block player (only if not at obstacle)
        ai_row, ai_col = ai_position
        ai_new_row = max(0, ai_row - 1)
        
        # AI can block if it moves to same column as player's predicted position
        # and is at the same row level after moving
        can_block = (player_new_row == ai_new_row and 
                    self.game_state.wall[ai_new_row, player_new_col] == 0)
        
        if can_block and not self.game_state.is_ai_ahead():
            # Try to move to player's predicted column
            blocking_moves = []
            for move in self.game_state.get_available_moves(ai_position):
                new_col = self._get_new_column(ai_col, move)
                if new_col == player_new_col:
                    blocking_moves.append(move)
            
            if blocking_moves:
                # Choose the first blocking move (prioritize blocking)
                best_move = blocking_moves[0]
                strategy = "Blocking"
            else:
                # Fall back to heuristic search
                best_move, _ = self.heuristic_search(ai_position)
                strategy = "Heuristic (No Block Available)"
        else:
            # AI is ahead or can't block, use heuristic search
            best_move, _ = self.heuristic_search(ai_position)
            strategy = "Heuristic (AI Ahead)" if self.game_state.is_ai_ahead() else "Heuristic (Can't Block)"
        
        decision_info = {
            'strategy': 'Adversarial Search',
            'sub_strategy': strategy,
            'predicted_player_move': predicted_player_move,
            'player_predicted_position': player_new_pos,
            'can_block': can_block,
            'selected_move': best_move,
            'reasoning': f"Predicted player move {predicted_player_move}, strategy: {strategy}"
        }
        
        return best_move, decision_info
    
    def fuzzy_logic(self, ai_position: Tuple[int, int], player_position: Tuple[int, int]) -> Tuple[int, Dict]:
        """
        Fuzzy Logic: Dynamic risk assessment based on game phase and relative positions.
        Returns: (best_move, decision_info)
        """
        game_phase = self.game_state.get_game_phase()
        is_ai_ahead = self.game_state.is_ai_ahead()
        leader_distance = self.game_state.get_leader_distance()
        
        # Determine risk level based on game phase and position
        if game_phase == "early" and not is_ai_ahead:
            risk_level = "high"
            risk_weight = 0.8  # Favor aggressive moves
        elif game_phase == "mid" and leader_distance <= 2:
            risk_level = "medium"
            risk_weight = 0.5  # Balanced approach
        else:
            risk_level = "low"
            risk_weight = 0.2  # Conservative approach
        
        # Evaluate moves with risk consideration
        available_moves = self.game_state.get_available_moves(ai_position)
        move_evaluations = {}
        
        for move in available_moves:
            # Calculate new position
            row, col = ai_position
            new_col = self._get_new_column(col, move)
            new_row = max(0, row - 1)
            new_pos = (new_row, new_col)
            
            # Skip if obstacle at destination
            if self.game_state.wall[new_row, new_col] == 1:
                move_evaluations[move] = {
                    'score': -10,
                    'obstacles_ahead': 1,
                    'distance_to_top': new_row,
                    'risk_adjustment': 0,
                    'speed_bonus': 0
                }
                continue
            
            obstacles_ahead = self.game_state.get_obstacles_ahead(new_pos, 1)
            distance_to_top = new_row
            
            # Base heuristic score
            distance_score = 1.0 / max(1, distance_to_top)
            obstacle_penalty = obstacles_ahead * 0.3
            
            # Risk adjustment based on risk level
            if risk_level == "high":
                # High risk: prioritize speed over safety
                risk_adjustment = obstacles_ahead * -0.1  # Less penalty for obstacles
                speed_bonus = distance_score * 0.3
            elif risk_level == "medium":
                # Medium risk: balanced approach
                risk_adjustment = 0
                speed_bonus = 0
            else:
                # Low risk: prioritize safety
                risk_adjustment = obstacles_ahead * 0.2  # More penalty for obstacles
                speed_bonus = -distance_score * 0.1
            
            final_score = distance_score - obstacle_penalty + risk_adjustment + speed_bonus
            
            move_evaluations[move] = {
                'score': final_score,
                'obstacles_ahead': obstacles_ahead,
                'distance_to_top': distance_to_top,
                'risk_adjustment': risk_adjustment,
                'speed_bonus': speed_bonus
            }
        
        # Choose best move based on fuzzy evaluation
        if move_evaluations:
            best_move = max(move_evaluations.keys(), key=lambda m: move_evaluations[m]['score'])
        else:
            best_move = 1
            
        decision_info = {
            'strategy': 'Fuzzy Logic',
            'game_phase': game_phase,
            'risk_level': risk_level,
            'risk_weight': risk_weight,
            'is_ai_ahead': is_ai_ahead,
            'leader_distance': leader_distance,
            'move_evaluations': move_evaluations,
            'selected_move': best_move,
            'reasoning': f"Phase: {game_phase}, Risk: {risk_level}, AI ahead: {is_ai_ahead}"
        }
        
        return best_move, decision_info
    
    def _get_new_column(self, current_col: int, move: int) -> int:
        """Helper method to get new column position."""
        if move == 0:  # Left
            return max(0, current_col - 1)
        elif move == 1:  # Center
            return current_col
        else:  # Right
            return min(self.game_state.width - 1, current_col + 1)

class AIAgent:
    """Main AI agent that combines all strategies."""
    
    def __init__(self, game_state: GameState):
        self.strategies = AIStrategies(game_state)
        self.game_state = game_state
        
    def make_move(self, strategy: str = "fuzzy") -> Tuple[int, Dict]:
        """
        Make an AI move using the specified strategy.
        Returns: (move, decision_info)
        """
        ai_pos = self.game_state.ai_pos
        player_pos = self.game_state.player_pos
        
        if strategy == "heuristic":
            return self.strategies.heuristic_search(ai_pos)
        elif strategy == "adversarial":
            return self.strategies.adversarial_search(ai_pos, player_pos)
        elif strategy == "fuzzy":
            return self.strategies.fuzzy_logic(ai_pos, player_pos)
        else:
            # Default to fuzzy logic
            return self.strategies.fuzzy_logic(ai_pos, player_pos)
