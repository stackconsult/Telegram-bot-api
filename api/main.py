"""
FastAPI REST API
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Telegram Bot API", version="1.0.0")

class MessageRequest(BaseModel):
    chat_id: int
    text: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"status": "running", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.post("/message")
async def send_message(request: MessageRequest):
    """Send message endpoint"""
    return {"success": True, "message": "Message sent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
