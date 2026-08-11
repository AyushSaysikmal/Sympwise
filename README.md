# 🩺 SympWise – AI-Powered Medical LLM Advisor

SympWise is an AI-powered medical advisory web application that analyzes **user-provided symptoms and medical images** to provide preliminary health insights. It uses **multimodal AI capabilities through the Groq API** to process text and image-based inputs and generate easy-to-understand health information.

> ⚠️ **Disclaimer:** SympWise is an educational and informational project. It is not intended to replace professional medical diagnosis, treatment, or consultation.

---

## 🚀 Features

* 🔐 **User Authentication**

  * User registration and login
  * Secure session management

* 📝 **Symptom Analysis**

  * Enter symptoms using natural language
  * AI analyzes the provided symptoms
  * Generates preliminary health insights

* 🖼️ **Medical Image Analysis**

  * Upload medical-related images
  * Analyze image and symptom information together

* 🤖 **AI-Powered Analysis**

  * Uses Groq API for fast AI inference
  * Generates possible health conditions and explanations

* 📋 **Health Report Generation**

  * Generates a structured health analysis report
  * Download the generated report for personal reference

* 🔒 **Secure API Configuration**

  * API keys are stored using environment variables
  * `.env` and virtual environment files are excluded from GitHub

* 🌐 **Web-Based Application**

  * Simple and user-friendly interface
  * Accessible through a web browser

---

## 🧠 How It Works

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                  Symptoms / Medical Image
                             │
                             ▼
                    ┌─────────────────┐
                    │    SympWise     │
                    │  Web Application│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Groq API     │
                    │ Multimodal AI   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  AI Analysis    │
                    │ & Health Insights│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Health Report  │
                    └─────────────────┘
```

---

## 🛠️ Technology Stack

| Category                   | Technologies                          |
| -------------------------- | ------------------------------------- |
| **Programming Language**   | Python                                |
| **Backend**                | Django                                |
| **Frontend**               | HTML, CSS, JavaScript                 |
| **AI**                     | Groq API, Multimodal LLM              |
| **Database**               | SQLite / Django Database              |
| **Report Generation**      | ReportLab                             |
| **Environment Management** | Python dotenv / Environment Variables |
| **Version Control**        | Git, GitHub                           |

---

## 📂 Project Structure

```text
Sympwise Project/
│
├── doctorAppointmentProjct/
│   ├── manage.py
│   │
│   ├── doctorAppointmentProjct/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── ...
│   │
│   ├── templates/
│   ├── static/
│   └── ...
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AyushSaysikmal/Sympwise.git
```

Navigate to the project:

```bash
cd Sympwise
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv env
```

Activate the environment:

```bash
env\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv env
```

Activate:

```bash
source env/bin/activate
```

---

### 3. Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The application should read the API key from the environment instead of storing it directly in the source code.

Example:

```python
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

### 🔒 Important

Never commit your `.env` file or API keys to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
env/
__pycache__/
*.pyc
```

---

## ▶️ Running the Application

Navigate to the Django project directory:

```bash
cd doctorAppointmentProjct
```

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

## 📊 Application Workflow

1. 👤 Register or log in to the application.
2. 📝 Enter your symptoms.
3. 🖼️ Upload a medical image if required.
4. 🚀 Submit the information for analysis.
5. 🤖 SympWise sends the input to the AI service.
6. 🧠 The multimodal AI processes the provided information.
7. 📋 The application displays preliminary health insights.
8. 📄 Generate and download the health report.

---

## 🎯 Project Objectives

The main objectives of SympWise are:

* To demonstrate the application of **Generative AI in healthcare**.
* To analyze both **text-based symptoms and medical images**.
* To provide preliminary and understandable health information.
* To integrate an AI API with a web-based application.
* To generate structured health reports using AI-generated analysis.
* To demonstrate the use of **multimodal AI technology** in a practical application.

---

## 🔐 Security

SympWise follows basic security practices:

* API keys are stored using environment variables.
* `.env` is excluded from version control.
* Python virtual environments are excluded from Git.
* Sensitive credentials are not hard-coded into source files.

---

## 🔮 Future Enhancements

* 👨‍⚕️ Doctor consultation integration
* 📅 Appointment scheduling
* 📊 Personalized health dashboard
* 🧾 Improved medical report generation
* 🌐 Multilingual support
* ☁️ Cloud deployment
* 🔐 Advanced data encryption
* 🧠 Support for additional AI models
* 🩻 Improved medical image analysis
* 📚 Medical history tracking

---

## ⚠️ Disclaimer

SympWise is developed for **educational and research purposes**.

The information generated by this application should not be considered a medical diagnosis or a substitute for professional medical advice. Users should consult a qualified healthcare professional for diagnosis, treatment, and medical decisions.

---

## 👨‍💻 Author

### Ayush Saysikmal

**B.Tech – Artificial Intelligence & Data Science**

GitHub: [@AyushSaysikmal](https://github.com/AyushSaysikmal)

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
