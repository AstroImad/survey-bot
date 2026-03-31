import requests
import json
import time
from dotenv import load_dotenv
import os
import threading
from flask import Flask, request, jsonify

# --- Setup Flask App ---
app = Flask(__name__)

# --- Load Environment Variables ---
load_dotenv()
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")

# --- Your Existing GreenAPITester Class (No changes needed) ---
class GreenAPITester:
    def __init__(self, id_instance, api_token_instance):
        self.base_url = f"https.api.green-api.com" # Removed 7107, as it's in the instance ID
        self.id_instance = id_instance
        self.api_token_instance = api_token_instance
        self.headers = {
            'Content-Type': 'application/json'
        }

    def send_message(self, chat_id, message):
        """Send a plain text message to a chat ID (e.g., 60123456789@c.us)"""
        url = f"{self.base_url}/waInstance{self.id_instance}/sendMessage/{self.api_token_instance}"
        
        payload = {
            "chatId": chat_id, # Use chat_id directly
            "message": message
        }
        
        try:
            print(f"📤 Sending plain message to {chat_id}...")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            print(f"📥 Response Status: {response.status_code}")
            print(f"📥 Response Text: {response.text}")
            
            if response.status_code == 200 and 'idMessage' in response.json():
                print("✅ Message sent successfully!")
                return True, response.json()
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False, response.text
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False, str(e)
        except Exception as e:
            print(f"❌ Unexpected error in send_message: {e}")
            return False, str(e)

    def send_poll(self, chat_id, message, options, multiple_answers=False):
        """Send a poll to a chat ID (e.g., 60123456789@c.us)"""
        url = f"{self.base_url}/waInstance{self.id_instance}/sendPoll/{self.api_token_instance}"
        
        payload = {
            "chatId": chat_id, # Use chat_id directly
            "message": message,
            "options": options,
            "multipleAnswers": multiple_answers
        }
        
        try:
            print(f"📤 Sending poll to {chat_id}...")
            print(f"📝 Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            print(f"📥 Response Status: {response.status_code}")
            print(f"📥 Response Text: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if 'idMessage' in result:
                    print("✅ Poll sent successfully!")
                    return True, result
                else:
                    print("❌ Failed to send poll")
                    return False, result
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False, response.text
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False, str(e)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False, str(e)

# --- Initialize API Tester (globally) ---
if not ID_INSTANCE or not API_TOKEN_INSTANCE:
    print("❌ ERROR: ID_INSTANCE or API_TOKEN_INSTANCE not found in .env file.")
    # In a real app, you'd exit, but for Flask, we'll let it run and fail on request
    api_tester = None 
else:
    api_tester = GreenAPITester(ID_INSTANCE, API_TOKEN_INSTANCE)


# --- Define Survey Content (globally) ---
intro_message = """Your KL, Your Voice! 🏢📢

Suara Anda Penting, Warga Kuala Lumpur!

Hidup di KL tidak selalu mudah — dari kos sara hidup yang meningkat hingga cabaran harian, setiap suara ada kisahnya. Tinjauan ringkas ini memberi peluang kepada anda untuk berkongsi perkara yang benar-benar penting bagi diri dan komuniti anda.

Pandangan anda akan membantu membentuk Kuala Lumpur yang lebih adil dan sejahtera untuk semua.

Hanya 5 minit diperlukan — namun suara anda mampu membawa perubahan.

👉 Sertai tinjauan ini dan suarakan pendapat anda.

----------------------------------------------------------------

Life in KL isn’t always easy — from rising costs to daily struggles, every voice has a story. This short survey lets you share what truly matters to you and your community.

Your views will help shape a fairer, more liveable Kuala Lumpur for all.

It only takes 5 minutes — but your voice can make a real difference.

👉 Take the survey and be heard."""

final_message = """Sila balas "Done" selepas anda selesai menjawab tinjauan.

Terima kasih.

----------------------------------------------------------------

Please reply "Done" after you finished answering the survey.

Thank you."""

polls = [
    {
        "message": "1. Pada pendapat anda, bagaimanakah Datuk Bandar Kuala Lumpur sepatutnya dipilih? // In your opinion, how should the Mayor of Kuala Lumpur be selected?",
        "options": [
            {"optionName": "Dilantik oleh Kerajaan Persekutuan // Appointed by the Federal Government"},
            {"optionName": "Dipilih secara langsung oleh pengundi KL // Directly Elected by KL Voters"},
            {"optionName": "Dipilih oleh Majlis Tempatan yang dipilih // Chosen by an Elected Local Council"},
            {"optionName": "Lain-lain // Other"},
            {"optionName": "Tidak pasti // Unsure"}
        ],
        "multiple_answers": False
    },
    {
        "message": "2. Antara pilihan berikut, yang manakah paling mewakili pilihan anda? // Which of the following options best represents your preference?",
        "options": [
            {"optionName": "Datuk Bandar & Majlis dilantik oleh Kerajaan Persekutuan // Mayor & Council appointed by Fed. Govt"},
            {"optionName": "Kerajaan pilih Datuk Bandar, Pengundi KL pilih Majlis//Govt appoints Mayor, KL Voters elect Council"},
            {"optionName": "Pengundi KL pilih Datuk Bandar, Kerajaan pilih Majlis // KL Voters elect Mayor, Govt elect Council"},
            {"optionName": "Pengundi KL pilih Datuk Bandar & Majlis // KL Voters elect Mayor & Council"}
        ],
        "multiple_answers": False
    },
    # ... [ALL YOUR OTHER 8 POLLS GO HERE] ...
    # (I'm omitting them for brevity, but you should copy-paste them all back in)
    {
        "message": "9. Apakah jantina anda? // What is your gender?",
        "options": [
            {"optionName": "Perempuan // Female"},
            {"optionName": "Lelaki // Male"}
        ],
        "multiple_answers": False    
    },
    {
        "message": "10. Berapakah jumlah pendapatan bulanan isi rumah anda? // What is your monthly household income range?",
        "options": [
            {"optionName": "RM5,250 and below"},
            {"optionName": "RM5,251 - RM13,000"},
            {"optionName": "RM13,000 and above"}
        ],
        "multiple_answers": False
    }
]

# --- NEW: Function to send the survey to a *single user* ---
# This runs in a separate thread so the webhook can reply "OK" immediately
def send_full_survey(chat_id):
    if not api_tester:
        print("💥 API Tester not initialized. Cannot send survey.")
        return

    print("\n" + "="*50)
    print(f"Processing survey for: {chat_id}")
    print("="*50)
    
    # 1. Send the introduction message
    print("--- Sending Introduction Message ---")
    intro_success, _ = api_tester.send_message(chat_id, intro_message)
    
    if not intro_success:
        print(f"💥 Failed to send intro message to {chat_id}. Aborting.")
        return # Stop here for this user

    # Wait 5 seconds for the user to read the intro
    print("--- Waiting 5 seconds before starting poll... ---")
    time.sleep(5)

    # 2. Send each poll
    success_for_this_user = True
    for j, poll in enumerate(polls):
        print(f"--- Sending Poll {j+1}/{len(polls)} ---")
        poll_success, _ = api_tester.send_poll(
            chat_id=chat_id,
            message=poll["message"],
            options=poll["options"],
            multiple_answers=poll["multiple_answers"]
        )

        if not poll_success:
            print(f"💥 Failed to send poll {j+1} to {chat_id}. Aborting polls for this user.")
            success_for_this_user = False
            break # Stop sending more polls

        if j < len(polls) - 1: # Don't wait after the last poll
            print("--- Waiting 2 seconds before next poll... ---")
            time.sleep(2) # Short delay between polls

    # 3. Send the final "Done" message if all polls were sent
    if success_for_this_user:
        print("--- Sending Final Message ---")
        time.sleep(2) # Short delay after last poll
        final_success, _ = api_tester.send_message(chat_id, final_message)
        if final_success:
            print(f"✅ Survey and final message successfully sent to {chat_id}.")
        else:
            print(f"⚠️ Survey polls sent, but failed to send final message to {chat_id}.")
    
    print(f"--- Survey process finished for {chat_id} ---")


# --- NEW: Flask Webhook Route ---
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    try:
        data = request.json
        print(f"\n--- 📥 INCOMING WEBHOOK ---")
        print(json.dumps(data, indent=2))
        
        # Check if it's an incoming message
        if data.get('typeWebhook') == 'incomingMessageReceived':
            message_data = data.get('messageData', {})
            text_message_data = message_data.get('textMessageData', {})
            message_text = text_message_data.get('textMessage', '').strip().lower()
            
            # Get the sender's Chat ID (e.g., "60123456789@c.us")
            sender_chat_id = data.get('senderData', {}).get('chatId')

            if not sender_chat_id:
                print("⚠️ Received a message but couldn't find sender's chatId.")
                return jsonify({"status": "error", "message": "No chatId"}), 400

            # Check if the message is "start"
            if message_text in ["start", "/start"]:
                print(f"✅ 'Start' command received from {sender_chat_id}. Triggering survey.")
                
                # IMPORTANT: Start the survey in a new thread.
                # This lets us return "200 OK" to Green-API immediately,
                # while the survey sends in the background.
                threading.Thread(target=send_full_survey, args=(sender_chat_id,)).start()
            
            else:
                print(f"Ignoring message from {sender_chat_id}: '{message_text}'")

        # Always return 200 OK to Green-API to show we received the hook
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ ERROR in webhook handler: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- NEW: Main entry point to run the Flask server ---
if __name__ == "__main__":
    print("--- Starting WhatsApp Survey Bot Server ---")
    print("Listening on http://127.0.0.1:5000")
    print("Set your Green-API Webhook URL to <your_ngrok_url>/webhook")
    app.run(port=5000, debug=True) # debug=True is good for development