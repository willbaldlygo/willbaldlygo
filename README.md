# willbaldlygo RAG App

This repository contains a simple two-page Retrieval-Augmented Generation (RAG) app built with [Streamlit](https://streamlit.io/).

## Features

- **Two pages**
  - **AIWP Bot**: upload PDFs or scrape websites, manage source library, and chat using text or voice input.
  - **The Agents**: configure up to four agents by assigning roles and prompts that steer answers.
- Uploaded files and scraped text are embedded and stored in a Supabase vector database.
- Chatbot responses are generated using OpenAI's `gpt-4o-mini` model via API or compatible OSS models on Hugging Face.
- Voice input powered by `streamlit-mic-recorder`.

## Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables for Supabase and OpenAI:
   ```bash
   export SUPABASE_URL="https://<your-project>.supabase.co"
   export SUPABASE_KEY="<service_role_key>"
   export OPENAI_API_KEY="<openai_or_oss_key>"
   ```
3. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Add sources** on the **AIWP Bot** page by uploading PDFs or entering a website URL and clicking *Fetch & Store*.
2. **Ask questions** in the Chat section via text or voice.
3. **Configure agents** on **The Agents** page, assigning each agent a role and prompt to tailor responses. Without configured agents, the app gives brief answers without citations.

## Deployment

The app can be hosted on platforms that support Streamlit:

- **Streamlit Community Cloud** – Fork this repository, sign in at [share.streamlit.io](https://share.streamlit.io), create a new app targeting `app.py`, and add the Supabase and OpenAI keys under *Secrets*.
- **Replit** – Create a Python Repl, upload the project files, configure the environment variables in *Secrets*, then run `streamlit run app.py`.
- **Vercel** – Use the Python deployment template, set `streamlit run app.py` as the start command, and add the required environment variables in project settings.

## Notes

- The vector store expects a Supabase table named `documents` with the `pgvector` extension enabled.
- Multiple users can access the hosted app simultaneously through the platforms above.

