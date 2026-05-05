import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any,Dict, List, Optional, Tuple

# ===========================================================================================

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

print(to_float("1a"))
print(to_float(""))
print(to_float(10))
print(to_float(3.14))
print(to_float("123"))
print(to_float("  45.67 "))
print(to_float("1.234,56"))
print(to_float("R$ 99,90"))
print(to_float("abc")) 
print(to_float("10,5"))

print()

# ===========================================================================================

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

print(to_bool(None))
print(to_bool(""))
print(to_bool(True))
print(to_bool(False))
print(to_bool(0))
print(to_bool(1))
print(to_bool("sim"))
print(to_bool("Não"))
print(to_bool("YES"))
print(to_bool("abc"))

print()

# ===========================================================================================

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

# teste=parse_date("2026/05/04")
# print(teste)

print(parse_date(None))
print(parse_date(""))
print(parse_date("2026-04-27"))
print(parse_date("27/04/2026"))
print(parse_date("27-04-2026"))
print(parse_date("2026/04/27"))
print(parse_date("04/27/2026"))
print(parse_date("2026.04.27"))
print(parse_date("abc"))
print(parse_date(12345))

print()

# ===========================================================================================

# Esse código define uma função simples em Python para ler e carregar um arquivo JSON.
# O parâmetro path: str indica que a função espera receber o caminho do arquivo como uma string.
# -> Dict[str, Any] é uma type hint (anotação de tipo), sugerindo que a função retorna um 
# dicionário com chaves do tipo str e valores de qualquer tipo (Any).
def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Esse código é o complemento natural do anterior: enquanto load_json lê um JSON,
# essa função salva dados em formato JSON em um arquivo.
def save_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# path: str: caminho onde o arquivo será salvo.
# data: Dict[str, Any]: os dados que serão gravados (normalmente um dicionário).
# -> None: indica que a função não retorna nada (apenas executa a escrita).
# json.dump(): converte o objeto Python (data) para JSON e escreve no arquivo f.
# ensure_ascii=False: permite que caracteres como á, ç, à sejam gravados normalmente.
# indent=2: formata o JSON com indentação de 2 espaços, deixando o arquivo mais legível.

# ===========================================================================================

def to_float(v):
    """Função auxiliar para tentar converter valores para float."""
    try:
        return float(v)
    except (ValueError, TypeError):
        return None
    
# ===========================================================================================

# Essa função tenta inferir automaticamente o tipo de um campo de dados, ou seja,
# ela olha para uma lista de valores e decide se aquilo parece número, categoria, texto etc.
# Isso é muito usado em análise de dados e sistemas que "auto-entendem" tabelas.
def infer_field_type(values: List[Any]) -> str:
    # Função que tenta descobrir o tipo de uma coluna de dados
    not_null = [v for v in values if v is not None and v != ""]  # Remove valores vazios (None e "")
    if not not_null:
        return "indefinido"  # Se não sobrou nenhum valor válido
    
    # Conta quantos valores podem ser interpretados como números
    # (diretamente ou via conversão com to_float)
    numeric = sum(1 for v in not_null if isinstance(v, (int, float)) or to_float(v) is not None)
    
    if numeric == len(not_null):  # Se TODOS os valores são numéricos
        unique = len(set(to_float(v) for v in not_null if to_float(v) is not None))
        # Um set guarda apenas valores únicos (remove duplicatas)
        if unique <= 12:  # Poucos valores distintos -> provavelmente discreto
            return "quantitativa_discreta"
        return "quantitativa_continua"  # Muitos valores distintos -> contínuo (ex: salário, peso)
        
    unique = len(set(str(v) for v in not_null))  # Se não for totalmente numérico, trata como texto
    if unique <= 12:  # Poucas categorias -> variável categórica simples
        return "qualitativa_nominal"
    
    return "qualitativa_ordinal_ou_textual"  # Muitas categorias -> texto livre ou variável complexa

