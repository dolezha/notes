import sqlite3


class NotesDatabase:
    def __init__(self, db_name) -> None:
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.conn.row_factory = sqlite3.Row

    def create_table(self) -> None:
        """
        Create table with notes
        """

        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS notes
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  title TEXT NOT NULL,
                                  content TEXT NOT NULL)''')

    def create_note(self, title: str, content: str) -> None:
        """
        Creating new note
        :param title: title of note
        :param content: content of note
        """

        with self.conn:
            self.conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)',
                              (title, content))

    def get_all_notes(self) -> list:
        """
        Retuen all notes, whick are in database
        """

        with self.conn:
            cursor = self.conn.execute('SELECT * FROM notes')
            return cursor.fetchall()

    def search_notes(self, keyword: str) -> list:
        """
        Return all notes, that have keyword in title or content
        :param keyword: search keyword
        """

        with self.conn:
            keyword = keyword.strip().lower()

            query = """SELECT * FROM notes WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ?"""
            params = ('%{}%'.format(keyword), '%{}%'.format(keyword))

            cursor = self.conn.execute(query, params)
            return cursor.fetchall()


    def delete_note(self, note_id: int) -> None:
        """
        Delete note by uid
        :param note_id: uid of note
        """
        with self.conn:
            self.conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))

    def show_note(self, note_id: int | str):
        """
        Return note by uid
        :param note_id: uid of note
        """

        with self.conn:
            try:
                cursor = self.conn.execute('SELECT * FROM notes WHERE id = ?', (int(note_id),))
                return cursor.fetchone()
            except AttributeError:
                return None
