# AI-Powered Knowledge Base with pgvector and Sentence Transformer

## Overview
This project utilizes **pgvector** for vector-based storage and retrieval, combined with an **open-source sentence transformer** for text embedding. The default OpenAI embedder requires an API key, which may exceed credit limits; thus, we configure the system to use a **sentence transformer model with 1024 dimensions** instead of the default 1536 dimensions.

### Open-Source PDF Assistant
I have created an **open-source PDF assistant** that eliminates the limitations imposed by OpenAI's embedder. This assistant can be used **without any restrictions**, allowing unlimited queries and document processing.
This project utilizes **pgvector** for vector-based storage and retrieval, combined with an **open-source sentence transformer** for text embedding. The default OpenAI embedder requires an API key, which may exceed credit limits; thus, we configure the system to use a **sentence transformer model with 1024 dimensions** instead of the default 1536 dimensions.

## Setup Instructions

### Prerequisites
- **Docker & Docker Compose** installed
- **Python 3.8+** installed
- **PostgreSQL with pgvector extension** enabled
- **Streamlit** for the frontend

### Running the Project

#### Step 0: Clone the GitHub Repository
First, clone the project repository from GitHub:
```bash
git clone <repository_url>
cd <repository_name>
```
Replace `<repository_url>` with the actual repository link.

#### Step 1: Start pgvector with Docker
Ensure your `docker-compose.yaml` file is correctly set up, then run:
```bash
docker-compose up -d
```

#### Step 2: Configure the Database
After the Docker container is running, execute the following commands:
```bash
docker exec -it <container_id> psql -U root -d mydb
```
Replace `<container_id>` with the actual container ID (can be found using `docker ps`).

Connect to the database:
```sql
\c mydb
```

Check existing tables:
```sql
\dt
```

Drop the existing embeddings table if it exists:
```sql
DROP TABLE IF EXISTS ai.embeddings;
```

Create the new table with **1024-dimensional embeddings**:
```sql
CREATE TABLE ai.embeddings (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    meta_data JSONB,
    filters JSONB,
    content TEXT NOT NULL,
    embedding vector(1024), -- Adjusted to match the embedding model dimensions
    usage JSONB,
    content_hash VARCHAR UNIQUE
);
```

Verify that the table was created successfully:
```sql
\dt ai.*
```

#### Step 3: Install Dependencies
Navigate to your project directory and install required packages:
```bash
pip install -r requirements.txt
```

#### Step 4: Run the Application
Start the Streamlit application:
```bash
streamlit run app.py
```

Once running, open your browser and go to:
```
http://localhost:8501/
```

#### Step 5: Load the Knowledge Base
1. **Add `GROQ_API_KEY`** in the sidebar.
2. **Provide the PDF link** containing knowledge base content.
3. Click **"Load Knowledge Base"**.
4. Once you see the message **"Knowledge Base Loaded Successfully!"**, you can start asking questions.

## Troubleshooting
- If you get an error about mismatched vector dimensions, ensure that the **embedding dimension in PostgreSQL matches the sentence transformer (1024)**.
- If OpenAI is still being used, check that your Python script is correctly configured to use **sentence transformers instead of OpenAI embeddings**.
- Ensure that all required dependencies are installed using `pip install -r requirements.txt`.

## Future Enhancements
- Adding **user authentication** for secure access
- Implementing **cache storage** to speed up repeated queries
- Enhancing **UI/UX** for a more interactive experience

## License
This project is licensed under the MIT License.

## Contributors
- **Your Name** - [Your GitHub](https://github.com/yourgithub)

Feel free to contribute by submitting pull requests or reporting issues!

"# PDF_Assistant" 
