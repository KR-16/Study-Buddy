from process_pdf import extract_pdf_text
from generate_flashcard import generate_qna
import gradio as gr
import json
from pathlib import Path

def save_flashcards(qna_data, format = "txt"):
    """
    Will save the flashcard in txt format
    """

    filename = "flashcard.txt"
    with open(filename, "w") as file:
        for question_num, question in enumerate(qna_data.get("questions", []), 1):
            file.write(f"Q{question_num}: {question["question"]}\n")
            file.write(f"A{question_num}: {question["answer"]}\n\n")
        return filename

def process_input(pdf_file, num_questions, display_mode):
    """
    Extract and process text
    """

    text = extract_pdf_text(pdf_file.name)
    qna = generate_qna(text, num_questions)

    # Save the flashcard
    file_path = save_flashcards(qna)

    # prepare output based on display mode
    if display_mode == "All":
        markdown_output = "ALL FLASHCARDS\n"
        for i, item in enumerate(qna.get("questions",[]),1):
            markdown_output += f"{i}. **{item["question"]}**\n"
            markdown_output += f"   -> {item["answer"]}\n\n"
        return markdown_output, file_path
    else:
        # return first question and full set for iterations
        first_question = qna.get("question",[{}])[0]
        first_output = f"1. **{first_question.get("question", "")}**\n  -> {first_question.get("answer", "")}"
        return first_output, file_path, gr.update(visible=True), qna
    
def show_next(flashcard_data, current_index):
    """Display next flashcard"""
    questions = flashcard_data.get("questions", [])
    if current_index < len(questions):
        current_q = questions[current_index]
        output = f"{current_index+1}. **{current_q['question']}**\n   → {current_q['answer']}"
        return output, current_index+1, gr.update(visible=current_index+1 < len(questions))
    return "", current_index, gr.update(visible=False)

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🧠 AI Study Buddy - Flashcard Generator")
    
    # Store flashcard data between callbacks
    flashcard_data = gr.State()
    current_index = gr.State(0)
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="📄 Upload PDF", file_types=[".pdf"])
            num_questions = gr.Slider(3, 20, value=5, label="Number of Questions")
            display_mode = gr.Radio(
                ["All at once", "One by one"],
                value="All at once",
                label="Display Mode"
            )
            submit_btn = gr.Button("Generate Flashcards", variant="primary")
        
        with gr.Column():
            output_display = gr.Markdown()
            download_file = gr.File(label="Download Flashcards", visible=False)
            next_btn = gr.Button("Next Card ➡️", visible=False)
    
    # Main generation callback
    submit_btn.click(
        fn=process_input,
        inputs=[pdf_input, num_questions, display_mode],
        outputs=[output_display, download_file, next_btn, flashcard_data]
    )
    
    # Next card callback
    next_btn.click(
        fn=show_next,
        inputs=[flashcard_data, current_index],
        outputs=[output_display, current_index, next_btn]
    )

if __name__ == "__main__":
    app.launch(server_port=7860)