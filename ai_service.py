import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional, Literal, List

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ItemTransacao(BaseModel):
    tipo: Literal["ENTRADA", "SAIDA"]
    valor: float = Field(description="Valor numérico positivo da movimentação")
    categoria: Optional[str] = Field(default="geral", description="Ex: almoço, corte, combustível")
    forma_pagamento: Optional[Literal["dinheiro", "pix", "cartao_credito", "cartao_debito", "outro"]] = "outro"

class ExtracaoFinanceira(BaseModel):
    intencao: Literal["REGISTRAR", "CONSULTAR", "DESCONHECIDO"]
    itens: Optional[List[ItemTransacao]] = Field(default_factory=list, description="Lista de movimentações identificadas")
    consulta_tipo: Optional[Literal["SALDO_HOJE", "GASTOS_MES", "ENTRADAS_HOJE", "RESULTADO_MES"]] = None

SYSTEM_PROMPT = """
Você é um assistente contábil operacional rigoroso. Interprete mensagens de comerciantes registrando entradas/saídas ou consultando saldo.
Responda ESTRITAMENTE no schema JSON fornecido.

Regras:
- 'Recebi', 'Entrou', 'Vendi' -> tipo: ENTRADA.
- 'Paguei', 'Gastei', 'Comprei' -> tipo: SAIDA.
- Se houver mais de uma movimentação na mesma mensagem (ex: 'Paguei 50 no almoço e recebi 100 do cliente'), extraia CADA UMA como um item separado na lista 'itens'.
- Sempre garanta valores positivos no campo valor.
- Se for consulta de saldo, marque intencao como CONSULTAR e classifique consulta_tipo.
- Se for mensagem irrelevante ou sem dados contábeis, marque intencao como DESCONHECIDO.
"""

def processar_mensagem_financeira(texto: str) -> ExtracaoFinanceira:
    resposta = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=texto,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=ExtracaoFinanceira,
            temperature=0.1
        )
    )
    dados = json.loads(resposta.text)
    return ExtracaoFinanceira(**dados)