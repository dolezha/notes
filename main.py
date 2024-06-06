from db import NotesDatabase
from interface import ConsoleInterface


def main():
    try:
        db = NotesDatabase('notes.db')
        console = ConsoleInterface(db, True)
    
        console.display_menu()
    except KeyboardInterrupt:
        db = NotesDatabase('notes.db')
        console = ConsoleInterface(db)
        
        console.clear()
        console.console.print("[bold green]До свидания! [/]")


if __name__ == "__main__":
    main()
