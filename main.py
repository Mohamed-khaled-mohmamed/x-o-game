"""
Roadmap:

1. mov(board, win_condition, player)
   - Determines the next move based on the current board, win conditions, and player.

2. ai_algorithm(board)
   - AI algorithm to determine the AI's move based on difficulty level and mode.

3. check_win(board, player)
   - Checks for a win condition or tie.

4. disable_all_buttons()
   - Disables all buttons on the board.

5. enable_all_buttons()
   - Enables all buttons and resets their appearance.

6. draw_color()
   - Sets the color for all buttons in case of a draw.

7. win_color(p1, p2, p3)
   - Sets the color for the winning buttons.

8. update_score()
   - Updates the score display for the human and AI.

9. restart_game()
   - Restarts the game by enabling all buttons and resetting the result label.

10. update_board(buttons)
    - Updates the board state from the button texts.

11. button_click(i)
    - Handles user button clicks.

12. play(i)
    - Main function to play the game based on user input.

13. ai_move()
    - Handles AI moves and updates the board accordingly.

14. update_difficulty(event)
    - Updates the difficulty level based on user selection.

15. update_mode(event)
    - Updates the game mode based on user selection.

16. handle_crazy_mode()
    - Handles the UI changes for crazy mode.

"""





import random
import tkinter as tk
from tkinter import ttk

# Initialize game status and variables
gameRanning = True
position = 0
player = "user"
difficulty_level = "Medium"
mode = "normal"
human = "🤪"
ai_player = "👻"

# Function to determine the next move based on the current board, win conditions, and player
def mov(board, win_condition, player, level=1):
    for win in win_condition:
        for pair in win:
            if board[pair[0]] == player and board[pair[1]] == player:
                next_pair = win[(win.index(pair) + 1) % len(win)]
                if next_pair[0] < len(board) and board[next_pair[0]] == " ":
                    return next_pair[0]
                elif next_pair[1] < len(board) and board[next_pair[1]] == " ":
                    return next_pair[1]
    return None

# AI algorithm to determine the AI's move based on difficulty level
def ai_algorethem(board):
    win_condition = [
        [(0, 1), (1, 2), (0, 2)],
        [(3, 4), (4, 5), (3, 5)],
        [(6, 7), (7, 8), (6, 8)],
        [(0, 3), (3, 6), (0, 6)],
        [(1, 4), (4, 7), (1, 7)],
        [(2, 5), (5, 8), (2, 8)],
        [(0, 4), (4, 8), (0, 8)],
        [(2, 4), (4, 6), (2, 6)],
    ]

    if mode == "crazy":
        # Default move (random) for Easy or no other moves found
        available_moves = [i for i, spot in enumerate(board) if spot == " "]  # Find all available moves
        move = mov(board, win_condition, ai_player)  # Try to find a move to help AI win
        if move is not None:
            crazyMove = random.choice(available_moves)
            while crazyMove == move:
                crazyMove = random.choice(available_moves)
            return crazyMove
        
        move = mov(board, win_condition, human)  # Try to find a move to help human win
        if move is not None:
            crazyMove = random.choice(available_moves)
            while crazyMove == move:
                crazyMove = random.choice(available_moves)
            return crazyMove
        
        else:
            sides = [1, 3, 5, 7]
            random.shuffle(sides)
            for move in sides:
                if board[move] == " ":
                    return move
    else:
        # Normal mode: Play to win or block the opponent
        if difficulty_level in ["Medium", "Hard"]:
            # Attempt to win
            move = mov(board, win_condition, ai_player)
            if move is not None:
                return move

            # Attempt to block opponent from winning
            move = mov(board, win_condition, human)
            if move is not None:
                return move

        if difficulty_level == "Hard":
            # Choose center if available
            if board[4] == " ":
                return 4

            # Choose corners randomly if available
            corners = [0, 2, 6, 8]
            random.shuffle(corners)
            for move in corners:
                if board[move] == " ":
                    return move

        # Choose sides randomly if available
        sides = [1, 3, 5, 7]
        random.shuffle(sides)
        for move in sides:
            if board[move] == " ":
                return move

    # Default move (random) for Easy or no other moves found
    available_moves = [i for i, spot in enumerate(board) if spot == " "]
    if available_moves:
        return random.choice(available_moves)
    
    return None

