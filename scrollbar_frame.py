import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.canvas = tk.Canvas(self, bg="white")
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal",
                                         command=self.canvas.xview)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical",
                                         command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.create_window((0, 0),
                                  window=self.scrollable_frame,
                                  anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            #ここのlambda e:を付け忘れたらスクロールバーのバーが出なかった。
            # エラーも出なかった。おそらくリストボックスとかはscrollregionの
            # デフォルト設定があるのだと思う。キャンバスにはない。
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind("<MouseWheel>", self.y_wheel)
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

    def y_wheel(self, event):
        unit_count = 0
        if event.delta > 0:
            unit_count = -1
        elif event.delta < 0:
            unit_count = 1
        self.canvas.yview_scroll(unit_count, 'units')
