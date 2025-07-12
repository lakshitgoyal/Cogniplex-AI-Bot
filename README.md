<div align="center">
  <h1>Cogniplex</h1>
  <p>
    An advanced, multimodal AI chatbot powered by Google's Gemini API.
  </p>
</div>

---

**Cogniplex** is a sophisticated, proof-of-concept AI application that leverages the power of Large Language Models to create a versatile and intelligent conversational agent. It goes beyond simple chat by integrating Retrieval-Augmented Generation (RAG) for document analysis, multimodal understanding for images, and a clean, responsive web interface.

## ✨ Features

*   **💬 Conversational AI:** Engages in natural, context-aware conversations using the `gemini-1.5-pro` model.
*   **🧠 Document Knowledge (RAG):** Upload PDF documents and ask specific questions about their content. The AI is "grounded" by the information in your documents for accurate, fact-based answers.
*   **👁️ Multimodal Analysis:** Upload an image and ask questions about it (e.g., "What is happening in this picture?").
*   **🚀 Fast & Modern Backend:** Built with **FastAPI** for high-performance, asynchronous request handling.
*   **💻 Interactive Frontend:** A clean, user-friendly interface built with vanilla HTML, CSS, and JavaScript. No frontend frameworks needed.
*   **🔒 Secure:** API keys are handled securely on the backend and are not exposed to the client.

## 🛠️ Tech Stack

| Component         | Technology                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| **Backend**       | [**FastAPI**](https://fastapi.tiangolo.com/), [**Uvicorn**](https://www.uvicorn.org/)                           |
| **AI Model**      | [**Google Gemini API**](https://ai.google.dev/) (`gemini-1.5-pro-latest`, `text-embedding-004`) |
| **RAG Framework** | [**LangChain**](https://www.langchain.com/) for document loading, splitting, and retrieval.                       |
| **Vector Store**  | [**ChromaDB**](https://www.trychroma.com/) for efficient, local vector storage and similarity search.            |
| **Frontend**      | **HTML5**, **CSS3**, **JavaScript (ES6+)**                                                                   |
| **Deployment**    | Container-ready (Dockerfile can be added).                                                                   |

## 🚀 Getting Started

Follow these steps to set up and run the Cogniplex project on your local machine.

### 1. Prerequisites

*   **Python 3.9+**
*   **Git** for cloning the repository.
*   A **Google Gemini API Key**. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

Open your terminal and clone the project:

```bash
git clone https://github.com/lakshitgoyal/Cogniplex-AI-Bot
cd Cogniplex
```
### 3. Set Up the Python Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
### 4. Install Dependencies
Install all the required Python packages using the requirements.txt file.
```bash
pip install -r requirements.txt
```
### 5. Configure Your API Key
The application loads your API key from an environment file for security.
Find the file named .env.example in the root directory.
Rename it to .env.
Open the new .env file and replace YOUR_GEMINI_API_KEY_HERE with your actual Gemini API key.

### 6. Run the Application
You are now ready to start the backend server!
```bash
uvicorn backend.main:app --reload
```
### 7. Open the Frontend
Open your favorite web browser and navigate to:
```bash
http://127.0.0.1:8000
```
You should now see the Cogniplex user interface, ready for you to chat, upload documents, and analyze images!
<div align="center">
Made with ❤️ and a lot of vectors.
</div>
