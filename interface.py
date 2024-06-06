from db import NotesDatabase

from rich.console import Console

import platform
import os
import time
import art


class ConsoleInterface:
    def __init__(self, db: NotesDatabase, load=False) -> None:
        self.db = db
        self.console = Console()
        self.plt = platform.system()
        self.load = load

        if load:
            art.tprint("Loading...")
            time.sleep(1)
            self.clear()

    def clear(self) -> bool:
        """Clear console, return if it was successful."""

        if self.plt == "Windows":
            clear = lambda: os.system('cls')
            clear()

            return True
        
        elif self.plt == "Linux" or self.plt == "Darwin":
            clear = lambda: os.system('clear')
            clear()

            return True
        
        else:
            self.console.print("[bold red]Я не могу продолжить корректное функционирование и покидаю тебя ;(\n"
                               "Совет: скачай Windows или Linux[/]")
            
            return False

    def multiline_input(self) -> str:
        """
        Get multiline input from user.
        :return: user input
        """

        contents = []
        while True:
            
            try:
                line = self.console.input("[bold blue]| [/]")
            except EOFError:
                break
            else:
                if line == "" or line.lower() == "end":
                    break
                else:
                    contents.append(line)

        content = "\n".join(contents)
        return content

    def display_menu(self) -> None:
        """Print menu with options and input."""

        self.clear()

        self.console.print("[bold]1. Создать новую заметку.[/]")
        self.console.print("[bold]2. Показать все заметки.[/]")
        self.console.print("[bold]3. Найти заметку.[/]")
        self.console.print("[bold]4. Удалить заметку.[/]")
        self.console.print("[bold]5. Посмотреть заметку.[/]")
        self.console.print("[bold]6. Выход.[/]")

        option = None

        while option not in ['1', '2', '3', '4', '5', '6']:
            option = self.console.input("\n[bold blue]Выберите действие >> [/]")

            if option == '1':
                self.add_note_dialog()
            elif option == '2':
                self.show_all_notes()
            elif option == '3':
                self.search_notes_dialog()
            elif option == '4':
                self.delete_note_dialog()
            elif option == '5':
                self.display_note()
            elif option == '6':
                self.clear()
                self.console.print("До свидания!", style="bold green")
                exit()
            else:
                self.console.print("Выберите действие, обозначенное цифрами от 1 до 6.", style="bold red")

    def add_note_dialog(self) -> None:
        """
        Create new note.
        """

        self.clear()

        title = self.console.input("[bold]Введите название заметки >> [/]")
        self.clear()

        self.console.print("[bold green]{}[/]".format(title), justify="center")
        self.console.print("[bold]Для остановки ввода оставьте строку пустой и нажмите Enter.[/]".format(title), justify="center")
        content = self.multiline_input()

        self.db.create_note(title, content)

        self.clear()
        self.console.print("[bold green]Заметка успешно добавлена![/]", justify="center")
        self.console.print("[bold]Вы возвращены в меню![/]", justify="center")

        time.sleep(2)
        self.display_menu()

    def show_all_notes(self) -> None:
        """
        Show all notes to user.
        """

        self.clear()
        notes = self.db.get_all_notes()
        self.console.print("[bold yellow]Сейчас будут выведены все заметки с кратким их описанием. "
                           "Запомните ID заметки для взаимодействия.[/]", justify="center")
        time.sleep(2)

        for note in notes:
            content = (note[2][:70]).replace('\n', '  ') + '...' if len(note[2]) > 70 else (note[2]).replace('\n', '  ')
            self.console.print(f"[bold]· Заметка #{note[0]}[/]\n"
                               f"    [bold]Название:[/] {note[1][:70] + '...' if len(note[1]) > 70 else note[1]}\n"
                               f"    [bold]Содержание:[/] {content}\n")

            time.sleep(0.5)
        
        self.console.print("[bold yellow]Выберите действие[/]")
        self.console.print("[bold]1. Найти заметку.[/]")
        self.console.print("[bold]2. Удалить заметку.[/]")
        self.console.print("[bold]3. Вернуться в меню.[/]")
        self.console.print("[bold]4. Раскрыть заметку.[/]")
        
        option = None

        while option not in ['1', '2', '3', '4']:
            option = self.console.input("\n[bold blue]Выберите действие >> [/]")

            if option == '1':
                self.search_notes_dialog()
            elif option == '2':
                self.delete_note_dialog()
            elif option == '3':
                self.display_menu()
            elif option == '4':
                self.display_note()
            else:
                self.console.print("Выберите действие, обозначенное цифрами от 1 до 4.", style="bold red")

    def search_notes_dialog(self) -> None:
        """
        Search notes.
        """

        self.clear()

        keyword = self.console.input("[bold]Введите ключевое слово для поиска >> [/]")

        self.clear()
        self.console.print("[bold yellow]Сейчас будут выведены все заметки по ключевому слову с кратким их описанием. "
                           "Запомните ID заметки для взаимодействия.[/]", justify="center")
        
        time.sleep(2)
        notes = self.db.search_notes(keyword)

        if notes:
            for note in notes:
                content = (note[2][:70]).replace('\n', '  ') + '...' if len(note[2]) > 70 else (note[2]).replace('\n', '  ')
                self.console.print(f"[bold yellow]· Заметка #{note[0]}[/]\n"
                                   f"    [bold]Название:[/] {note[1][:70] + '...' if len(note[1]) > 70 else note[1]}\n"
                                   f"    [bold]Содержание:[/] {content}\n")
                time.sleep(0.5)

            self.console.print("[bold yellow]Выберите действие[/]")
            self.console.print("[bold]1. Показать все заметки.[/]")
            self.console.print("[bold]2. Удалить заметку.[/]")
            self.console.print("[bold]3. Вернуться в меню.[/]")
            self.console.print("[bold]4. Раскрыть заметку.[/]")
            
            option = None

            while option not in ['1', '2', '3', '4']:
                option = self.console.input("\n[bold blue]Выберите действие >> [/]")

                if option == '1':
                    self.show_all_notes()
                elif option == '2':
                    self.delete_note_dialog()
                elif option == '3':
                    self.display_menu()
                elif option == '4':
                    self.display_note()
                else:
                    self.console.print("Выберите действие, обозначенное цифрами от 1 до 4.", style="bold red")
                
        else:
            self.console.print("[bold red]Не найдено ни 1 заметки.\nНажмите Enter для перемещения в главное меню[/]", justify="center")
            input()
            self.display_menu()

    def delete_note_dialog(self):
        """
        Delete note by uid.
        """

        self.clear()

        note_id = self.console.input("[bold]Введите номер заметки для удаления >> [/]")
        time.sleep(1)

        if note_id.isdigit():
            note_id = int(note_id)

            self.db.delete_note(note_id)

            self.console.print("[bold green]Заметка успешно удалена.\nНажмите Enter для перемещения в главное меню[/]", justify="center")
        else:
            self.console.print("[bold red]Некорректный ввод.\nНажмите Enter для перемещения в главное меню[/]", justify="center")

        input()
        self.display_menu()
    
    def display_note(self) -> None:
        """
        Display note.
        """

        self.clear()
        
        note_id = self.console.input("[bold]Введите номер заметки для отображения >> [/]")
        if note_id.isdigit():
            note_id = int(note_id)
        else:
            self.console.print("[bold red]Некорректный ввод.\nНажмите Enter для перемещения в главное меню[/]", justify="center")
            input()
            self.display_menu()

        self.clear()

        note = self.db.show_note(note_id)

        if note is None:
            self.console.print("[bold red]Заметка не найдена.[/]", justify="center")
        else:
            self.console.print("[bold yellow]Заметка #{}[/]".format(note[0]), justify="center")
            self.console.print('[bold]"{}"[/]'.format(note[1]), justify="center")

            for line in note[2].split('\n'):
                self.console.print("[bold blue]| {}[/]".format(line))

        self.console.print("[bold yellow]Нажмите Enter для перемещения в главное меню[/]", justify="center")
        input()
        self.display_menu()

            