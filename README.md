# AI Chatbot

AI Chatbot是一个由AI大语言模型驱动的聊天软件，支持 **OpenAI (ChatGPT)** 和 **Google Gemini** 两种AI后端，通过Voicevox与用户进行语音交互。

### 要求

- Python 3.8或更高版本及其依赖包
- Git (可选)
- OpenAI API密钥 或 Google Gemini API密钥 (二选一)
- Voicevox引擎

### 安装
1. 克隆存储库或者[下载zip](https://github.com/skygongque/tts/archive/refs/heads/main.zip)：
   ```bash
   git clone https://github.com/Inupedia/AI-Chatbot.git
   ```
2. 安装系统依赖 (Ubuntu/Debian):
   ```bash
   sudo apt-get install -y portaudio19-dev python3-dev ffmpeg
   ```
3. 安装所需的Python包：
   ```bash
   pip install -r requirements.txt 
   ```

4. 下载VoiceVox引擎并运行：
   1. [官方软件](https://voicevox.hiroshiba.jp/)
   2. [Docker镜像](https://hub.docker.com/r/voicevox/voicevox_engine) (推荐):
      ```bash
      docker run -d --name voicevox -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest
      ```
   3. [Google Colab](https://github.com/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb)

### 使用方法
1. 选择AI后端并设置API密钥:
   
   **OpenAI (默认)**:
   - 修改 `module/config.json` 中 `provider` 为 `"openai"`
   - 设置密钥: 环境变量 `export OPENAI_API_KEY="your-key"` 或修改配置文件中 `openai.api_key`
   
   **Google Gemini**:
   - 修改 `module/config.json` 中 `provider` 为 `"gemini"`
   - 设置密钥: 环境变量 `export GEMINI_API_KEY="your-key"` 或修改配置文件中 `gemini.api_key`
   - Gemini API密钥可在 [Google AI Studio](https://aistudio.google.com/apikey) 免费获取

2. 修改`module/config.json`的信息
   1. `provider`: `openai` 或 `gemini`，选择AI后端
   2. `chat_mode`: `voice`,`text`或者`live`，选择使用语音，文本或直播模式
   3. `role`: 角色性格塑造，可根据个人喜好自行调教
   4. `max_tokens`, `temperature`，`top_p`，`frequency_penalty`，`presence_penalty`: AI参数调整
   4. `endpoint`: VoiceVox引擎的地址，根据本地运行方式进行调整
   5. `speaker_id`: VoiceVox引擎的ID，可参照[官方声音样品](https://voicevox.hiroshiba.jp/)及对比[对应角色](/speaker.json)进行调整
   6. `username`: 用户名, 仅在`voice`和`text`模式下有效
   7. `queue_size`: 能最大存储消息队列大小, 仅在`live`和`text`模式下有效。为保持记录最新，当消息队列达到最大值时，会自动清空早期1/2的消息
   8. `room_id`: 直播间ID，如`https://live.bilibili.com/123456`中的`123456`
   9. `proxy`: 免翻墙代理，如需使用代理，请将`enabled`设置为`true`并在`host`中填写代理地址
   
2. 运行程序 (首先运行Voicevox)：
   ```bash
   python main.py
   ```

### 补充说明
1. vtuber运行角色皮肤需要用到[Vtube Studio](https://denchisoft.com/)
2. 如果需要将音频信号从一个应用程序传递到另一个应用程序或系统组件，可以使用[Virtual Audio Cable](https://vb-audio.com/Cable/)
   
### 免责声明
本项目仅供学习交流使用，不得用于商业用途，否则后果自负。

### License
[MIT](https://choosealicense.com/licenses/mit/)
