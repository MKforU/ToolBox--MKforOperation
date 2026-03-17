import tkinter as tk
from tkinter import ttk

# ========== 全局配色 - 柔软多巴胺风格 ==========
BG       = "#fff5f9"   # 奶霜白底
BTN_BG   = "#ffd6e0"   # 糖果粉
BTN_FG   = "#c2607a"   # 玫瑰豆沙
BTN_HO   = "#ffb8d0"   # 浅莓粉
TITLE_FG = "#e85a8f"   # 玫瑰粉
SUB_FG   = "#ffb6c1"   # 浅粉
OK_BG    = "#ff9eba"   # 樱花粉
OK_HO    = "#ff7a9e"   # 深樱花粉
OK_FG    = "#ffffff"   # 纯白
ENTRY_BG = "#fff0f5"   # 淡薰衣草粉

# ========== 圆角按钮 ==========
class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command, radius=15,
                 bg=BTN_BG, fg=BTN_FG, hover=BTN_HO,
                 font=("微软雅黑", 13, "bold"),
                 width=200, height=52, **kwargs):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0,
                         width=width, height=height, **kwargs)
        
        self._bg = bg
        self._hover = hover
        self._fg = fg
        self._font = font
        self._command = command
        self._radius = radius
        self._text = text
        self._width = width
        self._height = height
        
        # 绘制初始圆角背景（延迟确保初始化完成）
        self.after(10, lambda: self._draw(bg))
        
        # 绑定事件
        self.bind("<Enter>", lambda e: self._draw(hover))
        self.bind("<Leave>", lambda e: self._draw(bg))
        self.bind("<Button-1>", lambda e: self._click())

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        self.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="pieslice", **kw)
        self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="pieslice", **kw)
        self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="pieslice", **kw)
        self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="pieslice", **kw)
        self.create_rectangle(x1+r, y1, x2-r, y2, **kw)
        self.create_rectangle(x1, y1+r, x2, y2-r, **kw)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(0, 0, self._width, self._height, self._radius,
                         fill=color, outline=color)
        self.create_text(self._width//2, self._height//2,
                        text=self._text, fill=self._fg, font=self._font)

    def _click(self):
        self._draw(self._hover)
        self.after(100, lambda: self._draw(self._bg))
        if self._command:
            self._command()
