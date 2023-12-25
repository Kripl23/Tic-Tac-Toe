from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random

BOT_TOKEN = ""

app = Client("my_bot", bot_token=BOT_TOKEN)


board = [[' ' for _ in range(3)] for _ in range(3)]
player = "❌"
bot = "⭕️"

def print_board():
    keyboard = []
    for i, row in enumerate(board):
        keyboard_row = []
        for j, cell in enumerate(row):
            callback_data = f"move_{i}_{j}"
            button_text = f"{cell}" if cell != ' ' else f"({i+1},{j+1})"
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)

def check_win(player):
    # Проверка строк, столбцов и диагоналей
    for i in range(3):
        if all([cell == player for cell in board[i]]) or \
           all([board[j][i] == player for j in range(3)]):
            return True
    return (board[0][0] == board[1][1] == board[2][2] == player) or \
           (board[0][2] == board[1][1] == board[2][0] == player)

def check_draw():
    return all(all(cell != ' ' for cell in row) for row in board)

def reset_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

def bot_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[x][y] = bot
        return True
    return False
@app.on_callback_query(filters=filters.regex("^start$"))
@app.on_message(filters.command("start"))
def start(client, msg):
    try:
            
        msg.delete()
        reset_game()
        msg.reply("Добро пожаловать в игру Крестики-Нолики!\nВы играете крестиками.\nНажмите на кнопку, чтобы сделать ход.", reply_markup=print_board())
    except:
        reset_game()
        msg.message.edit("Добро пожаловать в игру Крестики-Нолики!\nВы играете крестиками.\nНажмите на кнопку, чтобы сделать ход.", reply_markup=print_board())

@app.on_callback_query()
def on_msg(client, msg: CallbackQuery):
    global player, bot
    _, x, y = msg.data.split('_')
    x, y = int(x), int(y)
    if board[x][y] == ' ':
        board[x][y] = player

        if check_win(player):
            msg.message.edit(f"Вы победили!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ещё раз?", "start")]]))
            reset_game()
            return
        if check_draw():
            msg.message.edit("Ничья!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ещё раз?", "start")]]))
            reset_game()
            return

        if bot_move():
            if check_win(bot):
                msg.message.edit(f"Бот победил!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ещё раз?", "start")]]))
                reset_game()
                return
            if check_draw():
                msg.message.edit("Ничья!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ещё раз?", "start")]]))
                reset_game()
                return

        msg.message.edit("Ваш ход.", reply_markup=print_board())
    else:
        msg.answer("Эта клетка уже занята!", show_alert=True)

app.run()