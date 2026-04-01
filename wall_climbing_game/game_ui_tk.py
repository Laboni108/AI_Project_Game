import tkinter as tk
from tkinter import messagebox, ttk
from game_state import GameState
from ai_strategies import AIAgent

class HillClimbingGameTk:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hill Climbing - Human vs AI")
        self.root.geometry("1500x950")
        self.root.configure(bg='#f8f9fa')
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#7c3aed',    # Purple
            'success': '#10b981',      # Green
            'warning': '#f59e0b',      # Orange
            'danger': '#ef4444',       # Red
            'light': '#f8f9fa',        # Light gray
            'dark': '#1f2937',         # Dark gray
            'surface': '#ffffff',      # White
            'accent': '#06b6d4',       # Cyan
            'muted': '#6b7280'         # Gray
        }
        
        self.game_state = GameState()
        self.ai_agent = AIAgent(self.game_state)
        self.current_strategy = "fuzzy"
        self.waiting_for_input = True
        self.last_ai_decision = None
        
        self.setup_ui()
        self.update_display()
        
        # Enhanced keyboard controls
        self.root.bind('<Key-a>', lambda e: self.make_player_move(0))        # A for Left
        self.root.bind('<Key-A>', lambda e: self.make_player_move(0))
        self.root.bind('<Key-s>', lambda e: self.make_player_move(1))        # S for Straight
        self.root.bind('<Key-S>', lambda e: self.make_player_move(1))
        self.root.bind('<Key-d>', lambda e: self.make_player_move(2))        # D for Right
        self.root.bind('<Key-D>', lambda e: self.make_player_move(2))
        self.root.bind('<Left>', lambda e: self.make_player_move(0))         # Arrow keys
        self.root.bind('<Up>', lambda e: self.make_player_move(1))
        self.root.bind('<Right>', lambda e: self.make_player_move(2))
        self.root.bind('<Key-1>', lambda e: self.make_player_move(0))        # Number keys
        self.root.bind('<Key-2>', lambda e: self.make_player_move(1))
        self.root.bind('<Key-3>', lambda e: self.make_player_move(2))
        self.root.bind('<Key-r>', lambda e: self.restart_game())             # R for restart
        self.root.bind('<Key-R>', lambda e: self.restart_game())
        self.root.bind('<F5>', lambda e: self.restart_game())                # F5 for restart
        self.root.bind('<Key-h>', lambda e: self.set_strategy('heuristic'))  # H for heuristic
        self.root.bind('<Key-f>', lambda e: self.set_strategy('fuzzy'))      # F for fuzzy
        self.root.bind('<Key-v>', lambda e: self.set_strategy('adversarial')) # V for adversarial
        
        # Focus on root for keyboard events
        self.root.focus_set()
    
    def setup_ui(self):
        # Main container with modern styling
        main = tk.Frame(self.root, bg=self.colors['light'])
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header with game title
        header = tk.Frame(main, bg=self.colors['surface'], relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title_frame = tk.Frame(header, bg=self.colors['surface'])
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="🏔️ HILL CLIMBING", font=('Segoe UI', 28, 'bold'),
                bg=self.colors['surface'], fg=self.colors['primary']).pack()
        
        tk.Label(title_frame, text="Human vs AI Challenge", font=('Segoe UI', 14),
                bg=self.colors['surface'], fg=self.colors['muted']).pack()
        
        # Main content area
        content = tk.Frame(main, bg=self.colors['light'])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar with modern styling
        sidebar = tk.Frame(content, bg=self.colors['surface'], width=350, relief=tk.RAISED, bd=2)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Stats section
        stats_container = tk.Frame(sidebar, bg=self.colors['surface'])
        stats_container.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(stats_container, text="📊 GAME STATS", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['surface'], fg=self.colors['dark']).pack(pady=(0, 15))
        
        stats_frame = tk.Frame(stats_container, bg=self.colors['primary'], relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_labels = {}
        for key, label, color in [('turn', 'Turn', self.colors['warning']), 
                                  ('player_moves', 'Your Moves', self.colors['success']), 
                                  ('ai_moves', 'AI Moves', self.colors['secondary'])]:
            row = tk.Frame(stats_frame, bg=self.colors['surface'])
            row.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(row, text=label, bg=self.colors['surface'], fg=self.colors['dark'],
                    font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
            self.stats_labels[key] = tk.Label(row, text='0', bg=self.colors['surface'],
                                             fg=color, font=('Segoe UI', 11, 'bold'))
            self.stats_labels[key].pack(side=tk.RIGHT)
        
        # AI Strategy section
        strategy_container = tk.Frame(sidebar, bg=self.colors['surface'])
        strategy_container.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(strategy_container, text="🤖 AI STRATEGY", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['surface'], fg=self.colors['dark']).pack(pady=(0, 15))
        
        self.strategy_buttons = {}
        strategy_info = [
            ('heuristic', 'Heuristic Search', '🎯', self.colors['success']),
            ('adversarial', 'Adversarial Search', '⚔️', self.colors['danger']),
            ('fuzzy', 'Fuzzy Logic', '🧠', self.colors['secondary'])
        ]
        
        for key, text, emoji, color in strategy_info:
            btn_frame = tk.Frame(strategy_container, bg=self.colors['surface'])
            btn_frame.pack(fill=tk.X, pady=5)
            
            btn = tk.Button(btn_frame, text=f"{emoji} {text}", font=('Segoe UI', 11, 'bold'),
                          command=lambda k=key: self.set_strategy(k),
                          bg=color, fg='white', relief=tk.RAISED, bd=3,
                          cursor='hand2', padx=20, pady=12, activebackground=color)
            btn.pack(fill=tk.X)
            self.strategy_buttons[key] = btn
        
        # Controls section
        controls_container = tk.Frame(sidebar, bg=self.colors['surface'])
        controls_container.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(controls_container, text="🎮 CONTROLS", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['surface'], fg=self.colors['dark']).pack(pady=(0, 15))
        
        controls_frame = tk.Frame(controls_container, bg=self.colors['accent'], relief=tk.RAISED, bd=2)
        controls_frame.pack(fill=tk.X)
        
        controls_text = [
            "A/← : Move Left",
            "S/↑ : Move Straight", 
            "D/→ : Move Right",
            "R/F5 : Restart Game",
            "H : Heuristic AI",
            "F : Fuzzy Logic AI",
            "V : Adversarial AI"
        ]
        
        for control in controls_text:
            tk.Label(controls_frame, text=control, font=('Segoe UI', 10),
                    bg=self.colors['surface'], fg=self.colors['dark'],
                    anchor='w').pack(fill=tk.X, padx=15, pady=2)
        
        # Restart button
        restart_frame = tk.Frame(sidebar, bg=self.colors['surface'])
        restart_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.restart_btn = tk.Button(restart_frame, text="🔄 RESTART GAME", 
                                   font=('Segoe UI', 14, 'bold'),
                                   command=self.restart_game,
                                   bg=self.colors['warning'], fg='white',
                                   relief=tk.RAISED, bd=4, cursor='hand2',
                                   padx=20, pady=15, activebackground=self.colors['warning'])
        self.restart_btn.pack(fill=tk.X)
        
        self.update_strategy_buttons()
        
        # Right side - Game area
        game_area = tk.Frame(content, bg=self.colors['surface'], relief=tk.RAISED, bd=2)
        game_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Game canvas section
        canvas_header = tk.Frame(game_area, bg=self.colors['surface'])
        canvas_header.pack(fill=tk.X, pady=20)
        
        tk.Label(canvas_header, text="🧗 CLIMBING WALL", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['surface'], fg=self.colors['primary']).pack()
        
        # Canvas with modern scrollbar
        canvas_container = tk.Frame(game_area, bg=self.colors['surface'])
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        self.canvas = tk.Canvas(canvas_container, width=700, height=550,
                               bg=self.colors['light'], highlightthickness=2,
                               highlightbackground=self.colors['primary'])
        
        # Modern scrollbar
        scrollbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL, 
                               command=self.canvas.yview, width=20)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scroll region
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        # Mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Movement status display (replacing buttons)
        status_frame = tk.Frame(game_area, bg=self.colors['surface'])
        status_frame.pack(fill=tk.X, padx=25, pady=(0, 25))
        
        tk.Label(status_frame, text="📍 MOVEMENT STATUS", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['surface'], fg=self.colors['dark']).pack(pady=(0, 15))
        
        moves_display = tk.Frame(status_frame, bg=self.colors['surface'])
        moves_display.pack()
        
        self.move_status = []
        move_info = [('⬅️ LEFT (A/←)', self.colors['danger']), 
                    ('⬆️ STRAIGHT (S/↑)', self.colors['success']), 
                    ('➡️ RIGHT (D/→)', self.colors['primary'])]
        
        for i, (text, color) in enumerate(move_info):
            frame = tk.Frame(moves_display, bg=self.colors['surface'])
            frame.pack(side=tk.LEFT, padx=20)
            
            label = tk.Label(frame, text=text, font=('Segoe UI', 12, 'bold'),
                           bg=color, fg='white', padx=15, pady=10,
                           relief=tk.RAISED, bd=3)
            label.pack()
            
            info = tk.Label(frame, text='...', font=('Segoe UI', 11),
                          bg=self.colors['surface'], fg=self.colors['muted'])
            info.pack(pady=8)
            
            self.move_status.append((label, info))
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling on canvas"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def draw_wall(self):
        self.canvas.delete('all')
        size = 50
        x_start, y_start = 60, 60
        
        # Modern finish line with gradient effect
        finish_y = y_start - 8
        self.canvas.create_rectangle(x_start, finish_y,
                                    x_start + self.game_state.width * size, finish_y + 6,
                                    fill=self.colors['success'], outline=self.colors['success'], width=2)
        self.canvas.create_text(x_start + 80, finish_y - 20,
                               text='🏆 FINISH LINE', font=('Segoe UI', 12, 'bold'),
                               fill=self.colors['success'])
        
        # Modern grid with improved styling
        wall_y = y_start + 25
        for row in range(self.game_state.height):
            for col in range(self.game_state.width):
                x = x_start + col * size
                y = wall_y + row * size
                
                # Base grid cell with modern styling
                self.canvas.create_rectangle(x, y, x + size, y + size,
                                            fill=self.colors['surface'], 
                                            outline=self.colors['muted'], width=1)
                
                # Add subtle grid pattern
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x, y, x + size, y + size,
                                                fill='#f3f4f6', outline='')
                
                # Modern obstacle design
                if self.game_state.wall[row, col] == 1:
                    # Obstacle with modern design
                    self.canvas.create_rectangle(x + 3, y + 3,
                                                x + size - 3, y + size - 3,
                                                fill=self.colors['danger'], 
                                                outline=self.colors['dark'], width=2)
                    self.canvas.create_text(x + size//2, y + size//2,
                                          text='🚫', font=('Arial', 20),
                                          fill='white')
        
        # Draw players with modern design
        self.draw_player(x_start, wall_y, self.game_state.player_pos, 
                        self.colors['primary'], '👤 YOU', size)
        self.draw_player(x_start, wall_y, self.game_state.ai_pos, 
                        self.colors['secondary'], '🤖 AI', size)
        
        # Modern start line
        start_y = wall_y + self.game_state.height * size + 15
        self.canvas.create_rectangle(x_start, start_y,
                                    x_start + self.game_state.width * size, start_y + 6,
                                    fill=self.colors['warning'], outline=self.colors['warning'], width=2)
        self.canvas.create_text(x_start + 80, start_y + 25,
                               text='🚀 START LINE', font=('Segoe UI', 12, 'bold'),
                               fill=self.colors['warning'])
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
        # Smart auto-scroll to show current action
        player_y = wall_y + self.game_state.player_pos[0] * size
        canvas_height = 550
        scroll_position = max(0, (player_y - canvas_height/2) / (start_y + 50))
        self.canvas.yview_moveto(scroll_position)
    
    def draw_player(self, x_start, y_start, pos, color, label, size):
        row, col = pos
        x = x_start + col * size + size//2
        y = y_start + row * size + size//2
        
        # Modern player design with glow effect
        radius = size//3
        # Outer glow
        for r in [radius + 8, radius + 6, radius + 4, radius + 2]:
            alpha = 0.1 + (radius + 8 - r) * 0.1
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                   fill='', outline=color, width=2)
        
        # Main player circle
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                               fill=color, outline='white', width=3)
        
        # Player label with better positioning
        if label.startswith('👤'):
            emoji, text = label.split(' ', 1)
            self.canvas.create_text(x, y-2, text=emoji, font=('Arial', 16))
        else:
            emoji, text = label.split(' ', 1)
            self.canvas.create_text(x, y-2, text=emoji, font=('Arial', 16))
        
        # Player name below
        self.canvas.create_text(x, y + radius + 15, text=label.split(' ', 1)[1],
                               font=('Segoe UI', 9, 'bold'), fill=color)
    
    def update_display(self):
        # Update stats with modern styling
        self.stats_labels['turn'].config(text=str(self.game_state.turn_counter))
        self.stats_labels['player_moves'].config(text=str(self.game_state.player_moves))
        self.stats_labels['ai_moves'].config(text=str(self.game_state.ai_moves))
        
        # Update movement status display (replacing old button system)
        for i, (label, info) in enumerate(self.move_status):
            obs = self.game_state.get_obstacles_ahead(self.game_state.player_pos, i)
            status_text = f'{obs} obstacles' if obs > 0 else 'Clear Path'
            info.config(text=status_text)
            
            # Visual feedback for availability
            if self.waiting_for_input and not self.game_state.game_over:
                label.config(relief=tk.RAISED, state=tk.NORMAL)
                if obs > 0:
                    info.config(fg=self.colors['danger'])
                else:
                    info.config(fg=self.colors['success'])
            else:
                label.config(relief=tk.FLAT, state=tk.DISABLED)
                info.config(fg=self.colors['muted'])
        
        self.draw_wall()
    
    def make_player_move(self, move):
        if not self.waiting_for_input or self.game_state.game_over:
            return
        
        # Visual feedback for move
        if hasattr(self, 'move_status'):
            label, info = self.move_status[move]
            original_bg = label.cget('bg')
            label.config(bg=self.colors['accent'])
            self.root.after(200, lambda: label.config(bg=original_bg))
        
        self.waiting_for_input = False
        self.game_state.move_player(move)
        self.update_display()
        
        if not self.game_state.game_over:
            self.root.after(500, self.make_ai_move)
        else:
            self.show_game_over()
    
    def make_ai_move(self):
        if self.game_state.game_over:
            return
        
        move, info = self.ai_agent.make_move(self.current_strategy)
        self.last_ai_decision = info
        self.game_state.move_ai(move)
        self.game_state.turn_counter += 1
        self.waiting_for_input = True
        self.update_display()
        
        if self.game_state.game_over:
            self.show_game_over()
    
    def set_strategy(self, strategy):
        self.current_strategy = strategy
        self.update_strategy_buttons()
    
    def update_strategy_buttons(self):
        """Update strategy button appearances with modern styling"""
        for key, btn in self.strategy_buttons.items():
            if key == self.current_strategy:
                # Active strategy - highlighted
                if key == 'heuristic':
                    btn.config(bg=self.colors['success'], activebackground=self.colors['success'])
                elif key == 'adversarial':
                    btn.config(bg=self.colors['danger'], activebackground=self.colors['danger'])
                else:  # fuzzy
                    btn.config(bg=self.colors['secondary'], activebackground=self.colors['secondary'])
                btn.config(relief=tk.RAISED, bd=4)
            else:
                # Inactive strategies - muted
                btn.config(bg=self.colors['muted'], activebackground=self.colors['muted'],
                          relief=tk.RAISED, bd=2)
    
    def restart_game(self):
        """Restart the game with visual feedback"""
        # Visual feedback for restart
        original_bg = self.restart_btn.cget('bg')
        self.restart_btn.config(bg=self.colors['success'], text="✨ RESTARTING...")
        self.root.update()
        
        # Reset game state
        self.game_state = GameState()
        self.ai_agent = AIAgent(self.game_state)
        self.waiting_for_input = True
        self.last_ai_decision = None
        
        # Update display
        self.update_display()
        
        # Reset button appearance
        self.root.after(500, lambda: self.restart_btn.config(
            bg=original_bg, text="🔄 RESTART GAME"))
    
    def show_game_over(self):
        """Show modern game over dialog"""
        winner = self.game_state.winner
        
        # Create custom dialog with modern styling
        dialog = tk.Toplevel(self.root)
        dialog.title("Game Over")
        dialog.geometry("400x250")
        dialog.configure(bg=self.colors['surface'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                   self.root.winfo_rooty() + 50))
        
        # Content
        content = tk.Frame(dialog, bg=self.colors['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Winner announcement
        if winner == "Human":
            emoji = "🎉"
            message = "Congratulations!"
            submsg = "You reached the top first!"
            color = self.colors['success']
        else:
            emoji = "🤖"
            message = "AI Wins!"
            submsg = "The AI reached the top first!"
            color = self.colors['secondary']
        
        tk.Label(content, text=emoji, font=('Segoe UI', 48),
                bg=self.colors['surface']).pack(pady=10)
        
        tk.Label(content, text=message, font=('Segoe UI', 20, 'bold'),
                bg=self.colors['surface'], fg=color).pack()
        
        tk.Label(content, text=submsg, font=('Segoe UI', 12),
                bg=self.colors['surface'], fg=self.colors['muted']).pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(content, bg=self.colors['surface'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🔄 Play Again", font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['primary'], fg='white', padx=20, pady=10,
                 command=lambda: [dialog.destroy(), self.restart_game()],
                 cursor='hand2', relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="❌ Exit", font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['muted'], fg='white', padx=20, pady=10,
                 command=dialog.destroy,
                 cursor='hand2', relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=10)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = HillClimbingGameTk()
    game.run()
