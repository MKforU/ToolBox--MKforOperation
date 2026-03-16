# ToolBox--MKforOperation
# 多功能工具箱

一个界面美观、操作简单的 GUI 实用小工具，支持 PDF 转图片、Excel 表格去重等功能，可打包成 EXE 文件直接使用。

---

## 功能介绍

### 1. PDF 转图片
- 选择 PDF 文件
- 选择输出文件夹
- 逐页转换为 PNG 图片
- 纯图形化界面操作，无命令行

### 2. 表格去重（Excel / xlsx）
- 支持按指定列去重（下拉选择列名，无需手动输入）
- 支持整行完全重复去重
- 显示去重统计信息：去重前数量、重复项数量、去重后数量
- 输出文件自动命名：原文件名 + 去重结果

---

## 依赖安装

在项目目录下执行以下命令安装依赖：

```bash
pip install pymupdf
pip install pywin32
pip install pandas
pip install openpyxl
pip install xlrd
