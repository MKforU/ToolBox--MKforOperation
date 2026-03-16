import tkinter as tk
from tkinter import ttk
from func_list import FUNCTION_LIST

def run_selected_func(key):
    root.destroy()
    FUNCTION_LIST[key]["func"]()

# ========== 主窗口 ==========
root = tk.Tk()
root.title("🧰 多功能工具箱")
root.geometry("380x260")
root.resizable(False, False)
root.configure(bg="#fdf6f0")

# 居中
x = (root.winfo_screenwidth() - 380) // 2
y = (root.winfo_screenheight() - 260) // 2
root.geometry(f"+{x}+{y}")

# 风格
style = ttk.Style()
style.configure("TButton", font=("微软雅黑", 11), padding=10)
style.configure("Title.TLabel", font=("微软雅黑", 16, "bold"), background="#fdf6f0", foreground="#5b5b5b")

# 标题
title = ttk.Label(root, text="✨ 请选择功能", style="Title.TLabel")
title.pack(pady=25)

# ========== 功能按钮（圆润多巴胺）==========
colors = ["#ffb7b7", "#b7d9ff", "#c8e6c9", "#fce19c", "#d1c4e9"]
idx = 0

for key, item in FUNCTION_LIST.items():
    btn = tk.Button(
        root,
        text=item["name"],
        font=("微软雅黑", 11, "bold"),
        bg=colors[idx % len(colors)],
        fg="#333",
        relief="flat",
        width=26,
        height=2,
        activebackground="#ffd1d1",
        activeforeground="#222",
        command=lambda k=key: run_selected_func(k),
        cursor="hand2"
    )
    btn.pack(pady=4)
    idx += 1

root.mainloop()