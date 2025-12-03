import pandas as pd
from pathlib import Path

# Определяем путь
file_path = Path('DataBase_csvs') / 'features_description.csv'

# Читаем файл
df = pd.read_csv(file_path, sep=';', encoding='windows-1251')

print(df.head())
