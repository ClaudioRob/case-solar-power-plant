import os
import pytest
import pandas as pd

base_dir = "/home/claudio/projetos/case-solar-power-plant/dados/"
sensor_files = [os.path.join(base_dir, "weather_sensor_plant_1.csv"),
                os.path.join(base_dir, "weather_sensor_plant_2.csv")]

@pytest.fixture
def load_sensor_data():
    return pd.concat([pd.read_csv(file) for file in sensor_files], ignore_index=True)

def test_files_exist():
    for file in sensor_files:
        assert os.path.exists(file), f"Arquivo {file} não encontrado."

def test_concat_sensor_data(load_sensor_data):
    assert not load_sensor_data.empty, "Os dados concatenados estão vazios."

def test_date_conversion(load_sensor_data):
    load_sensor_data['DATE_TIME'] = pd.to_datetime(
        load_sensor_data['DATE_TIME'], format='%Y-%m-%d %H:%M:%S', errors='coerce'
    )
    assert load_sensor_data['DATE_TIME'].isnull().sum() == 0, "Alguns valores de DATE_TIME não foram convertidos corretamente."

def test_columns(load_sensor_data):
    expected_columns = {'DATE_TIME', 'PLANT_ID', 'SOURCE_KEY', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION'}
    assert set(load_sensor_data.columns).issuperset(expected_columns), "Colunas esperadas não estão presentes."
