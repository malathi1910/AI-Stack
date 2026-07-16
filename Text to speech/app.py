# Text to speech
from gtts import gTTS
import gradio as gr

def text_to_speech(text):
  tts=gTTS(text=text,lang="en")
  output_file="output.mp3"
  tts.save(output_file)
  return output_file

demo=gr.Interface(fn=text_to_speech,
                  inputs=gr.Textbox(lines=5,label="Enter Text"),
                  outputs=gr.Audio(label="Speech"),
                  title="Text-to-Speech"
                  )
demo.launch()