print(infer_field_type([1, 2, 3, 4]))
print(infer_field_type([1.1, 2.2, 3.3, 4.4]))
print(infer_field_type(list(range(20))))
print(infer_field_type(["1", "2", "3"]))
print(infer_field_type(["a", "b", "c"]))
print(infer_field_type(["a"] * 50))
print(infer_field_type([None, "", None]))
print(infer_field_type(["A", "B", "C", "D", "E", "F"]))
print(infer_field_type([f"texto{i}" for i in range(20)]))
print(infer_field_type([1, "a", 2, "b"]))

print()

# ===========================================================================================

# Essa função gera um relatório de valores nulos (ou vazios) em uma lista de registros
# (dicionários). Ela conta quantos campos estão “faltando” em cada chave.
def null_report(records: List[Dict[str, Any]]) -> Dict[str, int]:
    # Função que conta valores nulos ou vazios em cada campo
    # records = lista de dicionários (tipo linhas de uma tabela)
    # retorna um dicionário com contagem de nulos por coluna
    counts: Dict[str, int] = Counter()  # counts deve se comportar como dicionário com chaves do tipo str e valores do tipo int
    # Counter é um tipo especial de dicionário usado para contar ocorrências.
    # Cria um contador vazio para armazenar quantos nulos cada chave tem
    for rec in records:   # Percorre cada registro (cada "linha" de dados)
        for k, v in rec.items():  # Percorre cada campo (chave e valor) dentro do registro
            # k recebe a chave (key)
            # v recebe o valor (value) associado a essa chave
            if v is None or v == "":  # Verifica se o valor está vazio (None ou string vazia)
                counts[k] += 1    # Incrementa 1 na contagem daquela chave
    return dict(counts)   # Converte o Counter para dict normal e retorna
# dict(counts) pega o objeto counts (que no seu caso é um Counter) e converte para um dicionário comum (dict).


# Esse código define uma classe chamada PreparedData, mas na forma atual ela está sendo usada como um
# “container de dados” (data structure) — ou seja, não tem lógica, só organiza informações.
# @dataclass é um decorador do Python (do módulo dataclasses) que serve para criar classes focadas em armazenar
# dados sem precisar escrever muito código repetitivo.
# Um decorador em Python é uma forma de modificar ou estender o comportamento
# de uma função ou classe sem alterar o código original dela.
# Ele é basicamente uma função que “envolve” outra função.

@dataclass
class PreparedData:
    negocio: Dict[str, Any]
    transacoes: List[Dict[str, Any]]
    dias: List[Dict[str, Any]]
    recepcao: Dict[str, Any]

