from fastapi import FastAPI, Request, Form
from typing import Optional
from main import templates
from fastapi.responses import HTMLResponse

questions = [
    {
        "question": "What is Vue?",
        "answer": 1,
        "options": [
            "A framework",
            "A library",
            "A type of hat"
        ],
        "selected": None
    },
    # Add more questions
]

def init_app(app: FastAPI):
    @app.get("/quiz/{question_id}", response_class=HTMLResponse)
    async def get_quiz(request: Request, question_id: int, message: Optional[str] = None):
        context = {"request": request, "question": questions[question_id], "message": message}
        return templates.TemplateResponse("trivia.html", context)

    @app.post("/quiz/{question_id}", response_class=HTMLResponse)
    async def post_quiz(request: Request, question_id: int, answer: int = Form(...)):
        message = None
        if answer == questions[question_id]["answer"]:
            message = "Correct!"
        else:
            message = "Incorrect. Try again."

        context = {"request": request, "question": questions[question_id], "message": message}
        return templates.TemplateResponse("trivia.html", context)