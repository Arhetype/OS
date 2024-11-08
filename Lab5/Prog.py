import threading
import time
import matplotlib.pyplot as plt
import networkx as nx

# Класс USB-накопителя
class USBDrive:
    def __init__(self, id):
        self.id = id
        self.is_busy = False
        self.lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()
        self.is_busy = True
        print(f'USB-{self.id} занят процессом {threading.current_thread().name}')

    def release(self):
        self.is_busy = False
        self.lock.release()
        print(f'USB-{self.id} освобожден процессом {threading.current_thread().name}')

# Класс процесса
class Process(threading.Thread):
    def __init__(self, id, usb_drive):
        super().__init__()
        self.id = id
        self.usb_drive = usb_drive

    def run(self):
        while True:
            # Запрашиваем USB-накопитель
            self.usb_drive.acquire()
            time.sleep(1)
            # Освобождаем USB-накопитель
            self.usb_drive.release()
            time.sleep(1)

# Создание USB-накопителей
usb_drives = [USBDrive(i) for i in range(3)]

# Создание процессов
processes = [Process(i, usb_drives[i % 3]) for i in range(3)]

# Граф для визуализации
G = nx.DiGraph()

# Запуск процессов
for process in processes:
    process.start()

# Функция для отображения графа
def draw_graph(G):
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=2000, font_size=20, arrows=True)
    plt.title('Граф распределения ресурсов', fontsize=20)
    plt.show()

while True:
    time.sleep(5)  # Перерыв для обновления графа

    # Обновление графа
    for usb in usb_drives:
        G.add_node(f'USB-{usb.id}', color='green' if not usb.is_busy else 'red')

    for process in processes:
        G.add_node(f'Процесс-{process.id}', color='green')
        if process.usb_drive.is_busy:
            G.add_edge(f'Процесс-{process.id}', f'USB-{process.usb_drive.id}', color='red')
        else:
            G.add_edge(f'Процесс-{process.id}', f'USB-{process.usb_drive.id}', color='green')

    draw_graph(G)

    # Очистка графа для следующего обновления
    G.clear()
