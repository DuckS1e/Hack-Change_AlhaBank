import pandas as pd
import numpy as np
from pathlib import Path
from colorama import init
from tabulate import tabulate
init()
from colorama import Fore, Back, Style



# Определяем путь
DATA_DIR = Path('DataBase_csvs')
file_paths = {
    'features': DATA_DIR / 'features_description.csv',
    'train': DATA_DIR / 'hackathon_income_train.csv',
    'test': DATA_DIR / 'hackathon_income_test.csv',
    'submission': DATA_DIR / 'sample_submission.csv'
}


def load_dataframe(name, path, encoding):
    try:
        df = pd.read_csv(path, sep=';', encoding=encoding)
        print(Fore.GREEN + f"Данные загружены: {name.capitalize()}" + Style.RESET_ALL + s)
        return df
    except Exception as e:
        print(Fore.RED + f"Не удалось загрузить данные {name.capitalize()}: {e}" + Style.RESET_ALL)
        return None

df_features = load_dataframe('features', file_paths['features'], 'windows-1251')
df_train = load_dataframe('train', file_paths['train'], 'utf-8')
df_test = load_dataframe('test', file_paths['test'], 'utf-8')
df_submission = load_dataframe('submission', file_paths['submission'], 'utf-8')