import customtkinter as ctk
from tkinter import messagebox
import os
import shutil
from datetime import datetime
import string
import random

# Импорт всех необходимых функций из твоего модуля БД
from data_io import (
    get_all_users, 
    add_new_user, 
    delete_user_completely, 
    update_user_password,
    get_departments,
    get_all_tests,
    get_questions_for_test,
    save_result,
    get_filtered_results,
    get_my_assignments as get_user_assignments, # Приводим к имени в коде
    assign_test_to_user,
    get_test_settings,
    get_test_info,
    get_connection
)
from processor import calculate_results, get_interpretation

def transliterate(text):
    # Словарь замен: ключ - русская буква, значение - английская
    slots = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
        'ж':'zh','з':'z','и':'i','й':'y','к':'k','л':'l','м':'m',
        'н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u',
        'ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch','ъ':'',
        'ы':'y','ь':'','э':'e','ю':'yu','я':'ya'
    }
    res = ""
    for char in text.lower():
        # Если нет в словаре, оставляем как есть
        res += slots.get(char, char)
    return res

def generate_random_password(length=8):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, user_data, logout_callback):
        super().__init__(master)
        self.user_data = user_data  # [id, name, role_id]
        self.logout_callback = logout_callback

        self.menu_buttons = {} # Словарь для управления подсветкой
        
        # Переменные для теста
        self.current_tid = None
        self.questions = []
        self.q_idx = 0
        self.raw_score = 0
        self.test_settings = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="САОПТ", font=("Arial", 24, "bold"), text_color="#3B8ED0").pack(pady=30)
        
        #Создание кнопок
        self.create_menu_button("tests", "📝 Тесты", self.show_tests)
        
        if self.user_data[2] in [1, 2]:
            self.create_menu_button("archive", "📂 Архив результатов", self.show_archive)
            self.create_menu_button("assign", "🎯 Назначить тест", self.show_assign)
            self.create_menu_button("admin", "⚙️ Управление", self.show_admin_panel)
            self.create_menu_button("logs", "📄 Системный лог", self.open_logs)

        # Кнопка выхода (её не подсвечиваем, оставляем как есть)
        ctk.CTkButton(self.sidebar, text="🚪 Выход", fg_color="#D35B58", hover_color="#B34B48", 
                      command=self.confirm_logout).pack(side="bottom", pady=20, padx=20, fill="x")

        #CONTENT
        self.content_area = ctk.CTkFrame(self, corner_radius=15)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_welcome()

    #ФУНКЦИИ (Добавлены внутрь класса)
    def create_menu_button(self, name, text, command):
        """Создает кнопку с четким текстом. Исправлено: удален стиль 'medium'"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            anchor="w", 
            command=command, 
            fg_color="transparent",
            text_color="#2C3E50", 
            hover_color="#D5D8DC",
            # Используем "bold" для четкости или "normal" для обычного текста
            font=("Arial", 14, "bold") 
        )
        btn.pack(pady=5, padx=20, fill="x")
        self.menu_buttons[name] = btn

    def highlight_button(self, active_name):
        """Переключает стили: выбранная кнопка синяя, остальные сбрасываются"""
        for name, btn in self.menu_buttons.items():
            if name == active_name:
                # Включаем активный стиль (Синий фон, белый текст)
                btn.configure(
                    fg_color="#3B8ED0", 
                    text_color="white",
                    hover_color="#2E74AF"
                )
            else:
                #стандартный стиль
                btn.configure(
                    fg_color="transparent", 
                    text_color="#2C3E50",
                    hover_color="#D5D8DC"
                )

    def clear_content(self):
        for widget in self.content_area.winfo_children(): widget.destroy()

    def show_welcome(self):
        self.clear_content()
        #Сбрасываем подсветку всех кнопок
        self.highlight_button(None) 
        ctk.CTkLabel(
            self.content_area, 
            text=f"Добро пожаловать,\n{self.user_data[1]}!", 
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        ).pack(expand=True)

    def open_logs(self):
        self.highlight_button("logs")
        if os.path.exists("system_log.txt"): os.startfile("system_log.txt")
        else: messagebox.showwarning("Внимание", "Файл логов не найден")

    def confirm_logout(self):
        if messagebox.askyesno("Выход", "Выйти из системы?"):
            self.logout_callback()

    #ЛОГИКА ТЕСТИРОВАНИЯ
    def show_tests(self):
        self.highlight_button("tests")  #кнопка будет выделяться!
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Доступные психологические методики", font=("Arial", 22, "bold")).pack(pady=20)
        
        assigned_data = get_user_assignments(self.user_data[0])
        assigned_ids = [t[0] for t in assigned_data]
        all_tests = get_all_tests()

        if not all_tests:
            ctk.CTkLabel(self.content_area, text="Список тестов пуст.").pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(self.content_area, width=600, height=400)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for test_item in all_tests:
        # Извлекаем ID и имя по индексам, игнорируя остальные данные
            t_id = test_item[0]
            t_name = test_item[1]
        
            is_urgent = t_id in assigned_ids
            f = ctk.CTkFrame(scroll, fg_color="#E8F0FE" if is_urgent else "transparent", 
                             border_width=2 if is_urgent else 1,
                             border_color="#3B8ED0" if is_urgent else "#D1D1D1")
            f.pack(fill="x", padx=10, pady=5)
            
            prefix = "🔔 [НАЗНАЧЕНО] " if is_urgent else "📄 "
            ctk.CTkLabel(f, text=f"{prefix}{t_name}", 
                         font=("Arial", 14, "bold" if is_urgent else "normal"),
                         text_color="#1A73E8" if is_urgent else "black").pack(side="left", padx=15, pady=10)
            
            ctk.CTkButton(f, text="Пройти" if is_urgent else "Открыть", width=120, 
                          fg_color="#3B8ED0" if is_urgent else "#7F8C8D",
                          command=lambda tid=t_id: self.run_test(tid)).pack(side="right", padx=10)

    def run_test(self, tid):
        self.current_tid = tid
        self.questions = get_questions_for_test(tid) 
        self.test_settings = get_test_settings(tid) #(name, variants_count, mu, sigma)
        self.q_idx = 0
        self.raw_score = 0 
        self.render_question()

    def render_question(self):
            self.clear_content()
            if self.q_idx >= len(self.questions):
                self.finish_test()
                return

            #Получаем данные текущего вопроса
            #q должно быть (text, is_direct, question_id)
            q = self.questions[self.q_idx]
            current_q_db_id = q[2] 

            #Отрисовка текста вопроса
            ctk.CTkLabel(self.content_area, text=f"Вопрос {self.q_idx + 1} из {len(self.questions)}", text_color="gray").pack(pady=10)
            ctk.CTkLabel(self.content_area, text=q[0], font=("Arial", 18, "bold"), wraplength=550).pack(pady=30)
        
            btn_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
            btn_frame.pack(pady=10, fill="x", padx=100)

            # варианты берем из базы
            from data_io import get_variants_for_question
            variants = get_variants_for_question(current_q_db_id)
        
            for v_text, v_score in variants:
                ctk.CTkButton(
                    btn_frame, 
                    text=v_text, 
                    height=45, 
                    font=("Arial", 13),
                    # Балл (score_value) берется напрямую из твоей таблицы
                    command=lambda s=v_score: self.next_q(s)
                ).pack(pady=5, fill="x")

    def next_q(self, val):
        # val — это score_value из таблицы вариантов
        self.raw_score += val
        self.q_idx += 1
        self.render_question()

    def finish_test(self):
        self.clear_content()
        from processor import calculate_results
    
        # 1. Считаем результат для отправки в базу
        mu = self.test_settings[2] if self.test_settings else None
        sigma = self.test_settings[3] if self.test_settings else None
        
        final_score = calculate_results(self.raw_score, self.current_tid, mu, sigma)

        
        save_result(self.user_data[0], self.current_tid, final_score)

        # 2. Оформление экрана 
        container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="✅", font=("Arial", 60)).pack(pady=10)

        ctk.CTkLabel(container, text="Тестирование завершено", 
                     font=("Arial", 28, "bold")).pack(pady=10)
    
        #Текст благодарности
        thanks_text = (
            "Спасибо за честное прохождение теста!\n\n"
            "Ваши результаты успешно отправлены психологу.\n"
            "Эта информация поможет нам в работе."
        )
    
        label_msg = ctk.CTkLabel(container, text=thanks_text, font=("Arial", 16), 
                                 wraplength=500, justify="center")
        label_msg.pack(pady=20)

        # 3. Кнопка возврата
        ctk.CTkButton(container, text="В главное меню", width=250, height=45, 
                      font=("Arial", 14, "bold"),
                      command=self.show_tests).pack(pady=30)

    # Все следующие методы
    def show_archive(self):
        self.highlight_button("archive")  #Подсвечиваем кнопку в боковой панели
        self.clear_content()
    
        ctk.CTkLabel(self.content_area, text="📊 Архив и Аналитика", font=("Arial", 22, "bold")).pack(pady=10)
        
        filter_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=5)

        self.ent_search = ctk.CTkEntry(filter_frame, placeholder_text="ФИО...", width=150)
        self.ent_search.pack(side="left", padx=5)
        self.ent_from = ctk.CTkEntry(filter_frame, placeholder_text="От (ГГГГ-ММ-ДД)", width=120)
        self.ent_from.pack(side="left", padx=5)
        self.ent_to = ctk.CTkEntry(filter_frame, placeholder_text="До (ГГГГ-ММ-ДД)", width=120)
        self.ent_to.pack(side="left", padx=5)

        ctk.CTkButton(filter_frame, text="🔍 Поиск", width=80, command=self.refresh_archive).pack(side="left", padx=5)
        ctk.CTkButton(filter_frame, text="📈 График", fg_color="#E67E22", command=self.show_group_chart).pack(side="right", padx=5)
        ctk.CTkButton(filter_frame, text="📄 Excel", fg_color="#1D6F42", width=100, command=self.export_group_excel).pack(side="right", padx=5)

        # Создаем фрейм для скролла, где будут лежать результаты
        self.archive_scroll = ctk.CTkScrollableFrame(self.content_area)
        self.archive_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        self.refresh_archive()

    def refresh_archive(self):
        # 1. Очистка списка
        for w in self.archive_scroll.winfo_children():
            w.destroy()

        # 2. Получение данных из БД
        data = get_filtered_results(self.ent_search.get(), self.ent_from.get(), self.ent_to.get())

        # 3. Настройка ширины колонок
        # ФИО (0), Тест (1), Баллы (2), Дата (3), Кнопка
        widths = [200, 350, 80, 150, 100]

        for row in data:
            # row = (fio, test_name, score, date, role_id, test_id)
            
            # Контейнер для строки
            f = ctk.CTkFrame(self.archive_scroll, fg_color="#F2F4F4", corner_radius=8)
            f.pack(fill="x", pady=2, padx=5)

            # Логика риска
            is_risk = row[2] >= 8 
            text_color = "#C0392B" if is_risk else "#2C3E50"

            # 1. ФИО 
            ctk.CTkLabel(f, text=row[0], width=widths[0], anchor="w", 
                         text_color="#2C3E50", font=("Arial", 12, "bold"),
                         wraplength=widths[0]-10, justify="left").grid(row=0, column=0, padx=10, pady=10, sticky="w")

            # 2. Название теста
            ctk.CTkLabel(f, text=row[1], width=widths[1], anchor="w", 
                         text_color="#2C3E50", font=("Arial", 12),
                         wraplength=widths[1]-10, justify="left").grid(row=0, column=1, padx=5, pady=10, sticky="w")

            #  3. Балл 
            ctk.CTkLabel(f, text=f"{row[2]} ст.", width=widths[2], 
                         text_color=text_color, font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, sticky="w")

            # 4. Дата 
            ctk.CTkLabel(f, text=row[3], width=widths[3], 
                         text_color="#7F8C8D", font=("Arial", 11)).grid(row=0, column=3, padx=5, sticky="w")

            # 5. Кнопка Word
            btn = ctk.CTkButton(f, text="📥 Word", width=widths[4], height=28,
                          fg_color="transparent", text_color="#2980B9", 
                          hover_color="#D5D8DC", border_width=1, border_color="#2980B9",
                          command=lambda r=row: self.generate_individual_word(r))
            btn.grid(row=0, column=4, padx=10, sticky="e")

    # УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
    def show_admin_panel(self):
        self.highlight_button("admin")  #"Управление"
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="⚙️ Управление доступом", font=("Arial", 22, "bold")).pack(pady=20)
        
        # Панель управления
        top_bar = ctk.CTkFrame(self.content_area, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=5)
        
        ctk.CTkButton(top_bar, text="➕ Новый сотрудник", width=150, command=self.show_add_user_form).pack(side="left", padx=5)
        
        # Кнопка Глаз
        self.btn_reveal = ctk.CTkButton(top_bar, text="👁️ Показать пароли", width=150, fg_color="#5D6D7E", 
                                        command=self.request_reveal_passwords)
        self.btn_reveal.pack(side="left", padx=5)

        # Заголовки таблицы 
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(10, 0))
        
        # Определяем ширину колонок для заголовков и строк
        self.col_widths = [200, 120, 120, 100, 120, 80] # ФИО, Логин, Пароль, Роль, Отдел, Действия
        headers = ["ФИО", "Логин", "Пароль", "Роль", "Отдел", ""]
        
        for i, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, font=("Arial", 12, "bold"), 
                         text_color="gray", width=self.col_widths[i], anchor="w").grid(row=0, column=i, padx=5)

        self.user_scroll = ctk.CTkScrollableFrame(self.content_area)
        self.user_scroll.pack(fill="both", expand=True, padx=30, pady=10)

        self.password_labels = {} 
        self.refresh_user_list()

    def refresh_user_list(self):
        # Очистка
        for w in self.user_scroll.winfo_children():
            w.destroy()
        
        # Определяем фиксированные ширины колонок 
        col_widths = {
            "fio": 200,
            "login": 100,
            "pass": 100,
            "role": 100,
            "dept": 220  # колонка для отделов
        }

        users_data = get_all_users()

        for u in users_data:
            user_id = u[0]
            
            # Контейнер строки (Frame)
            # Убираем фиксированную высоту height=40, чтобы рамка могла растягиваться вниз
            f = ctk.CTkFrame(self.user_scroll, fg_color="#E5E7E9", corner_radius=8)
            f.pack(fill="x", pady=2, padx=5)

            # ФИО 
            ctk.CTkLabel(
                f, text=u[1], font=("Arial", 12, "bold"), 
                width=col_widths["fio"], anchor="w",
                wraplength=col_widths["fio"] - 10 # Перенос текста
            ).grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
            
            # ЛОГИН 
            ctk.CTkLabel(
                f, text=u[2], width=col_widths["login"], anchor="w"
            ).grid(row=0, column=1, padx=5, sticky="nsew")
            
            # ПАРОЛЬ
            p_lbl = ctk.CTkLabel(f, text="********", width=col_widths["pass"], anchor="w")
            p_lbl.grid(row=0, column=2, padx=5, sticky="nsew")
            self.password_labels[user_id] = {'label': p_lbl, 'real_pass': u[3]}

            # РОЛЬ
            ctk.CTkLabel(
                f, text="Админ" if u[4]==1 else "Сотрудник", 
                width=col_widths["role"], anchor="w"
            ).grid(row=0, column=3, padx=5, sticky="nsew")

            # ОТДЕЛ
            ctk.CTkLabel(
                f, text=u[5] if u[5] else "—", 
                width=col_widths["dept"], 
                anchor="w",
                justify="left",             # Выравнивание текста
                wraplength=col_widths["dept"] - 20 # Перенос текста
            ).grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

            # КНОПКИ
            btn_cont = ctk.CTkFrame(f, fg_color="transparent")
            btn_cont.grid(row=0, column=5, padx=5, sticky="e")
            
            # смена пароля
            ctk.CTkButton(btn_cont, text="🔑", width=30, command=lambda r=u: self.show_change_pass_win(r)).pack(side="left", padx=2)
            # удаление
            ctk.CTkButton(btn_cont, text="🗑️", width=30, command=lambda uid=user_id: self.delete_user_ui(uid)).pack(side="left", padx=2)

    def request_reveal_passwords(self):
        # Пароль админа
        dialog = ctk.CTkInputDialog(text="Подтвердите пароль администратора:", title="Доступ к данным")
        entered_pass = dialog.get_input()
        
        # Сравниваем с текущим паролем из user_data
        if entered_pass:
            # Проверка паоля
            conn = get_connection()
            check = conn.execute("SELECT id FROM users WHERE id=? AND password=?", (self.user_data[0], entered_pass)).fetchone()
            conn.close()

            if check:
                self.reveal_all_passwords()
            else:
                messagebox.showerror("Ошибка", "Неверный пароль администратора!")

    def reveal_all_passwords(self):
        # Показываем пароли
        for uid in self.password_labels:
            item = self.password_labels[uid]
            item['label'].configure(text=item['real_pass'], text_color="#2E86C1")
        
        self.btn_reveal.configure(text="⌛ Скроется через 10с", state="disabled")
        
        # таймер на 10 секунд для скрытия
        self.after(10000, self.hide_all_passwords)

    def hide_all_passwords(self):
        for uid in self.password_labels:
            self.password_labels[uid]['label'].configure(text="********", text_color="gray")
        
        self.btn_reveal.configure(text="👁️ Показать пароли", state="normal")

    def show_change_pass_win(self, user_row):
        dialog = ctk.CTkInputDialog(text=f"Новый пароль для {user_row[1]}:", title="Смена пароля")
        new_p = dialog.get_input()
        if new_p and new_p.strip():
            update_user_password(user_row[0], new_p)
            messagebox.showinfo("Готово", "Пароль изменен")
            self.show_admin_panel()

    def show_add_user_form(self):
        win = ctk.CTkToplevel(self)
        win.title("Новый сотрудник")
        win.geometry("400x550") 
        win.attributes("-topmost", True)

        self.entry_fio = ctk.CTkEntry(win, placeholder_text="ФИО сотрудника", width=300)
        self.entry_fio.pack(pady=(20, 0))

        # Кнопка под ФИО для логина
        btn_gen_login = ctk.CTkButton(win, text="✨ Сгенерировать логин по ФИО", font=("Arial", 10, "underline"),
                                      fg_color="transparent", text_color="gray", hover_color="#D5D8DC",
                                      height=20, command=self.auto_fill_login)
        btn_gen_login.pack(pady=(2, 10))

        self.entry_login = ctk.CTkEntry(win, placeholder_text="Логин", width=300)
        self.entry_login.pack(pady=(10, 5))

        self.entry_pass = ctk.CTkEntry(win, placeholder_text="Пароль", width=300)
        self.entry_pass.pack(pady=(10, 0))
    
        # Кнопка под паролем
        btn_gen_pass = ctk.CTkButton(win, text="🎲 Сгенерировать случайный пароль", font=("Arial", 10, "underline"),
                                     fg_color="transparent", text_color="gray", hover_color="#D5D8DC",
                                     height=20, command=self.auto_fill_password)
        btn_gen_pass.pack(pady=(2, 10))

        rol = ctk.CTkComboBox(win, values=["1: Админ", "2: Психолог", "3: Сотрудник"], width=300)
        rol.pack(pady=10)
    
        dep = ctk.CTkComboBox(win, values=get_departments(), width=300)
        dep.pack(pady=10)

        def save():
            s_fio = self.entry_fio.get().strip()
            s_log = self.entry_login.get().strip()
            s_pas = self.entry_pass.get().strip()
            s_rol = int(rol.get()[0])
            s_dep = dep.get()

            if not s_fio or not s_log or not s_pas:
                messagebox.showwarning("Внимание", "Заполните все поля!")
                return

            if add_new_user(s_fio, s_log, s_pas, s_rol, s_dep):
                messagebox.showinfo("Успех", "Сотрудник успешно добавлен")
                win.destroy()
                self.show_admin_panel()
        
        ctk.CTkButton(win, text="Сохранить", fg_color="#2980B9", command=save).pack(pady=20)

    def delete_user_ui(self, uid):
        if messagebox.askyesno("Удаление", "Удалить пользователя?"):
            delete_user_completely(uid)
            self.show_admin_panel()



    def auto_fill_login(self):
        fio = self.entry_fio.get().strip() 
        if fio:
            parts = fio.split()
            if len(parts) >= 2:
                raw_login = f"{parts[0]}_{parts[1][0]}"
            else:
                raw_login = parts[0]
            
            base_login = transliterate(raw_login).lower()
            
            # проверка на уникальность
            final_login = base_login
            counter = 1
            
            from data_io import login_exists
            
            # логин существует
            while login_exists(final_login):
                final_login = f"{base_login}{counter}"
                counter += 1
            
            # свободный логин
            self.entry_login.delete(0, 'end')
            self.entry_login.insert(0, final_login)

    def auto_fill_password(self):
        new_pw = generate_random_password(8)
        self.entry_pass.delete(0, 'end')
        self.entry_pass.insert(0, new_pw)
    

    # НАЗНАЧЕНИЕ ТЕСТОВ
    def show_assign(self):
        self.highlight_button("assign") # "Назначить тест"
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="🎯 Назначить тест", font=("Arial", 20, "bold")).pack(pady=20)
        u_list = [f"{u[0]}: {u[1]}" for u in get_all_users()]
        t_list = [f"{t[0]}: {t[1]}" for t in get_all_tests()]
        self.u_cb = ctk.CTkComboBox(self.content_area, values=u_list, width=300); self.u_cb.pack(pady=10)
        self.t_cb = ctk.CTkComboBox(self.content_area, values=t_list, width=300); self.t_cb.pack(pady=10)
        ctk.CTkButton(self.content_area, text="Назначить", command=self.assign_logic).pack(pady=20)

    def assign_logic(self):
        try:
            uid = int(self.u_cb.get().split(":")[0])
            tid = int(self.t_cb.get().split(":")[0])
            assign_test_to_user(uid, tid)
            messagebox.showinfo("Успех", "Назначено!")
        except: messagebox.showerror("Ошибка", "Выберите данные")

    # ЭКСПОРТ И ГРАФИКИ
    def show_group_chart(self):
        import matplotlib.pyplot as plt
        data = get_filtered_results(self.ent_search.get(), self.ent_from.get(), self.ent_to.get())
        if not data: return
        names = [f"{r[0][:10]}." for r in data]
        scores = [r[2] for r in data]
        plt.figure(figsize=(10, 6))
        plt.bar(names, scores, color='#3B8ED0')
        plt.axhline(y=8, color='red', linestyle='--', label='Риск')
        plt.title("Результаты по фильтру")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def generate_individual_word(self, row):
        try:
            # 1. Импортируем правильную функцию из reports и графики
            from reports import generate_word_report
            from processor import get_interpretation
            
            # Предположим, график временно лежит в корне или генерируется динамически. 
            # Если графика пока нет, передаем пустую строку ""
            chart_path = "temp_chart.png" 
            
            # 2. Получаем правильный текст интерпретации (сначала БАЛЛ row[2], потом ID row[5])
            user_interpretation = get_interpretation(row[2], row[5])
            
            # 3. Приводим данные к формату, который ждет цикл в generate_word_report:
            # Цикл внутри reports ждет список, где: res[0]-имя теста, res[1]-балл, res[2]-дата
            test_results = [(row[1], row[2], row[3])]
            
            # 4. Вызываем профессиональный генератор отчета
            # row[0] - это ФИО сотрудника
            full_path = generate_word_report(
                user_name=row[0], 
                test_results=test_results, 
                chart_path=chart_path, 
                interpretation_text=user_interpretation
            )
            
            # 5. Открываем созданный файл
            os.startfile(full_path)
            
        except Exception as e: 
            messagebox.showerror("Word Error", str(e))

    def export_group_excel(self):
        try:
            # Вызываем твою крутую функцию из reports
            from reports import generate_group_excel
            data = get_filtered_results(self.ent_search.get(), self.ent_from.get(), self.ent_to.get())
            if not data: 
                messagebox.showinfo("Инфо", "Нет данных для экспорта")
                return
            path = generate_group_excel(data)
            os.startfile(path)
        except Exception as e: 
            messagebox.showerror("Excel Error", str(e))