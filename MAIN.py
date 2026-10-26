from working_fuctions.chessboard_GUI import CHESSGUI

import keyboard
def play():

    chessboard = CHESSGUI()
    chessboard.chessgui()

if __name__ == "__main__":
    keyboard.add_hotkey('shift+P',play)
    keyboard.send("shift+E")
    keyboard.wait('a')