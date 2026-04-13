#%%
print("\nImportando bibliotecas...\n")
import pandas as pd
import numpy as np

from ingestao import extract



#%%
print("Extraindo dados...\n")

df = extract("data/raw/MICRODADOS_ENEM_2023.csv")


#%%
print("Atribuindo valores às colunas...\n")

colunas_reformuladas = {
"Q001" : {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 5, "F" : 8, "G" : 10, "H" : None},

"Q002" : {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 5, "F" : 8, "G" : 10, "H" : None},

"Q003" : {'A' : 1, 'B' : 2, 'C' : 3, 'D' : 3, 'E' : 7, 'F' : None},

"Q004" : {'A' : 1, 'B' : 2, 'C' : 3, 'D' : 3, 'E' : 7, 'F' : None},

"Q006" : {'A': 0, 'B': 1320, 'C': 1650.005, 'D': 2310.005, 'E': 2970.005, 'F': 3630.005, 'G': 4620.005, 
          'H': 5940.005, 'I': 7260.005, 'J': 8580.005, 'K': 9900.005, 'L': 11220.005, 'M': 12540.005, 
          'N': 14520.005, 'O': 17820.005, 'P': 23100.005, 'Q': 26400},

"Q007" : {'A': 0,'B': 2,'C': 3,'D': 4},

"Q008" : {'A': 0,'B': 2,'C': 3,'D': 5,'E': 7},

"Q009" : {'A': 0,'B': 1,'C': 3,'D': 5,'E': 7},

"Q010" : {'A': 0,'B': 5,'C': 8,'D': 11,'E': 14},

"Q011" : {'A': 0,'B': 4,'C': 6,'D': 8,'E': 10},

"Q012" : {'A': 0,'B': 2,'C': 5,'D': 7,'E': 9},

"Q013" : {'A': 0,'B': 3,'C': 6,'D': 9,'E': 12},

"Q014" : {'A': 0,'B': 3,'C': 6,'D': 9,'E': 12},

"Q015" : {'A': 0,'B': 3,'C': 6,'D': 9,'E': 12},

"Q016" : {'A': 0,'B': 2,'C': 4,'D': 8,'E': 12},

"Q017" : {'A': 0,'B': 3,'C': 6,'D': 9,'E': 12},

"Q018" : {'A': 0,'B': 3},

"Q019" : {'A': 0,'B': 2,'C': 4,'D': 6,'E': 10},

"Q020" : {'A': 0,'B': 2},

"Q021" : {'A': 0,'B': 2},

"Q022" : {'A': 0,'B': 1,'C': 3,'D': 5,'E': 7},

"Q023" : {'A': 0,'B': 1},

"Q024" : {'A': 0,'B': 3,'C': 6,'D': 9,'E': 12},

"Q025" : {'A': 0,'B': 2}
}


#%%

for coluna, opcoes in colunas_reformuladas.items():
    if coluna in df:
        df[coluna] = df[coluna].map(opcoes)


#%%
print("Definindo renda per capita...\n")

df["renda_per_capita"] = df["Q006"] / df["Q005"]

#%%
print("Categorizando faixas salariais...\n")

intervalos = [0, 209, 665, 1064, 4591, 9900, float('inf')]
faixas = [0, 1, 3, 6, 9, 12]

df["faixa_salarial"] = pd.cut(df["renda_per_capita"], bins = intervalos, labels= faixas, include_lowest= True)

df['faixa_salarial'] = df["faixa_salarial"].astype("Int32")

#%%
print("Convertendo tipos de dados para melhora de performance...\n")

for coluna in df:
    if df[coluna].dtype == "int64":
        df[coluna] = df[coluna].astype("Int32")
    elif df[coluna].dtype == "float64":
        df[coluna] = df[coluna].astype("Float32")


#%%
print("Calculando scores...\n")

df["score_social"] = df["Q001"] + df["Q002"] + df["Q003"] + df["Q004"] + df["faixa_salarial"]

df["score_material"] = (df['Q007'] + df['Q008'] + df['Q009'] + df['Q010'] + df['Q011'] + df['Q012'] 
+ df['Q013'] + df['Q014'] + df['Q015'] + df['Q016'] + df['Q017'] + df['Q018'] + df['Q019'] 
+ df['Q020'] +df['Q021'] + df['Q022'] + df['Q023'] + df['Q024'] + df['Q025'])

#%%
print("Definindo estrutura final de colunas...\n")

df = df.rename(columns={"Q025" : "possui_internet"})

colunas_necessarias = ['TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_COR_RACA', 'TP_ST_CONCLUSAO',
       'TP_ANO_CONCLUIU', 'TP_ESCOLA', 'TP_ENSINO', 'IN_TREINEIRO',
       'SG_UF_ESC', 'TP_DEPENDENCIA_ADM_ESC', 'TP_LOCALIZACAO_ESC',
       'TP_SIT_FUNC_ESC', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC',
       'TP_PRESENCA_MT', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC',
       'NU_NOTA_MT', 'TP_STATUS_REDACAO', 'NU_NOTA_REDACAO', 'possui_internet', 'renda_per_capita',
       'score_social', 'score_material']

df = df[colunas_necessarias]

print("Transformações realizadas com sucesso!\n")

print(f"""Dados atualizados do dataframe:
      
- {len(df):,} linhas      
- {len(df.columns)} colunas
- Memória utilizada: {(int(df.memory_usage().sum())/1_000_000):,.2f} MBs\n""")

df.to_csv("../data/processed/dados_processados.csv", sep=";")

print("Dados transformados salvos no diretório data/processed.\n")