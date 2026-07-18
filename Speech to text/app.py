# From Speech to text

import gradio as gr
from google import genai

#Gemini API Key
client=genai.Client(api_key="YOUR_API_KEY")

def transcribe(audio_path):
  if audio_path is None:
    return "Please record some audio."

    #upload recorded audio
    audio_file=client.files.upload(file=audio_path)

    #transcribe
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "Transcribe this audio exactly as spoken. Do not summarize. Include punctuation.",
            audion_file,
        ],
    )
    return response.text

with gr.Blocks(title="Gemini Audio Transcription") as demo:
  gr.Markdown("# Audio Transcription with Gemini")

  audio=gr.Audio(
      sources=["microphone"],
      type="filepath",
      label="Record Your voice"
  )

  output=gr.Textbox(
     label="Transcript",
     lines=10
  )

  btn=gr.Button("Transcribe")

  btn.click(
      fn=transcribe,
      inputs=audio,
      outputs=output
  )
demo.launch()

