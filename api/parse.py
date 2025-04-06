import fitz  # PyMuPDF
import json

def handler(request):
    try:
        if request.method != "POST":
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Only POST allowed"})
            }

        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file uploaded"})
            }

        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page_count = min(len(doc), 300)

        all_text = ""
        for i in range(page_count):
            page_text = doc[i].get_text()
            all_text += f"\n\n--- Page {i+1} ---\n" + page_text

        cleaned = clean_text(all_text)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "ok",
                "source": f"{page_count} pages parsed",
                "raw_character_count": len(cleaned),
                "extracted_text": cleaned
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def clean_text(text):
    import re
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()
