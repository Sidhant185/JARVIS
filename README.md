<p align="center">
  <img src="Frontend/Graphics/Jarvis.gif" alt="J.A.R.V.I.S." width="200"/>
</p>

<h1 align="center">🧠 J.A.R.V.I.S. — Just A Rather Very Intelligent System</h1>

<p align="center">
  <b>A next-generation, voice-activated AI assistant powered by cutting-edge Large Language Models, real-time internet intelligence, and autonomous system automation — wrapped in a stunning futuristic holographic GUI.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange?style=for-the-badge&logo=ai&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-PyQt5%20Holographic-blueviolet?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/TTS-Edge%20Neural-green?style=for-the-badge&logo=microsoftedge&logoColor=white" />
  <img src="https://img.shields.io/badge/Image%20Gen-Stable%20Diffusion%20XL-red?style=for-the-badge&logo=stability-ai&logoColor=white" />
  <img src="https://img.shields.io/badge/Search-Real%20Time-gold?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge" />
</p>

---

## 🌟 What Is J.A.R.V.I.S.?

**J.A.R.V.I.S.** isn't just another chatbot — it's a **full-spectrum AI operating system** designed to function as your personal intelligent companion. Inspired by Tony Stark's legendary AI from the Marvel universe, this project brings science fiction to life.

J.A.R.V.I.S. combines the raw reasoning power of **Meta's LLaMA 3.3 70B** (via Groq's lightning-fast inference engine) with **real-time internet awareness**, **autonomous desktop automation**, **AI image generation**, **natural voice interaction**, and a **cinematic holographic interface** — all running locally on your machine.

Whether you're asking complex questions, commanding your computer hands-free, generating artwork, researching live topics, or having a deep philosophical conversation — J.A.R.V.I.S. handles it all effortlessly with **sub-second response latencies** thanks to Groq's industry-leading inference speed.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    J.A.R.V.I.S. CORE ENGINE                    │
├────────────┬────────────┬──────────────┬────────────────────────┤
│  🎙️ Voice   │  🧠 Brain   │  🌐 Search    │  🎨 Creative            │
│  Pipeline  │  Pipeline  │  Pipeline    │  Pipeline              │
├────────────┼────────────┼──────────────┼────────────────────────┤
│ STT Engine │ LLaMA 3.3  │ Google SERP  │ Stable Diffusion XL   │
│ (Google +  │ 70B via    │ Scraping +   │ 1.0 via HuggingFace   │
│  Selenium  │ Groq API   │ AI Synthesis │ Inference API          │
│  WebRTC)   │            │              │                        │
├────────────┼────────────┼──────────────┼────────────────────────┤
│ Edge TTS   │ Mixtral    │ Real-time    │ Async Batch Gen        │
│ Neural     │ 8x7B for   │ Context      │ (4 imgs parallel)      │
│ Synthesis  │ Content    │ Injection    │                        │
├────────────┴────────────┴──────────────┴────────────────────────┤
│              🖥️ FUTURISTIC HOLOGRAPHIC PyQt5 GUI                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Animated Wave BG │ HUD Core │ Neon Rings │ Particle FX  │   │
│  │ Glow Cursor Trail │ Hex Grid │ Bokeh FX  │ Parallax     │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│           ⚙️ AUTOMATION & SYSTEM CONTROL ENGINE                 │
│  App Launch/Kill │ YouTube │ Google │ Volume │ Content Writer   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features & Capabilities

### 🧠 Advanced AI Brain — Multi-Model Intelligence

| Capability | Model | Details |
|:---|:---|:---|
| **Conversational AI** | LLaMA 3.3 70B Versatile | Deep reasoning, contextual awareness, 8192-token context window |
| **Decision Making** | LLaMA 3.3 70B Versatile | Multi-intent query classification with zero-shot routing |
| **Content Generation** | Mixtral 8x7B 32K | Long-form writing, code generation, email drafting |
| **Fallback Intelligence** | LLaMA 3.1 8B Instant | Ultra-fast fallback for high-load scenarios |

