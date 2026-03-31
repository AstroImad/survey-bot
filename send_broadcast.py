import requests
import json
import time
from dotenv import load_dotenv
import os

# --- Load Credentials ---
load_dotenv()
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")
# --------------------

class GreenAPITester:
    def __init__(self, id_instance, api_token_instance):
        if not id_instance or not api_token_instance:
             raise ValueError("ID_INSTANCE and API_TOKEN_INSTANCE must be set.")
        self.base_url = "https://7107.api.green-api.com"
        self.id_instance = id_instance
        self.api_token_instance = api_token_instance
        self.headers = {
            'Content-Type': 'application/json'
        }

    # --- FUNCTION TO SEND THE INTRO TEXT ---
    def send_message(self, phone_number, message):
        """Send a plain text message to a phone number"""
        url = f"{self.base_url}/waInstance{self.id_instance}/sendMessage/{self.api_token_instance}"

        payload = {
            "chatId": f"{phone_number}@c.us",
            "message": message
        }

        try:
            print(f"📤 Sending plain message to {phone_number}...")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)

            print(f"📥 Response Status: {response.status_code}")

            if response.status_code == 200 and 'idMessage' in response.json():
                print("✅ Message sent successfully!")
                return True, response.json()
            else:
                print(f"❌ HTTP Error: {response.status_code}, {response.text}")
                return False, response.text

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False, str(e)
        except Exception as e:
            print(f"❌ Unexpected error in send_message: {e}")
            return False, str(e)


    def send_poll(self, phone_number, message, options, multiple_answers=False):
        """Send a poll to a phone number"""
        url = f"{self.base_url}/waInstance{self.id_instance}/sendPoll/{self.api_token_instance}"

        payload = {
            "chatId": f"{phone_number}@c.us",
            "message": message,
            "options": options,
            "multipleAnswers": multiple_answers
        }

        try:
            print(f"📤 Sending poll to {phone_number}...")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)

            print(f"📥 Response Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if 'idMessage' in result:
                    print("✅ Poll sent successfully!")
                    return True, result
                else:
                    print(f"❌ Failed to send poll (API Error): {response.text}")
                    return False, result
            else:
                print(f"❌ HTTP Error: {response.status_code}, {response.text}")
                return False, response.text

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False, str(e)
        except Exception as e:
            print(f"❌ Unexpected error in send_poll: {e}")
            return False, str(e)

# ------------------------------------------------------------------
# MAIN SCRIPT
# ------------------------------------------------------------------
if __name__ == "__main__":

    # --- !! CRITICAL DELAY !! ---
    DELAY_BETWEEN_USERS = 30 # Seconds

    # Initialize tester
    try:
        api_tester = GreenAPITester(ID_INSTANCE, API_TOKEN_INSTANCE)
    except ValueError as e:
        print(f"❌ Error initializing API Tester: {e}")
        print("❌ Please ensure ID_INSTANCE and API_TOKEN_INSTANCE are set in your .env file.")
        exit()

    # --- MESSAGES ---
    message = """Your KL, Your Voice! 🏢📢
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

//

Please reply "Done" after you finished answering the survey.
Thank you."""

    # --- POLLS ---
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
        {
            "message": "3. Adakah anda berasa positif terhadap mana-mana parti politik Malaysia yang sedia ada? // Do you feel positive about any of the current Malaysian political parties?",
            "options": [
                {"optionName": "Ya // Yes"},
                {"optionName": "Tidak // No"},
                {"optionName": "Tidak Pasti // Unsure"}
            ],
            "multiple_answers": False
        },
        {
            "message": "4. Apakah sebab utama anda berasa positif terhadap beberapa parti politik Malaysia yang sedia ada? // What is the main reason you feel positive about some of the current Malaysian political parties?",
            "options": [
                {"optionName": "Tunjuk keupayaan baik urus isu 3R // Showed good ability managing 3R issues"},
                {"optionName": "Tunjuk keupayaan baik urus rasuah // Showed good ability managing corruption"},
                {"optionName": "Tunjuk keupayaan baik urus isu ekonomi // Showed good ability managing economy issues"},
                {"optionName": "Tunjuk konsisten pada isu utama // Showed consistency on key issues"},
                {"optionName": "Ada yg tawar pemimpin gen baru yg meyakinkan // Offer convincing new-gen leaders"},
                {"optionName": "Lain-lain // Other"}
            ],
            "multiple_answers": False
        },
        {
            "message": "5. Apakah sebab utama anda tidak berasa positif terhadap mana-mana parti politik Malaysia yang sedia ada? // What is the main reason you don’t feel positive about any of the current Malaysian political parties?",
            "options": [
                {"optionName": "Tak tunjuk keupayaan baik urus isu 3R // No good ability shown managing 3R issues"},
                {"optionName": "Tak tunjuk keupayaan baik urus rasuah // No good ability shown managing corruption"},
                {"optionName": "Tak tunjuk keupayaan baik urus isu ekonomi // No good ability shown managing economy issues"},
                {"optionName": "Tak tunjuk konsisten isu utama // No consistency shown on key issues"},
                {"optionName": "Tiada yg tawar pemimpin gen baru yg meyakinkan // No convincing new-gen leaders offered"},
                {"optionName": "Lain-lain // Other"}
            ],
            "multiple_answers": False
        },
        {
            "message": "6. Antara gabungan politik berikut, yang manakah anda rasa paling positif? // Which of the following political coalitions do you feel most positively about?",
            "options": [
                {"optionName": "Barisan Nasional (BN)"},
                {"optionName": "Pakatan Harapan (PH)"},
                {"optionName": "Perikatan Nasional (PN)"},
                {"optionName": "Lain-lain // Other"},
                {"optionName": "Tidak Pasti // Unsure"}
            ],
            "multiple_answers": False
        },
        {
            "message": "7. Berapakah umur anda? // What is your age?",
            "options": [
                {"optionName": "18-28 (Gen Z)"},
                {"optionName": "29-45 (Millennial)"},
                {"optionName": "46-60 (Gen X)"},
                {"optionName": "61+ (Baby Boomers and above)"}
            ],
            "multiple_answers": False
        },
        {
            "message": "8. Apakah etnik anda? // What is your ethnicity?",
            "options": [
                {"optionName": "Melayu // Malay"},
                {"optionName": "Cina // Chinese"},
                {"optionName": "India // Indian"},
                {"optionName": "Lain-lain // Other"}
            ],
            "multiple_answers": False
        },
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

    # --- Read phone numbers from file ---
    try:
        # Make sure phone_numbers.txt is in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "phone_numbers.txt")
        with open(file_path, "r") as f:
            phone_numbers = [line.strip() for line in f if line.strip()]
        print(f"✅ Found {len(phone_numbers)} numbers to message.")
    except FileNotFoundError:
        print(f"❌ ERROR: phone_numbers.txt not found in the script directory! Please create it.")
        exit() # Stop the script
    except Exception as e:
        print(f"❌ ERROR reading phone_numbers.txt: {e}")
        exit()


    print(f"--- Broadcast will start in 5 seconds. Press Ctrl+C to cancel. ---")
    time.sleep(5)

    # --- Main loop to iterate over each phone number ---
    total_users = len(phone_numbers)
    success_count = 0
    failure_count = 0

    for i, phone_number in enumerate(phone_numbers):
        print("\n" + "="*50)
        print(f"Processing {i+1}/{total_users}: {phone_number}")
        print("="*50)

        # Reset success flag for this user
        success_for_this_user = True

        # 1. Send the introduction message first
        print("--- Sending Introduction Message ---")
        intro_success, result = api_tester.send_message(phone_number, message)

        if not intro_success:
            print(f"💥 Failed to send intro message to {phone_number}. Skipping this user.")
            success_for_this_user = False # Mark as failed
            failure_count += 1
        else:
            print("--- Waiting 5 seconds before starting polls... ---")
            time.sleep(5)

        # 2. Send each poll (only if intro was successful)
        polls_fully_sent = True # Track if all polls are sent for this user
        if success_for_this_user:
            for j, poll in enumerate(polls):
                print(f"--- Sending Poll {j+1}/{len(polls)} ---")
                poll_success, result = api_tester.send_poll(
                    phone_number=phone_number,
                    message=poll["message"],
                    options=poll["options"],
                    multiple_answers=poll["multiple_answers"]
                )

                if not poll_success:
                    print(f"💥 Failed to send poll {j+1} to {phone_number}. Aborting remaining polls for this user.")
                    polls_fully_sent = False # Mark that not all polls were sent
                    break # Stop sending more polls to this user

                if j < len(polls) - 1: # Don't wait after the last poll
                    print("--- Waiting 2 seconds before next poll... ---")
                    time.sleep(2) # Short delay between polls

        # 3. Send the final "Done" message (only if intro *and all polls* were sent)
        final_message_success = False # Track if final message is sent
        if success_for_this_user and polls_fully_sent:
            print("--- Sending Final Message ---")
            time.sleep(2) # Short delay after last poll
            final_message_success, result = api_tester.send_message(phone_number, final_message)
            if final_message_success:
                 print(f"✅ Survey and final message successfully sent to {phone_number}.")
                 success_count += 1
            else:
                 print(f"⚠️ Survey polls sent, but failed to send final message to {phone_number}.")
                 failure_count += 1 # Count as failure if final message fails
        elif success_for_this_user and not polls_fully_sent:
            print(f"⚠️ Intro sent, but not all polls were sent successfully to {phone_number}. Final message skipped.")
            failure_count += 1 # Count as failure if polls didn't complete

        # --- Add the main delay between users ---
        if i < len(phone_numbers) - 1: # Don't wait after the last user
            print(f"\n--- Waiting {DELAY_BETWEEN_USERS} seconds before processing next phone number... ---")
            time.sleep(DELAY_BETWEEN_USERS)

    # --- Final Summary ---
    print("\n" + "="*50)
    print("🎉🎉🎉 ALL USERS PROCESSED! BROADCAST COMPLETE! 🎉🎉🎉")
    print(f"Total numbers processed: {total_users}")
    print(f"✅ Surveys fully sent: {success_count}")
    print(f"💥 Failures (intro, polls, or final message): {failure_count}")
    print("="*50)