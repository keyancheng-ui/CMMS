import os
import hashlib
from typing import Optional, Dict, Any

class UserDAO:
    def __init__(self, conn):
        self.conn = conn

    def ensure_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS app_users (
              id INT PRIMARY KEY AUTO_INCREMENT,
              username VARCHAR(64) NOT NULL UNIQUE,
              password_hash VARBINARY(64) NOT NULL,
              salt VARBINARY(32) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              last_login TIMESTAMP NULL
            )
            """
        )
        self.conn.commit()
        cur.close()

    def _hash_password(self, password: str, salt: Optional[bytes] = None) -> (bytes, bytes):
        s = salt if salt is not None else os.urandom(16)
        h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), s, 100000)
        return s, h

    def create_user(self, username: str, password: str) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM app_users WHERE username=%s", (username,))
        exists = cur.fetchone()[0]
        if exists:
            cur.close()
            return {"success": False, "error": "username exists"}
        salt, pwd_hash = self._hash_password(password)
        cur.execute(
            "INSERT INTO app_users(username, password_hash, salt) VALUES(%s, %s, %s)",
            (username, pwd_hash, salt)
        )
        self.conn.commit()
        cur.close()
        return {"success": True}

    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, password_hash, salt FROM app_users WHERE username=%s", (username,))
        row = cur.fetchone()
        if not row:
            cur.close()
            return {"success": False}
        uid, stored_hash, salt = row[0], row[1], row[2]
        _, check_hash = self._hash_password(password, salt)
        ok = stored_hash == check_hash
        if ok:
            cur.execute("UPDATE app_users SET last_login=NOW() WHERE id=%s", (uid,))
            self.conn.commit()
        cur.close()
        return {"success": ok, "user_id": uid if ok else None}

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, username, created_at, last_login FROM app_users WHERE username=%s", (username,))
        row = cur.fetchone()
        cur.close()
        return row
