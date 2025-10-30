# 🧠 Resume Generator MCP Server  
**Generate Ready-to-Send, ATS-Friendly Resumes Instantly**

![GitHub stars](https://img.shields.io/github/stars/1abhi6/Resume-Generator-MCP-Server?style=social)
![GitHub forks](https://img.shields.io/github/forks/1abhi6/Resume-Generator-MCP-Server?style=social)
![GitHub license](https://img.shields.io/github/license/1abhi6/Resume-Generator-MCP-Server)
![GitHub issues](https://img.shields.io/github/issues/1abhi6/Resume-Generator-MCP-Server)
![GitHub pull requests](https://img.shields.io/github/issues-pr/1abhi6/Resume-Generator-MCP-Server)

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [MCP Tools Overview](#-mcp-tools-overview)
- [Security & Data Handling](#-security--data-handling)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Support](#-support)
- [Credits](#-credits)

---

## 💡 About the Project

**Resume Generator MCP Server** is a powerful, AI-driven backend server that automatically generates **ATS-friendly, professional resumes** from any input — whether it’s a text, file, or LinkedIn profile.

It uses **FastMCP** for the Model Context Protocol layer and integrates **OpenAI**, **Meta LLama**, **LangChain**, and other cloud tools to produce high-quality Word and PDF resumes — instantly uploaded to AWS with secure download links.

---

## ✨ Features

- 🧾 Generate resumes from **raw text, existing resume, or LinkedIn profile**  
- 📄 **Enhance and tailor** resumes for specific job descriptions  
- 🧠 Uses **LLM intelligence** (OpenAI + LLama) for resume optimization  
- ☁️ **Cloud-powered** (AWS S3, Textract, CloudConvert, Neon DB)  
- 🔒 Secure resume storage (auto-deletes after 7 days)  
- 🔁 Supports **multiple templates** dynamically rendered via `docxtpl + Jinja2`  
- ⚙️ Modular, scalable, and fully documented MCP server  
- 🌐 **Deployed with CI/CD** via GitHub Actions on Render & Vercel  

---

## 🧱 Architecture Overview

> **(Add your architecture diagram here)**  
> *(A placeholder is left for the diagram you will add later)*

**High-Level Flow:**
1. Choose a predefined resume template  
2. Provide your input (LinkedIn URL, text, or file)  
3. AI extracts, structures, and enhances your information  
4. MCP Server generates Word + PDF resumes  
5. You instantly receive secure download links  

---

## 🧰 Tech Stack

**Core Technologies**
- FastMCP  
- Python (LangChain, docxtpl, Jinja2)  
- AWS (S3, Textract, IAM)  
- PostgreSQL (Neon)  
- CloudConvert, ScrapingDog APIs  
- OpenAI + Meta LLama  
- ReactJS (Documentation & Demo UI)  
- Alembic (DB Migration)  
- Stytch Authentication  
- CI/CD with GitHub Actions + Render Deployment  

---

## ⚙️ Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10+  
- PostgreSQL (Neon DB connection string)  
- AWS Account with S3, IAM, and Textract access  
- CloudConvert & ScrapingDog API keys  
- Stytch Authentication credentials  
- OpenAI and Meta API keys  

### Steps

```bash
# Clone the repo
git clone https://github.com/1abhi6/Resume-Generator-MCP-Server.git

# Navigate to project directory
cd Resume-Generator-MCP-Server

# uv setup
uv init
uv venv
.venv/Scripts/activate

# Install dependencies
uv sync

# Set environment variables
cp .env.example .env
# Update .env with your credentials

# Run the MCP Server
uv run main.py
```
We recommend using [ngrok](https://ngrok.com/)

---

## 🚀 Usage Guide

Once the server is running locally or deployed:

1. Choose an input mode:
   - Raw text  
   - Resume file (PDF/DOCX/Image)  
   - LinkedIn profile URL  

2. Call the corresponding API endpoint or MCP client tool.

3. Receive instant Word & PDF download links.

Example API usage:
```bash
POST /generate-resume
{
  "input": "I am a software engineer with 5 years of experience in Python and AI..."
}
```

Response:
```json
{
  "pdf_link": "https://s3.amazonaws.com/xyz/resume.pdf",
  "docx_link": "https://s3.amazonaws.com/xyz/resume.docx"
}
```

---

## 🧩 MCP Tools Overview

**Primary Tools**
1. `Generate Resume from Raw Text`
2. `Enhance Existing Resume`
3. `Generate Resume based on Job Description`
4. `Generate Resume from LinkedIn Profile`

**Utility Tools**
- `Check Server Health`
- `Upload Resume File`
- `Check Uploaded File`

Each tool returns **Word + PDF** download links of the generated resume.

---

## 🔒 Security & Data Handling

- All resumes are stored in **AWS S3** for **7 days only** (auto-expiry).  
- Input/output guardrails prevent processing of harmful or sensitive data.  
- OAuth implemented via **Stytch Authentication**.  
- Secure role-based IAM policies for AWS resources.  

---

## 🧭 Roadmap

- [ ] Add more customizable templates  
- [ ] Introduce multi-language support  
- [ ] Add analytics dashboard for resume performance  
- [ ] Enable user accounts with history tracking  
- [ ] Integrate with more LLM providers  

---

## 🤝 Contributing

Contributions are welcome!  
Please follow these steps:

1. **Fork** the repository  
2. **Create** your feature branch (`git checkout -b feature/amazing-feature`)  
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)  
4. **Push** to the branch (`git push origin feature/amazing-feature`)  
5. **Open a Pull Request**

Ensure your code follows proper linting and modular design.

---

## 🪪 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🧑‍💻 Support

For support, questions, or feedback:
- Open an issue on GitHub  
- [Email](mailto:abhishekguptacode@gmail.com)
- Follow updates: [LinkedIn](https://linkedin.com/in/iautomates)

---

## 🙏 Credits

Special thanks to:
- **OpenAI & Meta** for LLMs  
- **AWS**, **Stytch**, and **Neon** for cloud infrastructure  
- **FastMCP** for protocol design  
- All open-source contributors helping make this project better!

---

⭐ **If you like this project, give it a star! It helps others find it and motivates future development.**