import sqlite3

import main

class TicketDatabase:
    def __init__(self):
        """
        Initializes the database connection.
        """
        self.db_name = main.config.getdata('database-file-name')
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


    def create_table(self):
        """
        Creates the 'tickets' table if it doesn't exist.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                                user_id INTEGER,
                                message_id INTEGER,
                                channel_id INTEGER,
                                focusup_id TEXT DEFAULT NULL
                            )''')
        self.conn.commit()
    
    
    def has_ticket(self, channel_id):
        """
        Checks if a ticket exists for a given user ID.

        Args:
            channel_id (int): The ID of the ticket channel.

        Returns:
            bool: True if a ticket exists, False otherwise.
        """
        self.cursor.execute('''SELECT COUNT(*) FROM tickets WHERE channel_id = ?''', (channel_id,))
        count = self.cursor.fetchone()[0]
        return count > 0


    def add_ticket(self, user_id, message_id, channel_id, focusup_id=None):
        """
        Adds a ticket to the 'tickets' table.

        Args:
            user_id (int): The ID of the user.
            message_id (int): The ID of the ticket message.
            channel_id (int): The ID of the ticket channel.
            focusup_id (str, optional): The ID of the FocusUp Account. Defaults to None.
        """
        self.cursor.execute('''INSERT INTO tickets (user_id, message_id, channel_id, focusup_id)
                               VALUES (?, ?, ?, ?)''', (user_id, message_id, channel_id, focusup_id))
        self.conn.commit()


    def get_ticket(self, user_id):
        """
        Retrieves a ticket from the 'tickets' table.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: The ticket information as a tuple (user_id, message_id, channel_id, focusup_id).
        """
        self.cursor.execute('''SELECT * FROM tickets WHERE user_id = ?''', (user_id,))
        return self.cursor.fetchone()


    def update_ticket_focusup_id(self, user_id, focusup_id):
        """
        Updates the FocusUp ID of a ticket in the 'tickets' table.

        Args:
            user_id (int): The ID of the user.
            focusup_id (str): The ID of the FocusUp Account.
        """
        self.cursor.execute('''UPDATE tickets SET focusup_id = ? WHERE user_id = ?''', (focusup_id, user_id))
        self.conn.commit()


    def remove_ticket(self, user_id):
        """
        Removes a ticket from the 'tickets' table.

        Args:
            user_id (int): The ID of the user.
        """
        self.cursor.execute('''DELETE FROM tickets WHERE user_id = ?''', (user_id,))
        self.conn.commit()


    def get_channel_id(self, user_id):
        """
        Retrieves the channel ID associated with a ticket from the 'tickets' table.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The channel ID associated with the ticket.
        """
        self.cursor.execute('''SELECT channel_id FROM tickets WHERE user_id = ?''', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    
    def get_message_id(self, channel_id):
        """
        Retrieves the message ID associated with a ticket from the 'tickets' table.

        Args:
            channel_id (int): The ID of the ticket channel.

        Returns:
            int: The message ID associated with the ticket.
        """
        self.cursor.execute('''SELECT message_id FROM tickets WHERE channel_id = ?''', (channel_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    
    def get_user_id(self, channel_id):
        """
        Retrieves the user ID associated with a ticket from the 'tickets' table.

        Args:
            channel_id (int): The ID of the ticket channel.

        Returns:
            int: The user ID associated with the ticket.
        """
        self.cursor.execute('''SELECT user_id FROM tickets WHERE channel_id = ?''', (channel_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    
    def get_focusup_id(self, user_id):
        """
        Retrieves the FocusUp ID associated with a ticket from the 'tickets' table.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str: The FocusUp ID associated with the ticket.
        """
        self.cursor.execute('''SELECT focusup_id FROM tickets WHERE user_id = ?''', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None


    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()