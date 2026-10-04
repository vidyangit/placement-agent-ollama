# Local Placement Support Agent with Ollama

This project demonstrates a complete local LLM agent:

User
-> Instruction-following prompt
-> Local LLM through Ollama
-> Function/tool calling
-> Python business tools
-> Tool results
-> LLM answer
-> Reflection
-> Final answer

No OpenAI/Gemini API key is required.

## 1. Install Ollama

Install Ollama from the official Ollama website:

https://ollama.com/

After installation, open a new terminal.

## 2. Download a model

Recommended starting model:

```bash
ollama pull qwen3:8b
```

If your computer has limited RAM, use a smaller model available in your Ollama installation, for example:

```bash
ollama pull qwen3:4b
```

Then change `.env`:

```text
OLLAMA_MODEL=qwen3:4b
```

Tool calling quality varies by model. The current Ollama documentation demonstrates tool calling with models such as qwen3 and llama3.1.

## 3. Check Ollama

```bash
ollama list
```

You should see the model.

You can also test it directly:

```bash
ollama run qwen3:8b
```

Type:

```text
Hello
```

Then type `/bye`.

## 4. Create Python environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

## 6. Create .env

Copy:

```text
.env.example
```

to:

```text
.env
```

Example:

```text
OLLAMA_MODEL=qwen3:8b
OLLAMA_HOST=http://localhost:11434
```

The Python code uses the local Ollama service. No secret API key is needed.

## 7. Run unit tests

```bash
pytest -q
```

Expected:

```text
4 passed
```

## 8. Run the agent

```bash
python app.py
```

Try:

```text
I have 2 backlogs and CGPA 7.8. Am I eligible for TechNova?
```

Then:

```text
I have 0 backlogs and CGPA 8.2. Am I eligible for TechNova? The package is 6 LPA. Calculate monthly gross salary.
```

## 9. What you should observe

For the second question, the agent may decide to call:

```text
get_company_rules
calculate_monthly_salary
```

The Python program executes those functions and sends the results back to the local LLM.

This is the agent loop:

```text
User
 |
 v
Local LLM
 |
 |-- tool call --> get_company_rules()
 |                      |
 |<----- result --------|
 |
 |-- tool call --> calculate_monthly_salary()
 |                      |
 |<----- result --------|
 |
 v
Draft answer
 |
 v
Reflection pass
 |
 v
Final answer
```

## 10. SDLC / GitHub

Initialize:

```bash
git init
git add .
git commit -m "feat: initial local placement agent"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Feature branch:

```bash
git checkout -b feature/company-rules
```

After changes:

```bash
git add .
git commit -m "feat: improve company eligibility rules"
git push -u origin feature/company-rules
```

Create a Pull Request.

GitHub Actions is included in:

```text
.github/workflows/ci.yml
```

It runs:

```text
install dependencies
       |
       v
pytest
       |
       v
PASS / FAIL
```

## 11. Important production idea

The model should not directly execute arbitrary Python.

The application owns the tool registry:

```python
AVAILABLE_TOOLS = {
    "get_company_rules": get_company_rules,
    "calculate_monthly_salary": calculate_monthly_salary,
}
```

The model can request one of these tools, but your application decides whether it is allowed and then executes it.

## 12. Next upgrade: Agentic RAG

Replace the local hard-coded company rules with:

```text
company_rules.json
        |
        v
Document loader
        |
        v
Chunking
        |
        v
Embeddings
        |
        v
Vector DB
        |
        v
RAG tool
        |
        v
Local Agent
```

Then add:

- hybrid search
- reranking
- company-wise job descriptions
- student profile
- skill matching
- eligibility filtering
- explanation
- evaluation
- FastAPI
- React
- Docker
- GitHub Actions
- deployment
