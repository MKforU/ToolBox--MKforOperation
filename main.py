import tkinter as tk
from tkinter import ttk
from ui_theme import RoundButton, BG, TITLE_FG, SUB_FG
from func_list import FUNCTION_LIST

def main():
    root = tk.Tk()
    root.title("🧁 MK学姐 · 软糯工具盒")
    root.geometry("680x550")
    root.resizable(True, True)
    root.config(bg=BG)

    x = (root.winfo_screenwidth() - 680) // 2
    y = (root.winfo_screenheight() - 550) // 2
    root.geometry(f"+{x}+{y}")

    tk.Label(root, text="🧁 MK 学姐 · 实用工具盒",
             font=("微软雅黑", 21, "bold"), bg=BG, fg=TITLE_FG).pack(pady=12)

    tk.Label(root, text="✨ 制作：MK 学姐｜软糯多巴胺版 ✨",
             font=("微软雅黑", 12, "bold"), bg=BG, fg=SUB_FG).pack(pady=4)

    frame = tk.Frame(root, bg=BG)
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    row = 0
    col = 0
    max_col = 2

    for key, item in FUNCTION_LIST.items():
        btn = RoundButton(frame, text=item["name"], command=item["func"],
                          width=240, height=56)
        btn.grid(row=row, column=col, padx=16, pady=16)
        col += 1
        if col >= max_col:
            col = 0
            row += 1

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    tk.Label(root, text="💗 温柔好用 · MK学姐专属工具盒 💗",
             font=("微软雅黑", 10, "bold"), bg=BG, fg=SUB_FG).pack(side="bottom", pady=18)

    root.mainloop()

if __name__ == "__main__":
    main()
