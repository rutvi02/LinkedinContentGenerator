# LinkedIn Content Creator AI Agent

This project is an AI-powered content assistant that analyzes successful LinkedIn posts and generates context-aware, high-performing variations — personalized to user feedback and trends.

It helps users:
- Understand what content performs well (top hashtags, keywords, post-length)
- Generate viral-ready post variations using RAG (Retrieval-Augmented Generation)
- Improve output quality over time using human-in-the-loop feedback

---

## Features

- ✅ **Post Retrieval**: Uses FAISS and SentenceTransformers to retrieve top-performing historical LinkedIn posts by semantic similarity.
- ✅ **AI-Powered Generation**: Generates multiple variations of new posts using OpenAI's GPT-4 and contextual examples.
- ✅ **RAG Architecture**: Enhances generation quality using retrieval-based prompts grounded in top engagement examples.
- ✅ **Feedback Loop**: Users can like/dislike generated posts and leave comments. The system learns from this to improve future output (e.g., this is too generic).
- ✅ **Trend Analysis**: Performs exploratory data analysis (EDA) to visualize trends:
  - Most used hashtags and keywords
  - Best time/day to post
  - Ideal post length vs engagement
- ✅ **Streamlit UI**: Interactive interface to generate, view, and vote on content with live feedback.

---

## Exploratory Analysis (`FG_trend_analysis.ipynb`)

The project performs in-depth analysis on scraped LinkedIn posts:

- **Top Hashtags and keywords** by frequency
- **Best Times to Post** (part_of_the_day)
- **Post Length vs Engagement** (words vs engagement)
- **Media Type Effect** (mostly images or videos)

---

## Approach Used

### 1. Scraping & Preprocessing (`FG_task.ipynb`)
- Scraped data from the provided linkedin profiles using apify's linkedin post scraper
- Cleaned and preprocessed to remove noise
- Engagement scores used to filter top-performing posts

### 2. Embedding & Retrieval (`fgTask.py`)
- `SentenceTransformer` embeddings stored in FAISS index
- Real-time similarity search retrieves semantically similar posts based on the user entered topic

### 3. RAG-Based Post Generation
- Contextual examples used in prompt
- Two system prompts generate:
  - **Brand-focused** content (promoting the business value of Fuelgrowth)
  - **Founder-focused** content (highlighting Founder's journey and success)

### 4. Feedback Loop
- Users submit 👍/👎 and optional notes
- Logs stored in `simple_feedback_log.csv`
- Notes are analyzed to detect patterns (e.g., "too generic", "vague")
- Future prompts are dynamically enhanced based on feedback

---

## Sample Output

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt


.
├── app.py                      # Streamlit app entrypoint
├── .streamlit/secrets.toml     # OpenAI key (local only)
├── requirements.txt
├── feedback_log.csv            # Stores user feedback
├── linkedin_posts_index.faiss  # FAISS index of post embeddings
├── linkedin_top_texts.pkl      # Cleaned high-engagement texts
└── .vscode/settings.json       # (optional) Interpreter config

