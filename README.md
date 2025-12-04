# 🤖 AI Document QA System

A complete RAG (Retrieval-Augmented Generation) system for document question-answering with semantic search, built with FastAPI and vanilla JavaScript.

**Project Live at:**
- https://ai-document-qa-system.vercel.app/ 

## 🚀 Features

- **RAG Question Answering**: Ask questions and get AI-generated answers with source citations
- **Semantic Search**: Find documents using similarity-based search
- **Document Management**: Full CRUD operations for documents
- **Query Caching**: 5-minute cache for improved performance
- **Batch Operations**: Upload multiple documents at once
- **API Authentication**: API key-based authentication
- **Pagination**: Efficient document listing with skip/limit
- **Input Validation**: Secure input validation with Pydantic
- **Interactive Frontend**: Beautiful web interface for all features
- **Comprehensive Logging**: Track queries and performance

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2. Start the Backend

```bash
python -m uvicorn generativeai:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### 3. Open the Frontend

Simply open `frontend/index.html` in your web browser.

That's it! 🎉

## 🏗️ Project Structure

```
.
├── generativeai.py          # Main FastAPI application
├── frontend/
│   └── index.html          # Interactive web interface
├── docs/                   # Documentation files
│   ├── exercise1_stats_endpoint.txt
│   ├── exercise2_input_validation.txt
│   ├── exercise3_logging.txt
│   ├── exercise4_pagination.txt
│   ├── exercise5_similarity_filter.txt
│   ├── exercise6_update_document.txt
│   ├── exercise7_caching.txt
│   ├── exercise8_batch_upload.txt
│   ├── exercise9_authentication.txt
│   └── exercise10_html_frontend.txt
├── tests/                  # Test output files
│   ├── test1_query_documents.txt
│   ├── test2_add_document.txt
│   ├── test3_list_documents.txt
│   ├── test4_health_check.txt
│   └── test5_python_query.txt
├── exercises.md            # Practice exercises
├── instructions.md         # Setup instructions
└── README.md              # This file
```

## 🔧 Backend API

### Core Endpoints

#### Health & Statistics
- `GET /` - Health check
- `GET /stats` - Database statistics with category breakdown

#### Documents (CRUD)
- `POST /documents` - Add a single document
- `POST /documents/batch` - Add multiple documents at once
- `GET /documents` - List all documents (with pagination)
- `GET /documents/{doc_id}` - Get specific document
- `PUT /documents/{doc_id}` - Update existing document
- `DELETE /documents/{doc_id}` - Delete document

#### Search & Query
- `POST /query` - RAG question answering (main feature)
- `GET /search` - Semantic search with similarity filtering

#### Cache Management
- `GET /cache/stats` - View cache statistics
- `DELETE /cache` - Clear all cached results

#### Authentication
- `GET /auth/keys` - List valid API keys (demo only)
- `GET /protected/example` - Example protected endpoint

### Example API Calls

#### Ask a Question (RAG)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "top_k": 3,
    "include_sources": true
  }'
```

#### Add a Document
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "doc_010",
    "text": "Your document text here (minimum 10 characters)",
    "metadata": {"category": "programming"}
  }'
```

#### List Documents with Pagination
```bash
curl "http://localhost:8000/documents?skip=0&limit=5"
```

#### Semantic Search with Similarity Filter
```bash
curl "http://localhost:8000/search?q=docker&min_score=0.8&limit=5"
```

#### Batch Upload Documents
```bash
curl -X POST "http://localhost:8000/documents/batch" \
  -H "Content-Type: application/json" \
  -d '[
    {"doc_id": "doc_011", "text": "First document content..."},
    {"doc_id": "doc_012", "text": "Second document content..."}
  ]'
```

#### Protected Endpoint (with API Key)
```bash
curl "http://localhost:8000/protected/example" \
  -H "X-API-Key: demo-key-12345"
