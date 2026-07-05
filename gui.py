import customtkinter as ctk
from tkinter import messagebox
import logging
from auth import login_user
from main_menu import MainMenu

# НАСТРОЙКА ЛОГИРОВАНИЯ 
logging.basicConfig(
    filename='system_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("САОПТ - Автоматизированная система психологического тестирования")
        self.geometry("1100x700")
        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue")

        logging.info("Приложение запущено.")
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.show_login()

    def show_login(self):
        for child in self.container.winfo_children():
            child.destroy()
            
        login_frame = ctk.CTkFrame(self.container, width=400, height=500)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(login_frame, text="Вход в систему", font=("Arial", 26, "bold"), text_color="#3B8ED0").pack(pady=(40, 30))
        
        self.login_entry = ctk.CTkEntry(login_frame, placeholder_text="Логин", width=280, height=45)
        self.login_entry.pack(pady=10)
        
        self.pw_entry = ctk.CTkEntry(login_frame, placeholder_text="Пароль", show="*", width=280, height=45)
        self.pw_entry.pack(pady=10)

        ctk.CTkButton(login_frame, text="Авторизоваться", width=280, height=50, 
                      font=("Arial", 16, "bold"), command=self.attempt_login).pack(pady=40)

    def attempt_login(self):
        login = self.login_entry.get()
        password = self.pw_entry.get()
        user = login_user(login, password)
        
        if user:
            logging.info(f"Успешный вход: {user[1]}")
            self.show_main_menu(user)
        else:
            logging.warning(f"Ошибка входа: {login}")
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_main_menu(self, user_data):
        for child in self.container.winfo_children():
            child.destroy()
        self.menu = MainMenu(self.container, user_data, self.show_login)
        self.menu.pack(fill="both", expand=True)

if __name__ == "__main__":
    try:
        upgrade_db()
        app = App()
        app.mainloop()
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")