import pandas as pd

# Carregar dados
generation_plant_1 = pd.read_csv("dados/power_generation_plant_1.csv")
generation_plant_2 = pd.read_csv("dados/power_generation_plant_2.csv")
weather_sensor_1 = pd.read_csv("dados/weather_sensor_plant_1.csv")
weather_sensor_2 = pd.read_csv("dados/weather_sensor_plant_2.csv")

# Combinar dados das duas plantas de geração
generation_data = pd.concat([generation_plant_1, generation_plant_2])
weather_data = pd.concat([weather_sensor_1, weather_sensor_2])


# Função para padronizar e converter o campo DATE_TIME para timestamp
def convert_to_timestamp(df, date_column):
    # Tenta converter o campo para datetime, tratando diferentes formatos
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    return df


# Converter a coluna DATE_TIME para formato datetime
# generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
# weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

# Agrupar dados por hora para facilitar a análise
generation_data["HOUR"] = generation_data["DATE_TIME"].dt.hour
weather_data["HOUR"] = weather_data["DATE_TIME"].dt.hour


# 1. Melhor horário para redirecionamento de energia para baterias
def analyze_peak_hours(generation_df):
    hourly_ac_power = generation_df.groupby("HOUR")["AC_POWER"].sum()

    # Identificar o período de maior geração contínua (mínimo 3 horas)
    peak_hours = hourly_ac_power.sort_values(ascending=False).head(3).index.tolist()

    return peak_hours


# 2. Eficiência da disposição dos painéis
def analyze_panel_efficiency(generation_df):
    total_dc_power = generation_df["DC_POWER"].sum()
    total_ac_power = generation_df["AC_POWER"].sum()

    efficiency = (total_ac_power / total_dc_power) * 100
    return efficiency


# 3. Impacto da temperatura na eficiência
def analyze_temperature_impact(generation_df, weather_df):
    merged_data = pd.merge(
        generation_df,
        weather_df,
        on=["DATE_TIME", "PLANT_ID"],
        suffixes=("_gen", "_weather"),
    )

    # Correlação entre temperatura ambiente e AC_POWER
    correlation_ambient = (
        merged_data[["AMBIENT_TEMPERATURE", "AC_POWER"]].corr().iloc[0, 1]
    )
    # Correlação entre temperatura do módulo e AC_POWER
    correlation_module = (
        merged_data[["MODULE_TEMPERATURE", "AC_POWER"]].corr().iloc[0, 1]
    )

    return correlation_ambient, correlation_module


# 4. Outros insights (Exemplo: impacto da irradiação)
def analyze_irradiation_impact(generation_df, weather_df):
    merged_data = pd.merge(
        generation_df,
        weather_df,
        on=["DATE_TIME", "PLANT_ID"],
        suffixes=("_gen", "_weather"),
    )

    # Correlação entre irradiação e AC_POWER
    correlation_irradiation = merged_data[["IRRADIATION", "AC_POWER"]].corr().iloc[0, 1]

    return correlation_irradiation


# Execução das análises
peak_hours = analyze_peak_hours(generation_data)
efficiency = analyze_panel_efficiency(generation_data)
correlation_ambient, correlation_module = analyze_temperature_impact(
    generation_data, weather_data
)
correlation_irradiation = analyze_irradiation_impact(generation_data, weather_data)

# Resultados
print(f"Melhores horários para redirecionamento de energia: {peak_hours}")
print(f"Eficiência dos painéis: {efficiency:.2f}%")
print(
    f"Correlação entre temperatura ambiente e geração de energia: {correlation_ambient:.2f}"
)
print(
    f"Correlação entre temperatura do módulo e geração de energia: {correlation_module:.2f}"
)
print(
    f"Correlação entre irradiação e geração de energia: {correlation_irradiation:.2f}"
)
