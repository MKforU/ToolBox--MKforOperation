import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
import threading
import cv2
import numpy as np
import win32gui
import ctypes
from datetime import datetime
from PIL import ImageGrab
from ui_theme import RoundButton, BG, TITLE_FG, OK_BG, OK_HO, OK_FG, ENTRY_BG, BTN_FG

# 4K 高分屏修复
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

STOP_BG = "#ff7a9e"   # 深樱花粉（停止按钮）
STOP_HO = "#e85a8f"   # 玫瑰粉
DIS_BG  = "#f0e0e5"   # 淡灰粉（禁用状态）
DIS_FG  = "#c0a0a8"   # 浅灰粉


class ScreenRecorder:
    def __init__(self):
        self.recording  = False
        self.save_path  = ""
        self.hwnd       = None
        self.start_time = None

    def get_window_list(self):
        windows = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
            return True
        win32gui.EnumWindows(callback, None)
        return windows

    def get_correct_rect(self, hwnd):
        try:
            f    = ctypes.windll.dwmapi.DwmGetWindowAttribute
            rect = ctypes.wintypes.RECT()
            f(hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect))
            return rect.left, rect.top, rect.right, rect.bottom
        except:
            return win32gui.GetWindowRect(hwnd)

    def start_record(self, update_label):
        if not self.hwnd:
            messagebox.showwarning("提示", "请先选择要录制的窗口！"); return
        if not self.save_path:
            messagebox.showwarning("提示", "请选择保存目录！"); return

        self.recording  = True
        self.start_time = time.time()
        update_label("🎬 录制中...")

        left, top, right, bottom = self.get_correct_rect(self.hwnd)
        w, h = right - left, bottom - top
        filename  = f"录屏_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        save_full = os.path.join(self.save_path, filename)
        out = cv2.VideoWriter(save_full, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (w, h))

        while self.recording:
            try:
                img   = ImageGrab.grab(bbox=(left, top, right, bottom))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                out.write(frame)
            except:
                break
            time.sleep(0.05)

        out.release()
        update_label("✅ 录制完成")
        messagebox.showinfo("完成", f"录屏已保存！\n{save_full}")

    def stop_record(self, update_label):
        self.recording = False
        update_label("⏹ 已停止")

    def update_timer(self, update_time):
        while self.recording:
            cost = int(time.time() - self.start_time)
            update_time(f"已录制：{cost//60:02d}:{cost%60:02d}")
            time.sleep(1)


