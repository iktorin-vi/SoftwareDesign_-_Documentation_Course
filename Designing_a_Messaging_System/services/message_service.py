from storage.database import get_connection


class MessageService:
    @staticmethod
    def create_user(name: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        uid = cursor.lastrowid
        conn.close()
        return uid

    @staticmethod
    def send_message(conv_id: int, sender_id: int, text: str):
        if not text.strip(): return None  # Error Handling: empty message

        conn = get_connection()
        cursor = conn.cursor()
        # Variant 3: Offline delivery - повідомлення зберігається зі статусом pending
        cursor.execute(
            "INSERT INTO messages (conversationId, senderId, text, status) VALUES (?, ?, ?, ?)",
            (conv_id, sender_id, text, "pending")
        )
        conn.commit()
        mid = cursor.lastrowid
        conn.close()
        return mid

    @staticmethod
    def get_history(conv_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE conversationId = ?", (conv_id,))
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return messages

    @staticmethod
    def mark_as_delivered(message_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE messages SET status = 'delivered', deliveredAt = CURRENT_TIMESTAMP WHERE id = ?",
            (message_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def mark_as_read(message_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE messages SET status = 'read', readAt = CURRENT_TIMESTAMP WHERE id = ?",
            (message_id,)
        )
        conn.commit()
        conn.close()