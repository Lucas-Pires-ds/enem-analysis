#%%
import pandas as pd
from pathlib import Path
#%%
BASE_DIR = Path(__file__).resolve().parent.parent

def extract(caminho: str) -> pd.DataFrame:

    "Extrai o dado do csv e transforma em um Dataframe com as colunas selecionadas e otimizadas."
    caminho_completo = BASE_DIR / caminho
    df_importado = pd.read_csv(caminho_completo, encoding="ISO-8859-1", sep=";")

    colunas = ['TP_FAIXA_ETARIA','TP_SEXO','TP_COR_RACA','TP_ST_CONCLUSAO','TP_ANO_CONCLUIU','TP_ESCOLA','TP_ENSINO','IN_TREINEIRO','SG_UF_ESC',
        'TP_DEPENDENCIA_ADM_ESC','TP_LOCALIZACAO_ESC','TP_SIT_FUNC_ESC','TP_PRESENCA_CN','TP_PRESENCA_CH','TP_PRESENCA_LC','TP_PRESENCA_MT',
        'NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','TP_STATUS_REDACAO','NU_NOTA_REDACAO','Q001','Q002','Q003','Q004','Q005','Q006',
        'Q007','Q008','Q009','Q010','Q011','Q012','Q013','Q014','Q015','Q016','Q017','Q018','Q019','Q020','Q021','Q022','Q023','Q024','Q025']

    df_importado = df_importado[colunas]

    for coluna in df_importado:
        if df_importado[coluna].dtype == "int64":
            df_importado[coluna] = df_importado[coluna].astype("int32")
        elif df_importado[coluna].dtype == "float64":
            df_importado[coluna] = df_importado[coluna].astype("float32")

    print(f"""Dados carregados com sucesso!

Dados atualizados do dataframe:
          
- {len(df_importado):,} linhas
- {len(colunas)} colunas
- Memória utilizada: {(int(df_importado.memory_usage().sum())/1_000_000_000):,.2f}
        """)

    return df_importado
