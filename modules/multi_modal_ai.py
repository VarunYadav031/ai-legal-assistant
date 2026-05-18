from modules.qa_chatbot import ask_question
from modules.image_reader import extract_text_from_image
from modules.table_reader import extract_table_insights


def process_input(file, file_type, question=None, chat_history=None, language="hinglish"):

    text = ""

    # ---------------- IMAGE ----------------
    if file_type == "image":
        text = extract_text_from_image(file)

    # ---------------- TABLE ----------------
    elif file_type == "table":
        data = extract_table_insights(file)
        text = str(data)

    # ---------------- TEXT/PDF ----------------
    else:
        text = file


    # ---------------- IF USER ONLY WANTS INSIGHT ----------------
    if question is None:
        return f"📌 Extracted Data:\n\n{text[:2000]}"


    # ---------------- SEND TO AI (RAG + MEMORY) ----------------
    return ask_question(
        question + "\n\nContext:\n" + text,
        chat_history=chat_history,
        language=language
    )