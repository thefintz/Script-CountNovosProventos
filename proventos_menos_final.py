import pandas as pd

antes_file = 'final.csv' # final.csv     alup_antes.csv
depois_file = 'proventos.csv' # proventos.csv    alup_depois.csv
output_file = 'diferencas_linhas_mauricio.csv' #diferencas_linhas.csv   diferencas_linhas_alup.csv


def count_and_save_diffs():
    # Ler os arquivos CSV
    df_antes = pd.read_csv(antes_file)
    df_depois = pd.read_csv(depois_file)
    # df_antes['isin'] = df_antes['isin'].astype(str)
    # df_depois['isin'] = df_depois['isin'].astype(str)
    # print(df_antes.dtypes)
    # print(df_depois.dtypes)
    # print('----')
 
    # Converter as colunas de data para string ou datetime para garantir consistência
    df_antes['data_aprovacao'] = pd.to_datetime(df_antes['data_aprovacao'])
    df_antes['data_com'] = pd.to_datetime(df_antes['data_com']).dt.date
    df_antes['data_ult_preco_com'] = pd.to_datetime(df_antes['data_ult_preco_com'])
    df_antes['data_pagamento'] = pd.to_datetime(df_antes['data_pagamento'])
    df_depois['data_aprovacao'] = pd.to_datetime(df_depois['data_aprovacao'])
    df_depois['data_com'] = pd.to_datetime(df_depois['data_com']).dt.date
    df_depois['data_ult_preco_com'] = pd.to_datetime(df_depois['data_ult_preco_com'])
    df_depois['data_pagamento'] = pd.to_datetime(df_depois['data_pagamento'])

    # Ignorar a coluna 'data_pagamento' ao comparar e aplicar margem de erro para 'valor'
    cols_to_compare = df_depois.columns.difference(['data_pagamento', 'valor', 'isin', 'data_aprovacao', 'data_ult_preco_com', 'ult_preco_com', 'tipo_ativo', 'ticker_base'])

    # Lista para armazenar as diferenças
    diffs_list = []

    # Copiar o DataFrame para evitar remoções na iteração original
    df_antes_copy = df_antes.copy()

    # Para cada provento em proventos.csv
    for index, row in df_depois.iterrows():
        # print(f"Comparando linha {index}: {row}")
        # Verificar se existe uma linha igual em final.csv (exceto data_pagamento e valor e isin)
        if row['ticker'] == 'AZEV3':
            print(row)
            print(df_antes_copy[df_antes_copy['ticker'] == 'AZEV3'])
            
        matching_rows = df_antes_copy[cols_to_compare].eq(row[cols_to_compare]).all(axis=1)
        if row['ticker'] == 'AZEV3':
            print(df_antes_copy[matching_rows])

        # Exibir as linhas correspondentes encontradas
        # print(f"Linhas correspondentes no DataFrame anterior para a linha {index}: {matching_rows.sum()}")
        if matching_rows.any():
            matched_df = df_antes_copy[matching_rows]
            # print(f"Linhas correspondentes:\n{matched_df}")

            # Verificar se o valor está dentro da margem de erro de 10%
            close_enough = abs(matched_df['valor'] - row['valor']) <= 0.01 * row['valor']

            # print(f"Valor: {row['valor']}, Correspondência com margem de erro: {close_enough.any()}")
            if not close_enough.any():
                # print(f"Adicionando linha {index} à lista de diferenças")
                diffs_list.append(row)
            else:
                # Remover todas as correspondências do DataFrame original
                # print(f"Removendo correspondência para a linha {index}")
                if row['ticker'] == 'AZEV3':
                    print('linha proxima:')
                    print(close_enough)
                df_antes_copy = df_antes_copy.drop(matched_df.index[close_enough][0])
        else:
            # print(f"Sem correspondência, adicionando linha {index} à lista de diferenças")
            diffs_list.append(row)

    # Converter a lista de diferenças em um DataFrame
    df_diffs = pd.DataFrame(diffs_list)

    # Salvar as diferenças em um arquivo CSV
    df_diffs.to_csv(output_file, index=False)
    # print(df_diffs.dtypes)

    # Retornar o número de diferenças encontradas
    print(f"Número de diferenças encontradas e salvas: {len(diffs_list)}")
    return len(diffs_list)


# def count_duplicates(df_depois): # 
#     # Step 1: Find duplicates within df_depois, ignoring 'data_pagamento'
    
#     # Define the columns to compare, excluding 'data_pagamento'
#     cols_to_compare = df_depois.columns.difference(['data_pagamento'])

#     # Find duplicates using the selected columns, ignoring 'data_pagamento'
#     duplicates_in_depois = df_depois[df_depois.duplicated(subset=cols_to_compare, keep=False)]  # Keep all duplicates (not just first/last)

#     # Count duplicates
#     duplicate_count = len(duplicates_in_depois)

#     # Return duplicates and count
#     return duplicates_in_depois, duplicate_count

# Exemplo de uso
diff_count = count_and_save_diffs()
# print(f'Número de diferenças encontradas e salvas: {diff_count}')

