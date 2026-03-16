import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

def run():
    win = tk.Tk()
    win.title("📊 表格去重工具")
    win.geometry("560x520")
    win.resizable(False, False)
    win.config(bg="#f0f9ff")

    x = (win.winfo_screenwidth() - 560) // 2
    y = (win.winfo_screenheight() - 520) // 2
    win.geometry(f"+{x}+{y}")

    # 变量
    file_path = tk.StringVar(value="未选择")
    save_dir = tk.StringVar(value="未选择")
    mode = tk.StringVar(value="col")
    df = None  # 表格数据
    columns = []  # 列名列表

    # 读取文件并加载列名
    def select_file():
        nonlocal df, columns
        fp = filedialog.askopenfilename(
            filetypes=[("Excel 文件", "*.xlsx"), ("Excel 旧版", "*.xls")]
        )
        if not fp:
            return

        file_path.set(fp)
        try:
            df = pd.read_excel(fp, dtype=str)
            columns = df.columns.tolist()
            col_cb["values"] = columns
            if columns:
                col_cb.current(0)
        except Exception as e:
            messagebox.showerror("错误", f"读取失败：{str(e)}")

    # 选择保存目录
    def select_save():
        d = filedialog.askdirectory()
        if d:
            save_dir.set(d)

    # 开始去重
    def start_remove():
        nonlocal df
        if df is None:
            messagebox.showwarning("提示", "请先选择Excel文件！")
            return
        if save_dir.get() == "未选择":
            messagebox.showwarning("提示", "请选择保存目录！")
            return

        try:
            before = len(df)
            if mode.get() == "col":
                selected_col = col_cb.get()
                new_df = df.drop_duplicates(subset=[selected_col], keep="first")
            else:
                new_df = df.drop_duplicates(keep="first")

            after = len(new_df)
            dup = before - after

            # 输出文件名：原文件名 + 去重结果
            folder, name_ext = os.path.split(file_path.get())
            name, ext = os.path.splitext(name_ext)
            out_file = f"{name}_去重结果{ext}"
            out_path = os.path.join(save_dir.get(), out_file)

            new_df.to_excel(out_path, index=False)

            messagebox.showinfo(
                "✅ 去重完成",
                f"处理成功！\n\n"
                f"去重前：{before} 行\n"
                f"重复项：{dup} 行\n"
                f"去重后：{after} 行\nn"
                f"已保存到：\n{out_path}"
            )
            win.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"失败：{str(e)}")

    # ==================== 界面 ====================
    tk.Label(
        win, text="表格去重工具",
        font=("微软雅黑", 16, "bold"),
        bg="#f0f9ff", fg="#374151"
    ).pack(pady=20)

    # 选择文件
    tk.Button(
        win, text="1. 选择 Excel 文件",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=24, height=2,
        command=select_file
    ).pack(pady=3)
    tk.Entry(win, textvariable=file_path, font=("微软雅黑", 10), width=55, state="readonly").pack(pady=2)

    # 选择保存目录
    tk.Button(
        win, text="2. 选择保存目录",
        font=("微软雅黑", 10, "bold"),
        bg="#bae6fd", fg="#1e3a8a",
        relief="flat", cursor="hand2",
        width=24, height=2,
        command=select_save
    ).pack(pady=3)
    tk.Entry(win, textvariable=save_dir, font=("微软雅黑", 10), width=55, state="readonly").pack(pady=5)

    # 模式
    tk.Label(win, text="3. 去重模式", bg="#f0f9ff", font=("微软雅黑", 10, "bold")).pack(pady=4)
    mode_frame = tk.Frame(win, bg="#f0f9ff")
    mode_frame.pack(pady=2)
    tk.Radiobutton(mode_frame, text="按指定列去重", variable=mode, value="col", bg="#f0f9ff").pack(side="left", padx=8)
    tk.Radiobutton(mode_frame, text="整行完全重复去重", variable=mode, value="row", bg="#f0f9ff").pack(side="left", padx=8)

    # 列选择（下拉框）
    tk.Label(win, text="4. 选择去重依据列", bg="#f0f9ff", font=("微软雅黑", 10, "bold")).pack(pady=4)
    col_cb = ttk.Combobox(win, width=30, font=("微软雅黑", 11), state="readonly")
    col_cb.pack(pady=2)

    # 开始按钮
    tk.Button(
        win, text="✅ 开始去重",
        font=("微软雅黑", 11, "bold"),
        bg="#4ade80", fg="white",
        relief="flat", cursor="hand2",
        width=22, height=2,
        command=start_remove
    ).pack(pady=25)

    win.mainloop()