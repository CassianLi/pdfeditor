import time

import PyPDF2
import fitz  # PyMuPDF
import argparse
import json

from borb.pdf import PDF
from borb.toolkit import SimpleFindReplace
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def replace_text_in_pdf(pdf_path, replacement_map, output_path, font_size=8):
    """
    Replace text in a PDF file and make it unselectable.

    :param pdf_path: The path to the input PDF file.
    :param replacement_map: A dictionary with text to be replaced and its replacement.
    :param output_path: The path to save the modified PDF.
    :param font_size: The font size for replacement text (default is 8).
    """
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("blocks")

        for block in blocks:
            replaced = 0
            r_text = block[4]
            for search_text, replacement_text in replacement_map.items():
                if search_text in r_text:
                    replaced = 1
                    r_text = r_text.replace(search_text, replacement_text)

            if replaced == 1:
                x0, y0, x1, y1 = block[:4]
                rect = fitz.Rect(x0, y0 + 1, x1, y1)
                page.draw_rect(rect, color=(1, 1, 1), fill=1)

                replacement_annot = page.add_freetext_annot(
                    rect,
                    r_text,
                    fontname="courier",
                    fontsize=font_size,
                    rotate=0
                )
                replacement_annot.update()

        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    try:
        pdf_document.save(output_path)
    except Exception as e:
        print(f"Error saving PDF: {e}")
    finally:
        pdf_document.close()


def convert_pdf_to_image_pdf(pdf_path, output_path):
    """
    Convert a PDF to an image PDF.
    :param pdf_path:
    :param output_path:
    :return:
    """
    pdf_document = fitz.open(pdf_path)

    # 创建一个新的文档
    output_document = fitz.open()

    resolution = 300  # 例如，设置为600 DPI
    quality = 75
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        # 设置更高的分辨率
        image = page.get_pixmap(matrix=fitz.Matrix(resolution / 72, resolution / 72))

        # 创建一个新的页面，用于容纳图像
        output_page = output_document.new_page(width=image.width, height=image.height)

        # 将图像插入到新的页面中
        output_page.insert_image(output_page.rect, pixmap=image)

    # 保存新的PDF文档
    output_document.save(output_path)
    output_document.close()

    pdf_document.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Replace text in a PDF file.")
    parser.add_argument("--ipdf", type=str, required=True, help="The path to the input PDF file.")
    parser.add_argument("--opdf", type=str, required=True, help="The path where the modified PDF will be saved.")
    parser.add_argument("--replace", type=str, required=True,
                        help="A JSON string containing the replacement map.")

    args = parser.parse_args()

    # Convert the JSON string to a Python dictionary
    replacement_map = json.loads(args.replace)

    start = time.time()
    replace_text_in_pdf(args.ipdf, replacement_map, "temp.pdf")
    convert_pdf_to_image_pdf("temp.pdf", args.opdf)
    end = time.time()
    print("time: ", end - start)
