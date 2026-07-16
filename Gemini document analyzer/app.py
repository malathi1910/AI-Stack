import gradio as gr
import os
from google import genai
from google.genai import types
from gtts import gTTS
import tempfile

# ====================================
# Gemini API Key
# ====================================
client = genai.Client(
    api_key=os.getenv("Gemini_API")
)

# ====================================
# Core Task Functions
# ====================================
def extract_text(file):
    if file is None:
        return "Please upload a file first.", None

    uploaded_file_ref = client.files.upload(file=file.name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file_ref, "Extract all text exactly as written."]
    )
    return response.text, None


def summarize(file):
    if file is None:
        return "Please upload a file first.", None

    uploaded_file_ref = client.files.upload(file=file.name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file_ref, "Summarize this document in simple language."]
    )
    return response.text, None


def answer_question(file, question):
    if file is None:
        return "Please upload a file first.", None
    if not question.strip():
        return "Please enter a question.", None

    uploaded_file_ref = client.files.upload(file=file.name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded_file_ref,
            f"Answer the following question using ONLY this document.\n\nQuestion:\n{question}"
        ]
    )
    return response.text, None


def audio_summary(file):
    if file is None:
        return "Please upload a file first.", None

    uploaded_file_ref = client.files.upload(file=file.name)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file_ref, "Summarize this document."]
    )
    summary = response.text

    # Generate Audio file
    audio_file = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ).name
    gTTS(summary).save(audio_file)

    return summary, audio_file


# ====================================
# UI Layout (No Dropdown Layout)
# ====================================
with gr.Blocks() as demo:

    gr.Markdown("# 📄 Gemini Document Analyzer")

    with gr.Row():
        # Left Side: File Upload Window
        with gr.Column(scale=1):
            file = gr.File(label="Upload PDF/Image")

        # Right Side: Structured Actions Panels
        with gr.Column(scale=2):
            gr.Markdown("### 🛠️ Choose an Action")

            with gr.Row():
                btn_extract = gr.Button("🔍 Extract Text", variant="secondary")
                btn_summarize = gr.Button("📝 Summarize Document", variant="secondary")
                btn_audio = gr.Button("🔊 Generate Audio Summary", variant="secondary")

            gr.Markdown("---")
            gr.Markdown("### ❓ Document Q&A")
            question = gr.Textbox(
                label="Ask a specific question about the document",
                placeholder="Type your question here..."
            )
            btn_qa = gr.Button("💡 Answer Question", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### 📊 Outputs")

    with gr.Row():
        output = gr.Textbox(label="Text Output", lines=12, scale=2)
        audio = gr.Audio(label="Audio Playback", scale=1)

    # ====================================
    # Button Event Bindings
    # ====================================
    btn_extract.click(
        fn=extract_text,
        inputs=[file],
        outputs=[output, audio]
    )

    btn_summarize.click(
        fn=summarize,
        inputs=[file],
        outputs=[output, audio]
    )

    btn_audio.click(
        fn=audio_summary,
        inputs=[file],
        outputs=[output, audio]
    )

    btn_qa.click(
        fn=answer_question,
        inputs=[file, question],
        outputs=[output, audio]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    debug=True
)
