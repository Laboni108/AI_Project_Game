import random
import numpy as np
from typing import Tuple, List, Dict, Optional

class GameState:
    """Manages the game state including the climbing wall, player positions, and obstacles."""
    
    def __init__(self, height: int = 20, width: int = 5, obstacle_density: float = 0.3):
        self.height = height
        self.width = width
        self.obstacle_density = obstacle_density
        
        # Initialize positions (bottom of wall)
        self.player_pos = (height - 1, width // 2)  # Center column
        self.ai_pos = (height - 1, width // 2 + 1)  # Next to player
        
        # Generate climbing wall with obstacles
        self.wall = self._generate_wall()
        
        # Game tracking
        self.turn_counter = 0
        self.player_moves = 0
        self.ai_moves = 0
        self.player_obstacles_hit = 0
        self.ai_obstacles_hit = 0
        self.game_over = False
        self.winner = None
        
    def _generate_wall(self) -> np.ndarray:
        """Generate a random climbing wall with obstacles."""
        wall = np.zeros((self.height, self.width), dtype=int)
        
        # Add obstacles randomly (1 = obstacle, 0 = clear path)
        for row in range(self.height):
            for col in range(self.width):
                if random.random() < self.obstacle_density:
                    wall[row, col] = 1
                    
        # Ensure starting positions are clear
        wall[self.player_pos] = 0
        wall[self.ai_pos] = 0
        
        # Clear a continuous path in the best column
        obstacle_counts = np.sum(wall, axis=0)
        best_column = np.argmin(obstacle_counts)
        
        # Clear a continuous path in the best column
        for row in range(self.height):
            wall[row, best_column] = 0
        
        return wall
    
    def get_available_moves(self, position: Tuple[int, int]) -> List[int]:
        """Get available moves for a position (0=left, 1=center, 2=right)."""
        row, col = position
        moves = []
        
        # Left move
        if col > 0:
            moves.append(0)
        # Center move (stay in same column)
        moves.append(1)
        # Right move
        if col < self.width - 1:
            moves.append(2)
            
        return moves
    
    def move_player(self, move: int) -> bool:
        """Move player and return True if successful."""
        if self.game_over:
            return False
            
        row, col = self.player_pos
        new_col = self._get_new_column(col, move)
        
        # Move up one row
        new_row = max(0, row - 1)
        
        # Check for obstacles at the destination
        if self.wall[new_row, new_col] == 1:
            self.player_obstacles_hit += 1
            # Don't move when hitting obstacle
            return True
            
        # Update position
        self.player_pos = (new_row, new_col)
        self.player_moves += 1
        
        # Check win condition - must reach top row (row 0)
        if new_row == 0:
            self.game_over = True
            self.winner = "Human"
            
        return True
    
    def move_ai(self, move: int) -> bool:
        """Move AI and return True if successful."""
        if self.game_over:
            return False
            
        row, col = self.ai_pos
        new_col = self._get_new_column(col, move)
        
        # Move up one row
        new_row = max(0, row - 1)
        
        # Check for obstacles at the destination
        if self.wall[new_row, new_col] == 1:
            self.ai_obstacles_hit += 1
            # Don't move when hitting obstacle
            return True
            
        # Update position
        self.ai_pos = (new_row, new_col)
        self.ai_moves += 1
        
        # Check win condition - must reach top row (row 0)
        if new_row == 0:
            self.game_over = True
            self.winner = "AI"
            
        return True
    
    def _get_new_column(self, current_col: int, move: int) -> int:
        """Convert move (0,1,2) to new column position."""
        if move == 0:  # Left
            return max(0, current_col - 1)
        elif move == 1:  # Center
            return current_col
        else:  # Right
            return min(self.width - 1, current_col + 1)
    
    def get_obstacles_ahead(self, position: Tuple[int, int], move: int) -> int:
        """Count obstacles in the path for the next 5 rows."""
        row, col = position
        new_col = self._get_new_column(col, move)
        
        obstacles = 0
        for i in range(1, min(6, row + 1)):  # Look ahead 5 rows
            if row - i >= 0 and self.wall[row - i, new_col] == 1:
                obstacles += 1
                
        return obstacles
    
    def get_distance_to_top(self, position: Tuple[int, int]) -> int:
        """Get distance from position to top of wall."""
        return position[0]
    
    def get_game_phase(self) -> str:
        """Determine current game phase based on turn counter."""
        estimated_turns = self.height * 2  # Rough estimate
        if estimated_turns == 0:
            return "early"
            
        phase_ratio = self.turn_counter / estimated_turns
        
        if phase_ratio < 0.33:
            return "early"
        elif phase_ratio < 0.66:
            return "mid"
        else:
            return "late"
    
    def is_ai_ahead(self) -> bool:
        """Check if AI is ahead of player."""
        return self.ai_pos[0] < self.player_pos[0]
    
    def get_leader_distance(self) -> int:
        """Get distance between leader and follower."""
        return abs(self.ai_pos[0] - self.player_pos[0])
