#%%
import pandas as pd
from pathlib import Path
from tqdm import tqdm

#%%


def extract(caminho: Path) -> pd.DataFrame:

    "Extrai o dado do csv e transforma em um Dataframe com as colunas selecionadas e otimizadas."
    caminho = Path(caminho)
    tamanho_total = caminho.stat().st_size
    chunks = []

    # Abrimos o arquivo manualmente para ter controle do ponteiro de leitura
    with open(caminho, 'r', encoding="ISO-8859-1") as f:
        with tqdm(total=tamanho_total, unit="B", unit_scale=True, desc="Extraindo CSV") as pbar:
            # Passamos o arquivo aberto para o read_csv
            reader = pd.read_csv(f, sep=";", chunksize=10_000)
            
            ultimo_pos = 0
            for chunk in reader:
                chunks.append(chunk)
                
                # f.tell() diz em qual byte do arquivo o leitor está agora
                pos_atual = f.tell()
                pbar.update(pos_atual - ultimo_pos)
                ultimo_pos = pos_atual
        df_importado = pd.concat(chunks, ignore_index=True)

    print(f"\nMemória utilizada: {(int(df_importado.memory_usage().sum())/1_000_000_000):,.2f} GBs.")
    colunas = ['TP_FAIXA_ETARIA','TP_SEXO','TP_COR_RACA','TP_ST_CONCLUSAO','TP_ANO_CONCLUIU','TP_ESCOLA','TP_ENSINO','IN_TREINEIRO','SG_UF_ESC',
        'TP_DEPENDENCIA_ADM_ESC','TP_LOCALIZACAO_ESC','TP_SIT_FUNC_ESC','TP_PRESENCA_CN','TP_PRESENCA_CH','TP_PRESENCA_LC','TP_PRESENCA_MT',
        'NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','TP_STATUS_REDACAO','NU_NOTA_REDACAO','Q001','Q002','Q003','Q004','Q005','Q006',
        'Q007','Q008','Q009','Q010','Q011','Q012','Q013','Q014','Q015','Q016','Q017','Q018','Q019','Q020','Q021','Q022','Q023','Q024','Q025']
    
    print("\nDescartando colunas  inúteis...")

    df_importado = df_importado[colunas]

    print("\nConvertendo tipos de dados para melhorar performance...")

    for coluna in df_importado:
        if df_importado[coluna].dtype == "int64":
            df_importado[coluna] = df_importado[coluna].astype("int32")
        elif df_importado[coluna].dtype == "float64":
            df_importado[coluna] = df_importado[coluna].astype("float32")

    print(f"""\nDados carregados com sucesso!

Dados atualizados do dataframe:
          
- {len(df_importado):,} linhas
- {len(colunas)} colunas
- Memória utilizada: {(int(df_importado.memory_usage().sum())/1_000_000_000):,.2f} GBs.
        """)

    return df_importado


#%%

if __name__ == "__main__":
    extract("../data/raw/MICRODADOS_ENEM_2023.csv")