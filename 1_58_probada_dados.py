import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any,Dict, List, Optional, Tuple

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