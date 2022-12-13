import tkinter as tk
import tkinter.ttk as ttk
import merukari_search
import scrollbar_frame
from PIL import Image, ImageTk
import tools
import os

root = tk.Tk()
root.title("メルカリセラー分析")
root.geometry("800x540")

notebook = ttk.Notebook(root)
tab_one = tk.Frame(notebook, bg='white')
tab_two = tk.Frame(notebook, bg='white')

notebook.add(tab_one, text="商品一覧", underline=0)
notebook.add(tab_two, text="売り切れ商品人気順リスト")
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# tab_oneに配置するウィジェットの作成
t1_frame1 = tk.Frame(tab_one, bg="white", height=90)
t1_frame1.pack(side="top", fill="x")

label = ttk.Label(t1_frame1, text="セラーURL", background='white')
label.place(x=20, y=12)

url_box = ttk.Entry(t1_frame1, width=50)
url_box.insert(0, "https://jp.mercari.com/user/profile/134437721")
url_box.place(x=80, y=10)

img_list = []
# tab1のリスト
label_list = []
# タブ2のリスト
label_list_2 = []

popular_list = []


def button_on():
    img_dir = 'for_img'
    for f in os.listdir(img_dir):
        os.remove(os.path.join(img_dir, f))

    sold_list = []
    url = url_box.get()
    search = merukari_search.MeruSearch(url)
    search.search()

    seller_name['text'] = search.seller_name
    t2_seller_name['text'] = search.seller_name
    t2_label4['text'] = search.seller_pro_num + "品"
    t2_label6['text'] = search.seller_sell_num + "品"
    t2_label8['text'] = str(int(search.seller_pro_num) - int(search.seller_sell_num)) + "品"
    t2_label10['text'] = str(round(100 - int(search.seller_sell_num) / int(search.seller_pro_num) * 100, 1)) + "％"

    t1_list_space.destroy()
    s_frame = scrollbar_frame.ScrollableFrame(t1_frame2)
    s_frame.pack(fill="both", expand=True)

    # img_dir = 'for_img'
    # for f in os.listdir(img_dir):
    #     os.remove(os.path.join(img_dir, f))

    for idx in range(len(search.pro_list)):
        try:
            img = Image.open('for_img/img{}.jpg'.format(idx + 1))
        except FileNotFoundError:
            img = Image.open('except_img/except_img.jpg')

        img = img.resize((60, 60))
        img = ImageTk.PhotoImage(img)
        img_list.append(img)

        li = search.pro_list[idx].title
        li2 = search.pro_list[idx].price
        li3 = search.pro_list[idx].flag_sold
        li4 = search.pro_list[idx].pro_url
        li5 = search.pro_list[idx].pro_num - 1
        li6 = tools.timeget(search.pro_list[idx].created_day, "m")

        s_label = ttk.Label(s_frame.scrollable_frame,
                            text=str(idx) + ":" + li + li2 + "円" + li3 + li4,
                            image=img_list[idx],
                            background="white",
                            compound="left",
                            padding=[10])
        s_label.bind("<MouseWheel>", s_frame.y_wheel)

        label_list.append(s_label)

        # タブ２のためのプログラム
        # 売り切れ商品をリストアップ
        day_only = li6
        price_only = li2 + "円"

        if search.pro_list[idx].flag_sold == "売り切れ":
            if len(sold_list) == 0:
                sold_list.append([li5, li, 1, [day_only], [price_only]])

            else:
                for j in range(len(sold_list)):
                    if li == sold_list[j][1]:
                        sold_list[j][2] += 1
                        sold_list[j][3].append(day_only)
                        sold_list[j][4].append(price_only)
                        break
                    elif j == len(sold_list) - 1:
                        sold_list.append([li5, li, 1, [day_only], [price_only]])
        if idx < 100:
            s_label.pack(side="top", fill="x")
        elif idx == 1000:
            break
        else:
            continue

    # 売れてる順に並び変え
    global popular_list
    popular_list = sorted(sold_list, reverse=True, key=lambda x: x[2])

    # タブ2にデータを配置
    t2_list_space.destroy()
    s_frame2 = scrollbar_frame.ScrollableFrame(t2_frame2)
    s_frame2.pack(fill="both", expand=True)

    for idx2 in range(len(popular_list)):
        li_2 = popular_list[idx2][1]  # 商品タイトル
        li2_2 = popular_list[idx2][2]  # 売れた個数
        li3_2 = popular_list[idx2][3]  # 日付
        li4_2 = popular_list[idx2][4]  # 値段

        s_label2 = ttk.Label(s_frame2.scrollable_frame,
                             text=str(li2_2) + "個売れています。" + '\n' + "商品名: " + li_2 + '\n' + "出品日" + str(
                                 li3_2) + '\n' + "値段の変化: " + str(li4_2),
                             image=img_list[popular_list[idx2][0]],
                             background="white",
                             compound="left",
                             padding=[10])
        s_label2.bind("<MouseWheel>", s_frame2.y_wheel)
        label_list_2.append(s_label2)

        if idx2 < 100:
            s_label2.pack(side="top", fill="x")
        else:
            continue


