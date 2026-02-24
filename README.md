# Red Team Bot

An adversarial AI that stress-tests your ideas, plans, and arguments by finding weaknesses, generating failure scenarios, and scoring survivability.

## Live Demo
[Try it on Hugging Face Spaces](https://huggingface.co/spaces/apurvapillai24/red-team-bot)

## What it does
- Takes any idea, startup pitch, plan, or argument as input
- Identifies the weakest points with specific criticism
- Generates a concrete failure scenario
- Assigns a survivability score from 0-100
- Asks one hard question you must answer to defend your idea
- Supports multi-turn conversation so you can fight back

## Tech Stack
- **LLM:** LLaMA 3.3 70B via Groq API
- **Frontend:** Gradio
- **Deployment:** Hugging Face Spaces

## How it was built
The app is built around a carefully engineered system prompt that instructs LLaMA 3.3 70B to act as a ruthless red team analyst. Rather than giving generic feedback, the model is forced into a structured output format  weaknesses, failure scenario, survivability score, and a single hard question  making responses actionable and consistent.

The conversation history is passed back to the model on each turn, enabling multi-round debates where the user can defend their idea and the bot continues to push back with context.

The interface is built with Gradio and served via Hugging Face Spaces. The Groq API was chosen for its low-latency inference on large open-source models, enabling near real-time responses.

## Run Locally
```bash
git clone https://github.com/apurvapillai/red-team-bot
cd red-team-bot
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
python app.py
```
