# AGENTS.md

## Cursor Cloud specific instructions

### Product Overview
This is an AI Chatbot / AI VTuber application: a Python app supporting **OpenAI (ChatGPT)** and **Google Gemini** as AI backends, with Google Translate (via `deep-translator`) for Japanese translation and Voicevox for Japanese text-to-speech. It supports three modes: `text`, `voice`, and `live` (Bilibili live stream). See `README.md` for full usage details (in Chinese).

### Running the Application
- Entry point: `python main.py` (requires Voicevox running and a valid AI API key)
- AI provider is configured in `module/config.json` via `provider` (`openai` or `gemini`)
- Chat mode is configured via `chat_mode` (`text`, `voice`, or `live`)
- The app is interactive (reads from stdin in text mode, microphone in voice mode)

### Required Services
- **Voicevox Engine**: Must be running on `http://localhost:50021`. Start via Docker:
  ```
  sudo docker start voicevox || sudo docker run -d --name voicevox -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest
  ```
  Wait ~10 seconds for it to become ready. Verify with `curl http://localhost:50021/version`.
- **AI API Key** (one of):
  - OpenAI: `OPENAI_API_KEY` env var or `openai.api_key` in config
  - Gemini: `GEMINI_API_KEY` env var or `gemini.api_key` in config
- **Docker daemon**: Required for Voicevox. Start with `sudo dockerd &>/tmp/dockerd.log &` if not already running.

### System Dependencies (pre-installed in snapshot)
- `portaudio19-dev` and `python3-dev`: required to build `pyaudio`
- `ffmpeg`: required by `pydub` for audio playback
- Docker + `fuse-overlayfs` + iptables-legacy: for running Voicevox in nested container environment

### Gotchas
- The `keyboard` package requires root privileges for key capture in voice mode.
- There are no automated tests or linting configuration in this repository.
- `deep-translator` uses Google Translate under the hood but is a stable, maintained wrapper (replaced the unmaintained `googletrans==4.0.0rc1`).
- Both providers share `temperature`, `max_tokens`, and `role` from the `chatgpt` config section. The `gemini` section only needs `model` and optionally `api_key`.
- Gemini uses the modern `google-genai` SDK (not the deprecated `google-generativeai`).
- Default config uses `provider: "gemini"` with `gemini-2.5-flash`. Gemini free-tier has per-model daily quotas — if one model is exhausted, try another (e.g. `gemini-2.5-flash` when `gemini-2.0-flash` is rate-limited).
- `GEMINI_API_KEY` and `GOOGLE_API_KEY` are both supported as env var names for Gemini.
