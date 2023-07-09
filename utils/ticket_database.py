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


class BannedDatabase:
    def __init__(self):
        """
        Initializes the database connection.
        """
        self.db_name = main.config.getdata('database-file-name')
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


    def create_table(self):
        """
        Creates the 'banned_from_tickets' table if it doesn't exist.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS banned_from_tickets (
                                user_id INTEGER,
                                moderator_id INTEGER,
                                focusup_id TEXT DEFAULT NULL,
                                reason TEXT DEFAULT NULL,
                                ban_appeal BOOLEAN DEFAULT FALSE
                            )''')
        self.conn.commit()
    
    
    def is_banned(self, user_id):
        """Checks if a user is banned from creating tickets.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user is banned, False otherwise.
        """
        banned_user = self.get_banned_user(user_id)

        if banned_user is None:
            return False
        else:
            return True

    
    def get_banned_user(self, user_id):
        """
        Retrieves information about a banned user.

        Args:
            user_id (int): The ID of the banned user.

        Returns:
            tuple: The banned user's information as a tuple (user_id, moderation_id, focusup_id, reason, ban_appeal).
                   Returns None if the user is not found.
        """
        self.cursor.execute('''SELECT * FROM banned_from_tickets WHERE user_id = ?''', (user_id,))
        return self.cursor.fetchone()


    def add_banned_user(self, user_id, moderator_id, focusup_id=None, reason=None):
        """
        Adds a banned user to the 'banned_from_tickets' table.

        Args:
            user_id (int): The ID of the user.
            moderator_id (int): The ID of the moderation.
            focusup_id (str, optional): The FocusUp ID of the banned user. Defaults to None.
            reason (str, optional): The reason for the ban. Defaults to None.
        """
        self.cursor.execute('''INSERT INTO banned_from_tickets (user_id, moderator_id, focusup_id, reason, ban_appeal)
                               VALUES (?,?,?,?,?)''', (user_id, moderator_id, focusup_id, '"' + reason + '"', False))
        self.conn.commit()
    
    
    def remove_banned_user(self, user_id):
        """
        Removes a banned user from the 'banned_from_tickets' table.

        Args:
            user_id (int): The ID of the user.
        """
        self.cursor.execute('''DELETE FROM banned_from_tickets WHERE user_id = ?''', (user_id,))
        self.conn.commit()
    
    
    def get_ban_reason(self, user_id):
        """
        Retrieves the ban reason for a banned user.

        Args:
            user_id (int): The ID of the banned user.

        Returns:
            str: The ban reason for the user. Returns None if the user is not found or there is no reason provided.
        """
        self.cursor.execute('''SELECT reason FROM banned_from_tickets WHERE user_id = ?''', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    
    def update_ban_appeal(self, user_id):
        """
        Updates the ban appeal status for a banned user to True.

        Args:
            user_id (int): The ID of the banned user.
        """
        self.cursor.execute('''UPDATE banned_from_tickets SET ban_appeal = ? WHERE user_id = ?''', (True, user_id))
        self.conn.commit()

    
    def get_ban_appeal(self, user_id):
        """
        Retrieves the ban appeal status for a banned user.

        Args:
            user_id (int): The ID of the banned user.

        Returns:
            bool: The ban appeal status for the user. Returns False if the user is not found or no ban appeal is recorded.
        """
        self.cursor.execute('''SELECT ban_appeal FROM banned_from_tickets WHERE user_id = ?''', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return bool(result[0])
        else:
            return False


    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
