from functions.pdf_to_image import run as pdf_to_image
from functions.remove_duplicate import run as remove_duplicate
from functions.file_to_pdf import run as file_to_pdf
from functions.screen_record import run as screen_record  # 新增

FUNCTION_LIST = {
    "1": {"name": "PDF 转 图片", "func": pdf_to_image},
    "2": {"name": "表格去重", "func": remove_duplicate},
    "3": {"name": "文件 转 PDF", "func": file_to_pdf},
    "4": {"name": "窗口录屏", "func": screen_record}  # 新增
}