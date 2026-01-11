import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def generate_job_from_text(user_text: str):
    """
    Usa a OpenRouter para transformar texto em JSON de vaga.
    """
    
    system_prompt = """
    Você é um especialista em RH, com anos de experiência no mercado. Sua tarefa é criar descrições de vagas baseadas em textos fornecidos pelos usuários.
    RETORNE APENAS UM JSON VÁLIDO. NÃO ESCREVA NADA ANTES OU DEPOIS DO JSON.
    O formato deve ser exatamente este:
    {
        "title": "Título da Vaga",
        "description": "Texto da descrição...",
        "requirements": "Requisitos separados por vírgula",
        "status": "aberta"
    }
    """

    try:
        response = client.chat.completions.create(
        
            model="meta-llama/llama-3.3-70b-instruct:free", 
            
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
           
            extra_headers={
                "HTTP-Referer": "http://localhost:8000", 
                "X-Title": "Banco de Talentos App",     
            }
        )
        
        content = response.choices[0].message.content
        
        # --- LIMPEZA DE SEGURANÇA ---
        # Modelos gratuitos às vezes colocam ```json no início. Vamos limpar.
        content = content.replace("```json", "").replace("```", "").strip()
        
        job_data = json.loads(content)
        return job_data

    except json.JSONDecodeError:
        print("Erro: A IA não retornou um JSON válido.")
        return None
    except Exception as e:
        print(f"Erro na OpenRouter: {e}")
        return None