J.A.R.V.I.S. uses a sophisticated **First-Layer Decision Making Model (DMM)** that classifies every user query into one or more actionable intents before routing them to the appropriate pipeline. This isn't simple keyword matching — it's an AI model understanding natural language intent at a deep semantic level.

**Multi-intent handling** means you can say: *"Open Chrome, search for quantum computing on Google, play some lo-fi music, and tell me a joke"* — and J.A.R.V.I.S. will parse this into 4 separate commands and execute them all simultaneously using async concurrency.

### 🎙️ Natural Voice Interface — Speak, Don't Type

- **Google Speech Recognition** with ambient noise calibration for crystal-clear voice capture
- **Multi-language input support** — speak in Hindi, Spanish, French, or any language; J.A.R.V.I.S. translates to English in real-time using neural translation
- **Edge TTS Neural Synthesis** — responses are spoken back in a natural, human-like voice (configurable voice personas)
- **Intelligent response truncation** — for long answers, J.A.R.V.I.S. speaks a concise summary and displays the full text on screen
- **Selenium-powered WebRTC STT** — browser-grade speech recognition running headlessly for maximum accuracy
- **Continuous listening mode** — always-on voice detection with automatic silence handling

### 🌐 Real-Time Internet Intelligence

Unlike traditional chatbots trapped in their training data, J.A.R.V.I.S. has **live internet access**:

- **Google SERP scraping** — fetches top 5 real-time search results with titles and descriptions
- **AI-powered synthesis** — doesn't just dump search results; the AI reads, understands, and synthesizes a coherent, professional answer from live data
- **Automatic routing** — the DMM intelligently determines when a query requires real-time data vs. when the AI's built-in knowledge is sufficient
- **Current events awareness** — ask about today's news, stock prices, sports scores, weather, or any live topic
- **Real-time date/time injection** — always knows the current day, date, and time without external API calls

### 🎨 AI Image Generation — Stable Diffusion XL

J.A.R.V.I.S. can create stunning, photorealistic images from natural language descriptions:

- **Stable Diffusion XL 1.0** via HuggingFace Inference API
- **Batch generation** — generates 4 unique variations simultaneously using async parallelism
- **1024×1024 resolution** — high-fidelity outputs with 50-step inference
- **Random seed diversity** — each image uses a unique random seed for maximum creative variation
- **Auto-display** — generated images are automatically opened and displayed
- **Natural language prompts** — just say *"Generate an image of a cyberpunk city at sunset"*

### ⚙️ Desktop Automation Engine — Your Computer, Hands-Free

J.A.R.V.I.S. can take full control of your desktop environment:

| Command | What It Does |
|:---|:---|
| `"Open Chrome"` | Launches any application or website |
| `"Close Notepad"` | Force-terminates any running application |
| `"Play Shape of You"` | Searches and plays any song/video on YouTube |
| `"Google search quantum computing"` | Opens Google with your search query |
| `"YouTube search Python tutorials"` | Opens YouTube with your search query |
| `"Volume up / down / mute"` | Controls system audio levels |
| `"Write an email about project update"` | AI generates content and opens it in your text editor |

**Cross-platform support** — works on **Windows**, **macOS**, and **Linux** with platform-specific command routing.

**Async parallel execution** — multiple automation commands run concurrently using `asyncio.gather()`, meaning *"Open Chrome, play music, and mute the volume"* all execute simultaneously, not sequentially.

### 🖥️ Futuristic Holographic GUI — A Visual Masterpiece

The frontend is a **jaw-dropping, Iron Man–inspired holographic interface** built with PyQt5:

- **🌊 Animated Wave Background** — multi-layered sine waves with purple/blue gradients that react to mouse movement with parallax effects
- **✨ Floating Particle System** — glowing particles drift across the screen with physics-based motion
- **🔮 HUD Core Display** — rotating concentric rings with neon glow effects, reminiscent of the Arc Reactor
- **💫 Glow Cursor Trail** — your mouse leaves a luminous trail with decaying alpha transparency
- **🔷 Hex Grid Overlay** — subtle hexagonal grid pattern adds depth and sci-fi atmosphere
- **🌟 Bokeh Light Effects** — soft, out-of-focus light orbs create cinematic depth-of-field
- **🔄 Rotating Neon Rings** — animated orbital rings with gradient coloring
- **💬 Chat Interface** — real-time message display with smooth scrolling and gradient chat bubbles
- **🎤 Mic Animation** — visual feedback showing listening/processing states
- **🌈 Mode Switching** — dynamic background modes (Idle, Listening, Speaking, Thinking) with distinct visual themes

