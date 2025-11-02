# S.Cb. — Multimodal Sentiment-aware Chatbot for Discord

S.Cb. is a multimodal Discord chatbot designed to provide conversational responses like ChatGPT while simultaneously analyzing user sentiment and conversational context. It combines an advanced language generation model (GPT-3.5 / Davinci via API) with a custom, lightweight recurrent neural network (GRU) that performs sentiment analysis and contextual state-tracking. The bot is intended for research/prototyping and community interactions where richer, context-aware responses and moderation cues are useful.

---

## Table of contents

- Overview
- Intent & Goals
- High-level architecture
- Models
  - GPT-3.5 / Davinci (generation)
  - Custom GRU with embedding layer (sentiment & context)
- Training & Data (GRU)
- How sentiment + context are used
- Multimodal inputs
- Getting started (quick run)
- Configuration / Environment
- Privacy & Safety
- Contributing
- License & Credits

---

## Overview

S.Cb. is a Discord bot that:
- Chats with users like ChatGPT (powered by GPT-3.5 / Davinci through the OpenAI API).
- Analyzes sentiment and conversational context using a custom GRU model.
- Uses the sentiment/context analysis to influence responses, moderation flags, or internal state to make replies feel more aware of conversation history and user emotion.
- Accepts multimodal inputs (text + attachments such as images / audio) and can incorporate features extracted from those attachments into context analysis (feature extraction modules are optional/integrations).

---

## Intent & Goals

Primary intents:
- Provide an engaging conversational experience similar to ChatGPT.
- Demonstrate how a lightweight local model (GRU) can augment a powerful LLM by providing sentiment and short-term context awareness.
- Allow researchers and devs to experiment with context-sensitive response shaping, safe-guarding, and multimodal interactions in a Discord environment.

Secondary intents:
- Provide hooks for moderation workflows (e.g., flagging extremely negative or harmful sentiment).
- Serve as a foundation for experiments where low-latency, on-device inference of user state is desirable alongside a cloud LLM.

---

## High-level architecture

1. Discord event (message / attachment) received by bot.
2. Preprocessing:
   - Text cleaned, tokenized.
   - Optional feature extraction for attachments (image/audio → embeddings via an extractor).
3. GRU pipeline:
   - Input tokens (and optional multimodal embeddings) → embedding layer → GRU stack → sentiment + context vector (local state).
4. Decision logic:
   - Sentiment/context vector influences how we craft the prompt for GPT-3.5 (tone, safety checks, clarifying questions).
   - If necessary, internal policies or moderation triggers are activated.
5. GPT-3.5 / Davinci is called with the constructed prompt and returns the natural language response.
6. Bot posts response to Discord with optional metadata (e.g., detected sentiment score, stateful cues).

---

## Models

### GPT-3.5 / Davinci (generation)
- Role: primary natural language generator. Used to produce fluent, varied, and contextual replies.
- Integration: Accessed via the OpenAI API (or equivalent wrapper). Prompts are dynamically constructed to include conversation history and GRU-derived cues (sentiment level, context tags).
- Notes: All decision logic and final generation remain dependent on prompt design and safe-guards (rate limits, token management, and API keys).

### Custom GRU with embedding layer (sentiment & context)
- Role: a compact recurrent network that provides per-message sentiment predictions and a short-term contextual embedding summarizing the recent conversation.
- Architecture (representative):
  - Token embedding layer (learned embeddings, e.g., 128–512 dims).
  - One or two GRU layers (hidden size typically 128–512).
  - Optional attention or pooling over recent hidden states for a fixed-length context vector.
  - Output heads:
    - Sentiment head: softmax for classes (e.g., negative / neutral / positive) or regression for a sentiment score.
    - Context vector head: dense projection used to condition prompts or influence internal state.
- Why GRU?
  - GRUs are computationally lightweight compared to LSTMs and simpler to train for short-term conversational dependencies.
  - They are suitable when you want efficient inference on a small server or edge environment.

---

## Training & Data (GRU)

Below is a description of how the GRU was trained conceptually. If you want to reproduce or extend the training pipeline, see the training scripts in the repository (if present) or adapt this outline:

- Data sources:
  - Curated conversational datasets with sentiment labels (public sentiment datasets, chat logs annotated for sentiment, and domain-specific examples).
  - Augmented examples created by pairing utterances with prior-turn context to teach the GRU to incorporate history.
  - Optional multimodal pairs where embeddings from images/audio are concatenated with text embeddings for training.

- Preprocessing:
  - Normalize text, lowercase (if using uncased embeddings), tokenize with the repository's tokenizer.
  - Build vocabulary for the GRU embedding or use subword units.
  - Create windows of recent messages (N previous messages + current message) to provide temporal context.

