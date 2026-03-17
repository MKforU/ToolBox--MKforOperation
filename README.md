<div align="center">

# 🧁 MK学姐 · 软糯工具盒

**一个颜值在线、功能实在的 GUI 小工具集合**
专治各种"这个操作好麻烦啊"的日常困扰 ✨

![Python](https://img.shields.io/badge/Python-3.8+-f472b6?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-be3a7e?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-fda4cf?style=flat-square)

</div>

---

## 🎀 这是什么？

一个由 MK学姐 亲手打造的多功能小工具盒子 🧁

界面软糯粉嫩、操作傻瓜无脑，专门收纳那些"每次都要搜一遍怎么做"的日常操作。
打包成 EXE，双击即用，不需要装任何环境，拿来就跑 🏃‍♀️

---

## ✨ 功能一览

### 📄 1. PDF 转图片
> "这个 PDF 我只想截几张图，但截图又模糊……"

- 选择 PDF 文件，选择输出文件夹，一键逐页转为高清 PNG
- 全程图形化，不用命令行，不用动脑子

---

### 📊 2. 表格去重（Excel / xlsx）
> "这份名单里有好多重复的，一个个删要死了……"

- 支持按**指定列**去重（下拉选列名，不用手动输）
- 支持**整行完全重复**去重
- 去重前/重复数/去重后，数据一目了然
- 输出文件自动命名，原文件安全不覆盖

---

### 📁 3. 文件转 PDF
> "发给甲方的文件要 PDF 格式，但我只有 Word/图片……"

- 支持格式：图片（PNG/JPG/JPEG/GIF/BMP/TIFF）、Word（DOCX/DOC）、TXT、HTML
- 图片自动适配 A4 尺寸，等比缩放，好看不变形
- 自定义保存目录，转完告诉你存哪了

---

### 🎬 4. 窗口录屏
> "我想录一下这个窗口的操作，但不想录到其他乱七八糟的东西……"

- 支持选择**指定窗口**录制
- 输出 MP4 格式
- 图形化控制开始 / 停止，实时显示录制时长

---

## 🚀 快速开始

### 方式一：直接用 EXE（推荐，无需任何环境）

前往 [Releases](../../releases) 页面下载最新的 `main.exe`，双击运行即可。

> ⚠️ Windows 可能弹出安全提示，点「仍要运行」就好，这是正常现象。

---

### 方式二：从源码运行（开发者 / 想自己改改的同学）

#### 1. 环境要求

| 依赖 | 版本要求 |
|------|---------|
| Python | 3.8 及以上 |
| 操作系统 | Windows（录屏功能依赖 Win32 API） |

#### 2. 克隆项目

```bash
git clone https://github.com/MKforU/ToolBox--MKforOperation.git
cd ToolBox--MKforOperation
```

#### 3. 安装依赖

```bash
pip install pymupdf pillow pandas openpyxl python-docx reportlab opencv-python pywin32
```

#### 4. 运行

```bash
python main.py
```

---

### 方式三：自己打包成 EXE

```bash
pip install pyinstaller
pyinstaller main.spec
```

打包完成后，`dist/main.exe` 就是你的专属工具盒 🎁

---

## 📦 项目结构

```
ToolBox--MKforOperation/
├── main.py              # 主入口，负责渲染主界面
├── func_list.py         # 功能注册表，新增功能在这里登记
├── ui_theme.py          # UI 主题和样式定义
├── functions/           # 各功能模块
│   ├── pdf_to_image.py  # PDF 转图片
│   ├── remove_duplicate.py  # 表格去重
│   ├── file_to_pdf.py   # 文件转 PDF
│   └── screen_record.py # 窗口录屏
└── main.spec            # PyInstaller 打包配置
```

---

## 💗 关于作者

**MK学姐** · 软糯多巴胺版工具制造者

> 做工具是因为懒，懒得每次都重复同样的操作。
> 如果你也觉得好用，给个 ⭐ 就是最好的鼓励！

---

<div align="center">
💗 温柔好用 · MK学姐专属工具盒 💗
</div>
