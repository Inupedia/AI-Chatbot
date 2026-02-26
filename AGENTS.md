# AGENTS.md

## Cursor Cloud specific instructions

### Product Overview
This is an AI Chatbot / AI VTuber application: a Python app using OpenAI ChatGPT for conversation, Google Translate for Japanese translation, and Voicevox for Japanese text-to-speech. It supports three modes: `text`, `voice`, and `live` (Bilibili live stream). See `README.md` for full usage details (in Chinese).

### Running the Application
- Entry point: `python main.py` (requires Voicevox running and a valid OpenAI API key)
- Chat mode is configured in `module/config.json` via `chat_mode` (`text`, `voice`, or `live`)
- The app is interactive (reads from stdin in text mode, microphone in voice mode)

### Required Services
- **Voicevox Engine**: Must be running on `http://localhost:50021`. Start via Docker:
  ```
  sudo docker start voicevox || sudo docker run -d --name voicevox -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest
  ```
  Wait ~10 seconds for it to become ready. Verify with `curl http://localhost:50021/version`.
- **OpenAI API Key**: Must be set in `module/config.json` under `openai.api_key`. The `OPENAI_API_KEY` environment variable is **not** automatically used by this codebase; the key must be in the config file.
- **Docker daemon**: Required for Voicevox. Start with `sudo dockerd &>/tmp/dockerd.log &` if not already running.

### System Dependencies (pre-installed in snapshot)
- `portaudio19-dev` and `python3-dev`: required to build `pyaudio`
- `ffmpeg`: required by `pydub` for audio playback
- Docker + `fuse-overlayfs` + iptables-legacy: for running Voicevox in nested container environment

### Gotchas
- `openai` resolves to version `0.28.1` due to dependency constraints from `googletrans==4.0.0rc1` (which pins `httpx==0.13.3`). This means the codebase uses the legacy `openai.ChatCompletion.create()` API, not the new `openai.OpenAI()` client.
- `pyaudio` requires `portaudio19-dev` **and** `python3-dev` to compile from source.
- The `keyboard` package requires root privileges for key capture in voice mode.
- There are no automated tests or linting configuration in this repository.
- The app uses the older `googletrans==4.0.0rc1` which is an unofficial Google Translate wrapper; it may be unreliable.
