import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from groq import Groq
import pymupdf

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024  # 15 MB limit

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key) if api_key else None

def get_available_model(client, vision=False):
    model_ids = {model.id for model in client.models.list().data}
    if vision:
        preferred_models = [
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
        ]
    else:
        preferred_models = [
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "qwen/qwen3-32b",
        ]
    return next((model for model in preferred_models if model in model_ids), None)

def extract_text_from_pdf(pdf_file):
    pdf_bytes = pdf_file.read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc).strip()
    page_images = []
    
    if not text:
        for page in doc[:5]:
            pixmap = page.get_pixmap(dpi=120, alpha=False)
            encoded = base64.b64encode(pixmap.tobytes("jpeg")).decode("ascii")
            page_images.append(f"data:image/jpeg;base64,{encoded}")
            
    return text, page_images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded.'}), 400

        file = request.files['pdf']
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please select a valid PDF file.'}), 400

        action_type = request.form.get('action')
        user_question = request.form.get('question', '')

        if action_type not in {'summary', 'quiz', 'question'}:
            return jsonify({'error': 'Invalid action selected.'}), 400
        if action_type == 'question' and not user_question.strip():
            return jsonify({'error': 'Please enter a question.'}), 400

        client = get_groq_client()
        if client is None:
            return jsonify({'error': 'GROQ_API_KEY is not configured. Set it in the same PowerShell terminal that runs this app.'}), 503

        pdf_text, page_images = extract_text_from_pdf(file)
        if not pdf_text and not page_images:
            return jsonify({'error': 'The PDF contains no readable pages.'}), 422

        truncated_text = pdf_text[:5000]

        if action_type == 'summary':
            prompt = f"Provide a clear, detailed, and structured summary of the following document content in simple English:\n\n{truncated_text}"
        elif action_type == 'quiz':
            prompt = f"Create 5 multiple-choice questions from this content in clear English. For every question include: Question, Options A-D, Correct Answer, and a one-sentence Explanation. Always show the correct answer clearly.\n\n{truncated_text}"
        else:
            prompt = f"Answer this question directly based on the provided text:\nQuestion: '{user_question}'\n\nDocument Text:\n{truncated_text}"

        model_name = get_available_model(client, vision=bool(page_images))
        if model_name is None:
            return jsonify({'error': 'Your Groq account has no compatible model enabled for this request.'}), 503

        if page_images:
            message_content = [{'type': 'text', 'text': prompt}]
            message_content.extend(
                {'type': 'image_url', 'image_url': {'url': image}}
                for image in page_images
            )
        else:
            message_content = prompt

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
            model=model_name,
        )

        result_text = chat_completion.choices[0].message.content
        return jsonify({'result': result_text})

    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({'error': f"AI request failed: {str(e)}"}), 502

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True, port=port)