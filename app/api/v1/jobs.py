from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.job_service import create_job, get_jobs, get_job, get_job_matches
from app.schemas.job import JobCreate, JobResponse, JobSummary
from app.services.job_service import update_job
# import app.templates as templates
from fastapi.templating import Jinja2Templates


## CRUD de Vagas ##
router = APIRouter(prefix="/jobs", tags=["jobs"])

templates = Jinja2Templates(directory="app/templates")

# Rota para ABRIR a página do Chatbot
@router.get("/ai-assistant") # Remova o response_class por um momento
def ai_assistant_page(request: Request):
    try:
        return templates.TemplateResponse("ai_assistant.html", {"request": request})
    except Exception as e:
        return {"error": str(e)}
    
# Criar uma nova vaga
@router.post("/", response_model=JobResponse)
def create_job_api(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, job)

# Ver todas as vagas
@router.get("/", response_model=list[JobSummary])
def read_jobs(db: Session = Depends(get_db)):
    return get_jobs(db)

# Ver uma vaga específica
@router.get("/{job_id:int}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return job
# Ver candidatos correspondentes a uma vaga
@router.get("/{job_id}/matches")
def read_job_matches(job_id: int, db: Session = Depends(get_db)):
    return get_job_matches(db, job_id)

# Atualizar uma vaga
@router.put("/{job_id}", response_model=JobResponse)
def update_job_api(job_id: int, job_data: JobCreate, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    updated_job = update_job(db, job_id, job_data)
    return updated_job

# Deletar uma vaga
@router.delete("/{job_id}")
def delete_job_api(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(job)
    db.commit()
    return {"detail": "Vaga deletada com sucesso"}

