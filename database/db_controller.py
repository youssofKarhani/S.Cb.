from database import db_config

class db_controller:
    def __init__(self):
        self.db = db_config.connection()
        self.conn = self.db.get_connection()
        self.cur = None
        if self.conn:
            self.cur = self.conn.cursor()
        else:
            print("CRITICAL: Database connection failed. Verify MYSQL environment variables.")

    def _is_connected(self):
        if self.conn and self.cur:
            return True
        # Try one last-ditch reconnect
        self.db = db_config.connection()
        self.conn = self.db.get_connection()
        if self.conn:
            self.cur = self.conn.cursor()
            return True
        return False

    #-----------User functions-----------#
    def select_users(self):
        if not self._is_connected(): return None
        self.cur.execute('SELECT * FROM Users')
        users = self.cur.fetchone()
        return users
        
    def select_user(self, username):
        if not self._is_connected(): return None
        self.cur.execute('SELECT Username FROM Users WHERE Username=%s', (username,))
        user = self.cur.fetchone()
        return user

    def insert_user(self, username):
        if not self._is_connected(): return
        try:
            # Handle both old discriminators (Name#1234) and new handles (@name)
            name = username.split('#')[0] if '#' in username else username
            self.cur.execute('INSERT INTO `Users` (`Username`) VALUES(%s)', (username,))
            self.conn.commit()
            self.update_name(username, name)
            print(f"Username: {username} insert was successful")
        except Exception as e:
            print(f"There was an error while inserting the user: {e}")
        
    def update_name(self, username, name):
        if not self._is_connected(): return
        try:
            self.cur.execute('UPDATE `Users` SET `Name`=%s WHERE `Username`=%s', (name, username))
            self.conn.commit()
            print(f"The User: {username}'s name update was successful")
        except Exception as e:
            print(f"There was an error while updating the name of the user: {e}")
        
    #-----------Chatlog functions-----------#
    def add_Chatlog(self, username:str, chatlog, sentiment, anger, sadness, fear, joy, surprise, love):
        if not self._is_connected(): return
        try:
            self.cur.execute('INSERT INTO `ChatLog`(`username`, `chatlog`, `sentiment`, `anger`, `sadness`, `fear`, `joy`, `surprise`, `love`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, chatlog, sentiment, anger, sadness, fear, joy, surprise, love))
            self.conn.commit()
            print(f"{username}'s ChatLog was successfully updated")
        except Exception as e:
            print(f"There was an error while updating chatlog: {e}")

    def get_ChatLog(self, username:str):
        if not self._is_connected(): return []
        try:
            self.cur.execute('SELECT `chatlog` FROM `ChatLog` WHERE `username`=%s', (username,))
            all_chatlog = self.cur.fetchall()
            if not all_chatlog:
                return []
            
            # Formatting logic: combine history
            chatlog_strings = [row[0] for row in all_chatlog]
            first_chatlog = chatlog_strings[0]
            recent_context = chatlog_strings[-20:]
            recent_context.append(first_chatlog)
            
            print(f"{username}'s chatlog was fetched successfully.")
            return recent_context
        except Exception as e:
            print(f"There was an error while fetching chatlog: {e}")
            return []
    
    #-----------Sentiment functions-----------#
    def get_sentiment(self, username:str):
        if not self._is_connected(): return []
        try:
            self.cur.execute('SELECT `sentiment` FROM `ChatLog` WHERE `username`=%s ORDER BY ID DESC LIMIT 4', (username,))
            sentiments_array = self.cur.fetchall()
            print(f"{username}'s sentiment was fetched successfully.")
            return sentiments_array
        except Exception as e:
            print(f"There was an error while fetching sentiments: {e}")
            return []
            
    def get_sentiments_array(self, username:str):
        if not self._is_connected(): return []
        try:
            self.cur.execute('SELECT `anger`, `sadness`, `fear`, `joy`, `surprise`, `love` FROM `ChatLog` WHERE `username`=%s ORDER BY ID DESC LIMIT 4', (username,))
            sentiments = self.cur.fetchall()
            print(f"{username}'s sentiments were fetched successfully.")
            return sentiments
        except Exception as e:
            print(f"There was an error while fetching sentiment array: {e}")
            return []


    