import pandas as pd

antes_file = 'final.csv'
manuais_file = 'manuais.csv'
output_file = 'diferencas.csv'

def count_and_save_diffs():
    # Ler os arquivos CSV
    df_antes = pd.read_csv(antes_file)
    df_manuais = pd.read_csv(manuais_file)

    # Converter as colunas de data para string ou datetime para garantir consistência
    df_antes['data_com'] = pd.to_datetime(df_antes['data_com'], errors='coerce')
    df_manuais['data_com'] = pd.to_datetime(df_manuais['data_com'], errors='coerce')
    df_antes['data_pagamento'] = pd.to_datetime(df_antes['data_pagamento'], errors='coerce')
    df_manuais['data_pagamento'] = pd.to_datetime(df_manuais['data_pagamento'], errors='coerce')

    # Ignorar a coluna 'data_pagamento' ao comparar
    cols_to_compare = df_manuais.columns.difference(['data_pagamento', 'valor'])

    # Lista para armazenar as diferenças
    diffs_list = []

    # Para cada provento em manuais.csv
    for index, row in df_manuais.iterrows():
        # Verificar se existe uma linha igual em final.csv (exceto data_pagamento e comparando valor com uma margem de 10%)
        matching_rows = df_antes[cols_to_compare].eq(row[cols_to_compare]).all(axis=1)

        # Verificar se algum valor correspondente está dentro da margem de 10%
        if matching_rows.any():
            matched_df = df_antes[matching_rows]
            close_enough = matched_df['valor'].apply(lambda x: abs(x - row['valor']) <= 0.1 * row['valor'])
            if not close_enough.any():
                diffs_list.append(row)
        else:
            diffs_list.append(row)

    # Converter a lista de diferenças em um DataFrame
    df_diffs = pd.DataFrame(diffs_list)

    # Salvar as diferenças em um arquivo CSV
    df_diffs.to_csv(output_file, index=False)

    # Retornar o número de diferenças encontradas
    return len(diffs_list)

# Exemplo de uso
diff_count = count_and_save_diffs()
print(f'Número de diferenças encontradas e salvas: {diff_count}')
