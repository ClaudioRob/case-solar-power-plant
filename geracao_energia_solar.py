import pandas as pd

def read_generation_data(filename, date_format='%Y-%m-%d %H:%M:%S', timezone='UTC'):
    """
    Lê um arquivo de geração de energia e parseia a coluna de data e hora.

    Args:
        filename (str): Caminho para o arquivo CSV.
        date_format (str, optional): Formato da data e hora. Padrão: '%Y-%m-%d %H:%M:%S'.
        timezone (str, optional): Zona horária dos dados. Padrão: 'UTC'.

    Returns:
        pandas.DataFrame: Os dados carregados com a coluna de data e hora parseada.
    """

    try:
        df = pd.read_csv(filename, parse_dates=['DATE_TIME'], date_parser=lambda col: pd.to_datetime(col, format=date_format, utc=True))
        df['DATE_TIME'] = df['DATE_TIME'].dt.tz_convert(timezone)
        return df
    except pd.errors.ParserError:
        print(f"Erro ao carregar o arquivo {filename}. Verifique o formato da data e tente novamente com um formato diferente.")
        return None

# Carregando os dados, assumindo o formato padrão
generation_plant_1 = read_generation_data('dados/power_generation_plant_1.csv')
generation_plant_2 = read_generation_data('dados/power_generation_plant_2.csv')

# Se os formatos forem diferentes, especifique:
# generation_plant_1 = read_generation_data('dados/power_generation_plant_1.csv', date_format='%d-%m-%Y %H:%M')

# Verificando se os DataFrames foram carregados corretamente
if generation_plant_1 is not None and generation_plant_2 is not None:
    # Continuar com a análise dos dados
    print("Dados carregados com sucesso!")
    # ... seu código de análise aqui ...