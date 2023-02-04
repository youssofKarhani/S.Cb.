from database import db_config

class db_controller:

    db = db_config.connection();
    conn = db.get_connection();
    cur = conn.cursor();

    #-----------User functions-----------#
    def select_users(self):
        self.cur.execute('SELECT * FROM User');
        users = self.cur.fetchone();
        return users;
        
    def select_user(self, username):
        self.cur.execute('SELECT Username FROM users WHERE username=%s', (username,));
        user = self.cur.fetchone();
        return user;

    def insert_user(self, username):
        try:
            name = username[0:-5]; #On discord the username ends with '#4numbers' (e.g. MyName#1234)
            self.cur.execute('INSERT INTO `Users` (`Username`) VALUES(%s)', (username,));
            self.conn.commit();
            self.update_name(username, name);
            print("Username: ", username," insert was successful");
            
        except(Exception) as e:
            print("There was an error while inserting the user: " + e);
        
    def update_name(self, username, name):
        try:
            self.cur.execute('UPDATE `Users` SET `Name`=%s WHERE `Username`=%s', (name, username));
            self.conn.commit();
            print("The User: ", username,"'s name update was successful");
        except(Exception) as e:
            print("There was an error while updating the name of the user: " + e);
        
    #-----------Chatlog functions-----------#
    def add_Chatlog(self, username:str, chatlog, sentiment, anger, sadness, fear, joy, surprise, love):
        try:
            self.cur.execute('INSERT INTO `ChatLog`(`username`, `chatlog`, `sentiment`, `anger`, `sadness`, `fear`, `joy`, `surprise`, `love`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, chatlog, sentiment, anger, sadness, fear, joy, surprise, love));
            self.conn.commit();
            print(username,"'s ChatLog was successfully Updated");
        except(Exception) as e:
            print("There was an error while updating chatlog: ", e);

    def get_ChatLog(self, username:str):
        try:
            self.cur.execute('SELECT `chatlog` FROM `ChatLog` WHERE `username`=%s', (username,));
            all_chatlog = self.cur.fetchall();
            first_chatlog = all_chatlog[0];
            chatlog = all_chatlog[-20:];
            chatlog.append(first_chatlog);
            print(username,"'s chatlog was fetched successfully.");
            return chatlog;
        except(Exception) as e:
            print("There was an error while fetching chatlog: ", e);
    
    #-----------Sentiment functions-----------#
    def get_sentiment(self, username:str):
        try:
            self.cur.execute('SELECT `sentiment` FROM `chatlog` where `username`=%s ORDER BY ID DESC LIMIT 4', (username,));
            sentiments_array = self.cur.fetchall();
            print(username,"'s sentiment was fetched successfully.");
            return sentiments_array;
        except(Exception) as e:
            print("There was an error while fetching sentiments: ", e);
            
            
    def get_sentiments_array(self, username:str):
        try:
            self.cur.execute('SELECT `anger`, `sadness`, `fear`, `joy`, `surprise`, `love` FROM `chatlog` where `username`=%s ORDER BY ID DESC LIMIT 4', (username,));
        
            sentiments = self.cur.fetchall();
        
            print(username,"'s sentiments was fetched successfully.");
            return sentiments;
        except(Exception) as e:
            print("There was an error while fetching sentiment: ", e);
            
    
'''          
    def insert_sentiments(self, username:str, sentiment_array):
        try:
            self.cur.execute('UPDATE `ChatLog` SET `sentiment`=%s WHERE `username`=%s', (sentiment, username));
            self.conn.commit();
            print(username,"'s sentiment was successfully Updated");
        except(Exception) as e:
            print("There was an error while updating sentiment: ", e);
'''   

    