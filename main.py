import tkinter as tk
from tkinter import ttk
from func_list import FUNCTION_LIST

def create_round_button(parent, text, command):
    # 自定义圆角按钮样式（真正圆润无棱角）
    btn = tk.Button(
        parent,
        text=text,
        font=("微软雅黑", 13, "bold"),
        bg="#f8cfe1",       # 软糯浅粉
        fg="#be3a7e",       # 柔和豆沙红
        activebackground="#f5b9d2",
        activeforeground="#a32d6b",
        relief="flat",
        bd=0,
        padx=20,
        pady=12,
        cursor="hand2",
        command=command
    )
    # Tkinter圆角模拟（柔和无边角）
    btn.config(
        highlightthickness=0,
        borderwidth=0,
    )
    return btn

def main():
    root = tk.Tk()
    root.title("🧁 MK学姐 · 软糯工具盒")
    root.geometry("680x550")
    root.resizable(True, True)
    root.config(bg="#fdf0f6")  # 超柔和马卡龙浅粉底

    # 窗口居中
    x = (root.winfo_screenwidth() - 680) // 2
    y = (root.winfo_screenheight() - 550) // 2
    root.geometry(f"+{x}+{y}")

    # ========== 标题 ==========
    tk.Label(
        root,
        text="🧁 MK 学姐 · 实用工具盒",
        font=("微软雅黑", 21, "bold"),
        bg="#fdf0f6",
        fg="#c74a87"
    ).pack(pady=12)

    # ========== 署名 ==========
    tk.Label(
        root,
        text="✨ 制作：MK 学姐｜软糯多巴胺版 ✨",
        font=("微软雅黑", 12, "bold"),
        bg="#fdf0f6",
        fg="#e16a9c"
    ).pack(pady=4)

    # ========== 功能按钮区域 ==========
    frame = tk.Frame(root, bg="#fdf0f6")
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    row = 0
    col = 0
    max_col = 2

    for key, item in FUNCTION_LIST.items():
        name = item["name"]
        func = item["func"]

        btn = create_round_button(frame, name, func)
        btn.grid(row=row, column=col, padx=16, pady=16, sticky="nsew")

        col += 1
        if col >= max_col:
            col = 0
            row += 1

    # 自适应布局
    for c in range(max_col):
        frame.grid_columnconfigure(c, weight=1)

    # ========== 底部 ==========
    tk.Label(
        root,
        text="💗 温柔好用 · MK学姐专属工具盒 💗",
        font=("微软雅黑", 10, "bold"),
        bg="#fdf0f6",
        fg="#d15a8c"
    ).pack(side="bottom", pady=18)

    root.mainloop()

if __name__ == "__main__":
    main()