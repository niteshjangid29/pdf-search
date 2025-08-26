from pydantic import BaseModel
from typing import Literal, Union, List
from PIL import Image
import pytesseract
import pymupdf
import io

class ExtractedContentFormat(BaseModel):
    type: Literal["text", "table", "image"]
    page_number: int
    block_index: int
    content: str
    error: Union[str, None] = None

class ExtractedContent(BaseModel):
    all_content: List[ExtractedContentFormat] = []
    error: Union[str, None] = None


def format_table_content(table_data: List[List[str]]) -> str:
    if not table_data:
        return ""
    
    formatted_data = ""
    headers = table_data[0] if table_data and table_data[0] else []
    rows = table_data[1:] if len(table_data) > 1 else []

    if headers:
        formatted_data += "Headers: " + ", ".join(str(h).strip() for h in headers if h is not None) + ". "

    if rows:
        for idx, row in enumerate(rows):
            formatted_data += f"Row {idx + 1}: " + ", ".join(str(cell).strip() for cell in row if cell is not None) + ". "

    return formatted_data.strip()


def extract_pdf_content(pdf_content: bytes) -> ExtractedContent:
    extracted_data = ExtractedContent()

    try:
        pdf = pymupdf.open(stream=pdf_content, filetype="pdf")

        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)

            # 1. Extract text blocks
            text_blocks = page.get_text("blocks")
            for idx, block in enumerate(text_blocks):
                content = block[4].strip()
                if content:
                    extracted_data.all_content.append(ExtractedContentFormat(
                        type="text",
                        page_number=page_num,
                        block_index=idx,
                        content=content
                    ))

            # 2. Extract Tables
            tables = page.find_tables()
            for idx, table in enumerate(tables):
                try:
                    table_data = table.extract()
                    content = format_table_content(table_data=table_data)
                    if content:
                        extracted_data.all_content.append(ExtractedContentFormat(
                            type="table",
                            page_number=page_num,
                            block_index=idx,
                            content=content
                        ))
                except Exception as e:
                    print(f"Error extracting table on page {page_num}, table {idx}: {e}")
                    extracted_data.all_content.append(ExtractedContentFormat(
                        type="table",
                        page_number=page_num,
                        block_index=idx,
                        content="",
                        error=f"Failed to extract table: {e}"
                    ))

            # 3. Extract Images
            images = page.get_images(full=True)
            for idx, img_info in enumerate(images):
                xref = img_info[0]

                try:
                    base_image = pdf.extract_image(xref)
                    image_bytes = base_image["image"]

                    image_stream = io.BytesIO(image_bytes)
                    pil_image = Image.open(image_stream)

                    # OCR
                    ocr_text = pytesseract.image_to_string(pil_image, lang="eng").strip()

                    if ocr_text:
                        extracted_data.all_content.append(ExtractedContentFormat(
                            type="image",
                            page_number=page_num,
                            block_index=idx,
                            content=ocr_text
                        ))

                except Exception as e:
                    print(f"Error extracting image on page {page_num}, image {idx}: {e}")

        pdf.close()

    except Exception as e:
        print(f"Error processing PDF: {e}")
        extracted_data.error = f"An error occurred during PDF processing: {e}"

    return extracted_data