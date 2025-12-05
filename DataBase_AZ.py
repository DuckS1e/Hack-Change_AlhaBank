import pandas as pd
import numpy as np
from pathlib import Path
from colorama import init
from tabulate import tabulate
init()
from colorama import Fore, Back, Style



# Определяем путь

file_path_features = Path('DataBase_csvs') / 'features_description.csv'
file_path_income_test = Path('DataBase_csvs') / 'hackathon_income_test.csv'
file_path_income_train = Path('DataBase_csvs') / 'hackathon_income_train.csv'
file_path_sample_submission = Path('DataBase_csvs') / 'sample_submission.csv'



# Читаем и делаем вывод features_description.csv
# Крч в features объясняется что каждый столбец в самих датасетах значат

print(Fore.GREEN + "_"*35)
print('DataFrame_Features')
print("_"*35 + Style.RESET_ALL)
df_features = pd.read_csv(file_path_features, sep=';', encoding='windows-1251')
print(tabulate(df_features.head(), headers=df_features.columns, tablefmt='pretty'))
print(Fore.LIGHTYELLOW_EX + f"Shape: {df_features.shape}" + Style.RESET_ALL)


# Читаем и делаем вывод hackathon_income_train.csv
# Сам датафрейм, куча значений. Нужно вычленять лишние

print(Fore.GREEN + "_"*35)
print('DataFrame_train')
print("_"*35 + Style.RESET_ALL)
df_train = pd.read_csv(file_path_income_train, sep=';', encoding='utf-8')
print(tabulate(df_train.head(), headers=df_train.columns, tablefmt='pretty'))
print(Fore.LIGHTYELLOW_EX + f"Shape: {df_train.shape}" + Style.RESET_ALL)


# Читаем и выводим hackaton_income_test.csv
# Отдельный тествый датасет для проверки модели

print(Fore.GREEN + "_"*35)
print('DataFrame_test')
print("_"*35 + Style.RESET_ALL)
df_test = pd.read_csv(file_path_income_test, sep=';', encoding='utf-8')
print(tabulate(df_test.head(), headers=df_test.columns, tablefmt='pretty'))
print(Fore.LIGHTYELLOW_EX + f"Shape: {df_test.shape}" + Style.RESET_ALL)



# Читаем и делаем вывод sample_submission.csv
# Данный датасет надо менять под target, который мы сами получили.

print(Fore.GREEN + "_"*35)
print('DataFrame_Sample_Submission')
print("_"*35 + Style.RESET_ALL)
df_sample_submission = pd.read_csv(file_path_sample_submission, sep=';', encoding='utf-8')
print(tabulate(df_sample_submission.head(), headers=df_sample_submission.columns, tablefmt='pretty'))
print(Fore.LIGHTYELLOW_EX + f"Shape: {df_sample_submission.shape}" + Style.RESET_ALL)

FEATURES = df_train.columns[2:]

# Убираем Features из df_train, количество пустых ячеек которых больше 50%

def remove_sparse_columns(df):
    for feature in FEATURES:
        column = df[feature]
        if column.isnull().sum() > len(column) * 0.2:
            df.drop(feature, axis=1)
    return df

df_train = remove_sparse_columns(df_train)
print(df_train.head())
