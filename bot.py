from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

import discord
from openai import OpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from tavily import TavilyClient


client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    collection_name="discord_memory",
    embedding_function=embeddings,
    persist_directory="./memory_db"
)

conversation_history = {}


model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def generate_image(prompt):
    result = client_openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    import base64
    return base64.b64decode(result.data[0].b64_json)


async def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client_openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    user_name = str(message.author.name)

    # Audio pipeline
    if message.attachments:
        attachment = message.attachments[0]

        if attachment.filename.endswith((".mp3", ".wav", ".ogg")):
            file_path = "audio_input.wav"
            await attachment.save(file_path)

            async with message.channel.typing():
                try:
                    # Step 1: Transcribe
                    text = await transcribe_audio(file_path)

                    await message.channel.send(f"🗣️ You said: {text}")

                    # Step 2: Treat as normal input
                    user_input = text

                except Exception as e:
                    await message.channel.send(f"⚠️ Audio failed: {str(e)}")
                    return
        else:
            return
    else:
        user_input = message.content.strip()

    # IMAGE DETECTION

    image_keywords = ["generate image", "create image", "draw", "image of", "!image"]

    if any(word in user_input.lower() for word in image_keywords):

        prompt = user_input.lower()
        for word in image_keywords:
            prompt = prompt.replace(word, "")
        prompt = prompt.strip()

        if not prompt:
            await message.channel.send("⚠️ Please provide a prompt.")
            return

        async with message.channel.typing():
            try:
                image_bytes = generate_image(prompt)

                with open("generated.png", "wb") as f:
                    f.write(image_bytes)

                await message.channel.send(file=discord.File("generated.png"))

            except Exception as e:
                await message.channel.send(f"⚠️ Image failed: {str(e)}")

        return


    if user_id not in conversation_history:
        conversation_history[user_id] = [
            SystemMessage(content="You are a helpful AI assistant.")
        ]

    async with message.channel.typing():

        # SEARCH LOGIC
        search_keywords = ["latest", "news", "today", "current", "price", "weather", "who won"]

        if any(word in user_input.lower() for word in search_keywords):
            try:
                search_result = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: tavily_client.search(query=user_input)
                )

                conversation_history[user_id].append(
                    SystemMessage(content=f"Web results:\n{str(search_result)}")
                )
            except:
                pass

        # CHAT

        conversation_history[user_id].append(HumanMessage(content=user_input))

        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: model.invoke(conversation_history[user_id])
        )

        reply = response.content

        conversation_history[user_id].append(AIMessage(content=reply))
        conversation_history[user_id] = conversation_history[user_id][-10:]

        # STORE MEMORY

        vectorstore.add_texts(
            texts=[f"User: {user_input} | Bot: {reply}"],
            metadatas=[{"user_id": user_id, "user_name": user_name}]
        )

        await message.channel.send(reply)



client.run(os.getenv("DISCORD_API_KEY"))