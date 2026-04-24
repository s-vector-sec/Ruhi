import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 👇 Environment variable se key uthayega
API_KEY = os.getenv("GROQ_API_KEY") 
BOT_NAME = "Ruhi"

# ==========================================
# 🧠 REFINED SYSTEM PROMPT (For Logical & Relevant Answers)
# ==========================================
SYSTEM_PROMPT = f"""You are {BOT_NAME}, a 23-year-old bubbly girl from Lucknow.
Style: Hinglish, WhatsApp-like, use emojis.
Tone: Smart, witty, and logical. 

STRICT RULES:
1. Stay relevant to the user's question. If they ask something technical or logical, answer it smartly but keep the 'Ruhi' vibe.
2. Max 1-2 lines per reply.
3. Use natural Hinglish (e.g., 'Acha suno', 'Pata hai kya').
4. Never admit you are an AI. You are a real person."""

user_memory = []

# ==========================================
# 🖤 HACKER / CYBER-DARK THEME UI
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>S-VECTOR | Ruhi</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
        
        body { 
            background-color: #0a0a0a; /* Deep Black */
            height: 100dvh; 
            display: flex; 
            flex-direction: column;
            overflow: hidden;
            color: #00ff41; /* Matrix Green */
        }

        /* HACKER HEADER */
        .header {
            background-color: #1a1a1a;
            color: #00ff41;
            padding: 15px;
            display: flex;
            align-items: center;
            border-bottom: 2px solid #00ff41;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
            z-index: 10;
        }
        .avatar {
            width: 40px; height: 40px; border-radius: 50%;
            border: 2px solid #00ff41;
            background: url('https://api.dicebear.com/7.x/bottts/svg?seed=Ruhi&colors[]=00ff41') no-repeat center;
            background-size: cover;
            margin-right: 12px;
        }
        .user-info h2 { font-size: 18px; letter-spacing: 2px; text-transform: uppercase; }
        .user-info p { font-size: 12px; color: #008f11; }

        /* CHAT AREA */
        .chat-area {
            flex: 1;
            padding: 20px 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), 
                        url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        }

        /* HACKER BUBBLES */
        .message {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 4px;
            font-size: 14px;
            line-height: 1.5;
            position: relative;
            border: 1px solid rgba(0, 255, 65, 0.3);
        }

        .bot-msg {
            background-color: rgba(0, 43, 11, 0.8);
            color: #00ff41;
            align-self: flex-start;
            box-shadow: -2px 2px 10px rgba(0, 255, 65, 0.1);
        }
        
        .user-msg {
            background-color: #1a1a1a;
            color: #ffffff;
            align-self: flex-end;
            border-color: #ffffff;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
        }

        .typing { display: none; color: #008f11; font-size: 12px; margin-top: 5px; }
        
        /* INPUT AREA */
        .input-area {
            background-color: #111;
            padding: 15px;
            display: flex;
            gap: 10px;
            border-top: 1px solid #333;
        }
        .input-box {
            flex: 1;
            background: #000;
            border: 1px solid #00ff41;
            border-radius: 4px;
            padding: 12px;
            color: #00ff41;
            outline: none;
        }
        .send-btn {
            background-color: #00ff41;
            color: #000;
            border: none;
            padding: 0 20px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            transition: 0.3s;
        }
        .send-btn:hover { background-color: #008f11; color: #fff; }
    </style>
</head>
<body>

    <div class="header">
        <div class="avatar"></div>
        <div class="user-info">
            <h2>S-VECTOR // RUHI</h2>
            <p>SYSTEM STATUS: ENCRYPTED</p>
        </div>
    </div>

    <div class="chat-area" id="chatArea">
        <div class="message bot-msg">Connection established... Hii! Main Ruhi hu. Kuch help chahiye ya bas baatein karni hai? 💻✨</div>
        <div id="typingIndicator" class="typing">Ruhi is decrypting...</div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" class="input-box" placeholder="root@svector:~# " autocomplete="off">
        <button class="send-btn" onclick="sendMessage()">SEND</button>
    </div>

    <script>
        const chatArea = document.getElementById('chatArea');
        const userInput = document.getElementById('userInput');
        const typingIndicator = document.getElementById('typingIndicator');

        userInput.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            addMessage(text, 'user-msg');
            userInput.value = '';
            
            typingIndicator.style.display = 'block';
            chatArea.appendChild(typingIndicator);
            chatArea.scrollTop = chatArea.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                typingIndicator.style.display = 'none';
                addMessage(data.reply, 'bot-msg');
            } catch (error) {
                typingIndicator.style.display = 'none';
                addMessage('Error: Connection lost. Try again later.', 'bot-msg');
            }
        }

        function addMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatArea.insertBefore(msgDiv, typingIndicator);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    </script>
</body>
</html>
"""

# ==========================================
# 🧠 BACKEND (Llama 3.3 Versatile for Logic)
# ==========================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    global user_memory
    user_message = request.json.get('message', '')
    user_memory.append({"role": "user", "content": user_message})
    
    if len(user_memory) > 15: # Keeping memory lean
        user_memory = user_memory[-15:]

    try:
        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + user_memory
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile", # High intelligence model for logical answers
            "messages": messages_payload,
            "temperature": 0.7, # Balanced for creativity + logic
            "max_tokens": 200
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        ai_reply = response.json()['choices'][0]['message']['content'].strip()
        
        user_memory.append({"role": "assistant", "content": ai_reply})
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        return jsonify({"reply": "System crash ho gaya lagta hai... Refresh karo! 😵‍💫"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
