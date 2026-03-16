from functions.pdf_to_image import run as pdf_to_image
from functions.remove_duplicate import run as remove_duplicate

FUNCTION_LIST = {
    "1": {
        "name": "PDF 转 图片",
        "func": pdf_to_image
    },
    "2": {
        "name": "表格去重",
        "func": remove_duplicate
    }
}
