CREATE TABLE IF NOT EXISTS Users (
    Username VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ChatLog (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    chatlog TEXT,
    sentiment VARCHAR(50),
    anger FLOAT,
    sadness FLOAT,
    fear FLOAT,
    joy FLOAT,
    surprise FLOAT,
    love FLOAT,
    FOREIGN KEY (username) REFERENCES Users(Username)
);
