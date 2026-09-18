from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaLLM
from src.prompt import system_prompt
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# =========================
# Pinecone
# =========================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing from .env")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

print("Loading Hugging Face embeddings...")
embeddings = download_hugging_face_embeddings()

index_name = "medic"

print(f"Connecting to Pinecone index: {index_name}")

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

print("Pinecone connected successfully.")


# =========================
# Local LLM - Ollama
# =========================
print("Connecting to Ollama...")

llm = OllamaLLM(
    model="llama3.2:3b",
    temperature=0.1
)

print("Ollama connected successfully.")


# =========================
# RAG
# =========================
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_context(user_input):
    docs = retriever.invoke(user_input)

    context = format_docs(docs)

    print("\nRetrieved context from Pinecone:")
    print(context)

    return {
        "context": context,
        "input": user_input
    }


def run_rag_chain(user_input):

    # Handle simple thank-you messages before calling the LLM
    if user_input.strip().lower() in ["thank you", "thanks", "thankyou"]:
        return "you're welcome."

    context_dict = get_context(user_input)

    prompt_str = system_prompt.format(
        context=context_dict["context"],
        input=context_dict["input"]
    )

    print("\nPrompt sent to Ollama:")
    print(prompt_str)

    response = llm.invoke(prompt_str)

    answer = str(response).strip()

    return answer


# =========================
# Flask Routes
# =========================
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():

    msg = request.form["msg"]

    print("\nUser:", msg)

    response = run_rag_chain(msg)

    print("Response:", response)

    return str(response)


# =========================
# Start Flask
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )