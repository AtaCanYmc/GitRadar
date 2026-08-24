# 🚀 GitRadar Web Demo (Vercel Ready)

This directory contains the ready-to-deploy web demo for **GitRadar**, an AI-driven GitHub Market & Gap Analysis engine.

Anyone can deploy this demo to Vercel in 1 click and analyze developer tool ideas in their browser using their own **Groq API Key** and **GitHub Access Token**!

---

## ⚡ 1-Click Vercel Deployment

Deploy directly to your Vercel account:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAtaCanYmc%2FGitRadar&root-directory=demo)

---

## 🔐 How User API Keys Work

In this web demo, **no API keys are hardcoded or shared on the server**.

1. Users click the **Settings Modal** (⚙️ icon in the top navigation bar).
2. Users enter their own **Groq API Key** (`gsk_...`) and optional **GitHub Access Token** (`ghp_...`).
3. Keys are stored locally in the browser (`localStorage`) and passed via secure HTTPS headers (`X-Groq-Api-Key`, `X-Github-Token`) to Vercel serverless Python functions per request.

---

## 📁 Directory Structure

```
demo/
├── api/
│   └── index.py            # Vercel Serverless Function entrypoint (Flask WSGI)
├── public/                 # Static web dashboard assets
│   ├── css/style.css
│   ├── js/app.js
│   └── index.html
├── requirements.txt        # Python dependencies for Vercel Python runtime
└── vercel.json             # Vercel routing configuration
```

---

## 🛠 Local Testing with Vercel CLI

To run the demo locally using the Vercel CLI:

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Run local serverless dev environment
cd demo
vercel dev
```

Open `http://localhost:3000` in your browser.