# Function to check for a win condition or tie
def checkWin(board, player):
    global gameRanning
    win_condition = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    
    for condition in win_condition:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != " ":
            print(f"{player} wins!")
            gameRanning = False
            win_color(condition[0], condition[1], condition[2])
            return True
    
    if all(space != " " for space in board):
        print("It's a tie!")
        gameRanning = False
        draw_color()
        return None
    return False

# Functions to handle the coloring of the board
def disable_all_buttons():
    for i in range(1, 10):
        buttons[i].config(state=tk.DISABLED)

def enable_all_buttons():
    button_colors = {
        1: "#ffcccb",  # Light Coral
        2: "#90ee90",  # Light Green
        3: "#ffcccb",  # Light Coral
        4: "#90ee90",  # Light Green
        5: "#add8e6",  # Light Blue
        6: "#90ee90",  # Light Green
        7: "#ffcccb",  # Light Coral
        8: "#90ee90",  # Light Green
        9: "#ffcccb"   # Light Coral
    }
    for i in range(1, 10):
        buttons[i].config(state=tk.NORMAL, text=" ", bg=button_colors[i])

def draw_color():
    for i in range(1, 10):
        buttons[i].config(state=tk.DISABLED, bg="#282c34", fg="black")

def win_color(p1, p2, p3):
    for p in [p1, p2, p3]:
        if mode == "crazy":
            buttons[p + 1].config(bg="#282c34", fg="black")
        else:
            buttons[p + 1].config(bg="#FFD700", fg="black")  # Gold color for winning buttons

# Function to update the score
def update_score():
    score_human.config(text=f"You: {human_score} ")
    score_computer.config(text=f"Computer: {ai_score} ")

# Function to restart the game
def restart_game():
    enable_all_buttons()
    result_label.config(text="Tic Tac Toe")

# Function to update the board state
def update_board(buttons):
    return [buttons[i].cget("text") for i in range(1, 10)]

# Function to handle user button clicks
def button_click(i):
    if buttons[i].cget("text") == " ":
        button = buttons[i]
        button.config(text=human)
        return True
    return None

# Function to play the game
def play(i):
    global player, human_score, ai_score
    if player == "user":
        if button_click(i):
            board = update_board(buttons)
            if checkWin(board, human):
                if mode == "crazy":
                    result_label.config(text="Congratulations! You lose 👻!")
                    ai_score += 1
                    update_score()
                    disable_all_buttons()
                else:
                    result_label.config(text="Oops! You win 🤪!")
                    human_score += 1
                    update_score()
                    disable_all_buttons()
            elif all(space != " " for space in board):
                result_label.config(text="It's a tie! But you'll lose next time. 😤")
            else:
                player = "ai"
                ai_move()

# Function to handle AI moves
def ai_move():
    global player, ai_score , human_score
    board = update_board(buttons)
    ai = ai_algorethem(board)
    if ai is not None:
        buttons[ai + 1].config(text=ai_player)
    board = update_board(buttons)
    if checkWin(board, ai_player):
        if mode == "crazy":
            result_label.config(text="Oops! You win 🤪!")
            human_score += 1
            update_score()
            disable_all_buttons()
        else:
            result_label.config(text="Congratulations! You lose 👻!")
            ai_score += 1
            update_score()
            disable_all_buttons()
    player = "user"

# Function to update the difficulty level
def update_difficulty(event):
    global difficulty_level
    difficulty_level = difficulty_combobox.get()
    print(f"Difficulty level set to: {difficulty_level}")

# Function to update the game mode
def update_mode(event):
    global mode
    mode = mode_combobox.get()
    hendelCrazy()
    print(f"Mode set to: {mode}")

# Function to handle changes for "crazy" mode
def hendelCrazy():
    if mode == "crazy":
        difficulty_label.grid_forget()
        difficulty_combobox.grid_forget()
        mode_label.grid(row=2, column=0, padx=(20, 5), pady=10, sticky="e")
        mode_combobox.grid(row=2, column=1, padx=(5, 20), pady=10, sticky="w")
    else:
        difficulty_label.grid(row=2, column=0, padx=(20, 5), pady=10, sticky="e")
        difficulty_combobox.grid(row=2, column=1, padx=(5, 150), pady=50, sticky="w")
        mode_label.grid(row=2, column=1, padx=(20, 5), pady=10, sticky="e")
        mode_combobox.grid(row=2, column=2, padx=(5, 20), pady=10, sticky="w")

