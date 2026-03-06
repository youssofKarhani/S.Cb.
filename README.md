# S.Cb. — Multimodal Sentiment-aware Chatbot for Discord

S.Cb. (Sentiment-aware Chatbot) is a sophisticated Discord companion that bridges the gap between large-scale language generation and local emotional intelligence. By combining Google Gemini's generative capabilities with a custom-trained, lightweight GRU (Gated Recurrent Unit) neural network, S.Cb. provides responses that are contextually aware and emotionally resonant.

---

## Key Features

- **Hybrid Intelligence Architecture:** Leverages Gemini 1.5 Flash for fluent conversation and a local GRU model for real-time sentiment analysis across six core emotions: Anger, Sadness, Fear, Joy, Surprise, and Love.
- **Weighted Emotional State:** Implements a proprietary algorithm that tracks conversational context over a rolling window. This ensures the bot maintains a realistic perception of the user's mood, preventing erratic emotional shifts from single-word inputs.
- **Dynamic Emotional Triggers:** Users can configure autonomous reactions based on detected emotions. For example, the bot can interface with music players to suggest tracks that match or mitigate the user's current emotional state.
- **Persistent Personalization:** Integrates with a MySQL backend to store interaction history and emotional trends, allowing for a consistent personality across multiple sessions.
- **Flexible Deployment:** Optimized for both local development and cloud hosting platforms like Railway, with full support for modern dependency management via uv.

---

## Getting Started

### Prerequisites
- **Python 3.13 or higher**
- **uv** for high-performance dependency management.
- **MySQL Database** for state persistence.
- **API Keys:** A Gemini API key and a Discord Bot Token are required.

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/youssofKarhani/S.Cb..git
   cd S.Cb.
   ```

2. **Setup environment variables:**
   Create a .env file in the root directory:
   ```env
   DISCORD_TOKEN="your_discord_bot_token"
   GEMINI_API_KEY="your_gemini_api_key"
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Initialize Database:**
   Apply the provided schema.sql to your MySQL instance to create the necessary tables for user tracking and chat history.

### Running the Application
```bash
uv run main.py
```

---

## Interaction Guide

| Method | Description |
| :--- | :--- |
| ! [message] | Standard channel interaction. The bot replies directly in the chat. |
| !? [message] | Private interaction. The bot processes the request and replies via DM. |
| !#customize | Opens the configuration menu for emotional triggers and song assignments. |
| !#1, [emo], [lv], [song] | Configures a specific trigger (e.g., !#1, sadness, 2, Moonlight Sonata). |
| §join | Commands the bot to join your current voice channel. |

---

## Roadmap and Contribution Opportunities

S.Cb. is an evolving project, and we are actively looking for contributors to help expand its capabilities. Below is a list of current priorities where your expertise could make a significant impact:

### High Priority Improvements
- **Configuration Externalization:** Transition hardcoded variables and song assignments in the bot logic into a structured configuration system (YAML/JSON) or database-driven settings.
- **Enhanced Error Resilience:** Improve the exception handling framework to provide more descriptive feedback and graceful recovery during API or database connectivity issues.
- **API Modernization:** Refine the interaction with the Google Generative AI SDK to utilize the latest features of Gemini 1.5 Pro and Flash, including system instructions and safer content filtering.

### Feature Expansion
- **True Multimodal Analysis:** While the framework is designed for it, the bot currently lacks robust logic for processing image and audio attachments. We need contributors to help integrate CV (Computer Vision) and ASR (Automatic Speech Recognition) modules.
- **Universal Music Integration:** Replace the current brittle dependency on a specific music bot ID with a standardized integration for popular Discord music libraries or direct Spotify/YouTube API support.
- **Automated Testing:** The project currently lacks a comprehensive test suite. Implementing unit and integration tests using pytest would greatly increase stability.

### Architecture and DevOps
- **Containerization:** Creation of a optimized Dockerfile for easier deployment across diverse environments.
- **Documentation:** Expanding code-level documentation and docstrings to improve maintainability for new contributors.

---

## Technical Overview

The "Brain" of S.Cb. resides in its coordination layer, which fuses data from two distinct sources:
- **Generation:** Handled by Gemini 1.5 Flash, providing rapid and intelligent text generation.
- **Sentiment Logic:** A local GRU model processes inputs through a 500-token window. The resulting sentiment vector is then passed through a weighted average filter, which considers previous states and frequency-based rules to determine the final emotional output.

---

## Privacy and Ethics

S.Cb. is designed with transparency in mind. Sentiment analysis is performed locally to minimize data exposure, though text content is processed by Google's Gemini API to generate responses. Users should be aware that interaction history is stored in the connected MySQL database for personalization purposes.

---

## License

This project is licensed under the terms found in the LICENSE file. If no license is provided, all rights are reserved.

*Developed for the exploration of emotional intelligence in conversational AI.*
