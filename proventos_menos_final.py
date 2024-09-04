import pandas as pd

antes_file = 'final.csv' # final.csv     alup_antes.csv
depois_file = 'proventos.csv' # proventos.csv    alup_depois.csv
output_file = 'diferencas_linhasssssssss.csv' #diferencas_linhas.csv   diferencas_linhas_alup.csv

def count_and_save_diffs():
    # Ler os arquivos CSV
    df_antes = pd.read_csv(antes_file)
    df_depois = pd.read_csv(depois_file)

    # Converter as colunas de data para string ou datetime para garantir consistência
    df_antes['data_aprovacao'] = pd.to_datetime(df_antes['data_aprovacao'], errors='coerce')
    df_antes['data_com'] = pd.to_datetime(df_antes['data_com'], errors='coerce')
    df_antes['data_ult_preco_com'] = pd.to_datetime(df_antes['data_ult_preco_com'], errors='coerce')
    df_antes['data_pagamento'] = pd.to_datetime(df_antes['data_pagamento'], errors='coerce')
    df_depois['data_aprovacao'] = pd.to_datetime(df_depois['data_aprovacao'], errors='coerce')
    df_depois['data_com'] = pd.to_datetime(df_depois['data_com'], errors='coerce')
    df_depois['data_ult_preco_com'] = pd.to_datetime(df_depois['data_ult_preco_com'], errors='coerce')
    df_depois['data_pagamento'] = pd.to_datetime(df_depois['data_pagamento'], errors='coerce')

    return count_duplicates(df_depois) # tirar  essa linha pois n precisamos mais
    # Ignorar a coluna 'data_pagamento' ao comparar
    cols_to_compare = df_depois.columns.difference(['data_pagamento'])

    # Lista para armazenar as diferenças
    diffs_list = []

    # Para cada provento em manuais.csv
    for index, row in df_depois.iterrows():
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

def count_duplicates(df_depois): # 
    # Step 1: Find duplicates within df_depois, ignoring 'data_pagamento'
    
    # Define the columns to compare, excluding 'data_pagamento'
    cols_to_compare = df_depois.columns.difference(['data_pagamento'])

    # Find duplicates using the selected columns, ignoring 'data_pagamento'
    duplicates_in_depois = df_depois[df_depois.duplicated(subset=cols_to_compare, keep=False)]  # Keep all duplicates (not just first/last)

    # Count duplicates
    duplicate_count = len(duplicates_in_depois)

    # Return duplicates and count
    return duplicates_in_depois, duplicate_count

# Exemplo de uso
diff_count = count_and_save_diffs()
print(f'Número de diferenças encontradas e salvas: {diff_count}')

