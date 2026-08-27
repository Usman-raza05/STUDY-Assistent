# STUDY Assistant

A modern AI-powered PDF study assistant built with **Python, Flask, and Groq AI**.

## 🌐 Live Demo

🚀 **Try the application here:**

👉 [STUDY Assistant Live Demo](https://study-assistent-m336.onrender.com/)

---

## ✨ Features

### 📄 PDF Upload

Upload PDF study materials directly from the website.

* PDF files only
* Maximum file size: **15 MB**
* Text extraction from standard PDFs
* Image-based PDF support for scanned documents

### 📝 AI Summary

Generate a clear, detailed, and structured summary of your document in simple English.

### 🧠 AI Quiz Generator

Automatically generate **5 multiple-choice questions** from your study material.

Each question includes:

* Question
* Options A–D
* Correct Answer
* Short Explanation

### 💬 Ask Questions

Ask questions directly about the uploaded PDF and get AI-generated answers based on the document content.

### 👁️ Scanned PDF Support

If a PDF does not contain extractable text, the application converts up to the first five pages into images and sends them to a vision-capable AI model.

### 🎨 Modern Premium UI

A clean and responsive dark interface designed for a modern study experience.

---

## 🛠️ Technologies Used

* Python
* Flask
* Groq API
* PyMuPDF
* HTML
* CSS
* JavaScript
* Marked.js

---

## 📂 Project Structure

```text
STUDY-Assistent/
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Usman-raza05/STUDY-Assistent.git
```

### 2. Navigate to the Project Folder

```bash
cd STUDY-Assistent
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

The application requires a Groq API key.

### PowerShell

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

### Windows Command Prompt

```cmd
set GROQ_API_KEY=your_groq_api_key
```

> Never upload your API key or `.env` file to GitHub.

---

## ▶️ Run Locally

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 📦 Requirements

Your `requirements.txt` should contain:

```text
Flask
groq
PyMuPDF
gunicorn
```

---

## 🌐 API Routes

### Home Page

```text
GET /
```

Loads the main STUDY Assistant interface.

### Process PDF

```text
POST /process-pdf
```

Processes the uploaded PDF and performs:

* `summary`
* `quiz`
* `question`

---

## 🤖 AI Model Selection

The application automatically checks the available Groq models and selects a compatible model.

### Text Models

* `openai/gpt-oss-20b`
* `llama-3.3-70b-versatile`
* `llama-3.1-8b-instant`
* `qwen/qwen3-32b`

### Vision Models

For scanned or image-based PDFs:

* `meta-llama/llama-4-scout-17b-16e-instruct`
* `meta-llama/llama-4-maverick-17b-128e-instruct`

---

## 🚀 Deployment

This project is deployed using **Render**.

### Render Configuration

| Setting       | Value                             |
| ------------- | --------------------------------- |
| Language      | Python                            |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app`                |

### Environment Variable

```text
GROQ_API_KEY=your_groq_api_key
```

### 🌍 Live Application

👉 **[Open STUDY Assistant](https://study-assistent-m336.onrender.com/)**

---

## 🔒 Security

Your `.gitignore` should include:

```gitignore
__pycache__/
*.py[cod]
.env
venv/
.venv/
```

---

## 📝 How It Works

```text
Upload PDF
    ↓
Flask Backend
    ↓
Extract PDF Text
    ↓
Text Available?
   /             \
 Yes             No
  ↓               ↓
Send Text      Convert Pages
to Groq AI      to Images
   \             /
    ↓           ↓
      AI Processing
           ↓
 Summary / Quiz / Answer
           ↓
    Display Result
```

---

## ⚠️ Limitations

* Only PDF files are supported.
* Maximum upload size is **15 MB**.
* Large PDFs are truncated before being sent to the AI.
* AI responses depend on Groq model availability.
* Scanned PDF processing depends on vision model availability.

---

## 👨‍💻 Author

**Usman Raza**

---

### ⭐ Support

If you like this project, consider giving the repository a **star** on GitHub!
