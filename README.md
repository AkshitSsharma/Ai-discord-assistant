# 🤖 AI-Powered Discord Assistant (RAG + Voice + Image)

## 🚀 Overview

This project is an intelligent **Discord AI assistant** that integrates Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), voice processing, and image generation.

The bot can **chat, remember conversations, search the web, generate images, and understand voice inputs**, making it a fully functional multimodal AI system.

---

## 🔥 Features

### 💬 Chat with Context (RAG)

* Maintains conversation history per user
* Uses **ChromaDB** for long-term memory
* Retrieves relevant past interactions for better responses

---

### 🌐 Real-Time Web Search

* Integrated with **Tavily API**
* Automatically fetches latest information for queries like:

  * "latest news"
  * "current price"
  * "today updates"

---

### 🎤 Voice Input → AI Response

* Accepts audio files (`.mp3`, `.wav`, `.ogg`)
* Converts speech to text using **OpenAI Whisper**
* Processes it through AI and returns intelligent responses

---

### 🖼️ Text → Image Generation

* Generate images using prompts like:

  * "generate image of a futuristic city"
  * "draw a cyberpunk robot"
* Powered by **OpenAI Image API**

---

### 🧠 Smart Memory System

* Stores user conversations in vector database
* Retrieves relevant context using similarity search
* Improves response quality over time

---

## 🧠 Tech Stack

* **Python**
* **Discord.py**
* **LangChain**
* **Groq (LLaMA 3 - 70B)**
* **OpenAI API (Whisper + Image Generation)**
* **ChromaDB (Vector Database)**
* **Tavily API (Web Search)**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/AkshitSsharma/Ai-discord-assistant.git
cd Ai-discord-assistant
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` file

```env
DISCORD_API_KEY=your_discord_token
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

### 4️⃣ Run the bot

```bash
python bot.py
```

---

## 🧪 Example Usage

### 💬 Chat

```
What is machine learning?
```

### 🌐 Search

```
latest AI news
```

### 🖼️ Image Generation

```
generate image of a futuristic city
```

### 🎤 Voice Input

* Upload audio file → bot transcribes + responds

---

## 📌 Future Improvements

* 🔊 Text-to-Speech (AI voice reply)
* 🎧 Discord voice channel integration
* 🧠 Advanced RAG (reranking + hybrid search)
* ⚡ Streaming responses

---

## 👨‍💻 Author

**Akshit Sharma**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
