# GEMINI.md - S.Cb. Project Context

## Project Overview
**S.Cb.** is a sentiment-aware Discord chatbot designed for research and community interaction. It uses a hybrid architecture:
- **Natural Language Generation:** Powered by OpenAI's `text-davinci-002` (GPT-3) via `model_1.py`.
- **Local Sentiment Analysis:** A custom GRU-based recurrent neural network (`model_2.py`) that classifies user input into six emotions: anger, sadness, fear, joy, surprise, and love.
- **State Management:** A MySQL database layer (`database/`) that tracks user chat logs and emotional trends over time.
- **Dynamic Interaction:** The bot can trigger specific actions (like playing music via a music bot) based on detected emotion levels and user-defined customization rules.

## Core Architecture
- **`main.py`:** The primary entry point.
- **`Discord_Bot.py`:** Contains the main Discord event loop and command logic. 
  - **Command Prefix:** `§` for built-in commands like `join`.
  - **Interaction Mode:** Users must prefix messages with `!` in channels. Using `!?` sends the response via DM.
  - **Customization:** Users can use `!#customize` to set up emotional triggers (e.g., play a song when sad).
- **`modules.py`:** The "brain" that coordinates between the GPT-3 generator and the GRU sentiment predictor. It implements a weighted-average algorithm to track emotional state over the last 5 turns.
- **`model_1.py`:** Manages OpenAI API calls and maintains the "first impression" prompt structure for GPT-3.
- **`model_2.py`:** Handles local inference for sentiment prediction. **Note:** Paths for `my_model.h5` and `tokenizer.pickle` are currently hardcoded to local absolute paths and may need updating.

## Building and Running

### Prerequisites
- **Python 3.10+**
- **uv:** The project uses `uv` for dependency management.
- **MySQL Database:** Ensure a MySQL instance is running with the schema expected by `database/db_config.py`.

### Setup and Installation
1.  **Install dependencies:**
    ```bash
    uv sync
    ```
2.  **Environment Setup:**
    Create a `.env` file in the root directory:
    ```env
    DISCORD_TOKEN="your_discord_bot_token"
    OPENAI_API_KEY="your_openai_api_key"
    ```

### Running the Bot
```bash
uv run main.py
```

### Deploying to Railway

### 1. Project Setup
- Create a new project on [Railway](https://railway.app/).
- Connect your GitHub repository.

### 2. Database (MySQL)
- Add a **MySQL** service to your project.
- In your Railway MySQL service settings, find the **Variables** tab. Railway will automatically inject `MYSQLHOST`, `MYSQLUSER`, etc., into your bot service.
- **Initialize Schema:** Copy the contents of `schema.sql` and run them in the **Data** tab of your MySQL service to create the necessary tables.

### 3. Variables
- In your main service settings, add the following environment variables:
  - `DISCORD_TOKEN`: Your bot's token.
  - `GEMINI_API_KEY`: Your Google Gemini API key.

### 4. Weights & Models
- **IMPORTANT:** Ensure you upload the `my_model.h5` and `tokenizer.pickle` files to the root directory of your project before deploying, or update the paths in `model_2.py` if you store them in a subfolder.

## Development Conventions
- **Sentiment Mapping:** The system maps indices 0-5 to `['anger', 'sadness', 'fear', 'joy', 'surprise', 'love']`.
- **Database Logic:** Usernames are sanitized (removing the last 5 characters/discriminator) before storage.
- **Emotion Persistence:** The bot uses a weighted average of recent sentiments to avoid erratic changes in its "perception" of the user's mood.
- **Music Bot Integration:** The bot currently expects a specific music bot (ID: `547905866255433758`) to be present in the server to fulfill "play song" triggers.

## Key Files Summary
- `Discord_Bot.py`: Bot logic and emotion-triggered customization.
- `modules.py`: Weighted sentiment logic and cross-model coordination.
- `model_2.py`: GRU model loader and predictor (Sentiment).
- `model_1.py`: GPT-3 integration (Generation).
- `database/db_controller.py`: CRUD operations for users, chatlogs, and sentiment history.