def run():
    recorder = ScreenRecorder()
    win = tk.Toplevel()
    win.title("🎬 MK学姐 - 窗口录屏工具")
    win.resizable(True, True)
    win.config(bg=BG)
    win.lift()
    win.attributes("-topmost", True)
    win.focus_force()

    # 创建居中内容容器
    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True)

    # 内容区域，居中显示
    content = tk.Frame(container, bg=BG)
    content.pack(padx=20, pady=20, anchor="center")

    content.grid_columnconfigure(0, weight=1)
    for r, w in enumerate([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]):
        content.grid_rowconfigure(r, weight=w)

    window_list = tk.StringVar()
    save_dir    = tk.StringVar(value="未选择")
    status_text = tk.StringVar(value="等待开始")
    time_text   = tk.StringVar(value="")

    def refresh_windows():
        titles = [f"{h} | {t}" for h, t in recorder.get_window_list() if len(t) > 3]
        combobox['values'] = titles
        if titles: combobox.current(0)

    def select_window(event):
        sel = combobox.get()
        if sel: recorder.hwnd = int(sel.split(" | ")[0])

    def select_save():
        d = filedialog.askdirectory()
        if d:
            save_dir.set(d)
            recorder.save_path = d
        win.lift()
        win.focus_force()

    def start_thread():
        if recorder.recording: return
        # 开始按钮变灰
        btn_start._bg = btn_start._hover = DIS_BG
        btn_start._fg = DIS_FG
        btn_start._draw(DIS_BG)
        btn_start.unbind("<Enter>")
        btn_start.unbind("<Leave>")
        btn_start.unbind("<Button-1>")
        # 停止按钮激活
        btn_stop._bg = STOP_BG; btn_stop._hover = STOP_HO; btn_stop._fg = OK_FG
        btn_stop._draw(STOP_BG)
        btn_stop.bind("<Enter>",    lambda e: btn_stop._draw(STOP_HO))
        btn_stop.bind("<Leave>",    lambda e: btn_stop._draw(STOP_BG))
        btn_stop.bind("<Button-1>", lambda e: stop_thread())
        threading.Thread(target=lambda: recorder.start_record(status_text.set), daemon=True).start()
        threading.Thread(target=lambda: recorder.update_timer(time_text.set),   daemon=True).start()

    def stop_thread():
        recorder.stop_record(status_text.set)
        time_text.set("")
        # 开始按钮恢复
        btn_start._bg = OK_BG; btn_start._hover = OK_HO; btn_start._fg = OK_FG
        btn_start._draw(OK_BG)
        btn_start.bind("<Enter>",    lambda e: btn_start._draw(OK_HO))
        btn_start.bind("<Leave>",    lambda e: btn_start._draw(OK_BG))
        btn_start.bind("<Button-1>", lambda e: start_thread())
        # 停止按钮变灰
        btn_stop._bg = btn_stop._hover = DIS_BG
        btn_stop._fg = DIS_FG
        btn_stop._draw(DIS_BG)
        btn_stop.unbind("<Enter>")
        btn_stop.unbind("<Leave>")
        btn_stop.unbind("<Button-1>")

    # ===== UI =====
    tk.Label(content, text="🎬 窗口录屏工具",
             font=("微软雅黑", 18, "bold"), bg=BG, fg=TITLE_FG).grid(row=0, column=0, pady=(16, 4))

    tk.Label(content, text="选择要录制的窗口",
             font=("微软雅黑", 12), bg=BG, fg=BTN_FG).grid(row=1, column=0, pady=(4, 0))

    style = ttk.Style()
    style.configure("Pink.TCombobox", fieldbackground=ENTRY_BG, background=ENTRY_BG)
    combobox = ttk.Combobox(content, textvariable=window_list,
                            font=("微软雅黑", 11), width=55, style="Pink.TCombobox")
    combobox.grid(row=2, column=0, padx=20, pady=5)
    combobox.bind("<<ComboboxSelected>>", select_window)

    RoundButton(content, text="🔄 刷新窗口列表", command=refresh_windows,
                width=200, height=40).grid(row=3, column=0, pady=4)

    RoundButton(content, text="📂 选择保存目录", command=select_save,
                width=200, height=40).grid(row=4, column=0, pady=4)

    tk.Entry(content, textvariable=save_dir, font=("微软雅黑", 10),
             width=50, state="readonly", relief="flat",
             bg=ENTRY_BG, fg=BTN_FG).grid(row=5, column=0, padx=20, pady=4)

    tk.Label(content, textvariable=status_text,
             font=("微软雅黑", 14, "bold"), bg=BG, fg=TITLE_FG).grid(row=6, column=0, pady=(10, 2))

    tk.Label(content, textvariable=time_text,
             font=("微软雅黑", 12), bg=BG, fg=BTN_FG).grid(row=7, column=0, pady=(0, 4))

    btn_frame = tk.Frame(content, bg=BG)
    btn_frame.grid(row=9, column=0, pady=(8, 20))

    btn_start = RoundButton(btn_frame, text="▶️ 开始录制", command=start_thread,
                            bg=OK_BG, hover=OK_HO, fg=OK_FG, width=160, height=46)
    btn_start.grid(row=0, column=0, padx=12)

    btn_stop = RoundButton(btn_frame, text="⏹️ 停止保存", command=None,
                           bg=DIS_BG, hover=DIS_BG, fg=DIS_FG, width=160, height=46)
    btn_stop.grid(row=0, column=1, padx=12)

    refresh_windows()

    win.update_idletasks()
    w  = max(win.winfo_reqwidth() + 40, 620)
    h  = max(win.winfo_reqheight() + 20, 480)
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    win.minsize(580, 460)
