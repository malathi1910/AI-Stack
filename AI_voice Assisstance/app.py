import gradio as gr
from google import genai
import speech_recognition as sr
from gtts import gTTS
import tempfile

client=genai.Client(api_key="")

#Speech to Text
def speech_to_text(audio):
  recognizer=sr.Recognizer()

  with sr.AudioFile(audio) as source:
    audio_data=recognizer.record(source)
  try:
    return recognizer.recognize_google(audio_data)
  except:
    return "Sorry, I couldn't understand."

def ask_gemini(text):
  response=client.models.generate_content(
      model="gemini-2.5-flash",
      contents=text
  )
  return response.text

#text to speech
def text_to_speech(text):
  tts=gTTS(text)
  path=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3").name
  tts.save(path)
  return path

#main Function
def voice_assisstant(audio):
  user_text=speech_to_text(audio)
  ai_reply=ask_gemini(user_text)
  voice=text_to_speech(ai_reply)

  return user_text,ai_reply,voice

demo=gr.Interface(
    fn=voice_assisstant,
    inputs=gr.Audio(type="filepath",label="Speak"),
    outputs=[
        gr.Textbox(label="You Said"),
        gr.Textbox(label="Gemini"),
        gr.Textbox(label="Voice Response")
    ],
    title="Simple AI voice Assisstance."
)

demo.launch(debug=True,share=True)
