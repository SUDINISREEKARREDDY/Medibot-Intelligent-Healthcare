from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
#from llama_cpp import Llama
from src.prompt import *
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)
load_dotenv()

# =========================
# Pinecone
# =========================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medic"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# =========================
# CPU-ONLY LLM (GGUF)
# =========================
# !pip install llama-cpp-python

# llm = Llama.from_pretrained(
# 	repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
# 	filename="mistral-7b-instruct-v0.2.Q5_K_M.gguf",
#     n_ctx=4096,
#     temperature = 0.1,
#     top_p = 0.9,
#     top_k = 40,
#     repeat_penalty = 1.15,
#     stop=["</s>", "User:", "Assistant:"]
# )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# New RAG chain using Runnable interfaces (LangChain v1+)
def get_context(input):
    docs = retriever.invoke(input)
    context = format_docs(docs)
    print("Retrieved context from Pinecone:\n", context)
    return {"context": context, "input": input}

rag_chain = get_context


def run_rag_chain(input):
    context_dict = rag_chain(input)
    prompt_str = system_prompt.format(context=context_dict['context'], input=context_dict['input'])
    print("Prompt sent to LLM:\n", prompt_str)  # Debug print
    response = llm(prompt_str, max_tokens=140)
    # Extract only the generated text from the Llama response
    if isinstance(response, dict) and "choices" in response:
        answer = response["choices"][0]["text"].strip()
    else:
        answer = str(response)
    # Post-process: if user said thank you/thanks, return only 'you're welcome.'
    if input.strip().lower() in ["thank you", "thanks", "thankyou"]:
        return "you're welcome."
    return answer

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = run_rag_chain(input)
    print("Response : ", response)
    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
