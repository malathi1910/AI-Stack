from google import genai
import gradio as gr

#Gemini API key
client=genai.Client(api_key="YOUR_GEMINI_API_KEY")

def review_code(code):


  prompt=f"""Review This Pyhton Code

  Code:{code}
  Include
  1.Summary
  2.Bugs
  3.performance improvements
  4.secutity Isuue
  5.Improve code
  6.Rating out of 10

  """
  response=client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt
  )

  return response

demo=gr.Interface(
    fn=review_code,
    inputs=gr.Textbox(label="code"),
    outputs="markdown",
    title="Code Reviewing"
)
demo.launch()
