import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TableTennisApp:
    def __init__(self, master):
        self.master = master
        master.title("Table Tennis Statistics")
        master.geometry("1000x800")

        # Create main frames
        self.player_frame = ttk.Frame(master, padding="10")
        self.player_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.score_frame = ttk.Frame(master, padding="10")
        self.score_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.input_frame = ttk.Frame(master, padding="10")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.history_frame = ttk.Frame(master, padding="10")
        self.history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.stats_frame = ttk.Frame(master, padding="10")
        self.stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)

        self.player_score = 0
        self.opponent_score = 0
        self.point_history = []
        self.player_name = tk.StringVar()
        self.opponent_name = tk.StringVar()
        self.first_server = tk.StringVar(value="Player")
        self.games = []
        self.current_game = None

        # set default options on game start

        self.server_options = ["Player", "Opponent"]
        self.serve_type_options = ["Pendulum", "Backhand", "Tomohawk", "Punch", "Reverse pendulum", "Fault"]
        self.opening_shot_options = ["Forehand loop", "Backhand loop", "Forehand flick", "Backhand flick", "Forehand loop error", 
                                     "Backhand loop error", "Forehand flick error", "Backhand flick error", "Push Error"]
        self.point_winner_options = ["Player", "Opponent"]

        self.server = tk.StringVar(value="Player")
        self.serve_type = tk.StringVar(value="Pendulum")
        self.opening_shot_type = tk.StringVar(value="Forehand loop")
        self.opening_shot_player = tk.StringVar(value="Player")
        self.point_winner = tk.StringVar(value="Player")

        self.create_widgets()

        # Set the initial values
        self.update_input_values()

    def create_widgets(self):
        # Player Information
        ttk.Label(self.player_frame, text="Player:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.player_frame, textvariable=self.player_name).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(self.player_frame, text="Opponent:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.player_frame, textvariable=self.opponent_name).grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Add First Server selection
        ttk.Label(self.player_frame, text="First Server:").grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(self.player_frame, text="Player", variable=self.first_server, value="Player").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(self.player_frame, text="Opponent", variable=self.first_server, value="Opponent").grid(row=2, column=2, sticky=tk.W)

        # Add New Game button
        ttk.Button(self.player_frame, text="New Game", command=self.new_game).grid(row=3, column=0, columnspan=2)

        # Add Save and Load buttons
        ttk.Button(self.player_frame, text="Save Game", command=self.save_game).grid(row=4, column=0)
        ttk.Button(self.player_frame, text="Load Game", command=self.load_game).grid(row=4, column=1)

        # Add Statistics button
        ttk.Button(self.player_frame, text="Show Statistics", command=self.show_statistics).grid(row=5, column=0, columnspan=2)

        # Current Score
        ttk.Label(self.score_frame, text="Current Game:").grid(row=0, column=0, columnspan=2)
        self.current_score_label = ttk.Label(self.score_frame, text="0 - 0")
        self.current_score_label.grid(row=1, column=0, columnspan=2)

        # Previous Games
        ttk.Label(self.score_frame, text="Previous Games:").grid(row=2, column=0, columnspan=2)
        self.previous_games_label = ttk.Label(self.score_frame, text="No previous games")
        self.previous_games_label.grid(row=3, column=0, columnspan=2)

        # Input Area
        ttk.Label(self.input_frame, text="Serve Type:").grid(row=0, column=0, sticky=tk.W)
        serve_types = ["Pendulum", "Backhand", "Tomohawk", "Punch", "Reverse pendulum", "Fault"]
        self.serve_type = tk.StringVar()
        for i, serve in enumerate(serve_types):
            ttk.Radiobutton(self.input_frame, text=serve, variable=self.serve_type, value=serve).grid(row=0, column=i+1, sticky=tk.W)

        # Create a custom style for error shots
        style = ttk.Style()
        style.configure("Red.TRadiobutton", foreground="red")

        ttk.Label(self.input_frame, text="Opening Shot Type:").grid(row=1, column=0, sticky=tk.W)
        opening_shots = ["Forehand loop", "Backhand loop", "Forehand flick", "Backhand flick", "Forehand loop error", 
                         "Backhand loop error", "Forehand flick error", "Backhand flick error", "Push Error"]
        self.opening_shot_type = tk.StringVar()
        for i, shot in enumerate(opening_shots):
            if "error" in shot.lower():
                ttk.Radiobutton(self.input_frame, text=shot, variable=self.opening_shot_type, value=shot, style="Red.TRadiobutton").grid(row=1, column=i+1, sticky=tk.W)
            else:
                ttk.Radiobutton(self.input_frame, text=shot, variable=self.opening_shot_type, value=shot).grid(row=1, column=i+1, sticky=tk.W)

        ttk.Label(self.input_frame, text="Opening Shot Player:").grid(row=2, column=0, sticky=tk.W)
        self.opening_shot_player = tk.StringVar(value="Player")
        ttk.Radiobutton(self.input_frame, text="Player", variable=self.opening_shot_player, value="Player").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(self.input_frame, text="Opponent", variable=self.opening_shot_player, value="Opponent").grid(row=2, column=2, sticky=tk.W)

        ttk.Label(self.input_frame, text="Point Winner:").grid(row=3, column=0, sticky=tk.W)
        self.point_winner = tk.StringVar()
        ttk.Radiobutton(self.input_frame, text="Player", variable=self.point_winner, value="Player").grid(row=3, column=1, sticky=tk.W)
        ttk.Radiobutton(self.input_frame, text="Opponent", variable=self.point_winner, value="Opponent").grid(row=3, column=2, sticky=tk.W)

        ttk.Button(self.input_frame, text="Submit Point", command=self.submit_point).grid(row=4, column=0, columnspan=2)
        ttk.Button(self.input_frame, text="Undo Last Point", command=self.undo_point).grid(row=4, column=2, columnspan=1)

        # Point History
        ttk.Label(self.history_frame, text="Point History:").grid(row=0, column=0, sticky=tk.W)
        self.history_text = tk.Text(self.history_frame, height=20, width=150)
        self.history_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.history_text.insert(tk.END, "No points recorded yet.")
        self.history_text.config(state=tk.DISABLED)

    def new_game(self):
        if self.current_game:
            if messagebox.askyesno("New Game", "Are you sure you want to start a new game? Current game will be ended."):
                self.end_game()
            else:
                return

        if not self.player_name.get() or not self.opponent_name.get():
            messagebox.showerror("Error", "Please enter both player names before starting a new game.")
            return

        self.current_game = {
            "player": self.player_name.get(),
            "opponent": self.opponent_name.get(),
            "player_score": 0,
            "opponent_score": 0,
            "points": [],
            "first_server": self.first_server.get()
        }
        self.player_score = 0
        self.opponent_score = 0
        self.point_history = []
        self.current_score_label.config(text="0 - 0")
        self.update_history_display()
        messagebox.showinfo("New Game", f"New game started. {self.first_server.get()} serves first.")

        # Set the default values
        self.update_input_values()

    def update_input_values(self):
        # Determine the current server based on the point history and score
        if self.player_score >= 10 and self.opponent_score >= 10:
            # Swap servers each point
            if len(self.point_history) % 2 == 0:
                self.server.set(self.player_name.get() if self.server.get() == self.opponent_name.get() else self.opponent_name.get())
        else:
            # Swap servers every two points
            if len(self.point_history) % 2 == 0:
                self.server.set(self.first_server.get())
            else:
                self.server.set(self.player_name.get() if self.server.get() == self.opponent_name.get() else self.opponent_name.get())

        # Set the default values for other input fields
        self.serve_type.set("Pendulum")
        self.opening_shot_type.set("Forehand loop")
        self.opening_shot_player.set("Player")
        self.point_winner.set("Player")
        
        # Determine the current server based on the point history
        if len(self.point_history) % 2 == 0:
            self.server.set(self.first_server.get())
        else:
            # Check if the score is 10-10
            if self.player_score.get() == self.opponent_score.get() == 10:
                previous_server = self.point_history[-1]["server"]
                self.server.set(self.player_name.get() if previous_server == self.opponent_name.get() else self.opponent_name.get())
            else:
                self.server.set(self.player_name.get() if self.server.get() == self.opponent_name.get() else self.opponent_name.get())

        # Set the default values for other input fields
        self.serve_type.set("Pendulum")
        self.opening_shot_type.set("Forehand loop")
        self.opening_shot_player.set("Player")
        self.point_winner.set("Player")
            
    def end_game(self):
        if self.current_game:
            self.games.append(self.current_game)
            self.current_game = None
            self.update_previous_games()

    def submit_point(self):
        # Get the point winner and update the respective score
        point_winner = self.point_winner.get()

        if point_winner == "Player":
            self.player_score += 1
        else:
            self.opponent_score += 1

        # Check if the score is 10-10 or more
        if self.player_score >= 10 and self.opponent_score >= 10:
            # Swap servers each point
            if len(self.point_history) % 2 == 0:
                self.server.set("Player")
            else:
                self.server.set("Opponent")
        else:
            # Swap servers every two points
            if len(self.point_history) % 2 == 0:
                self.server.set("Player")
            elif len(self.point_history) % 2 == 1:
                self.server.set("Opponent")

        # Update the current score label
        self.current_score_label.config(text=f"{self.player_score} - {self.opponent_score}")

        # Create a string representing the point and add it to the history
        point = f"Server: {self.server.get()}, Winner: {point_winner}"
        self.point_history.append(point)

        # Update the point history display
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for point in self.point_history:
            self.history_text.insert(tk.END, point + "\n")
        self.history_text.config(state=tk.DISABLED)

        # Clear the radio button selections
        self.serve_type.set(None)
        self.opening_shot_type.set(None)
        self.opening_shot_player.set("Player")
        self.point_winner.set(None)
        
    def undo_point(self):
        if not self.current_game or not self.point_history:
            messagebox.showerror("Error", "No point to undo.")
            return

        # Remove the last point from history
        last_point = self.point_history.pop()

        # Update the score
        self.player_score = last_point['player_score_before']
        self.opponent_score = last_point['opponent_score_before']

        # Update the current game data
        self.current_game["player_score"] = self.player_score
        self.current_game["opponent_score"] = self.opponent_score
        self.current_game["points"] = self.point_history

        # Update the score display
        self.current_score_label.config(text=f"{self.player_score} - {self.opponent_score}")

        # Update the history display
        self.update_history_display()

        messagebox.showinfo("Undo", "Last point has been undone.")

    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)

        if self.point_history:
            for i, point in enumerate(self.point_history, start=1):
                serve_type = point["serve_type"]
                opening_shot_type = point["opening_shot_type"]
                opening_shot_player = point["opening_shot_player"]
                point_winner = point["point_winner"]
                player_score_before = point["player_score_before"]
                opponent_score_before = point["opponent_score_before"]
                server = point["server"]

                self.history_text.insert(tk.END, f"Point {i}: ")
                self.history_text.insert(tk.END, f"Server: {server}, ")
                self.history_text.insert(tk.END, f"Serve type: {serve_type}, ")
                self.history_text.insert(tk.END, f"Opening shot type: {opening_shot_type}, ")
                self.history_text.insert(tk.END, f"Opening shot player: {opening_shot_player}, ")
                self.history_text.insert(tk.END, f"Point winner: {point_winner}, ")
                self.history_text.insert(tk.END, f"Player score before: {player_score_before}, ")
                self.history_text.insert(tk.END, f"Opponent score before: {opponent_score_before}\n")
        else:
            self.history_text.insert(tk.END, "No points recorded yet.")
        
        self.history_text.config(state=tk.DISABLED)

    def update_previous_games(self):
        previous_games_text = "\n".join([f"{game['player']} vs {game['opponent']}: {game['player_score']}-{game['opponent_score']}" 
                                         for game in self.games[-3:]])
        if previous_games_text:
            self.previous_games_label.config(text=previous_games_text)
        else:
            self.previous_games_label.config(text="No previous games")

    def save_game(self):
        if not self.current_game:
            messagebox.showerror("Error", "No active game to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            data = {
                "current_game": self.current_game,
                "games": self.games,
                "player_name": self.player_name.get(),
                "opponent_name": self.opponent_name.get(),
                "first_server": self.first_server.get()
            }
            with open(file_path, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Save Successful", "Game data saved successfully.")

    def load_game(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.current_game = data["current_game"]
            self.games = data["games"]
            self.player_name.set(data["player_name"])
            self.opponent_name.set(data["opponent_name"])
            self.first_server.set(data.get("first_server", "Player"))  # Default to "Player" if not found

            if self.current_game:
                self.player_score = self.current_game["player_score"]
                self.opponent_score = self.current_game["opponent_score"]
                self.point_history = self.current_game["points"]
                self.current_score_label.config(text=f"{self.player_score} - {self.opponent_score}")
                self.update_history_display()
            
            self.update_previous_games()
            messagebox.showinfo("Load Successful", "Game data loaded successfully.")

    def show_statistics(self):
        if not self.games and not self.current_game:
            messagebox.showinfo("Statistics", "No game data available for statistics.")
            return

        # Combine current game (if exists) with previous games for analysis
        all_games = self.games + ([self.current_game] if self.current_game else [])

        # Calculate statistics
        total_points = sum(len(game['points']) for game in all_games)
        player_wins = sum(1 for game in all_games if game['player_score'] > game['opponent_score'])
        opponent_wins = sum(1 for game in all_games if game['opponent_score'] > game['player_score'])
        
        serve_stats = {'Player': {'won': 0, 'total': 0}, 'Opponent': {'won': 0, 'total': 0}}
        opening_shot_stats = {'Player': {'won': 0, 'total': 0}, 'Opponent': {'won': 0, 'total': 0}}
        
        for game in all_games:
            server = game['first_server']
            for point in game['points']:
                serve_stats[server]['total'] += 1
                if point['point_winner'] == server:
                    serve_stats[server]['won'] += 1
                
                opening_shot_stats[point['opening_shot_player']]['total'] += 1
                if point['point_winner'] == point['opening_shot_player']:
                    opening_shot_stats[point['opening_shot_player']]['won'] += 1
                
                server = 'Opponent' if server == 'Player' else 'Player'

        # Create a new window for statistics
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Game Statistics")

        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Summary tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")

        ttk.Label(summary_frame, text=f"Total Games: {len(all_games)}").pack()
        ttk.Label(summary_frame, text=f"Total Points Played: {total_points}").pack()
        ttk.Label(summary_frame, text=f"{self.player_name.get()} Wins: {player_wins}").pack()
        ttk.Label(summary_frame, text=f"{self.opponent_name.get()} Wins: {opponent_wins}").pack()

        # Serve Statistics tab
        serve_frame = ttk.Frame(notebook)
        notebook.add(serve_frame, text="Serve Statistics")

        player_serve_win_rate = serve_stats['Player']['won'] / serve_stats['Player']['total'] if serve_stats['Player']['total'] > 0 else 0
        opponent_serve_win_rate = serve_stats['Opponent']['won'] / serve_stats['Opponent']['total'] if serve_stats['Opponent']['total'] > 0 else 0

        ttk.Label(serve_frame, text=f"{self.player_name.get()} Serve Win Rate: {player_serve_win_rate:.2%}").pack()
        ttk.Label(serve_frame, text=f"{self.opponent_name.get()} Serve Win Rate: {opponent_serve_win_rate:.2%}").pack()

        # Create serve win rate chart
        fig, ax = plt.subplots()
        ax.bar([self.player_name.get(), self.opponent_name.get()], [player_serve_win_rate, opponent_serve_win_rate])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Serve Win Rate')
        ax.set_title('Serve Win Rate Comparison')

        canvas = FigureCanvasTkAgg(fig, master=serve_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Opening Shot Statistics tab
        opening_frame = ttk.Frame(notebook)
        notebook.add(opening_frame, text="Opening Shot Statistics")

        player_opening_win_rate = opening_shot_stats['Player']['won'] / opening_shot_stats['Player']['total'] if opening_shot_stats['Player']['total'] > 0 else 0
        opponent_opening_win_rate = opening_shot_stats['Opponent']['won'] / opening_shot_stats['Opponent']['total'] if opening_shot_stats['Opponent']['total'] > 0 else 0

        ttk.Label(opening_frame, text=f"{self.player_name.get()} Opening Shot Win Rate: {player_opening_win_rate:.2%}").pack()
        ttk.Label(opening_frame, text=f"{self.opponent_name.get()} Opening Shot Win Rate: {opponent_opening_win_rate:.2%}").pack()

        # Create opening shot win rate chart
        fig, ax = plt.subplots()
        ax.bar([self.player_name.get(), self.opponent_name.get()], [player_opening_win_rate, opponent_opening_win_rate])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Opening Shot Win Rate')
        ax.set_title('Opening Shot Win Rate Comparison')

        canvas = FigureCanvasTkAgg(fig, master=opening_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def main():
    root = tk.Tk()
    app = TableTennisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()