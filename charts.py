import matplotlib.pyplot as plt
import os

def create_results_chart(dates, scores, user_name, filename="temp_chart.png"):
    plt.style.use('seaborn-v0_8-whitegrid') # Светлый стиль с сеткой
    # Настройка стиля
    plt.figure(figsize=(10, 5))
    plt.plot(dates, scores, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label='Балл (стены)')
    
    # Оформление
    plt.title(f"Динамика психологического состояния: {user_name}", fontsize=14)
    plt.xlabel("Дата тестирования", fontsize=10)
    plt.ylabel("Стены (1-10)", fontsize=10)
    plt.ylim(0, 11)  # Шкала стенайнов
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Сохраняем файл
    plt.savefig(filename, dpi=100)
    plt.close()
    return filename