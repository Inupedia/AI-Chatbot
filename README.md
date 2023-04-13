# AI Chatbot

AI Chatbot是一个由OpenAI驱动的聊天软件，它可以通过Voicevox与用户进行语音交互。


### 要求
- Python 3.8或更高版本及其依赖包
- OpenAI API密钥
- Voicevox引擎

### 安装
1. 克隆存储库：
```bash
git clone https://github.com/Inupedia/AI-Chatbot.git
```
2. 安装所需的软件包：
```bash
pip install -r requirements.txt 
```

3. 下载VoiceVox引擎并运行：
   1. [官方软件](https://voicevox.hiroshiba.jp/)
   2. [Docker镜像](https://hub.docker.com/r/voicevox/voicevox_engine)
   3. [Google Colab](https://github.com/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb)

### 使用方法
1. 修改`module/config.json`的信息
   1. `chat-mode`: `voice`或`text`, 选择使用语音或文本模式
   2. `api_key`: OpenAI API密钥, 可以在[这里](https://beta.openai.com/account/api-keys)获取
   3. `role`: 角色性格塑造, 可根据个人喜好自行调教
   4. `max_tokens`, `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`: OpenAI GPT-3的参数, 参考[这里](https://beta.openai.com/docs/api-reference/completions/create)进行调整
   5. `endpoint`: VoiceVox引擎的地址, 根据本地运行方式进行调整
   6. `speaker_id`: VoiceVox引擎的ID, 可参照[官方声音样品](https://voicevox.hiroshiba.jp/)及对比[对应角色](/speaker.json)进行调整
2. 运行程序 (首先运行Voicevox)：
```bash
python main.py
```

