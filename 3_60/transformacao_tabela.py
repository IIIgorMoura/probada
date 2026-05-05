import json
import pandas as pd

# Suponha que o JSON acima esteja em um arquivo chamado 'resultado.json'
with open('teste_saida_aula3_modificado.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# ---------- 1. Tabela de Frequência por Categoria ----------
tabela_categoria = pd.DataFrame(dados['calculos']['tabela_frequencia_categoria'])
print("=== Tabela de Frequência por Categoria ===")
print(tabela_categoria)

# ---------- 2. Tabela de Frequência por Forma de Pagamento ----------
tabela_pagamento = pd.DataFrame(dados['calculos']['tabela_frequencia_forma_pagamento'])
print("\n=== Tabela de Frequência por Forma de Pagamento ===")
print(tabela_pagamento)

# ---------- 3. Tabela de Contingência Categoria x Forma de Pagamento ----------
# Transformando JSON aninhado em DataFrame
contingencia_dict = dados['calculos']['tabela_contingencia_categoria_pagamento']

# Criando lista de registros (linha = categoria, coluna = forma de pagamento, valor = frequência)
registros = []
for categoria, pagamentos in contingencia_dict.items():
    for forma, freq in pagamentos.items():
        registros.append({'Categoria': categoria, 'Forma_Pagamento': forma, 'Frequencia': freq})

tabela_contingencia = pd.DataFrame(registros)
# Pivotar para deixar categorias como linhas e formas de pagamento como colunas
tabela_contingencia_pivot = tabela_contingencia.pivot(index='Categoria', columns='Forma_Pagamento', values='Frequencia').fillna(0)
print("\n=== Tabela de Contingência Categoria x Forma de Pagamento ===")
print(tabela_contingencia_pivot)

# ---------- 4. Quartis de Receita Diária ----------
quartis_receita = pd.DataFrame([dados['calculos']['quartis_receita_diaria']])
print("\n=== Quartis Receita Diária ===")
print(quartis_receita)

# ---------- 5. Quartis de Lucro Diário ----------
quartis_lucro = pd.DataFrame([dados['calculos']['quartis_lucro_diario']])
print("\n=== Quartis Lucro Diário ===")
print(quartis_lucro)