# Initialize the GUI
root = tk.Tk()
buttons = {}

width = 850
height = 850

root.title("Tic Tac Toe | mohamed_khaled")
root.geometry(f"{width}x{height}")

# Configure the grid
for i in range(4):
    root.rowconfigure(i, weight=1)
for i in range(3):
    root.columnconfigure(i, weight=1)

human_score = 0
ai_score = 0

# Labels and button with new colors
result_label = tk.Label(root, text="Tic Tac Toe", font=('Arial', 20), bg="#ffcccb", fg="#282c34")
result_label.grid(row=0, column=0, columnspan=3, pady=10)

score_human = tk.Label(root, text=f"You: {human_score}", font=('Arial', 20), anchor="w", bg="#282c34", fg="#61afef")
score_human.grid(row=1, column=0, columnspan=3, sticky="w", padx=20, pady=10)

score_computer = tk.Label(root, text=f"Computer: {ai_score}", font=('Arial', 20), anchor="w", bg="#282c34", fg="#e06c75")
score_computer.grid(row=1, column=2, columnspan=3, sticky="w", padx=10, pady=10)

restart_button = tk.Button(root, text="Restart", font=('Arial', 20), command=restart_game, bg="#98c379", fg="black")
restart_button.grid(row=2, column=0, columnspan=3, padx=30, pady=20, sticky="w")

# Configure difficulty level label and combobox
difficulty_label = tk.Label(root, text="Difficulty:", font=('Arial', 20), bg="#282c34", fg="#61afef")
difficulty_label.grid(row=2, column=0, padx=(20, 5), pady=10, sticky="e")

difficulty_combobox = ttk.Combobox(root, values=["Easy", "Medium", "Hard"], font=('Arial', 20), width=10, state="readonly")
difficulty_combobox.current(1)  # Set default to Medium
difficulty_combobox.grid(row=2, column=1, padx=(5, 150), pady=50, sticky="w")
difficulty_combobox.bind("<<ComboboxSelected>>", update_difficulty)

# Configure mode label and combobox
mode_label = tk.Label(root, text="Mode:", font=('Arial', 20), bg="#282c34", fg="#61afef")
mode_label.grid(row=2, column=1, padx=(20, 5), pady=10, sticky="e")

mode_combobox = ttk.Combobox(root, values=["normal", "crazy"], font=('Arial', 20), width=10, state="readonly")
mode_combobox.current(0)  # Set default to normal
mode_combobox.grid(row=2, column=2, padx=(5, 20), pady=10, sticky="w")
mode_combobox.bind("<<ComboboxSelected>>", update_mode)

# Configure Combobox style
style = ttk.Style()
style.theme_use('clam')
style.configure(
    "TCombobox", 
    # fieldbackground="#add8e6",  # Light Blue
    # background="#90ee90",      # Light Green
    foreground="#e06c75",      # Light Coral
    arrowcolor="#61afef"       # Light Blue
)

# Create the buttons for the board
button_colors = {
    1: "#ffcccb",  # Light Coral
    2: "#90ee90",  # Light Green
    3: "#ffcccb",  # Light Coral
    4: "#90ee90",  # Light Green
    5: "#add8e6",  # Light Blue
    6: "#90ee90",  # Light Green
    7: "#ffcccb",  # Light Coral
    8: "#90ee90",  # Light Green
    9: "#ffcccb"   # Light Coral
}

for i in range(1, 10):
    color = button_colors[i]
    button = tk.Button(root, text=" ", font=('Arial', 50), width=5, height=2, bg=color, fg="black",
                       command=lambda i=i: play(i))
    button.grid(row=(i-1)//3+3, column=(i-1)%3, sticky="nsew", padx=(100 if (i-1)%3 == 0 else 0, 100 if (i-1)%3 == 2 else 0), pady=(0, 50) if (i-1)//3 == 2 else 0)
    buttons[i] = button

root.mainloop()
