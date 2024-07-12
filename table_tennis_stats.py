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

        self.create_widgets()

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

        ttk.Button(self.input_frame, text="Submit Point", command=self.submit_point).grid(row=4, column=0, columnspan=3)

        # Point History
        ttk.Label(self.history_frame, text="Point History:").grid(row=0, column=0, sticky=tk.W)
        self.history_text = tk.Text(self.history_frame, height=5, width=50)
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

    def end_game(self):
        if self.current_game:
            self.games.append(self.current_game)
            self.current_game = None
            self.update_previous_games()

    def submit_point(self):
        if not self.current_game:
            messagebox.showerror("Error", "Please start a new game before submitting points.")
            return

        # Validate input
        if not all([self.serve_type.get(), self.opening_shot_type.get(), 
                    self.opening_shot_player.get(), self.point_winner.get()]):
            messagebox.showerror("Error", "Please fill in all fields before submitting.")
            return

        # Record point data
        point_data = {
            "serve_type": self.serve_type.get(),
            "opening_shot_type": self.opening_shot_type.get(),
            "opening_shot_player": self.opening_shot_player.get(),
            "point_winner": self.point_winner.get()
        }
        self.point_history.append(point_data)

        # Update score
        if self.point_winner.get() == "Player":
            self.player_score += 1
        else:
            self.opponent_score += 1

        # Update score display
        self.current_score_label.config(text=f"{self.player_score} - {self.opponent_score}")

        # Update point history display
        self.update_history_display()

        # Clear input fields
        self.serve_type.set("")
        self.opening_shot_type.set("")
        self.opening_shot_player.set("Player")
        self.point_winner.set("")

        self.current_game["player_score"] = self.player_score
        self.current_game["opponent_score"] = self.opponent_score
        self.current_game["points"] = self.point_history

        # Check if the game has ended
        if (self.player_score >= 11 or self.opponent_score >= 11) and abs(self.player_score - self.opponent_score) >= 2:
            winner = self.current_game['player'] if self.player_score > self.opponent_score else self.current_game['opponent']
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.end_game()

    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for i, point in enumerate(self.point_history[-5:], 1):
            self.history_text.insert(tk.END, f"Point {i}: {point['point_winner']} won. "
                                             f"Serve: {point['serve_type']}, "
                                             f"Opening: {point['opening_shot_type']} "
                                             f"by {point['opening_shot_player']}\n")
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
            if not self.current_game or not self.current_game['points']:
                messagebox.showerror("Error", "No game data available for analysis.")
                return

            # Clear previous statistics
            for widget in self.stats_frame.winfo_children():
                widget.destroy()

            # Serve effectiveness
            serve_stats = self.analyze_serves()
            ttk.Label(self.stats_frame, text="Serve Effectiveness:").grid(row=0, column=0, sticky=tk.W)
            serve_text = "\n".join([f"{serve}: {win_rate:.2f}%" for serve, win_rate in serve_stats.items()])
            ttk.Label(self.stats_frame, text=serve_text).grid(row=1, column=0, sticky=tk.W)

            # Opening shot effectiveness
            opening_stats = self.analyze_opening_shots()
            ttk.Label(self.stats_frame, text="Opening Shot Effectiveness:").grid(row=0, column=1, sticky=tk.W)
            opening_text = "\n".join([f"{shot}: {win_rate:.2f}%" for shot, win_rate in opening_stats.items()])
            ttk.Label(self.stats_frame, text=opening_text).grid(row=1, column=1, sticky=tk.W)

            # Create pie charts
            self.create_pie_chart(serve_stats, "Serve Effectiveness", 2, 0)
            self.create_pie_chart(opening_stats, "Opening Shot Effectiveness", 2, 1)

    def analyze_serves(self):
        serve_stats = {}
        for point in self.current_game['points']:
            serve = point['serve_type']
            if serve not in serve_stats:
                serve_stats[serve] = {'total': 0, 'wins': 0}
            serve_stats[serve]['total'] += 1
            if point['point_winner'] == self.current_game['player']:
                serve_stats[serve]['wins'] += 1
        
        return {serve: (stats['wins'] / stats['total']) * 100 for serve, stats in serve_stats.items()}

    def analyze_opening_shots(self):
        opening_stats = {}
        for point in self.current_game['points']:
            shot = point['opening_shot_type']
            if shot not in opening_stats:
                opening_stats[shot] = {'total': 0, 'wins': 0}
            opening_stats[shot]['total'] += 1
            if point['point_winner'] == point['opening_shot_player']:
                opening_stats[shot]['wins'] += 1
        
        return {shot: (stats['wins'] / stats['total']) * 100 for shot, stats in opening_stats.items()}

    def create_pie_chart(self, data, title, row, column):
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column)

def main():
    root = tk.Tk()
    app = TableTennisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()