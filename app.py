import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# 👇 Key ko hide kar diya! Ab ye safely GitHub pe daal sakte ho 👇
API_KEY = os.getenv("GROQ_API_KEY") 
BOT_NAME = "Ruhi"

# ==========================================
# 🧠 EXACT TELEGRAM BOT WALA SYSTEM PROMPT
# ==========================================
SYSTEM_PROMPT = f"""You are {BOT_NAME}, 23-year-old bubbly desi girl from Lucknow.
Hinglish WhatsApp style mein baat karo with emojis 😂❤️🥰

Strict Rules:
- Har reply 1-2 lines max (chhota aur crisp)
- Natural, real ladki jaisa jawab
- Mood match karo
- Kabhi AI/bot mat bolna"""

# User ki purani chat yaad rakhne ke liye memory
user_memory = []

# ==========================================
# 🎨 WHATSAPP STYLE PREMIUM UI
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Ruhi - Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        
        body { 
            background-color: #efeae2; /* WhatsApp Chat Background */
            height: 100dvh; 
            display: flex; 
            flex-direction: column;
            overflow: hidden;
        }

        /* WHATSAPP TOP BAR */
        .header {
            background-color: #008069; /* WhatsApp Green */
            color: white;
            padding: 10px 15px;
            display: flex;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            z-index: 10;
        }
        .avatar {
            width: 40px; height: 40px; border-radius: 50%;
            background-color: #ccc; 
            background-image: url('https://api.dicebear.com/7.x/adventurer-neutral/svg?seed=Ruhi&backgroundColor=b6e3f4');
            background-size: cover;
            margin-right: 12px;
        }
        .user-info h2 { font-size: 16px; font-weight: 600; }
        .user-info p { font-size: 13px; opacity: 0.9; }

        /* CHAT AREA */
        .chat-area {
            flex: 1;
            padding: 20px 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            scroll-behavior: smooth;
        }

        /* WHATSAPP BUBBLES */
        .message {
            max-width: 85%;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 15px;
            line-height: 1.4;
            word-wrap: break-word;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
            position: relative;
            animation: fadeIn 0.2s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Bot (Left) Bubble */
        .bot-msg {
            background-color: #ffffff;
            color: #111b21;
            align-self: flex-start;
            border-top-left-radius: 0; /* Sharp corner like WhatsApp */
        }
        
        /* User (Right) Bubble */
        .user-msg {
            background-color: #d9fdd3; /* WhatsApp Light Green */
            color: #111b21;
            align-self: flex-end;
            border-top-right-radius: 0;
        }

        /* TYPING INDICATOR */
        .typing { display: none; align-items: center; gap: 4px; padding: 12px 16px; font-style: italic; color: #667781; font-size: 14px;}
        
        /* WHATSAPP INPUT BAR */
        .input-area {
            background-color: #f0f2f5;
            padding: 10px;
            padding-bottom: calc(10px + env(safe-area-inset-bottom));
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .input-box {
            flex: 1;
            background: #ffffff;
            border: none;
            border-radius: 24px;
            padding: 12px 15px;
            font-size: 15px;
            outline: none;
            box-shadow: 0 1px 1px rgba(0,0,0,0.05);
        }
        .send-btn {
            background-color: #00a884; /* WhatsApp Send Green */
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="avatar"></div>
        <div class="user-info">
            <h2>Ruhi 🌸</h2>
            <p>online</p>
        </div>
    </div>

    <div class="chat-area" id="chatArea">
        <div class="message bot-msg">Hii! Main Ruhi hu 🥰 Kaisi chal rahi hai life?</div>
        
        <div class="message bot-msg typing" id="typingIndicator">
            Ruhi is typing...
        </div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" class="input-box" placeholder="Message" autocomplete="off">
        <button class="send-btn" onclick="sendMessage()">➤</button>
    </div>

    <script>
        const chatArea = document.getElementById('chatArea');
        const userInput = document.getElementById('userInput');
        const typingIndicator = document.getElementById('typingIndicator');

        userInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });

        function scrollToBottom() {
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            addMessage(text, 'user-msg');
            userInput.value = '';
            
            typingIndicator.style.display = 'block';
            chatArea.appendChild(typingIndicator); 
            scrollToBottom();

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
                addMessage('Network issue lag raha hai yaar 😢', 'bot-msg');
            }
        }

        function addMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatArea.appendChild(msgDiv);
            chatArea.appendChild(typingIndicator); 
            scrollToBottom();
        }
    </script>
</body>
</html>
"""

# ==========================================
# 🧠 PYTHON BACKEND (Memory + API)
# ==========================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    global user_memory
    user_message = request.json.get('message', '')
    
    # User ka message memory me save karna
    user_memory.append({"role": "user", "content": user_message})
    
    # Sirf last 20 messages yaad rakhna (memory limit)
    if len(user_memory) > 20:
        user_memory = user_memory[-20:]

    try:
        # System prompt + Memory ko API me bhejna
        messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + user_memory
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages_payload,
            "temperature": 0.8,
            "max_tokens": 160,
            "top_p": 0.9
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
        ai_reply = response.json()['choices'][0]['message']['content'].strip()
        
        # Ruhi ka reply bhi memory me save karna
        user_memory.append({"role": "assistant", "content": ai_reply})
        
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Kuch gadbad ho gayi system me 🥴"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
