import mysql.connector
from colorama import init
init()
from colorama import Fore, Style, Back


user = input(Fore.RED + 'Введите username: ')
password = input(Fore.RED + 'Введите password: ' + Style.RESET_ALL)

try:
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,  # ваш пароль
        auth_plugin='mysql_native_password'
    )
    print("✅ Подключение к MySQL успешно!")

    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")

    print("📋 Доступные базы данных:")
    for db in cursor:
        print(f"  - {db[0]}")

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"❌ Ошибка подключения: {e}")
    print("\n🔧 Возможные решения:")
    print("1. Убедитесь, что MySQL сервер запущен")
    print("2. Проверьте логин и пароль")
    print("3. Если пароль пустой, попробуйте:")
    print("   mysql -u root --protocol=tcp")