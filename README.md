# 🧠 LLM Arena — AI Model Comparator

LLM Arena is a web-based Django app that allows users to compare the responses of top AI models like GPT-4o, Gemini 2.5, Mistral 12B, and LLaMA 3 to the same user query — and then intelligently score and evaluate them for clarity, accuracy, relevance, and depth.

---

## 🚀 Features

- 🔐 User login/signup system with per-user dashboard
- 💬 Compare responses from multiple LLMs
- 📊 Gemini evaluates and scores all model responses
- 🗂️ Users can view all their past queries and responses
- 📈 Admin-only analytics dashboard
  - Query trends
  - Model popularity
  - User-wise usage
- ✨ 2x2 layout with copy buttons and "Show More" toggles
- ⏳ Query limit per user (10 per 12 hrs)
- 📂 Responses stored with timestamps



## ⚙️ Tech Stack

- 🐍 Python 3
- 🌐 Django 5.x
- 🧠 OpenAI, Gemini, Mistral, Groq (LLaMA)
- 🗃️ SQLite (can be switched to PostgreSQL easily)
- 📊 Chart.js for visual analytics
- 🎨 Custom CSS styling (no Bootstrap)

---

## 🛠️ How to Run Locally

1. Clone the repo:

2. Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Add your API keys to a .env file:

OPENAI_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
GROQ_API_KEY=...
CO_API_KEY=...


5. Run migrations:

python manage.py migrate


6. Run the app:

python manage.py runserver


## ✨ Planned Features:
1.💾 Export query results to PDF
2.🧠 Model-wise comparison graphs
3.🌍 Deployment on Render/EC2
4.🌓 Dark mode toggle
5.🔄 Editable query re-run


## 🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change or add.

## 📜 License
MIT License — use it freely, modify it, give credit when you can :)

## 🙌 Author
Made with ❤️ by Aaryan Kale







