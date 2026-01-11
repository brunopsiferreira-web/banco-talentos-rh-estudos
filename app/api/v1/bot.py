from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot import generate_job_from_text

router = APIRouter(prefix="/bot", tags=["bot"])

class UserMessage(BaseModel):
    message: str

@router.post("/suggest-job")
def suggest_job(data: UserMessage):
    """
    Recebe o pedido do usuário e retorna a estrutura da vaga sugerida
    """
    job_suggestion = generate_job_from_text(data.message)
    
    if not job_suggestion:
        raise HTTPException(status_code=500, detail="Não foi possível gerar a vaga.")
        
    return job_suggestion