bunseki_button = ttk.Button(t1_frame1, text="分析開始", command=button_on)
bunseki_button.place(x=390, y=8)

label2 = ttk.Label(t1_frame1, text="セラー名", background='white')
label2.place(x=20, y=40)

seller_name = ttk.Label(t1_frame1, text="", background='white')
seller_name.place(x=80, y=40)

label3 = ttk.Label(t1_frame1, text="商品一覧", background='white')
label3.place(x=350, y=70)

t1_frame2 = tk.Frame(tab_one, background="white", relief="ridge")
t1_frame2.pack(padx="10", pady="10", fill="both", expand=True)

t1_list_space = tk.Canvas(t1_frame2, bg="white")
t1_list_space.pack(fill="both", expand=True)

# tab2に配置するウィジェットの作成
pl_x = 20
pl_y = 40
t2_frame1 = tk.Frame(tab_two, bg="white", height=90)
t2_frame1.pack(side="top", fill="x")

t2_label2 = ttk.Label(t2_frame1, text="セラー名", background='white')
t2_label2.place(x=20, y=12)

t2_seller_name = ttk.Label(t2_frame1, text="", background='white')
t2_seller_name.place(x=80, y=12)

t2_label3 = ttk.Label(t2_frame1, text="総出品数", background='white')
t2_label3.place(x=pl_x, y=pl_y)

t2_label4 = ttk.Label(t2_frame1, text="", background='white')
t2_label4.place(x=pl_x + 60, y=pl_y)

t2_label5 = ttk.Label(t2_frame1, text="総販売数", background='white')
t2_label5.place(x=pl_x + 120 - 10, y=pl_y)

t2_label6 = ttk.Label(t2_frame1, text="", background='white')
t2_label6.place(x=pl_x + 180 - 10, y=pl_y)

t2_label7 = ttk.Label(t2_frame1, text="総在庫数", background='white')
t2_label7.place(x=pl_x + 240 - 10, y=pl_y)

t2_label8 = ttk.Label(t2_frame1, text="", background='white')
t2_label8.place(x=pl_x + 300 - 20, y=pl_y)

t2_label9 = ttk.Label(t2_frame1, text="在庫率", background='white')
t2_label9.place(x=pl_x + 360 - 20, y=pl_y)

t2_label10 = ttk.Label(t2_frame1, text="", background='white')
t2_label10.place(x=pl_x + 420 - 20, y=pl_y)

t2_list_label = ttk.Label(t2_frame1, text="売り切れ商品人気順リスト", background='white')
t2_list_label.place(x=350, y=70)

t2_frame2 = tk.Frame(tab_two, background="white", relief="ridge")
t2_frame2.pack(padx="10", pady="10", fill="both", expand=True)

t2_list_space = tk.Canvas(t2_frame2, bg="white")
t2_list_space.pack(fill="both", expand=True)

root.mainloop()
