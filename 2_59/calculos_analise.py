import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

def safe_mean(values: List[float]) -> Optional[float]:
    return statistics.mean(values) if values else None

def safe_variance(values: List[float]) -> Optional[float]:
    return statistics.variance(values) if len(values) > 1 else 0.0 if values else None

def safe_std(values: List[float]) -> Optional[float]:
    return statistics.stdev(values) if len(values) > 1 else 0.0 if values else None

def amplitude(values: List[float]) -> Optional[float]:
    return (max(values) - min(values)) if values else None

def safe_median(values: List[float]) -> Optional[float]:
    return statistics.median(values) if values else None

def safe_mode(values: List[float]) -> Optional[float]:
    if not values:
        return None
    counts = Counter(values)
    top_count = max(counts.values())

    top_values = [k for k, v in counts.items() if v == top_count]
    return top_values[0] if top_values else None

# Testes
amostra_temperaturas_dia = [18.0, 17.5, 17.2, 17.0, 16.8, 17.1, 18.3, 20.0, 22.5, 25.0, 27.3, 29.1,
 30.0, 30.5, 29.8, 28.4, 26.7, 24.9, 23.0, 21.5, 20.3, 19.5, 18.8, 18.2]

print("Amplitude="+str(amplitude(amostra_temperaturas_dia)))
print("Media="+str(safe_mean(amostra_temperaturas_dia)))
print("Mediana="+str(safe_median(amostra_temperaturas_dia)))
print("Moda="+str(safe_mode(amostra_temperaturas_dia)))
print("Variancia="+str(safe_variance(amostra_temperaturas_dia)))
print("DesvioPadrao="+str(safe_std(amostra_temperaturas_dia)))