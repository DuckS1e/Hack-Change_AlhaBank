import pandas as pd
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

# Читаем и делаем вывод hackathon_income_test.csv
# Сам датафрейм, куча значений. Нужно вычленять лишние
print(Fore.GREEN + "_"*35)
print('DataFrame_Test')
print("_"*35 + Style.RESET_ALL)
df_test = pd.read_csv(file_path_income_test, sep=';', encoding='utf-8')
print(tabulate(df_test.head(), headers=df_test.columns, tablefmt='pretty'))

# Читаем и делаем вывод sample_submission.csv
# Либо это пример вывода, либо константая модель какая-то
print(Fore.GREEN + "_"*35)
print('DataFrame_Test')
print("_"*35 + Style.RESET_ALL)
df_sample_submission = pd.read_csv(file_path_sample_submission, sep=';', encoding='utf-8')
print(tabulate(df_sample_submission.head(), headers=df_sample_submission.columns, tablefmt='pretty'))


