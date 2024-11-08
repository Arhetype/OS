import pyautogui
import tkinter as tk
from tkinter import ttk
import subprocess
# Получаем текущее положение курсора мыши
x, y = pyautogui.position()
# Выводим полученные координаты
print("X:", x, "Y:", y)

# Функция для получения информации о загрузочных разделах с помощью команды 'lsblk'
def get_devices_info():
    result = subprocess.run(['lsblk'], stdout=subprocess.PIPE, text=True)
    return result.stdout

# Функция для получения информации о сетевых маршрутах с помощью команды 'ip route show'
def get_network_routes():
    result = subprocess.run(['ip', 'route', 'show'], stdout=subprocess.PIPE, text=True)
    return result.stdout

# Обработчик события нажатия на кнопку "Devices Info"
def on_click_devices_info():
    # Очистка текстового поля
    text.delete(1.0, tk.END)
    # Получение и вывод информации о загрузочных разделах
    text.insert(tk.END, get_devices_info())

# Обработчик события нажатия на кнопку "Network Routes"
def on_click_network_routes():
    # Очистка текстового поля
    text.delete(1.0, tk.END)
    # Получение и вывод информации о сетевых маршрутах
    text.insert(tk.END, get_network_routes())

# Создание главного окна
root = tk.Tk()
# Установка заголовка окна
root.title("System Information")

# Создание кнопки для получения информации о загрузочных разделах
devices_btn = ttk.Button(root, text="Devices Info", command=on_click_devices_info)
# Размещение кнопки на форме и настройка отступов
devices_btn.pack(pady=10, padx=20, fill=tk.X)

# Создание кнопки для получения информации о сетевых маршрутах
network_btn = ttk.Button(root, text="Network Routes", command=on_click_network_routes)
# Размещение кнопки на форме и настройка отступов
network_btn.pack(pady=10, padx=20, fill=tk.X)

# Создание текстового поля для вывода информации
text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
# Размещение текстового поля на форме и настройка отступов
text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Запуск главного цикла обработки событий
root.mainloop()