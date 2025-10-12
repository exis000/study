from fastapi import FastAPI

app = FastAPI(
    title="Studytwo",
    description="API for the AI-powered Learning Hub, STUDYTWO",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """root endpoint examle returns a welcome message a test  for now 
    """
    return {
        "message":"ROR WELCOME TO SOPING & lexing's STUDY HUB"
    }