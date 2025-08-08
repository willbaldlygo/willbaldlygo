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

## Notes

- If no agent roles or prompts are configured, the chatbot provides a brief answer without citing sources.
- Multiple users can access the app through Streamlit sharing platforms such as Streamlit Community Cloud, Replit, or Vercel.

