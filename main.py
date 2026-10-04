import tkinter as tk  # Сам GUI
import shlex  # Работа с командной строкой и кавычками
#реализация первого номера


VFS_NAME = "my_vfs.tar"
PROMPT = f"[{VFS_NAME}]$ "


class Emulator(tk.Tk):
    def __init__(self):
        super().__init__()

        # 2. Заголовок окна содержит имя VFS
        self.title(f"Эмулятор VFS — {VFS_NAME}")

        self.output = tk.Text(self, height=20, width=80, bg="black", fg="white")
        self.output.pack(fill=tk.BOTH, expand=True)

        # Строка ввода
        self.entry = tk.Entry(self, bg="white", fg="black", insertbackground="black")
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)

        # Выводим первое приглашение ко вводу
        self.show_prompt()

    def show_prompt(self):
        self.output.insert(tk.END, PROMPT)
        self.output.see(tk.END)

    def on_enter(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        # Печатаем введенную пользователем команду в консоль
        self.output.insert(tk.END, user_input + "\n")

        # 3. Парсер аргументов с учетом кавычек
        try:
            args = shlex.split(user_input)
        except Exception as e:
            # 4. Сообщение об ошибке (незакрытые кавычки и т.д.)
            self.output.insert(tk.END, f"Ошибка синтаксиса/кавычек: {e}\n")
            self.show_prompt()
            return

        if not args:
            self.show_prompt()
            return

        command = args[0]
        command_args = args[1:]

        self.parser(command, command_args)
        self.show_prompt()

    def parser(self, command, args):
        if command == "help":
            self.output.insert(tk.END,
                "Доступные команды:\n"
                "ls - вывести список файлов (заглушка)\n"
                "cd  - сменить директорию (заглушка)\n"
                "help        - показать справку\n"
                "exit        - завершить работу\n"
            )

        elif command == "cd":
            if len(args) != 1:
                # 4. Сообщение об ошибке неверных аргументов
                self.output.insert(tk.END, "Ошибка: cd требует ровно 1 аргумент\n")
            else:
                self.output.insert(tk.END, f"cd: {args}\n")

        # 5. Команда-заглушка ls
        elif command == "ls":
            self.output.insert(tk.END, f"ls: {args}\n")

        # 6. Команда exit
        elif command == "exit":
            if len(args) > 0:
                self.output.insert(tk.END, "Ошибка: команда exit не принимает аргументов\n")
                return
            self.destroy()

        # 4. Сообщение о неизвестной команде
        else:
            self.output.insert(tk.END, f"Ошибка: неизвестная команда '{command}'\n")


if __name__ == "__main__":
    app = Emulator()
    app.mainloop()
