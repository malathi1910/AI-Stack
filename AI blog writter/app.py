from google import genai
import gradio as gr

#Gemini API key
client=genai.Client(api_key="")

def generate_blog(topic,audience,tone,words,language):
  prompt=f"""
  write a {word}-word blog.
  Topic:{topic}
  Audience:{audience}
  Tone :{tone}
  Include:
  -Title
  -Introduction
  -facts
  -Advantages
  -Conclusion
  """
  response=client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt
  )

  return response

demo=gr.Interface(
    fn=generate_blog,
    inputs=[
        gr.Textbox(label="Topic"),
        gr.Textbox(label="Audience"),
        gr.Dropdown(
            ["Professional","Casual","Funny","sarcastic","Technical","Inspirational"],
            label="Tone"
        ),
        gr.Dropdown(
            ["English","Hindi","Telugu","Spanish"],
            label="Language"
        ),
        gr.Slider(200,1000,value=500,label="Word Count")

    ],
    outputs="markdown",
    title="AI Blog Generator(Gemini)"
)
demo.launch()
