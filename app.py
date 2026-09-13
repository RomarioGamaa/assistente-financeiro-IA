from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from ai_service import processar_mensagem_financeira
import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield

app = FastAPI(title="Assistente Financeiro IA", version="1.0.0", lifespan=lifespan)

class MensagemEntrada(BaseModel):
    telefone: str
    mensagem: str

@app.get("/")
def home():
    return FileResponse("chat.html")

@app.post("/webhook")
def webhook(payload: MensagemEntrada):
    try:
        dados = processar_mensagem_financeira(payload.mensagem)
        resposta_texto = ""

        if dados.intencao == "REGISTRAR" and dados.itens:
            linhas_confirmacao = []
            for item in dados.itens:
                db.registrar_transacao(
                    telefone=payload.telefone,
                    tipo=item.tipo,
                    valor=item.valor,
                    categoria=item.categoria or "geral",
                    forma_pagamento=item.forma_pagamento
                )
                simbolo = "💰" if item.tipo == "ENTRADA" else "💸"
                linhas_confirmacao.append(f"• {simbolo} R$ {item.valor:.2f} ({item.tipo.title()} - {item.categoria or 'Geral'})")
            
            resposta_texto = "✅ Lançamentos registrados:\n" + "\n".join(linhas_confirmacao)

        elif dados.intencao == "CONSULTAR":
            totais = db.consultar_saldo_hoje(payload.telefone)
            resposta_texto = (
                f"📊 Balanço de Hoje:\n"
                f"• Entradas: R$ {totais['entradas']:.2f}\n"
                f"• Saídas: R$ {totais['saidas']:.2f}\n"
                f"• Saldo do Dia: R$ {totais['saldo']:.2f}"
            )
        else:
            resposta_texto = "Não consegui entender a operação. Tente algo como 'Recebi 50 no pix' ou 'Quanto fechei hoje?'"

        return {
            "remetente": payload.telefone,
            "extração": dados.model_dump(),
            "mensagem_resposta": resposta_texto
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))