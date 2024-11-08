import argparse
import getpass
import os
import subprocess


def useradd(username):
    """Добавление нового пользователя"""
    try:
        subprocess.run(['useradd', username])
        print(f"Пользователь {username} успешно добавлен")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя {username}: {e}")


def userdel(username):
    """Удаление пользователя"""
    try:
        subprocess.run(['userdel', username])
        print(f"Пользователь {username} успешно удален")
    except Exception as e:
        print(f"Ошибка при удалении пользователя {username}: {e}")


def usermod(username, attribute, value):
    """Изменение атрибутов пользователя"""
    try:
        subprocess.run(['usermod', f'-{attribute}', value, username])
        print(f"Атрибут {attribute} для пользователя {username} успешно изменен")
    except Exception as e:
        print(f"Ошибка при изменении атрибута {attribute} для пользователя {username}: {e}")


def passwd(username):
    """Изменение пароля пользователя"""
    try:
        subprocess.run(['passwd', username])
        print(f"Пароль для пользователя {username} успешно изменен")
    except Exception as e:
        print(f"Ошибка при изменении пароля для пользователя {username}: {e}")


def ip():
    """Отображение сетевых интерфейсов и их статуса"""
    try:
        subprocess.run(['ip', 'a'])
    except Exception as e:
        print(f"Ошибка при выполнении команды ip: {e}")


def ping(host):
    """Пинг хоста"""
    try:
        subprocess.run(['ping', host, '-c', '4'])
    except Exception as e:
        print(f"Ошибка при выполнении команды ping: {e}")


def nethogs(interface):
    """Мониторинг трафика по интерфейсу"""
    try:
        subprocess.run(['nethogs', '-i', interface])
    except Exception as e:
        print(f"Ошибка при выполнении команды nethogs: {e}")


def traceroute(host):
    """Трассировка маршрута до хоста"""
    try:
        subprocess.run(['traceroute', host])
    except Exception as e:
        print(f"Ошибка при выполнении команды traceroute: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Управление безопасностью ОС")

    # Команды для управления пользователями
    parser.add_argument('--useradd', metavar='USERNAME', help='Добавить нового пользователя')
    parser.add_argument('--userdel', metavar='USERNAME', help='Удалить пользователя')
    parser.add_argument('--usermod', nargs=3, metavar=('USERNAME', 'ATTRIBUTE', 'VALUE'),
                        help='Изменить атрибут пользователя')

    # Команда для изменения пароля
    parser.add_argument('--passwd', metavar='USERNAME', help='Изменить пароль пользователя')

    # Команда для отображения сетевых интерфейсов
    parser.add_argument('--ip', action='store_true', help='Отобразить сетевые интерфейсы и их статуса')

    # Команда для пинга
    parser.add_argument('--ping', metavar='HOST', help='Пинг хоста')

    # Команда для мониторинга трафика
    parser.add_argument('--nethogs', metavar='INTERFACE', help='Мониторинг трафика по интерфейсу')

    # Команда для трассировки маршрута
    parser.add_argument('--traceroute', metavar='HOST', help='Трассировка маршрута до хоста')

    args = parser.parse_args()

    if args.useradd:
        useradd(args.useradd)
    elif args.userdel:
        userdel(args.userdel)
    elif args.usermod:
        usermod(*args.usermod)
    elif args.passwd:
        passwd(args.passwd)
    elif args.ip:
        ip()
    elif args.ping:
        ping(args.ping)
    elif args.nethogs:
        nethogs(args.nethogs)
    elif args.traceroute:
        traceroute(args.traceroute)
    else:
        parser.print_help()