---

## 📁 Project Structure

```
JARVIS/
├── Main.py                          # 🚀 Core engine — orchestrates all systems
├── Chatbot.py                       # 💬 Standalone chatbot interface
├── Requirements.txt                 # 📦 All dependencies
├── .env                             # 🔑 API keys & configuration (create your own)
│
├── Backend/                         # 🧠 Intelligence & Processing Layer
│   ├── __init__.py                  # Package initialization
│   ├── Model.py                     # 🧩 First-Layer Decision Making Model (DMM)
│   ├── Chatbot.py                   # 🤖 Conversational AI engine (Groq + LLaMA)
│   ├── RealtimeSearchEngine.py      # 🌐 Live internet search + AI synthesis
│   ├── Automation.py                # ⚙️ Desktop automation (apps, browser, system)
│   ├── ImageGeneration.py           # 🎨 AI image generation (Stable Diffusion XL)
│   ├── TextToSpeech.py              # 🔊 Neural TTS (Edge TTS + pygame)
│   └── SpeechToText.py              # 🎙️ Voice recognition (Selenium + WebRTC)
│
├── Frontend/                        # 🖥️ Holographic GUI Layer
│   ├── GUI.py                       # 🎨 853-line PyQt5 futuristic interface
│   ├── Graphics/                    # 🖼️ UI assets (icons, animations, graphics)
│   │   ├── Jarvis.gif               # Animated J.A.R.V.I.S. logo
│   │   ├── Mic_on.png / Mic_off.png # Microphone state indicators
│   │   ├── Home.png                 # Navigation icons
│   │   ├── Chats.png                # Chat panel icon
│   │   └── ...                      # Additional UI assets
│   └── Files/                       # 📂 Runtime state files
│
└── Data/                            # 💾 Runtime Data Store
    ├── ChatLog.json                 # 📝 Persistent conversation history
    ├── Images/                      # 🖼️ AI-generated images storage
    └── speech.mp3                   # 🔊 Current TTS audio file
```

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Chrome browser** installed (for Selenium-based speech recognition)
- **Microphone** access for voice commands
- **Internet connection** for AI inference and real-time search

### 1. Clone the Repository

```bash
git clone https://github.com/Sidhant185/JARVIS.git
cd JARVIS
```

