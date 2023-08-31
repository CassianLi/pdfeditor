import time
import fitz  # PyMuPDF
import argparse
import json


def replace_text_in_pdf(pdf_path, replacement_map, output_path):
    """
    Replace text in a PDF file.
    :param pdf_path:
    :param replacement_map:
    :param output_path:
    :return:
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
                rect = fitz.Rect(block[:4])  # Get the text block dimensions
                page.draw_rect(rect, color=(1, 1, 1), fill=1)  # Draw a rectangle to cover the text block

                font_size = 8  # Adjust this factor as needed
                replacement_annot = page.add_freetext_annot(
                    rect,
                    r_text,
                    fontname="courier",
                    fontsize=font_size,
                    rotate=0
                )
                replacement_annot.update()

        page.apply_redactions()  # Apply redactions after all replacements

    pdf_document.save(output_path)
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
    replace_text_in_pdf(args.ipdf, replacement_map, args.opdf)
    end = time.time()
    print("time: ", end - start)
