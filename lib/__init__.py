import re
from datetime import datetime, timezone, timedelta
from itertools import chain

TIMEZONE = timezone(timedelta(hours=9), "JST")

EVENT_NAME = "RTA in Japan Winter 2024"

# (word to plot, line style, color)
jls_extract_var = (("草", "ｗｗｗ", "LUL"), "--", "#1e9100")
jls_extract_var = jls_extract_var
RTA_EMOTES = (
    ("rtaClap", "-", "#ec7087"),
    (("rtaGg", "GG"), "-", "#ff381c"),
    (("rtaGl", "GL"), "-", "#5cc200"),
    ("rtaPray", "-", "#f7f97a"),
    ("rtaR", "-", "white"),
    ("rtaCheer", "-", "#ffbe00"),
    ("rtaHatena", "-", "#ffb5a1"),
    ("rtaCry", "-", "#5ec6ff"),

    ("rtaListen", "-.", "#5eb0ff"),
    ("rtaFear", "-.", "#aa60cc"),
    ("rtaUp", "-.", "#df4f69"),
    ("rtaPokan", "-.", "#838187"),
    ("rtaDaba", "-.", "white"),
    ("rtaLight", "-.", "#9acffd"),
    ("rtaKabe", ":", "#bf927a"),
    # (("rtaRedbull", "rtaRedbull2", "レッドブル"), "-.", "#98b0df"),
    # ("rtaBanana", ":", "#f3f905"),
    # ("rtaShogi", ":", "#c68d46"),
    # ("rtaThink", ":", "#f3f905"),
    # ("rtaIizo", ":", "#0f9619"),
    # ("rtaDeath", "-.", "#ffbe00"),

    ("rtaIce", ":", "#CAEEFA"),
    # ("rtaPog", ":", "#f8c900"),
    ("rtaFire", ":", "#E56124"),
    # ("rtaHello", ":", "#ff3291"),
    ("rtaHmm", ":", "#fcc7b9"),
    ("rtaGogo", ":", "#d20025"),
    ("rtaHeart", ":", "#ff3291"),
    # ("rtaMaru", ":", "#c80730"),
    # ("rtaThunder", ":", "#F5D219"),
    # ("rtaPoison", ":", "#9F65B2"),
    # ("rtaGlitch", ":", "#9F65B2"),
    # ("rtaWind", ":", "#C4F897"),
    # ("rtaOko", "-.", "#d20025"),
    # ("rtaWut", ":", "#d97f8d"),
    # ("rtaPolice", ":", "#7891b8"),
    # ("rtaChan", "-.", "green"),
    # ("rtaKappa", "-.", "#ffeae2"),

    # ("rtaSleep", "-.", "#ff8000"),
    # ("rtaCafe", "--", "#a44242"),
    # ("rtaDot", "--", "#ff3291"),

    # ("rtaShi", ":", "#8aa0ec"),
    # ("rtaGift", ":", "white"),
    # ("rtaAnkimo", ":", "#f92218 "),

    jls_extract_var,
    ("DinoDance", "--", "#00b994"),
    # ("rtaFrameperfect", "--", "#ff7401"),
    # # ("rtaPixelperfect", "--", "#ffa300"),
    ("Cheer（ビッツ）", "--", "#bd62fe"),
    ("無敵時間", "--", "red"),
    ("石油王", "--", "yellow"),
    ("かわいい", "--", "#ff3291")
)

VOCABULARY = set(w for w, _, _, in RTA_EMOTES if isinstance(w, str))
VOCABULARY |= set(chain(*(w for w, _, _, in RTA_EMOTES if isinstance(w, tuple))))

