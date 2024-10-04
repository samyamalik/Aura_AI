<p align="center">
  <img src="./logo.png" alt="Project Logo" />
</p>

# Gemini-Enhanced AI Chatbot for Mental Health and Emotional Support

This is a Gemini-Enhanced AI chatbot for Mental Health and Emotional Support created using Python, Streamlit, and Firebase.

## Steps for creating this Chatbot

### Step 1: Clone the repository
Clone this repository using the following command:

```
git clone https://github.com/samyamalik/Aura_AI
```

After cloning, navigate to the project directory:

```
cd Aura_AI
```

### Step 2: Create a virtual environment
Run the following command to create a virtual environment:

#### For Windows:
```
python -m venv env
```

#### For Mac:
```
python3 -m venv env
```

Activate the virtual environment:

#### For Windows:
```
.\env\Scripts\activate
```

#### For Mac:
```
source env/bin/activate
```

### Step 3: Install the required packages
Install the necessary packages listed in requirements.txt by running the following commands:

```
pip install google-generativeai
pip install python-dotenv
pip install firebase-admin
pip install streamlit
```

Use `pip3` instead of `pip` for Mac.

### Step 4: Set up the `.env` file
Create an `.env` file in the project root to store your API keys. The content of the `.env` file should look like this:

```bash
API_KEY="your_google_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
FIREBASE_CONFIG_KEY="your_firebase_config_key_here"
```

### Step 5: Set up Firebase configuration
You need to create your own Firebase project and download the service account credentials. Follow the steps below:

1. Go to the [Firebase Console](https://console.firebase.google.com/).
2. Create a new Firebase project.
3. Navigate to **Project Settings** > **Service accounts** > **Generate new private key**.
4. Download the JSON file, which will be named something like `firebase-adminsdk-XXXXX.json`.
5. Create a `firebase_config` folder in your project directory.
6. Move the downloaded `firebase-adminsdk-XXXXX.json` file into the `firebase_config` folder.

The content of this JSON file will look like this (this is a template—replace with your own credentials):

```json
{
  "type": "service_account",
  "project_id": "your_project_id_here",
  "private_key_id": "your_private_key_id_here",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your_client_email_here",
  "client_id": "your_client_id_here",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_client_email_here",
  "universe_domain": "googleapis.com"
}
```

**Note**: Each user must set up their own Firebase project and use their own service account credentials.

### Step 6: Run the application
Once the setup is complete, run your project by executing the `main.py` file in the virtual environment:

```bash
streamlit run main.py
```