# Esse trecho define uma classe chamada InsightCalculadoEngine, que parece ser o
# “motor” responsável por processar dados e gerar insights.
class InsightCalculadoEngine:
    def __init__(self, data: Dict[str, Any]):
        # self representa a própria instância do objeto que está sendo criada ou usada
        self.raw = data                            # guarda os dados originais
        self.prepared = self._prepare_data(data)   # chama o método da própria classe e salva o resultado em prepared

    # --------------------------------------------------------
    # Preparação
    # --------------------------------------------------------
    # Esse método _prepare_data é o coração do processamento de dados da sua classe. Ele pega
    # dados brutos e transforma em um formato limpo, padronizado e pronto para análise.
    def _prepare_data(self, data: Dict[str, Any]) -> PreparedData:
        negocio = data.get("negocio", {})
        dados = data.get("dados", {})
        recepcao = data.get("recepcao", {})
        # dict.get(chave, valor_padrao):
        # retorna o valor da chave se ela existir
        # se não existir, retorna o valor_padrao (em vez de dar erro)
        # se não existir, retorna {} (dicionário vazio)

        transacoes = []   # criando lista vazia
        for item in dados.get("transacoes",[]):     # [] retorna uma lista vazia
            record = dict(item)                     # cria um dicionário (dict) a partir de item.
            record["data"] = parse_date(record.get("data"))  # trata o formato de data
            if "valor" in record:
                record["valor"] = to_float(record.get("valor"))     # trata float
            if "pago_no_prazo" in record:
                record["pago_no_prazo"] = to_bool(record.get("pago_no_prazo"))   # trata boolean
            if "desconto" in record:
                record["desconto"] = to_float(record.get("desconto"))    # trata float
            if "marketing" in record:
                record["marketing"] = to_float(record.get("marketing"))  # trata float
            transacoes.append(record)     # adicionando na lista

        dias = []    # criando lista vazia
        for item in dados.get("dias", []):
            record = dict(item)
            record["data"] = parse_date(record.get("data"))
            for field in ["receita", "despesa", "vendas_qtd", "clientes", "marketing", "desconto_medio"]:
                if field in record:  # verifica se a chave field existe dentro do dicionário record
                    record[field] = to_float(record.get(field))   # trata float
            dias.append(record)

        if not dias and transacoes:
            dias = self._derive_daily_records(transacoes)

        return PreparedData(negocio=negocio, transacoes=transacoes, dias=dias, recepcao=recepcao)


 # Esse método aula_1 é basicamente uma função de “análise exploratória inicial” (EDA) do seu sistema.
    # Ele organiza informações básicas do dataset para responder: “o que eu tenho de dados aqui?”
    def aula_1(self) -> Dict[str, Any]:   # Define o método "aula_1", que retorna um dicionário com análises iniciais dos dados
        transacoes = self.prepared.transacoes   # Extrai a lista de transações já preparadas
        dias = self.prepared.dias               # Extrai a lista de registros diários já preparados
        if transacoes:                          # Verifica se existem transações
            keys = sorted({k for rec in transacoes for k in rec.keys()})      # sorted transforma o set em uma lista ordenada
            # Cria um conjunto com todas as chaves existentes nas transações
            # Depois converte em lista ordenada
            # Ex: ["valor", "data", "tipo", "cliente"]
            classificacao = {}    # Inicializa dicionário que armazenará o tipo de cada campo
            for key in keys:      # Itera sobre cada campo existente nas transações
                valores = [rec.get(key) for rec in transacoes]   # Coleta todos os valores daquele campo em todas as transações
                classificacao[key] = infer_field_type(valores)
                # Usa uma função que infere o tipo do campo
                # Ex: quantitativa, qualitativa, etc.
        else:   # Caso não existam transações
            classificacao = {}    # Define classificação vazia

        sample_size = min(5, len(transacoes))   # Define tamanho da amostra (no máximo 5 registros)
        amostra = transacoes[:sample_size]      # Pega os primeiros registros como amostra

        return {  # Retorna um relatório estruturado com análises da "aula 1"
            "tema": "Entender os dados do negócio",  # Define o objetivo da análise
            # Descreve o problema de negócio em linguagem simples
            "problema_financeiro": "O empreendedor possui dados, mas não sabe o que está registrando nem como organizar isso para análise.",
            "calculos": {  # Seção com métricas e cálculos
                "populacao_transacoes": len(transacoes),    # Quantidade total de transações
                "populacao_registros_diarios": len(dias),   # Quantidade total de registros diários
                "amostra_exibida": sample_size,             # Quantidade de registros mostrados na amostra
                "classificacao_campos_transacoes": classificacao,        # Tipos de cada campo das transações
                "campos_faltantes_transacoes": null_report(transacoes),  # Conta valores nulos/vazios nas transações
                "campos_faltantes_dias": null_report(dias),  # Conta valores nulos/vazios nos dados diários
                "amostra_transacoes": amostra,               # Exibe amostra dos dados
            },
            "insights": [ # Lista de interpretações automáticas
                # Explica o objetivo da análise de tipos
                "Nesta etapa o sistema identifica quais campos são qualitativos e quais são quantitativos.",
                # Explica que o sistema detecta problemas nos dados
                "Também aponta lacunas iniciais para preparar a análise exploratória das próximas aulas.",
            ],
        }
        
# dados_empresa = load_json('exemplo_entrada_insight_calculado.json')
# engine = InsightCalculadoEngine(dados_empresa)
# resultado = engine.aula_1()
# print(resultado)
# save_json('exemplo_entrada_insight_calculado.json',  resultado)

