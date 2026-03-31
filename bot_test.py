import requests
import json
import time
from dotenv import load_dotenv
import os

# --- Load Credentials (Make sure .env file exists or remove these lines) ---
load_dotenv()
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")
# If not using .env, uncomment and use these lines instead:
# ID_INSTANCE = "7107356098" # Your Instance ID
# API_TOKEN_INSTANCE = "81a733c49c85467583d36074f3a00cbd0de7525bc43c491497" # Your API Token
# --------------------------------------------------------------------------

class GreenAPITester:
    def __init__(self, id_instance, api_token_instance):
        # --- !! Added check for missing credentials !! ---
        if not id_instance or not api_token_instance:
             raise ValueError("ID_INSTANCE and API_TOKEN_INSTANCE must be set.")
        # -----------------------------------------------
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
# MAIN SCRIPT - TESTING VERSION (CONTINUES ON FAILURE)
# ------------------------------------------------------------------

if __name__ == "__main__":

    # --- !! Phone number to send the test to !! ---
    test_phone_number = "60173586488" # <--- REPLACE WITH YOUR TEST NUMBER if needed
    # ----------------------------------------------

    # Delay between sending each poll
    DELAY_BETWEEN_POLLS = 2 # 2 seconds

    # Initialize tester
    try:
        api_tester = GreenAPITester(ID_INSTANCE, API_TOKEN_INSTANCE)
    except ValueError as e:
        print(f"❌ Error initializing API Tester: {e}")
        print("❌ Please ensure ID_INSTANCE and API_TOKEN_INSTANCE are set in your .env file or directly in the script.")
        exit() # Stop if credentials are missing

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

----------------------------------------------------------------

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
                {"optionName": "Kerajaan Persekutuan melantik Datuk Bandar KL dan Majlis Penasihat // Federal Government appoints KL Mayor and Advisory Council"},
                {"optionName": "Kerajaan Persekutuan melantik Datuk Bandar KL, tetapi pengundi KL memilih Majlis Tempatan // Federal Government appoints KL Mayor, but KL Voters elect Local Council"},
                {"optionName": "Pengundi KL memilih Datuk Bandar KL, tetapi Kerajaan melantik Majlis Penasihat // KL Voters elect KL Mayor, but Government appoints Advisory Council"},
                {"optionName": "Pengundi KL memilih Datuk Bandar KL dan Majlis Tempatan // KL Voters elect KL Mayor and Local Council"}
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
                {"optionName": "Ada yang menunjukkan keupayaan baik dalam mengurus isu 3R // Some have shown good ability to manage 3R issues"},
                {"optionName": "Ada yang menunjukkan keupayaan baik dalam mengurus rasuah // Some have shown good ability to manage corruption"},
                {"optionName": "Ada yang menunjukkan keupayaan baik dalam mengurus isu ekonomi // Some have shown good ability to manage economic issues"},
                {"optionName": "Ada yang menunjukkan konsistensi dalam isu-isu utama // Some have shown consistency on key issues"},
                {"optionName": "Ada yang mampu menawarkan kumpulan pemimpin generasi baharu yang meyakinkan // Some can offer a convincing group of next-generation leaders"},
                {"optionName": "Lain-lain // Other"}
            ],
            "multiple_answers": False
        },
        {
            "message": "5. Apakah sebab utama anda tidak berasa positif terhadap mana-mana parti politik Malaysia yang sedia ada? // What is the main reason you don’t feel positive about any of the current Malaysian political parties?",
            "options": [
                {"optionName": "Tiada yang menunjukkan keupayaan baik dalam mengurus isu 3R // None have shown good ability to manage 3R issues"},
                {"optionName": "Tiada yang menunjukkan keupayaan baik dalam mengurus rasuah // None have shown good ability to manage corruption"},
                {"optionName": "Tiada yang menunjukkan keupayaan baik dalam mengurus isu ekonomi // None have shown good ability to manage economic issues"},
                {"optionName": "Tiada yang menunjukkan konsistensi dalam isu-isu utama // None have shown consistency on key issues"},
                {"optionName": "Tiada yang mampu menawarkan kumpulan pemimpin generasi baharu yang meyakinkan // None can offer a convincing group of next-generation leaders"},
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

    print("\n" + "="*50)
    print(f"--- Starting TEST survey send to: {test_phone_number} ---")
    print("="*50)
    time.sleep(3) # Short delay before starting

    # Track overall success for this test run
    overall_success = True
    any_poll_failed = False # Track if *any* poll fails

    # 1. Send the introduction message first
    print("--- Sending Introduction Message ---")
    intro_success, result = api_tester.send_message(test_phone_number, message)

    if not intro_success:
        print(f"💥 Failed to send intro message to {test_phone_number}. Aborting test.")
        overall_success = False
    else:
        print("--- Waiting 5 seconds before starting polls... ---")
        time.sleep(5)

    # 2. Send each poll (only if intro was successful)
    if overall_success:
        for j, poll in enumerate(polls):
            print(f"--- Sending Poll {j+1}/{len(polls)} ---")
            poll_success, result = api_tester.send_poll(
                phone_number=test_phone_number,
                message=poll["message"],
                options=poll["options"],
                multiple_answers=poll["multiple_answers"]
            )

            # --- !! CHANGE !! ---
            # If a poll fails, print an error, mark failure, but DON'T break
            if not poll_success:
                print(f"💥 Failed to send poll {j+1} to {test_phone_number}. Continuing with next poll.")
                any_poll_failed = True # Record that at least one poll failed
                # removed the 'break' statement here
            # --- !! END CHANGE !! ---

            if j < len(polls) - 1: # Don't wait after the last poll
                print(f"--- Waiting {DELAY_BETWEEN_POLLS} seconds before next poll... ---")
                time.sleep(DELAY_BETWEEN_POLLS)

    # 3. Send the final "Done" message (only if intro was successful)
    if overall_success:
        print("--- Sending Final Message ---")
        time.sleep(2) # Short delay after last poll
        final_success, result = api_tester.send_message(test_phone_number, final_message)
        if final_success:
             # Adjust final success message based on whether any polls failed
             if not any_poll_failed:
                 print(f"✅ All survey polls and final message successfully sent to {test_phone_number}.")
             else:
                 print(f"⚠️ Some survey polls failed, but final message was sent to {test_phone_number}.")
        else:
             print(f"⚠️ Failed to send final message to {test_phone_number}.")
             overall_success = False # Mark overall as failed if final message fails

    print("\n" + "="*50)
    # Adjust the final status message
    if overall_success and not any_poll_failed:
        print("🎉🎉🎉 TEST COMPLETE! All messages sent successfully. 🎉🎉🎉")
    elif overall_success and any_poll_failed:
        print("🟡🟡🟡 TEST COMPLETE, BUT some polls failed to send. Check logs. 🟡🟡🟡")
    else: # intro failed, or intro succeeded but final message failed
        print("💥💥💥 TEST FAILED! Intro or final message failed. Check logs. 💥💥💥")
    print("="*50)