# (title, movie start time as timestamp, offset hour, min, sec)
GAMES = (
    ("開幕のあいさつ", 1735073204, 0, 11, 23),
    ("\nスターフォックスアドベンチャー", 1735073204, 0, 19, 17),
    ("マリオスポーツミックス", 1735073204, 1, 28, 40),
    ("マリオvs.ドンキーコング", 1735073204, 2, 13, 43),
    ("New スーパーマリオ\nブラザーズ U", 1735073204, 3, 37, 18),
    ("Hi-Fi RUSH", 1735073204, 4, 30, 0),
    ("Pseudoregalia", 1735073204, 7, 47, 5, "right"),
    ("ALTF42", 1735073204, 8, 26, 1, "right"),
    ("ノラカムの\nスライダーチャレンジ", 1735073204, 8, 55, 11, "right"),
    ("パックンロール\nリミックス", 1735073204, 9, 16, 16),
    ("DAEMON X MACHINA", 1735073204, 9, 49, 18),
    ("Metal Gear Rising: Revengeance", 1735073204, 12, 17, 37),
    ("サモンナイト2", 1735073204, 13, 32, 29),
    ("4D Golf", 1735073204, 17, 25, 45),
    ("ジャンボ尾崎の\nホールインワン", 1735073204, 18, 27, 46),
    ("SANABI", 1735073204, 18, 57, 29),
    ("Freedom Planet 2", 1735073204, 19, 45, 56),
    ("EQUALINE", 1735073204, 21, 24, 10),
    ("Super Multitasking", 1735073204, 22, 33, 41, "right"),
    ("KinnikuNeko:\nSUPER MUSCLE CAT", 1735073204, 22, 56, 43),
    ("Carrion", 1735073204, 23, 46, 12),
    ("Aim Climb", 1735073204, 24, 50, 41),
    ("W.O.L.F", 1735073204, 25, 17, 12),
    ("ボンバーキング", 1735073204, 25, 37, 8),
    ("英雄伝説\n零の軌跡：改", 1735073204, 26, 28, 51, "right"),
    ("Disney's\nHercules:\nAction Game", 1735073204, 27, 2, 30, "right"),
    ("The Binding of\nIsaac: Repentance", 1735073204, 27, 38, 21, "right"),
    ("ライトニング リターンズ\nファイナルファンタジーXIII", 1735073204, 28, 41, 25, "right"),
    ("エイリアンソルジャー", 1735073204, 30, 50, 52, "right"),
    ("とんでもクライシス!", 1735073204, 31, 29, 44),
    ("BLUE REFLECTION 幻に舞う少女の剣", 1735073204, 32, 37, 15),
    ("テイルズオブシンフォニア\n-ラタトスクの騎士-", 1735073204, 35, 31, 31),
    ("ミニ四駆レッツ＆ゴー！！\nPOWER WGP2", 1735219594, 0, 2, 31),
    ("スター・ウォーズ ローグ・スコードロンIII\nレベルストライク", 1735219594, 2, 21, 35, "right"),
    ("コロコロ\nカービィ", 1735219594, 3, 21, 48),
    ("カービィファイターズ2", 1735219594, 3, 45, 3),
    ("ポケットモンスター\nピカチュウ", 1735219594, 5, 47, 7),
    ("いい大人達の大冒険", 1735219594, 6, 38, 25),
    ("御伽活劇 豆狸のバケル ～オラクル祭太郎の祭難！！", 1735219594, 7, 24, 24),
    ("プリルラ(Pu・Li・Ru・La)", 1735219594, 10, 8, 0, "right"),
    ("Dance Dance Revolution STRIKE", 1735219594, 10, 34, 55),
    ("コナステ GITADORA(GuitarFreaks)", 1735219594, 14, 31, 5),
    ("Grim Fandango:Remastered", 1735219594, 15, 38, 19),
    ("Sifu", 1735219594, 16, 41, 20),
    ("クロックタワー", 1735219594, 17, 34, 3),
    ("シャドウハーツ2", 1735219594, 19, 25, 54),
    ("GUNPEY", 1735219594, 26, 2, 7),
    ("すってはっくん", 1735219594, 26, 21, 56),
    ("ぷよぷよ通", 1735219594, 28, 30, 33),
    ("斑鳩", 1735219594, 30, 5, 40, "right"),
    ("マジカルテトリス\nチャレンジ\nfeaturingミッキー", 1735219594, 30, 38, 36, "right"),
    ("ソニックと秘密のリング", 1735219594, 31, 26, 31, "right"),
    ("ブロックアウト", 1735219594, 31, 57, 5, "right"),
    ("ソニックトゥーン 太古の秘宝", 1735219594, 33, 26, 41, "right"),
    ("Nintendo World\nChampionships\nファミコン世界大会", 1735219594, 34, 8, 56, "right"),
    ("マリオ1, 2, USA, 3, ワールド, 64", 1735219594, 34, 43, 23),
    ("スーパーマリオRPG リメイク", 1735219594, 35, 56, 10),
    ("アクアリウムは踊らない", 1735219594, 38, 47, 2, "right"),
    ("不思議のダンジョン 風来のシレン6 とぐろ島探検録", 1735219594, 40, 8, 24),
    ("バイオハザードRE:3", 1735219594, 43, 45, 48),
    ("SaGa SCARLET GRACE 緋色の野望", 1735381011, 0, 1, 41),
    ("ゼルダの伝説 大地の汽笛", 1735381011, 2, 35, 49),
    ("ゼルダの伝説 夢をみる島 (Switch)", 1735381011, 7, 33, 23, "right"),
    ("街へいこうよどうぶつの森", 1735381011, 8, 47, 2, "right"),
    ("霧留待夢 -kill time-", 1735381011, 11, 42, 5),
    ("スーパードンキーコング\nGBA", 1735381011, 12, 38, 17),
    ("もんすたあ★レース", 1735381011, 13, 28, 33),
    ("あつめてあそぶ　くまのプーさん　もりのたからもの", 1735381011, 16, 0, 29, "right"),
    ("スプラッターハウス\nわんぱく\nグラフィティ", 1735381011, 16, 53, 18, "right"),
    ("Half-Life / Half-Life 2", 1735381011, 17, 26, 22),
    ("Verlet\nSwing", 1735381011, 19, 19, 21),
    ("ローション侍", 1735381011, 19, 41, 26),
    ("\nQWOP", 1735381011, 19, 55, 24),
    ("ユニコーン\nオーバーロード", 1735381011, 20, 16, 22),
    ("Cyberbots:\nFullmetal Madness", 1735381011, 20, 47, 28),
    ("ポケットモンスター サン・ムーン", 1735381011, 21, 15, 19),
    ("メダロット1 カブトver", 1735381011, 26, 52, 17),
    ("大魔界村", 1735485337, 0, 1, 9),
    ("Rockman.EXE\nTransmission", 1735485337, 0, 29, 59),
    ("ロックマンX7", 1735485337, 1, 32, 0, "right"),
    ("マサラドライブ", 1735485337, 3, 13, 7),
    ("マリオカート8 デラックス", 1735485337, 3, 43, 3),
    ("ワリオランドアドバンス\nヨーキのお宝", 1735485337, 5, 48, 24),
    ("星のカービィ ディスカバリー", 1735485337, 6, 49, 30),
    ("悪魔城ドラキュラ ドミナスコレクション", 1735485337, 9, 33, 11),
    ("OVERLORD:\nESCAPE FROM\nNAZARICK", 1735485337, 10, 47, 5),
    ("MELTY BLOOD:\nTYPE LUMINA", 1735485337, 12, 8, 49, "right"),
    ("東方獣王園\n〜 Unfinished Dream of\nAll Living Ghost.", 1735485337, 13, 7, 26, "right"),
    ("リングフィット\nアドベンチャー", 1735485337, 13, 30, 50),
    ("ロロナのアトリエ DX：アーランドの錬金術士", 1735485337, 14, 15, 52),
    ("九怨-Kuon-", 1735485337, 15, 42, 51),
    ("龍が如く7 光と闇の行方 インターナショナル", 1735485337, 17, 30, 54),
    ("ドラゴンクエストモンスターズ2 マルタのふしぎな鍵", 1735485337, 21, 30, 56, "right"),
    ("ドラゴンクエスト10オフライン", 1735485337, 22, 14, 58),
    ("R4 -RIDGE RACER TYPE4-", 1735485337, 25, 1, 46, "right"),
    ("キングダムハーツII ファイナルミックス", 1735485337, 25, 37, 44),
    ("閉幕のあいさつ", 1735485337, 30, 37, 34, "right")
)


