# OpenAI Remote Query

A Python-based system that lets you send a prompt to your personal AI assistant — via email — and receive a response powered by the OpenAI API. The backend runs locally on your machine, giving you full control over how and when prompts are processed.

---

## 🎯 Purpose

This project was created to bypass the usage limits of the ChatGPT (o3) app by leveraging the OpenAI API directly. It enables:

- Unlimited custom prompts (within API credit limits)
- Full control over model parameters and tokens
- Remote access — send a query from your phone, get a reply back

## 🛠️ How It Works

1. You send an email with a prompt (e.g., "GPT-Query: Explain bond convexity").
2. Your local machine checks for new requests every 5 minutes.
3. The script parses the prompt and calls the OpenAI API.
4. The response is emailed back to you.

## 📦 Tech Stack

- Python 3.x
- OpenAI API
- IMAP & SMTP (email integration)
- `.env` for credentials and configuration
- Git for version control

## 🚀 Status

- ✅ Project initialized and connected to GitHub
- ⚙️ Implementation in progress (email handler, API processor)
- 🔁 Next steps: email automation, error handling, deployment

## 💡 Future Features

- Authentication filters (specific senders only)
- Multi-model support (GPT-4, GPT-3.5)
- File attachment parsing (e.g., summarize PDFs)
- Scheduled or recurring prompts

## 🔐 Security Note

Your API key and email credentials should be stored in a `.env` file (included in `.gitignore`) and never pushed to GitHub.

## 📄 License

MIT License (to be added).
