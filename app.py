import gradio as gr
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a brutal but fair red team analyst. 
When given an idea, plan, or argument, your job is to:
1. Find the weakest points and attack them specifically
2. Give concrete failure scenarios, not vague criticism
3. Rate the idea's survivability from 0-100
4. End with ONE specific question the person must answer to defend their idea

Be sharp, specific, and ruthless. No encouragement. Format your response as:
WEAKNESSES: (bullet points)
FAILURE SCENARIO: (a specific story of how this fails)
SURVIVABILITY SCORE: X/100
DEFEND THIS: (one hard question)"""

def redteam(idea, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": f"Red team this: {idea}"})

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
    )

    return response.choices[0].message.content

with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# =4 Red Team Bot")
    gr.Markdown("### Submit your idea. We will destroy it.")
    
    chatbot = gr.Chatbot(height=500)
    idea_input = gr.Textbox(
        placeholder="Describe your idea, plan, or argument...",
        label="Your Idea"
    )
    submit_btn = gr.Button(" Attack My Idea", variant="primary")
    clear_btn = gr.Button("Reset")

    def respond(idea, history):
        response = redteam(idea, history)
        history.append((idea, response))
        return "", history

    submit_btn.click(respond, [idea_input, chatbot], [idea_input, chatbot])
    idea_input.submit(respond, [idea_input, chatbot], [idea_input, chatbot])
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, idea_input])

demo.launch()
