# Mercedes-Benz AI Specialist: Real-Time RAG Assistant

> An AI-powered virtual product specialist that leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, real-time information about Mercedes-Benz vehicles.

## 💡 The Problem
Standard LLMs (Large Language Models) like ChatGPT have a **knowledge cutoff**. If Mercedes-Benz updates the pricing or range of the EQS SUV today, a standard AI won't know about it.

## 🚀 The Solution
This application solves the "stale data" problem by implementing a **real-time RAG pipeline**:
1.  **Live Scraping:** When a user selects a car model, the app uses **Firecrawl** to scrape the live Mercedes-Benz USA product page.
2.  **Context Injection:** The raw website data is cleaned and injected into the system prompt as context.
3.  **Grounded Answers:** **GPT-4o** answers user questions based *only* on the live data, effectively acting as a specialist with the brochure in hand.

## ⚙️ Technical Architecture

The application is built as a monolithic Streamlit app for rapid deployment and state management.

* **Frontend:** Custom-styled Streamlit interface with CSS injection to match the Mercedes-Benz "Dark Mode" aesthetic.
* **Backend Logic:** Python-based orchestration.
* **Data Pipeline:**
    * `FirecrawlApp`: Handles dynamic Javascript rendering to scrape complex car configurator pages.
    * `OpenAI API`: Processes the scraped context and handles the natural language conversation.

## 🛠️ Features

* **Dynamic Knowledge Base:** Supports 8+ distinct Mercedes models (S-Class, G-Wagon, EQS, etc.).
* **Luxury UI/UX:** Custom CSS implementation for a premium "showroom" feel (Ghost buttons, gradients, custom typography).
* **Session State Management:** Persists chat history and scraped context while switching between car models.

## 📦 Tech Stack

| Component | Technology | Reason for Choice |
| :--- | :--- | :--- |
| **Framework** | Streamlit | Allows for rapid full-stack development in pure Python. |
| **LLM** | OpenAI GPT-4o | High reasoning capability required for parsing complex car specs. |
| **Scraper** | Firecrawl | specialized for turning complex websites into LLM-ready Markdown. |

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/mercedes-ai-assistant.git](https://github.com/YOUR_USERNAME/mercedes-ai-assistant.git)
    cd mercedes-ai-assistant
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys**
    Create a file at `.streamlit/secrets.toml`:
    ```toml
    OPENAI_API_KEY = "sk-..."
    FIRECRAWL_API_KEY = "fc-..."
    ```

4.  **Launch the App**
    ```bash
    streamlit run mercedes_bot.py
    ```

## Future Roadmap

* [ ] **Voice Interface:** Allow users to speak to the assistant while driving (simulated).
* [ ] **Compare Mode:** Select two vehicles to generate a side-by-side comparison table.
* [ ] **Inventory Search:** Integrate with a dealership API to find available cars nearby.

---
*Created by Ishan Gandhi | Carnegie Mellon University*

Disclaimer **
This is a personal project for educational purposes. It is not affiliated with, endorsed by, 
or connected to Mercedes-Benz Group AG or Mercedes-Benz USA.
All trademarks and logos belong to their respective owners.

📄 License
MIT
