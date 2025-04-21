# 🧮 Math Solver Agent with LibreOffice Integration

This project is a **Math Agent System** that uses:
- **FastAPI** for serving AI queries
- **Google Gemini** for step-by-step reasoning
- **MCP Tools** for mathematical operations
- **LibreOffice Writer** automation to visually present results
- A **Chrome Extension** to interact via a browser popup

---

## 🚀 Features

- 🧠 **LLM Reasoning** via Google Gemini 1.5
- 🛠️ **Math tools** like add, subtract, sqrt, factorial, sin, etc.
- 🖼️ **LibreOffice Writer Automation** to draw and type final answers
- 🧪 **Consistency & Verification** tools to validate steps
- 🧩 **Chrome Extension** with popup UI for quick querying

---

## 🧰 Project Structure

```
.
├── mcp_client_libre_fastapi.py   # FastAPI backend logic (math agent + Gemini)
├── mcp_server_libre.py           # MCP tool server with math + LibreOffice tools
├── popup.html                    # Chrome extension UI
├── popup.js                      # Chrome extension logic
├── style.css                     # Styles for extension
├── manifest.json                 # Chrome extension manifest
```

---

## 🖥️ How It Works

### 🧠 Backend

1. Accepts a math query via FastAPI.
2. Google Gemini processes it step-by-step.
3. MCP tools (from `mcp_server_libre.py`) handle each step: math operations, drawing in LibreOffice, etc.
4. Results are verified and then drawn inside LibreOffice Writer.
5. Final response is returned with a step log.

### 🧩 Chrome Extension

1. Input a query in the extension popup.
2. Sends it to `http://localhost:8000/solve`.
3. Displays results and reasoning log.

---

## 🛠️ Requirements

- Python 3.9+
- LibreOffice (must be installed and GUI-accessible)
- Google Gemini API key (set as `GEMINI_API_KEY` in `.env`)
- `pyautogui`, `fastapi`, `mcp`, `python-dotenv`, `uvicorn`

Install via:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:
```txt
fastapi
pyautogui
python-dotenv
uvicorn
google-generativeai
```

---

## ▶️ Running the App

### 1. Start MCP Tool Server
```bash
python mcp_server_libre.py
```

### 2. Start FastAPI Server
```bash
uvicorn mcp_client_libre_fastapi:app --reload
```

Make sure LibreOffice can open in GUI (`DISPLAY=:0` for Linux).

---

## 🧪 Test a Query

Use your browser extension or send a query like:

```bash
curl -X POST http://localhost:8000/solve -H "Content-Type: application/json" -d '{"query":"(3 + 2)^2 - sqrt(16)"}'
```

---

## 🧱 Chrome Extension Setup

1. Go to `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load Unpacked** and select the folder containing:
   - `popup.html`, `popup.js`, `style.css`, and `manifest.json`

---

## 💡 Tips

- Update screen coordinates in `create_new_doc` or `draw_text_box` in case they don’t work with your resolution.
- If `LibreOffice` opens too slow, you can increase `sleep` delay in the tool scripts.
- Use `pyautogui.FAILSAFE = False` carefully to avoid script lockups.

---

## 📋 Prompt Design Evaluation

The math agent’s system prompt has been evaluated for robustness and clarity. Below is a structured analysis of its design qualities:

```json
{
  "explicit_reasoning": true,
  "structured_output": true,
  "tool_separation": true,
  "conversation_loop": true,
  "instructional_framing": true,
  "internal_self_checks": true,
  "reasoning_type_awareness": true,
  "fallbacks": true,
  "overall_clarity": "Exceptionally well-structured prompt. It promotes disciplined, modular reasoning with clear tool separation, internal verifications, and robust multi-turn guidance. Minor edge cases like what to do if verification fails repeatedly could be clarified further, but overall it strongly supports reliable agent behavior."
}
```

---

## 📄 License

MIT License. Use it, build on it, share it.
