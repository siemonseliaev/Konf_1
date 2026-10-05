import shlex
import tkinter as tk

VFS_NAME = "my_vfs.tar"
PROMPT = f"[{VFS_NAME}]$ "


class Emulator(tk.Tk):
    """Класс эмулятора командной строки VFS."""

    def __init__(self):
        super().__init__()

        # Заголовок окна содержит имя VFS
        self.title(f"Эмулятор VFS — {VFS_NAME}")

        self.output = tk.Text(
            self, height=20, width=80, bg="black", fg="white"
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        # Строка ввода
        self.entry = tk.Entry(
            self, bg="white", fg="black", insertbackground="black"
        )
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)

        # Выводим первое приглашение ко вводу
        self.show_prompt()

    def show_prompt(self):
        """Отображение приглашения к вводу."""
        self.output.insert(tk.END, PROMPT)
        self.output.see(tk.END)

    def on_enter(self, event=None):
        """Обработка нажатия Enter."""
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        # Печатаем введенную пользователем команду в консоль
        self.output.insert(tk.END, user_input + "\n")

        # Парсер аргументов с учетом кавычек
        try:
            args = shlex.split(user_input)
        except Exception as e:
            # Сообщение об ошибке (незакрытые кавычки и т.д.)
            msg = f"Ошибка синтаксиса/кавычек: {e}\n"
            self.output.insert(tk.END, msg)
            self.show_prompt()
            return

        if not args:
            self.show_prompt()
            return

        command = args[0]
        command_args = args[1:]

        self.parser(command, command_args)
        self.show_prompt()

    def _cmd_help(self, args):
        """Обработка команды help."""
        help_text = (
            "Доступные команды:\n"
            "ls - вывести список файлов (заглушка)\n"
            "cd - сменить директорию (заглушка)\n"
            "help - показать справку\n"
            "exit - завершить работу\n"
        )
        self.output.insert(tk.END, help_text)

    def _cmd_cd(self, args):
        """Обработка команды cd."""
        if len(args) != 1:
            self.output.insert(
                tk.END, "Ошибка: cd требует ровно 1 аргумент\n"
            )
        else:
            self.output.insert(tk.END, f"cd: {args}\n")

    def _cmd_ls(self, args):
        """Обработка команды ls."""
        self.output.insert(tk.END, f"ls: {args}\n")

    def _cmd_exit(self, args):
        """Обработка команды exit."""
        if len(args) > 0:
            self.output.insert(
                tk.END,
                "Ошибка: команда exit не принимает аргументов\n"
            )
            return
        self.destroy()

    def parser(self, command, args):
        """Парсер и обработчик команд."""
        commands = {
            "help": self._cmd_help,
            "cd": self._cmd_cd,
            "ls": self._cmd_ls,
            "exit": self._cmd_exit,
        }

        handler = commands.get(command)
        if handler:
            handler(args)
        else:
            # Сообщение о неизвестной команде
            msg = f"Ошибка: неизвестная команда '{command}'\n"
            self.output.insert(tk.END, msg)


if __name__ == "__main__":
    app = Emulator()
    app.mainloop()
