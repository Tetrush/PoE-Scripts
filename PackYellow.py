import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
import keyboard
import random
import threading

# 画面サイズ取得
screen_width, screen_height = pyautogui.size()

# マスの設定
rows = 5
cols = 12
total_cells = rows * cols

# 右側マスの左上座標と幅・高さ（割合で指定）
right_grid_left = 1270/1920
right_grid_top = 590/1080
right_grid_right = 1900/1920
right_grid_bottom = 850/1080

right_grid_width = right_grid_right - right_grid_left
right_grid_height = right_grid_bottom - right_grid_top

# 1マスの幅・高さ
cell_width = right_grid_width / cols
cell_height = right_grid_height / rows

# 左側の特定箇所
left_click_x = 145/1920
left_click_y = 290/1080

def get_cell_pos(index):
    """1始まりのマス番号から座標を計算"""
    col = (index - 1) // rows
    row = (index - 1) % rows
    x = (right_grid_left + cell_width * col + cell_width / 2) * screen_width
    y = (right_grid_top + cell_height * row + cell_height / 2) * screen_height
    return int(x), int(y)

def click_cell(index, button='right', times=1, interval=0.1):
    x, y = get_cell_pos(index)
    for _ in range(times):
        pyautogui.moveTo(x, y)
        time.sleep(random.uniform(0.01, 0.05))  # カーソル移動後ランダム遅延
        pyautogui.click(x, y, button=button)
        time.sleep(random.uniform(0.01, 0.03))  # クリック後ランダム遅延
        time.sleep(interval)

# グローバルフラグ
running = False
thread = None

def automation():
    global running
    try:
        right_click_counts = {i: 0 for i in range(1, 7)}
        left_cell_index = total_cells  # 60から1へ

        for right_index in range(6, 0, -1):
            for _ in range(10):
                if not running:
                    print("中断されました。")
                    return
                # 1. マス[right_index]を右クリック
                click_cell(right_index, button='right', times=1, interval=0.05)
                right_click_counts[right_index] += 1

                # 2. 左側の特定箇所を左クリック
                lx = int(left_click_x * screen_width)
                ly = int(left_click_y * screen_height)
                pyautogui.moveTo(lx, ly)
                time.sleep(random.uniform(0.01, 0.05))
                pyautogui.click(lx, ly, button='left')
                time.sleep(random.uniform(0.01, 0.03))
                time.sleep(0.2)

                # 3. 右側のマス[left_cell_index]を左クリック
                click_cell(left_cell_index, button='left', times=1, interval=0.05)
                left_cell_index -= 1

        # 4. 終了ダイアログ表示
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("終了", "すべてのマスが埋まりました。")
        root.destroy()
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        running = False

def toggle_automation():
    global running, thread
    if running:
        # 動作中なら停止
        running = False
    else:
        # 動作していなければ最初から開始
        if thread and thread.is_alive():
            # 念のため前のスレッド終了待ち
            thread.join()
        running = True
        thread = threading.Thread(target=automation)
        thread.start()

def main():
    print("Ctrl+Shift+Bで自動化開始／停止します。")
    keyboard.add_hotkey('ctrl+shift+b', toggle_automation)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all_hotkeys()

if __name__ == "__main__":
    main()