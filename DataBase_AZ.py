import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Определяем путь
file_path_features = Path('DataBase_csvs') / 'features_description.csv'
file_path_income_test = Path('DataBase_csvs') / 'hackathon_income_test.csv'
file_path_income_train = Path('DataBase_csvs') / 'hackathon_income_train.csv'
file_path_sample_submission = Path('DataBase_csvs') / 'sample_submission.csv'

# Читаем файл
df_features = pd.read_csv(file_path_features, sep=';', encoding='windows-1251')
df_test = pd.read_csv(file_path_income_test, sep=';', encoding='utf-8')
df_sample_submission = pd.read_csv(file_path_sample_submission, sep=';', encoding='utf-8')


