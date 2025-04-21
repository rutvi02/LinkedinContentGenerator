# LinkedIn Content Creator AI Agent

This project is an AI-powered content assistant that analyzes successful LinkedIn posts and generates context-aware, high-performing variations — personalized to user feedback and trends.

It helps users:
- Understand what content performs well (top hashtags, keywords, post-length)
- Generate viral-ready post variations using RAG (Retrieval-Augmented Generation)
- Improve output quality over time using human-in-the-loop feedback

---

## Features

- **Post Retrieval**: Uses FAISS and SentenceTransformers to retrieve top-performing historical LinkedIn posts by semantic similarity.
- **AI-Powered Generation**: Generates multiple variations of new posts using OpenAI's GPT-4 and contextual examples.
- **RAG Architecture**: Enhances generation quality using retrieval-based prompts grounded in top engagement examples.
- **Feedback Loop**: Users can like/dislike generated posts and leave comments. The system learns from this to improve future output (e.g., this is too generic).
- **Trend Analysis**: Performs exploratory data analysis (EDA) to visualize trends:
  - Most used hashtags and keywords
  - Best time/day to post
  - Ideal post length vs engagement
- **Streamlit UI**: Interactive interface to generate, view, and vote on content with live feedback.
---

## Approach Used

### 1. Scraping & Preprocessing
For Combining Scraped data (`Combining_scrapped_data.ipynb`) - stored in `all_users.csv`
- Scraped data from the provided linkedin profiles using apify's linkedin post scraper

### 2. EDA (`trend_analysis.ipynb`)

- Cleaned and preprocessed to remove noise
- Calculated engagement scores for filtering top-performing posts
- `'engagement' = 'likes' + 'support' + 'love' + 'insight' + 'celebrate' + (2 * 'comments') + (2 * 'reposts') ` - (Giving more importance to comments and reposts for engagement consideration)
- Extracted top 100 posts for further analysis based on the engagement score

In-depth analysis on the top scraped LinkedIn posts:
- **Top Hashtags and keywords** by frequency
- **Best Times to Post** (part_of_the_day)
- **Post Length vs Engagement** (words vs engagement)
- **Media Type Effect** (mostly images or videos)

### 3. Embedding & Retrieval (`fgTask.py`)
- `SentenceTransformer` embeddings stored in FAISS index (`linkedin_post_index.faiss`) and text embeddings (`linkedin_top_texts.pkl`)
- Real-time similarity search retrieves semantically similar posts based on the user entered topic

- High-engagement LinkedIn posts are embedded using SentenceTransformer (`all-MiniLM-L6-v2`) and stored in a FAISS vector index (`linkedin_post_index.faiss`), with corresponding post texts in `linkedin_top_texts.pkl`.
- When a user enters a new topic or idea, the system performs real-time semantic similarity search to retrieve the top k most relevant historical posts from the index.
- These retrieved examples are then used as context in the RAG-based generation step to guide tone, structure, and content relevance of the AI-generated post.

### 4. RAG-Based Post Generation

The system uses Retrieval-Augmented Generation (RAG) to create high-quality, relevant LinkedIn posts:
- It first retrieves top-performing historical posts similar to the user-entered topic using the FAISS index.
- These examples are embedded directly into the prompt, serving as the base context for the language model (GPT-4).

**Trend analysis results (from EDA)** — such as most used hashtags, optimal post length, and most used keywords — are incorporated into prompt construction to align with what has historically driven engagement.

Two distinct system prompts guide for generating different variants:
- Brand-focused: Promotes the business value of Fuelgrowth, tailored for potential clients or partners.
- Founder-focused: Shares lessons, milestones, and experiences from the founder's journey.

The result is a post that’s context-aware, trend-informed, and tailored to the audience’s expectations.


### 5. Feedback Loop
- Users submit 👍/👎 and optional notes
- Logs stored in `simple_feedback_log.csv`
- The stored responses are analyzed to detect patterns (e.g., "too generic", "vague")
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