```

### Valid API Keys (Demo)
- `demo-key-12345` - Demo User
- `test-key-67890` - Test User
- `admin-key-abcde` - Admin User

⚠️ **Note**: In production, use environment variables for API keys!

## 🎨 Frontend

The frontend is a single-page application built with vanilla JavaScript (no frameworks required).

### Features
- ✅ Ask questions and get AI answers
- ✅ Add and manage documents
- ✅ View statistics and analytics
- ✅ Semantic search with filters
- ✅ Cache management
- ✅ Responsive design (mobile-friendly)
- ✅ Real-time error handling
- ✅ Beautiful gradient UI

### Usage
1. Make sure the backend is running on port 8000
2. Open `frontend/index.html` in any modern browser
3. Start interacting with the API through the UI

No build process or npm install required!

## 🧪 Testing

### Using the Interactive Docs
Visit http://localhost:8000/docs to test all endpoints interactively.

### Using Python
```python
import requests

# Query documents
response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "What is FastAPI?",
        "top_k": 3
    }
)
print(response.json())
```

### Using curl
See the `tests/` directory for example curl commands and expected outputs.

## 🔑 Key Technologies

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

### Frontend
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Fetch API**: Modern HTTP requests
- **CSS3**: Gradient backgrounds and animations

### AI/ML Concepts
- **RAG**: Retrieval-Augmented Generation
- **Embeddings**: Vector representations of text (mock implementation)
- **Cosine Similarity**: Measure document relevance
- **Semantic Search**: Meaning-based search (not keyword-based)

## 📊 Features Breakdown

### 1. RAG Question Answering
- Retrieves relevant documents using semantic search
- Generates context-aware answers
- Provides source citations with similarity scores
- Caches results for 5 minutes

### 2. Document Management
- Add, update, delete documents
- Batch upload for efficiency
- Pagination for large datasets
- Category-based filtering

### 3. Semantic Search
- Similarity-based search (not keyword matching)
- Adjustable similarity threshold (0.0 to 1.0)
- Returns documents with relevance scores

### 4. Caching System
- 5-minute TTL (Time To Live)
- Automatic cache invalidation
- Cache statistics endpoint
- Manual cache clearing

### 5. Authentication
- API key-based authentication
- Header-based: `X-API-Key: your-key-here`
- Protected endpoint examples
- Role-based access (extensible)

### 6. Input Validation
- Pydantic models for type safety
- Custom validators (e.g., no special characters)
- Automatic error messages
- HTTP 422 for validation errors

### 7. Logging
- Console logging for all queries
- Processing time tracking
- Request/response logging
- Timestamp for each operation

## 🚀 Production Deployment

### Recommended Improvements

1. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Embeddings**: Use real embeddings (OpenAI, HuggingFace)
3. **Vector DB**: Use Pinecone, FAISS, or ChromaDB
4. **LLM Integration**: Connect to OpenAI/Anthropic API
5. **Caching**: Use Redis for distributed caching
6. **Authentication**: Implement OAuth2/JWT
7. **HTTPS**: Enable SSL/TLS
8. **Docker**: Containerize the application
9. **Monitoring**: Add Datadog, New Relic, or Sentry
10. **Testing**: Add unit, integration, and E2E tests

### Environment Variables
```bash
# .env file
API_KEY_1=your-secret-key-here
API_KEY_2=another-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "generativeai:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Documentation

Detailed documentation for each feature is available in the `docs/` directory:

- **Exercise 1**: GET /stats endpoint
- **Exercise 2**: Input validation
- **Exercise 3**: Logging
- **Exercise 4**: Pagination
- **Exercise 5**: Similarity filtering
- **Exercise 6**: Update documents (PUT)
- **Exercise 7**: Caching
- **Exercise 8**: Batch upload
- **Exercise 9**: Authentication
- **Exercise 10**: HTML frontend

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)

## 🙏 Acknowledgments

Built as a comprehensive learning project covering:
- Backend API development
- AI/ML concepts (RAG, embeddings, semantic search)
- Frontend development
- Production best practices

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ and FastAPI**
