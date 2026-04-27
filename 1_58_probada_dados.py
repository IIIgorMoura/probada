import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any,Dict, List, Optional, Tuple


# tratamento: Conversão para Float

def to_float(value: Any) -> Optional[float]:
    # value: Any: aceita qualquer tipo de valor.
    # -> Optional[float]: pode retornar um float ou None (caso não consiga converter).
    if value is None or value == "":
        return None
    
    if isinstance(value, (int, float)): # Se já for número (int ou float),
        return float(value)             # apenas converte para float (padroniza o tipo)

    if isinstance(value, str):
        # Se for string, entra no processamento mais interessante
        clean = value.strip().replace("R$", "").replace(".", "").replace(",", ".")
        try:
            return float(clean)
        except ValueError:
            return None
            
    return None



# teste=to_float("R$ 45,99")
# print(teste, type(teste))

# Recebe qualquer tipo (Any).
# Retorna True, False ou None.
def to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    
    if isinstance(value, bool):  # Se já for booleano (True ou False), retorna direto.
        return value

    # Converte números: 0 -> False, qualquer outro número -> True
    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):  # Se for string: remove espaços (strip) e converte
        text = value.strip().lower()
        
        if text in {"true", "1", "sim", "s", "yes", "y"}:
            return True
            
        if text in {"false", "0", "nao", "não", "n", "no"}:
            return False

        # Isso facilita comparar valores como "Sim", " SIM " etc.
        
    return None

# teste=to_bool("s")
# print(teste, type(teste))

def parse_date(value: Any) -> Optional[str]:
    # Recebe qualquer tipo (Any)
    # Tenta converter para data padronizada
    if value is None or value == "":    
        return None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
            # Define lista de formatos aceitos:
            # 2026-04-26 ISO ; 26/04/2026 BR comum ; 2026/04/26 ; 26-04-2026
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
                # strptime converte string em objeto de data
                # fmt define como a string está formatada
                # strftime converte o objeto de volta para string
            except ValueError:
                continue
        return value
    return None

teste=parse_date("2026/05/04")
print(teste)