class Game:
    def __init__(self, name, t, h, m, s, align="left"):
        self.name = name
        self.startat = datetime.fromtimestamp(t + h * 3600 + m * 60 + s).replace(tzinfo=timezone.utc).astimezone(TIMEZONE)
        self.align = align


GAMES = tuple(Game(*args) for args in GAMES)

WINDOWSIZE = 1
WINDOW = timedelta(seconds=WINDOWSIZE)
AVR_WINDOW = 60
PER_SECONDS = 60
FIND_WINDOW = 15
DOMINATION_RATE = 0.6
COUNT_THRESHOLD = 30

DPI = 200
ROW = 5
PAGES = 4
YMAX = 700
WIDTH = 3840
HEIGHT = 2160

FONT_COLOR = "white"
FRAME_COLOR = "#ffff79"
BACKGROUND_COLOR = "#352319"
FACE_COLOR = "#482b1e"
ARROW_COLOR = "#ffff79"
MESSAGE_FILL_COLOR = "#1e0d0b"
MESSAGE_EDGE_COLOR = "#7f502f"

ALPHA = 0.5

BACKGROUND = "2024w.png"


EXCLUDE_MESSAGE_TERMS = (
    " subscribed with Prime",
    " subscribed at Tier ",
    " gifted a Tier ",
    " is gifting ",
    " raiders from "
)

PNS = (
    "無敵時間",
    "石油王",
    "国境なき医師団",
    "ナイスセーヌ",
    "ハイプトレイン",
    "そうはならんやろ",
    "強制スクロール",
    "やったか",
    "おじょうず",
    "いつもの",
    "おじさん",
    "騙して悪いが",
    "池ポチャート",
    "もどして",
    "チャリで来た",
    "やったぜ",
    "あるのがいけない",
    "インド人を右に",
    "ナイスセーブ",
    "ファイナルナイト",
    "上に落ちる変態",
    "クポがよぉ",
    "やりぃ",
    "あさき",
    "掌底",
    "公開デバッグ",
    "ご期待ください",
    "エンドコンテンツ"
)

PN_PATTERNS = (
    (re.compile("[a-zA-Z]+[0-9]+"), "Cheer（ビッツ）"),
    (re.compile("世界[1１一]位?"), "世界一"),
    (re.compile("ヨシ！+"), "ヨシ！"),
    (re.compile("(良|よ)いお年を"), "良いお年を"),
    (re.compile("[iIｉＩ][gGｇＧ][aAａＡ]+"), "IGA")
)

STOP_WORDS = (
    "Squid2",
    ''
)
