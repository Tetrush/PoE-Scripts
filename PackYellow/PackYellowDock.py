import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
import keyboard
import random
import threading
import pystray
from PIL import Image, ImageDraw
import os
import configparser

# iniファイルのパス
INI_PATH = "settings.ini"

# デフォルト設定
default_settings = {
    "right_grid_left": 1270/1920,
    "right_grid_top": 590/1080,
    "right_grid_right": 1900/1920,
    "right_grid_bottom": 850/1080,
    "left_click_x": 145/1920,
    "left_click_y": 290/1080,
    "move_delay_min": 0.01,
    "move_delay_max": 0.05,
    "click_delay_min": 0.01,
    "click_delay_max": 0.05,
}

def load_settings():
    config = configparser.ConfigParser()
    if not os.path.exists(INI_PATH):
        save_settings(default_settings)
        return default_settings.copy()
    config.read(INI_PATH)
    s = config["settings"]
    return {
        "right_grid_left": float(s["right_grid_left"]),
        "right_grid_top": float(s["right_grid_top"]),
        "right_grid_right": float(s["right_grid_right"]),
        "right_grid_bottom": float(s["right_grid_bottom"]),
        "left_click_x": float(s["left_click_x"]),
        "left_click_y": float(s["left_click_y"]),
        "move_delay_min": float(s["move_delay_min"]),
        "move_delay_max": float(s["move_delay_max"]),
        "click_delay_min": float(s["click_delay_min"]),
        "click_delay_max": float(s["click_delay_max"]),
    }

def save_settings(settings):
    config = configparser.ConfigParser()
    config["settings"] = {k: str(v) for k, v in settings.items()}
    with open(INI_PATH, "w") as f:
        config.write(f)

settings = load_settings()

# 設定値を変数にセット
right_grid_left = settings["right_grid_left"]
right_grid_top = settings["right_grid_top"]
right_grid_right = settings["right_grid_right"]
right_grid_bottom = settings["right_grid_bottom"]
left_click_x = settings["left_click_x"]
left_click_y = settings["left_click_y"]
move_delay_min = settings["move_delay_min"]
move_delay_max = settings["move_delay_max"]
click_delay_min = settings["click_delay_min"]
click_delay_max = settings["click_delay_max"]

# 画面サイズ取得
screen_width, screen_height = pyautogui.size()

# マスの設定
rows = 5
cols = 12
total_cells = rows * cols

# 右側マスの左上座標と幅・高さ（割合で指定）
# right_grid_left = 1270/1920
# right_grid_top = 590/1080
# right_grid_right = 1900/1920
# right_grid_bottom = 850/1080

right_grid_width = right_grid_right - right_grid_left
right_grid_height = right_grid_bottom - right_grid_top

# 1マスの幅・高さ
cell_width = right_grid_width / cols
cell_height = right_grid_height / rows

# 左側の特定箇所
# left_click_x = 145/1920
# left_click_y = 290/1080

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
        time.sleep(random.uniform(move_delay_min, move_delay_max))  # ← ini値を使用
        pyautogui.click(x, y, button=button)
        time.sleep(random.uniform(click_delay_min, click_delay_max))  # ← ini値を使用
        time.sleep(interval)

# グローバルフラグ
running = False
thread = None

def automation():
    global running
    try:
        time.sleep(1)  # ← 動作開始時に1秒遅延を追加
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
                time.sleep(random.uniform(0.01, 0.05))
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
        running = False  # ← ここでrunningをFalseにして再度ホットキーを受け付ける

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

def create_image():
    # シンプルなアイコン画像を生成
    image = Image.new('RGB', (64, 64), color=(255, 255, 0))
    d = ImageDraw.Draw(image)
    d.ellipse((8, 8, 56, 56), fill=(255, 215, 0))
    return image

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

icon = pystray.Icon("PackYellow", create_image(), "PackYellow", menu=pystray.Menu(
    pystray.MenuItem("終了", on_quit)
))

def capture_positions():
    global right_grid_left, right_grid_top, right_grid_right, right_grid_bottom, left_click_x, left_click_y, settings

    def get_click_position(prompt):
        # ダイアログ表示
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)  # 追加：最前面に
        messagebox.showinfo("座標キャプチャ", prompt, parent=root)
        root.destroy()

        # 透明な全画面ウィンドウでクリック取得
        pos = []
        click_win = tk.Tk()
        click_win.attributes('-fullscreen', True)
        click_win.attributes('-alpha', 0.2)  # 透明度（0.0～1.0）
        click_win.attributes('-topmost', True)
        click_win.config(bg='black')
        click_win.overrideredirect(True)  # 枠なし

        def on_click(event):
            pos.append((event.x_root, event.y_root))
            click_win.destroy()

        click_win.bind("<Button-1>", on_click)
        click_win.mainloop()
        return pos[0] if pos else (0, 0)

    # 1. ビースト位置
    x, y = get_click_position("キャプチャするビーストの位置をクリックしてください")
    left_click_x = x / screen_width
    left_click_y = y / screen_height
    settings["left_click_x"] = left_click_x
    settings["left_click_y"] = left_click_y

    # 2. インベントリ最左最上段
    x, y = get_click_position("インベントリ最左最上段の枠の左上をクリックしてください")
    right_grid_left = x / screen_width
    right_grid_top = y / screen_height
    settings["right_grid_left"] = right_grid_left
    settings["right_grid_top"] = right_grid_top

    # 3. インベントリ最右最下段
    x, y = get_click_position("インベントリ最右最下段の枠の右下をクリックしてください")
    right_grid_right = x / screen_width
    right_grid_bottom = y / screen_height
    settings["right_grid_right"] = right_grid_right
    settings["right_grid_bottom"] = right_grid_bottom

    save_settings(settings)
    messagebox.showinfo("完了", "座標を保存しました。")

# ホットキー登録
def main():
    print("Ctrl+Shift+. で自動化開始／停止します。")
    print("Ctrl+Shift+; で座標キャプチャモード")
    keyboard.add_hotkey('ctrl+shift+.', toggle_automation)
    keyboard.add_hotkey('ctrl+shift+;', capture_positions)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all_hotkeys()

if __name__ == "__main__":
    # ここでmain()を別スレッドで起動
    t = threading.Thread(target=main)
    t.start()
    icon.run()