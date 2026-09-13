import sqlite3
from datetime import date
from typing import Optional

DB_FILE = "financeiro.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefone TEXT NOT NULL,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                forma_pagamento TEXT,
                data_registro TEXT DEFAULT (date('now'))
            )
        """)
        conn.commit()

def registrar_transacao(telefone: str, tipo: str, valor: float, categoria: str, forma_pagamento: Optional[str] = None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transacoes (telefone, tipo, valor, categoria, forma_pagamento, data_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (telefone, tipo, valor, categoria, forma_pagamento, date.today().isoformat()))
        conn.commit()

def consultar_saldo_hoje(telefone: str) -> dict:
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'ENTRADA' THEN valor ELSE 0 END), 0) AS total_entradas,
                COALESCE(SUM(CASE WHEN tipo = 'SAIDA' THEN valor ELSE 0 END), 0) AS total_saidas
            FROM transacoes
            WHERE telefone = ? AND data_registro = ?
        """, (telefone, date.today().isoformat()))
        row = cursor.fetchone()
        entradas, saidas = row[0], row[1]
        saldo = entradas - saidas
        return {"entradas": entradas, "saidas": saidas, "saldo": saldo}