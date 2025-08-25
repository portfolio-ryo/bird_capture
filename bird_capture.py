import tkinter
import random

# 定数や初期設定
FNT = ("Terminal", 40)
fade_colors = ["#FFFFFF", "#D0FFD0", "#A0FFA0", "#70CC70", "#60A060", "#60A060"]

# グローバル変数（最小限に）
bird_spot = [0] * 5
scene = "タイトル"
score = 0
high_score = 0
time = 0
key = ""
countdown = 3
fade_index = 0

# --- キーイベント ---
def pkey(e):
    global key
    key = e.keysym

# --- 描画関数群 ---
def draw_background():
    cvs.delete("all")
    background = cvs.create_image(512, 384, image=back)
    cvs.tag_lower(background)

def draw_title_screen():
    draw_background()
    cvs.create_text(512, 180, text="Bird_Capture", font=FNT, fill="pink")
    cvs.create_text(512, 300, text="HIGH SCORE: " + str(high_score), font=FNT, fill="orange")
    cvs.create_text(512, 420, text="[S]tart", font=FNT, fill="cyan")

def draw_game_screen():
    draw_background()
    # 上段の鳥
    for i in range(3):
        x = 340 * i + 170
        cvs.create_image(x, 256, image=img[bird_spot[i]])
        cvs.create_text(x, 384, text=i + 1, font=FNT, fill="yellow")
    # 下段の鳥
    for j in range(2):
        x = 340 * j + 340
        cvs.create_image(x, 512, image=img[bird_spot[j + 3]])
        cvs.create_text(x, 640, text=j + 4, font=FNT, fill="yellow")

    # スコア・時間表示
    cvs.create_text(200, 30, text="SCORE: " + str(score), font=FNT, fill="white")
    cvs.create_text(800, 30, text="TIME: " + str(time), font=FNT, fill="yellow")

def draw_game_over_screen():
    draw_background()
    cvs.create_text(500, 100, text="GAME END", font=FNT, fill="red")
    cvs.create_text(500, 200, text="[R]eplay", font=FNT, fill="lime")
    cvs.create_text(500, 300, text="YOUR SCORE: " + str(score), font=FNT, fill="blue")
    cvs.create_text(500, 400, text="HIGH SCORE: " + str(high_score), font=FNT, fill="orange")

def draw_countdown(num):
    draw_background()
    cvs.create_text(512, 384, text=str(num), font=("Terminal", 100), fill="white")

def draw_fade_start(color):
    draw_background()
    cvs.create_text(512, 384, text="START!!", font=("Terminal", 100), fill=color)

# --- ゲームロジック関数 ---
def update_game():
    global score, time, scene, key

    r = random.randint(0, 4)
    r2 = random.randint(0, 2)
    bird_spot[r] = r2

    # 鳥の捕獲処理
    if "1" <= key <= "3":
        m = int(key) - 1
        x = m * 340 + 170
        cvs.create_image(x, 256, image=buk)

        if bird_spot[m] == 0:
            score += 100
        elif bird_spot[m] == 1:
            score += 50
        else:
            score -= 30

    if key == "4" or key == "5":
        m = int(key) - 1
        x = (m - 3) * 340 + 340
        cvs.create_image(x, 512, image=buk)

        if bird_spot[m] == 0:
            score += 100
        elif bird_spot[m] == 1:
            score += 50
        else:
            score -= 30

    time -= 1
    if time <= 0:
        scene = "ゲームオーバー"

    key = ""

# --- メイン制御関数 ---
def main():
    global scene, countdown, fade_index, key, high_score

    if scene == "タイトル":
        draw_title_screen()
        if key == "s":
            key = ""
            start_countdown()

    elif scene == "カウントダウン":
        # カウントダウン中は何もしない、do_countdownで処理

        pass

    elif scene == "フェード":
        # フェード中は何もしない、do_fade_startで処理

        pass

    elif scene == "ゲーム":
        draw_game_screen()
        update_game()

    elif scene == "ゲームオーバー":
        draw_game_over_screen()
        if score > high_score:
            high_score = score
            with open("score.txt", "w") as f:
                f.write(str(high_score))
        if key == "r":
            key = ""
            start_countdown()

    if scene not in ("カウントダウン", "フェード"):
        root.after(330, main)

# --- カウントダウン処理 ---
def do_countdown():
    global countdown, scene, fade_index
    if countdown > 0:
        draw_countdown(countdown)
        countdown -= 1
        root.after(1000, do_countdown)
    elif countdown == 0:
        countdown -= 1
        fade_index = 0
        scene = "フェード"
        do_fade_start()
    else:
        scene = "ゲーム"
        main()

# --- フェード処理 ---
def do_fade_start():
    global fade_index, scene
    if fade_index < len(fade_colors):
        draw_fade_start(fade_colors[fade_index])
        fade_index += 1
        root.after(160, do_fade_start)
    else:
        scene = "ゲーム"
        main()

# --- ハイスコア読み込み ---
def load_high_score():
    global high_score
    try:
        with open("score.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0

# --- カウントダウンスタート ---
def start_countdown():
    global countdown, time, score, scene
    countdown = 3
    time = 100
    score = 0
    scene = "カウントダウン"
    do_countdown()

# --- Tkinter初期設定 ---
root = tkinter.Tk()
root.title("Bird_Capture")
root.resizable(False, False)
root.bind("<Key>", pkey)

cvs = tkinter.Canvas(width=1024, height=768)
cvs.pack()

# 画像読み込み
back = tkinter.PhotoImage(file="image/background.png")
img = [
    tkinter.PhotoImage(file="image/pigeon.png"),
    tkinter.PhotoImage(file="image/sparrow.png"),
    tkinter.PhotoImage(file="image/crow.png"),
]
buk = tkinter.PhotoImage(file="image/bucket.png")

load_high_score()
main()
root.mainloop()