### 2. Create & Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
Username = YourName
AssistantName = Jarvis
GrogAPIKey = your_groq_api_key_here
InputLanguage = en
AssistantVoice = en-CA-LiamNeural
HuggingFaceAPIKey = your_huggingface_api_key_here
```

> **🔑 Getting API Keys:**
> - **Groq API Key**: Sign up free at [console.groq.com](https://console.groq.com) — get blazing-fast LLM inference
> - **HuggingFace API Key**: Sign up free at [huggingface.co](https://huggingface.co/settings/tokens) — for Stable Diffusion XL image generation

### 5. Launch J.A.R.V.I.S.

```bash
python Main.py
```

J.A.R.V.I.S. will initialize all subsystems and begin listening for your voice commands. Speak naturally, and the AI will respond with intelligence and precision.

---

## 🎤 Voice Commands — What You Can Say

### 💬 General Conversation
```
"How are you doing today?"
"Explain quantum computing in simple terms"
"Write me a poem about the ocean"
"What's the meaning of life?"
"Help me debug this Python error"
"Tell me a joke"
```

### 🌐 Real-Time Queries
```
"Who is the current President of the United States?"
"What happened in the news today?"
"Tell me about the latest iPhone release"
"What's the weather like in New York?"
"What are the top trending topics right now?"
```

### 🎨 Image Generation
```
"Generate an image of a futuristic city at night"
"Create an image of a dragon flying over mountains"
"Generate an image of a photorealistic portrait of a robot"
```

### ⚙️ Automation
```
"Open Chrome"
"Open Chrome and Spotify"
"Close Notepad"
"Play Shape of You on YouTube"
"Search for machine learning tutorials on Google"
"Volume up"
"Mute the system"
"Write an application letter for a software engineer position"
```

### 🧠 Multi-Intent Commands
```
"Open Chrome, search for AI news on Google, and play some music"
"Tell me a joke and open Spotify"
"What time is it and remind me about the meeting"
```

---

## 🔧 Configuration & Customization

### Voice Personas

Change the AI's voice by modifying `AssistantVoice` in `.env`:

| Voice Code | Description |
|:---|:---|
| `en-CA-LiamNeural` | Canadian English (Male, Deep) |
| `en-US-AriaNeural` | American English (Female, Warm) |
| `en-US-GuyNeural` | American English (Male, Professional) |
| `en-GB-SoniaNeural` | British English (Female, Elegant) |
| `en-IN-NeerjaNeural` | Indian English (Female, Clear) |
| `en-AU-NatashaNeural` | Australian English (Female, Friendly) |

### Input Language Support

Set `InputLanguage` in `.env` to accept voice input in different languages:

| Code | Language |
|:---|:---|
| `en` | English |
| `hi` | Hindi |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `ja` | Japanese |
| `ko` | Korean |
| `zh` | Chinese |

J.A.R.V.I.S. will automatically translate non-English input to English before processing.

---

## 🛡️ Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **LLM Inference** | Groq Cloud | Ultra-fast inference (~10x faster than OpenAI) |
| **Primary Model** | LLaMA 3.3 70B Versatile | Reasoning, classification, conversation |
| **Content Model** | Mixtral 8x7B 32K | Long-form content generation |
| **Fallback Model** | LLaMA 3.1 8B Instant | High-speed fallback |
| **Image Generation** | Stable Diffusion XL 1.0 | Text-to-image synthesis |
| **Voice Recognition** | Google Speech Recognition | Real-time voice-to-text |
| **Text-to-Speech** | Microsoft Edge TTS | Neural voice synthesis |
| **Audio Playback** | pygame | Cross-platform audio |
| **Web Automation** | Selenium + ChromeDriver | Headless browser control |
| **Search Engine** | googlesearch-python | Live Google SERP scraping |
| **Translation** | mtranslate | Multi-language translation |
| **GUI Framework** | PyQt5 | Desktop application interface |
| **Image Processing** | Pillow (PIL) | Image handling and display |
| **HTTP Client** | aiohttp + requests | Async and sync networking |
| **Environment** | python-dotenv | Secure configuration management |

---

## 🧪 Module Testing

Each backend module can be tested independently:

```bash
# Test the Decision Making Model
python -m Backend.Model

# Test the Chatbot
python -m Backend.Chatbot

# Test Real-Time Search
python -m Backend.RealtimeSearchEngine

# Test Automation
python -m Backend.Automation

# Test Image Generation
python -m Backend.ImageGeneration

# Test Text-to-Speech
python -m Backend.TextToSpeech

# Test Speech-to-Text
python -m Backend.SpeechToText
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Ideas for Contributions
- 🔌 Plugin system for extending capabilities
- 📱 Mobile companion app (React Native)
- 🏠 Smart home integration (HomeKit / Home Assistant)
- 📊 Dashboard for analytics and usage stats
- 🔐 Wake word detection ("Hey Jarvis")
- 🎵 Spotify API integration for music control
- 📧 Email reading and drafting via Gmail API
- 🗓️ Calendar integration with Google Calendar

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Sidhant Pande**

- GitHub: [@Sidhant185](https://github.com/Sidhant185)

---

<p align="center">
  <b>⭐ If you found this project impressive, please give it a star! ⭐</b>
</p>

<p align="center">
  <i>"Sometimes you gotta run before you can walk."</i> — Tony Stark
</p>
