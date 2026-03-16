import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import time
import threading
import cv2
import numpy as np
import win32gui
import win32con
import ctypes
from datetime import datetime
from PIL import ImageGrab

# 4K 高分屏修复
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    pass

class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.save_path = ""
        self.hwnd = None
        self.start_time = None

    def get_window_list(self):
        windows = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                title = win32gui.GetWindowText(hwnd)
                windows.append((hwnd, title))
            return True
        win32gui.EnumWindows(callback, None)
        return windows

    def get_correct_rect(self, hwnd):
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, ctypes.byref(rect), ctypes.sizeof(rect))
            return rect.left, rect.top, rect.right, rect.bottom
        except:
            return win32gui.GetWindowRect(hwnd)

    def start_record(self, update_label):
        if not self.hwnd:
            messagebox.showwarning("提示", "请先选择要录制的窗口！")
            return
        if not self.save_path:
            messagebox.showwarning("提示", "请选择保存目录！")
            return

        self.recording = True
        self.start_time = time.time()
        update_label("🎬 录制中...")

        left, top, right, bottom = self.get_correct_rect(self.hwnd)
        w = right - left
        h = bottom - top

        filename = f"录屏_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        save_full = os.path.join(self.save_path, filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(save_full, fourcc, 20.0, (w, h))

        while self.recording:
            try:
                img = ImageGrab.grab(bbox=(left, top, right, bottom))
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
            m = cost // 60
            s = cost % 60
            update_time(f"已录制：{m:02d}:{s:02d}")
            time.sleep(1)

recorder = ScreenRecorder()

def run():
    win = tk.Tk()
    win.title("🎬 MK学姐 - 窗口录屏工具")
    win.geometry("600x500")
    win.resizable(True, True)
    win.config(bg="#fdf0f6")

    main_frame = tk.Frame(win, bg="#fdf0f6")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    window_list = tk.StringVar()
    save_dir = tk.StringVar(value="未选择")
    status_text = tk.StringVar(value="等待开始")
    time_text = tk.StringVar(value="")

    def refresh_windows():
        windows = recorder.get_window_list()
        titles = [f"{hwnd} | {title}" for hwnd, title in windows if len(title) > 3]
        combobox['values'] = titles
        if titles:
            combobox.current(0)

    def select_window(event):
        sel = combobox.get()
        if not sel:
            return
        hwnd_str = sel.split(" | ")[0]
        recorder.hwnd = int(hwnd_str)

    def select_save():
        d = filedialog.askdirectory()
        if d:
            save_dir.set(d)
            recorder.save_path = d

    def start_thread():
        if recorder.recording:
            return
        btn_start.config(state=tk.DISABLED, bg="#cccccc", text="▶️ 录制中")
        btn_stop.config(state=tk.NORMAL)
        t1 = threading.Thread(target=lambda: recorder.start_record(status_text.set), daemon=True)
        t2 = threading.Thread(target=lambda: recorder.update_timer(time_text.set), daemon=True)
        t1.start()
        t2.start()

    def stop_thread():
        recorder.stop_record(status_text.set)
        btn_start.config(state=tk.NORMAL, bg="#f472b6", text="▶️ 开始录制")
        btn_stop.config(state=tk.DISABLED)
        time_text.set("")

    # ===================== UI 界面 =====================
    tk.Label(main_frame, text="🎬 MK学姐 - 窗口录屏工具", font=("微软雅黑", 18, "bold"),
             bg="#fdf0f6", fg="#c74a87").pack(pady=10)

    tk.Label(main_frame, text="选择要录制的窗口", font=("微软雅黑", 12), bg="#fdf0f6", fg="#be3a7e").pack()
    combobox = ttk.Combobox(main_frame, textvariable=window_list, font=("微软雅黑", 11), width=55)
    combobox.pack(pady=5)
    combobox.bind("<<ComboboxSelected>>", select_window)

    tk.Button(main_frame, text="🔄 刷新窗口列表", font=("微软雅黑", 11),
              bg="#f8cfe1", fg="#be3a7e", relief="flat", command=refresh_windows).pack(pady=3)

    tk.Button(main_frame, text="📂 选择保存目录", font=("微软雅黑", 11),
              bg="#f8cfe1", fg="#be3a7e", relief="flat", command=select_save).pack(pady=5)

    tk.Entry(main_frame, textvariable=save_dir, font=("微软雅黑", 10), width=50, state="readonly").pack(pady=5)

    # 状态 + 计时
    tk.Label(main_frame, textvariable=status_text, font=("微软雅黑", 14, "bold"),
             bg="#fdf0f6", fg="#e11d60").pack(pady=8)
    tk.Label(main_frame, textvariable=time_text, font=("微软雅黑", 12),
             bg="#fdf0f6", fg="#c74a87").pack()

    # 🔥 关键提示：告诉你可以缩放窗口
    tk.Label(main_frame, text="💡 若看不见录制按钮，可拖动窗口边缘放大显示",
             font=("微软雅黑", 10, "bold"),
             bg="#fdf0f6", fg="#c74a87").pack(pady=5)

    # ===================== 按钮区域 =====================
    btn_frame = tk.Frame(main_frame, bg="#fdf0f6")
    btn_frame.pack(side=tk.BOTTOM, pady=20)

    btn_start = tk.Button(
        btn_frame, text="▶️ 开始录制", font=("微软雅黑", 12, "bold"),
        bg="#f472b6", fg="white", padx=15, pady=8,
        command=start_thread
    )
    btn_start.grid(row=0, column=0, padx=12)

    btn_stop = tk.Button(
        btn_frame, text="⏹️ 停止保存", font=("微软雅黑", 12, "bold"),
        bg="#db2777", fg="white", padx=15, pady=8,
        command=stop_thread, state=tk.DISABLED
    )
    btn_stop.grid(row=0, column=1, padx=12)

    refresh_windows()
    win.mainloop()