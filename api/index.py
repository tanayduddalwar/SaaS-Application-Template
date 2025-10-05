from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI  # type: ignore
import os
app = FastAPI()
google_api_key=os.getenv("GOOGLE_API_KEY")
@app.get("/api")
def idea():
    gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = "gemini-2.0-flash"
    prompt = [{"role": "user", "content": "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"}]
    stream = gemini.chat.completions.create(model=model_name, messages=prompt, stream=True)

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")