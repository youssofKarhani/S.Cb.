-- S.Cb. Database Schema

-- Table to store unique users and their display names
CREATE TABLE IF NOT EXISTS Users (
    Username VARCHAR(255) PRIMARY KEY,
    Name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store conversation history and sentiment scores
CREATE TABLE IF NOT EXISTS ChatLog (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    chatlog TEXT,
    sentiment VARCHAR(50),
    anger FLOAT DEFAULT 0.0,
    sadness FLOAT DEFAULT 0.0,
    fear FLOAT DEFAULT 0.0,
    joy FLOAT DEFAULT 0.0,
    surprise FLOAT DEFAULT 0.0,
    love FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES Users(Username),
    INDEX idx_user_history (username, ID DESC)
);