- Losses:
  - Sentiment classification: Cross-entropy loss for discrete classes.
  - Optional auxiliary losses:
    - Contrastive or triplet loss to shape context vector space.
    - Next-turn prediction or intent classification to improve contextual signals.

- Optimization:
  - Optimizer: Adam / AdamW.
  - Typical hyperparameters: learning rate in the 1e-3 → 1e-4 range, batch sizes adjusted to available hardware.
  - Regularization: dropout on GRU outputs, early stopping based on validation accuracy.

- Evaluation:
  - Standard classification metrics: accuracy, precision / recall / F1 for sentiment.
  - Context vector usefulness validated by downstream impact on prompt quality and user-perceived coherence (A/B testing with or without GRU cues).

- Inference:
  - The trained GRU produces a sentiment score and a context embedding per message. These are stored in a short-lived conversation state and used to influence prompts sent to GPT-3.5.

---

## How sentiment + context are used

- Prompt shaping:
  - The bot adjusts the prompt for GPT-3.5 according to the sentiment score (e.g., adopt a more empathetic tone if sentiment is negative).
  - The context vector is summarized into tags or explicit instructions (e.g., "User is frustrated about X; keep response concise and supportive").

- Safety & moderation:
  - High-risk sentiment patterns (rapid negative escalation / detected aggression or self-harm signals) can trigger moderation workflows: warning messages, escalation to moderators, or refusal to answer.

- Conversation memory:
  - A rolling window of context vectors and message summaries forms a short-term memory for better coherence across turns without exposing full chat logs to the LLM.

---

## Multimodal inputs

S.Cb. is designed to accept attachments from Discord:
- Images: optional image feature extractor (e.g., prebuilt embeddings) can be concatenated to text embeddings before the GRU.
- Audio: audio can be transcribed (via an external service) and processed like text; raw audio features may also be used if available.

Note: The repository includes integration points for extracting multimodal features; exact integrations and third-party models are optional and configurable.

---

## Getting started (quick run)

Example steps (project may provide scripts; adapt as needed):

1. Clone repository
   ```bash
   git clone https://github.com/youssofKarhani/S.Cb..git
   cd S.Cb.
   ```

2. Install dependencies (example for Python)
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Environment variables (example)
   ```bash
   export DISCORD_TOKEN="your-discord-bot-token"
   export OPENAI_API_KEY="your-openai-api-key"
   export GRU_MODEL_PATH="./models/gru_sentiment.pt"   # path to GRU weights
   ```

4. Run the bot
   ```bash
   python bot.py
   ```

- The repo may contain more specific run scripts or Docker configuration — check the codebase root for exact commands.

---

## Configuration

- DISCORD_TOKEN — Discord bot token.
- OPENAI_API_KEY — OpenAI API key for GPT-3.5 / Davinci.
- GRU_MODEL_PATH — Filepath to the serialized GRU weights.
- FEATURE_EXTRACTOR_* — Optional connectors for multimodal feature extraction services.
- PROMPT_TEMPLATES — Directory or file controlling how the GRU outputs are injected into LLM prompts.

---

## Privacy & Safety

- The bot may send conversation content to third-party APIs (e.g., OpenAI). Be mindful of user consent and private data.
- Consider redaction or on-device preprocessing for sensitive information before sending to any cloud API.
- Use rate limits and safety checks to avoid abusive outputs.
- The GRU runs locally (if you host weights locally), which allows some sentiment computation to remain on-premise. Balance this with usability and model maintenance.

---

## Limitations

- The GRU is a compact model for short-term context and sentiment — it is not a replacement for large-context retrieval or long-term memory systems.
- GPT-3.5 / Davinci behaviour depends heavily on prompts; unexpected responses are possible and require careful prompt engineering and safety rules.
- Sentiment detection can be imperfect, especially with sarcasm, slang, or mixed modality inputs.

---

## Contributing

Contributions are welcome. Suggested ways to help:
- Improve prompt templates and response shaping logic.
- Add or refine training data for the GRU.
- Add multimodal feature extractors or integrations (image/audio).
- Improve testing, CI, and deployment examples (Docker, Kubernetes manifests).

Please open issues or PRs with proposals and code.

---

## Credits & Acknowledgements

- GPT-3.5 / Davinci (OpenAI) for natural language capabilities (via API).
- Custom GRU model — developed in-repo as a small, efficient sentiment/context module.
- Community datasets and open-source libraries used for training and inference (check requirements.txt for exact dependencies).

---

## License

See LICENSE file in the repository root for license terms. If none exists, please add a license that matches how you want others to use this project.

---

If you want, I can:
- Add example prompts used to combine GRU outputs with GPT-3.5.
- Draft training scripts or a sample dataset pipeline for re-training the GRU.
- Create a CONTRIBUTING.md or deployment guide (Dockerfile, k8s) tailored to the repo.

 
