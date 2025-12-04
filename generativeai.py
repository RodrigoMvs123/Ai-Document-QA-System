"""
JUNIOR AI ENGINEER - COMPLETE CODING PRACTICE EXERCISE
Practice all key concepts: FastAPI, RAG, Embeddings, Error Handling, Git
"""

from fastapi import FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import json
from datetime import datetime, timedelta
import math
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

app = FastAPI(
    title="AI Document QA System",
    description="RAG-based question answering API",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ============================================================================
# PYDANTIC MODELS (Data Validation)
# ============================================================================

class Document(BaseModel):
    """Document model with validation"""
    doc_id: str = Field(..., min_length=1, description="Unique document ID")
    text: str = Field(..., min_length=10, description="Document content")
    metadata: Optional[Dict] = Field(default={}, description="Additional info")
    
    @validator('doc_id')
    def validate_doc_id(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('doc_id must be alphanumeric with _ or -')
        return v

class Query(BaseModel):
    """Query model"""
    question: str = Field(..., min_length=5, description="User question")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of results")
    include_sources: bool = Field(default=True, description="Include source docs")
    
    @validator('question')
    def validate_question(cls, v):
        """Validate that question doesn't contain special characters"""
        # Allow: letters, numbers, spaces, and basic punctuation (. , ? !)
        import re
        if not re.match(r'^[a-zA-Z0-9\s.,?!\-]+$', v):
            raise ValueError(
                'Question must only contain letters, numbers, spaces, and basic punctuation (. , ? ! -)'
            )
        return v

class SearchResult(BaseModel):
    """Single search result"""
    doc_id: str
    text: str
    similarity_score: float
    metadata: Dict

class Answer(BaseModel):
    """API response model"""
    question: str
    answer: str
    sources: List[SearchResult]
    timestamp: str
    processing_time_ms: float

# ============================================================================
# MOCK DATABASE (In production, use PostgreSQL/MongoDB)
# ============================================================================

# Document storage
documents_db: Dict[str, Document] = {}

# Query cache storage (Exercise 7)
# Structure: {cache_key: {"result": Answer, "timestamp": datetime}}
query_cache: Dict[str, Dict] = {}
CACHE_TTL_MINUTES = 5  # Cache time-to-live: 5 minutes

# API Key Authentication (Exercise 9)
# In production: store in environment variables or secure vault
VALID_API_KEYS = {
    "demo-key-12345": "Demo User",
    "test-key-67890": "Test User",
    "admin-key-abcde": "Admin User"
}

# Pre-populate with sample data
SAMPLE_DOCS = [
    {
        "doc_id": "doc_001",
        "text": "Python is a high-level programming language known for its simplicity and readability. It is widely used in AI and machine learning.",
        "metadata": {"category": "programming", "language": "python"}
    },
    {
        "doc_id": "doc_002",
        "text": "FastAPI is a modern web framework for building APIs with Python. It uses type hints and provides automatic API documentation.",
        "metadata": {"category": "frameworks", "language": "python"}
    },
    {
        "doc_id": "doc_003",
        "text": "RAG (Retrieval-Augmented Generation) combines document retrieval with LLM generation to provide accurate, context-aware answers.",
        "metadata": {"category": "ai", "technique": "rag"}
    },
    {
        "doc_id": "doc_004",
        "text": "Vector databases store embeddings and enable semantic search. Popular options include Pinecone, FAISS, and ChromaDB.",
        "metadata": {"category": "databases", "type": "vector"}
    },
    {
        "doc_id": "doc_005",
        "text": "Docker containers package applications with dependencies, ensuring consistency across development and production environments.",
        "metadata": {"category": "devops", "tool": "docker"}
    }
]

# Initialize database
for doc_data in SAMPLE_DOCS:
    doc = Document(**doc_data)
    documents_db[doc.doc_id] = doc

# ============================================================================
# CACHE FUNCTIONS (Exercise 7)
# ============================================================================

def generate_cache_key(question: str, top_k: int) -> str:
    """
    Generate a unique cache key based on query parameters.
    Uses MD5 hash of question + top_k for consistent keys.
    """
    cache_string = f"{question.lower().strip()}_{top_k}"
    return hashlib.md5(cache_string.encode()).hexdigest()

def get_cached_result(cache_key: str) -> Optional[Dict]:
    """
    Retrieve cached result if it exists and hasn't expired.
    Returns None if cache miss or expired.
    """
    if cache_key not in query_cache:
        return None
    
    cached_entry = query_cache[cache_key]
    cache_time = cached_entry["timestamp"]
    
    # Check if cache has expired
    if datetime.now() - cache_time > timedelta(minutes=CACHE_TTL_MINUTES):
        # Cache expired, remove it
        del query_cache[cache_key]
        return None
    
    return cached_entry["result"]

def set_cached_result(cache_key: str, result: Dict):
    """
    Store result in cache with current timestamp.
    """
    query_cache[cache_key] = {
        "result": result,
        "timestamp": datetime.now()
    }

def clear_expired_cache():
    """
    Remove all expired cache entries.
    Called periodically to prevent memory bloat.
    """
    current_time = datetime.now()
    expired_keys = [
        key for key, value in query_cache.items()
        if current_time - value["timestamp"] > timedelta(minutes=CACHE_TTL_MINUTES)
    ]
    for key in expired_keys:
        del query_cache[key]

# ============================================================================
# AUTHENTICATION FUNCTIONS (Exercise 9)
# ============================================================================

def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request headers (Exercise 9).
    
    Usage: Add as dependency to protected endpoints
    Example: def my_endpoint(api_key: str = Depends(verify_api_key))
    
    Header format: X-API-Key: your-api-key-here
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Include 'X-API-Key' header."
        )
    
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    # Return the user associated with this key
    return VALID_API_KEYS[x_api_key]

# ============================================================================
# EMBEDDING FUNCTIONS (Mock Implementation)
# ============================================================================

def generate_embedding(text: str) -> List[float]:
    """
    Generate mock embedding vector.
    In production: use OpenAI embeddings, HuggingFace, or sentence-transformers
    
    Example with OpenAI:
    import openai
    response = openai.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
    """
    # Simple mock: convert text to numerical representation
    # Real embeddings are 768-1536 dimensions
    words = text.lower().split()
    embedding = []
    
    for i in range(5):  # Mock 5-dimensional embedding
        value = sum(ord(c) for c in words[i % len(words)]) / 1000
        embedding.append(round(value, 4))
    
    return embedding

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    Formula: cos(θ) = (A · B) / (||A|| × ||B||)
    Returns: value between 0 and 1 (1 = identical)
    """
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)
    return round(similarity, 4)

# ============================================================================
# RAG PIPELINE FUNCTIONS
# ============================================================================

def retrieve_documents(query: str, top_k: int = 3) -> List[SearchResult]:
    """
    STEP 1: RETRIEVAL
    Find most relevant documents using embedding similarity
    """
    if not documents_db:
        raise ValueError("Document database is empty")
    
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # Calculate similarity with all documents
    results = []
    for doc_id, doc in documents_db.items():
        doc_embedding = generate_embedding(doc.text)
        similarity = cosine_similarity(query_embedding, doc_embedding)
        
        results.append({
            "doc_id": doc.doc_id,
            "text": doc.text,
            "similarity": similarity,
            "metadata": doc.metadata
        })
    
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Return top_k results
    top_results = results[:top_k]
    
    return [
        SearchResult(
            doc_id=r["doc_id"],
            text=r["text"],
            similarity_score=r["similarity"],
            metadata=r["metadata"]
        )
        for r in top_results
    ]

def generate_answer(query: str, context_docs: List[SearchResult]) -> str:
    """
    STEP 2: GENERATION
    Generate answer using retrieved context.
    In production: call OpenAI/Anthropic API
    
    Example with OpenAI:
    import openai
    context = "\n".join([doc.text for doc in context_docs])
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
    )
    return response.choices[0].message.content
    """
    # Mock answer generation
    context = " ".join([doc.text for doc in context_docs])
    
    # Simple answer template
    answer = (
        f"Based on the available information: {context[:200]}... "
        f"This relates to your question about '{query}'. "
        f"The most relevant information comes from {len(context_docs)} source(s)."
    )
    
    return answer

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "total_documents": len(documents_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/cache/stats", tags=["Cache"])
def get_cache_stats():
    """
    Get cache statistics (Exercise 7).
    Shows number of cached queries and their details.
    """
    # Clean expired entries first
    clear_expired_cache()
    
    cache_entries = []
    for key, value in query_cache.items():
        age_seconds = (datetime.now() - value["timestamp"]).total_seconds()
        cache_entries.append({
            "cache_key": key,
            "question": value["result"]["question"],
            "age_seconds": round(age_seconds, 2),
            "expires_in_seconds": round((CACHE_TTL_MINUTES * 60) - age_seconds, 2)
        })
    
    return {
        "total_cached_queries": len(query_cache),
        "cache_ttl_minutes": CACHE_TTL_MINUTES,
        "cached_entries": cache_entries
    }

@app.delete("/cache", tags=["Cache"])
def clear_cache():
    """
    Clear all cached query results (Exercise 7).
    Useful for testing or forcing fresh results.
    """
    count = len(query_cache)
    query_cache.clear()
    return {
        "message": "Cache cleared successfully",
        "entries_removed": count
    }

@app.get("/auth/keys", tags=["Authentication"])
def list_api_keys():
    """
    List valid API keys for testing (Exercise 9).
    WARNING: In production, NEVER expose API keys like this!
    This is only for demonstration purposes.
    """
    return {
        "message": "Valid API keys for testing",
        "keys": [
            {"key": key, "user": user}
            for key, user in VALID_API_KEYS.items()
        ],
        "usage": "Include in request header as: X-API-Key: your-key-here"
    }

@app.get("/protected/example", tags=["Authentication"])
def protected_endpoint_example(user: str = Header(None, alias="X-API-Key")):
    """
    Example of a protected endpoint (Exercise 9).
    Requires valid API key in X-API-Key header.
    """
    # Verify API key
    if user not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    
    return {
        "message": "Access granted!",
        "user": VALID_API_KEYS[user],
        "note": "This endpoint requires authentication"
    }

@app.get("/stats", tags=["Health"])
def get_stats():
    """
    Get database statistics including total documents and categories.
    
    Returns:
    - total_documents: Total number of documents in the database
    - categories: List of unique categories with document counts
    - timestamp: Current server timestamp
    """
    # Count documents by category
    category_counts = {}
    for doc in documents_db.values():
        category = doc.metadata.get("category", "uncategorized")
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        "total_documents": len(documents_db),
        "categories": category_counts,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/documents", status_code=status.HTTP_201_CREATED, tags=["Documents"])
def add_document(document: Document):
    """
    Add a new document to the database.
    
    Example request:
    {
        "doc_id": "doc_006",
        "text": "Kubernetes orchestrates containerized applications...",
        "metadata": {"category": "devops"}
    }
    """
    try:
        # Check if document already exists
        if document.doc_id in documents_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document {document.doc_id} already exists"
            )
        
        # Add to database
        documents_db[document.doc_id] = document
        
        return {
            "message": "Document added successfully",
            "doc_id": document.doc_id,
            "text_length": len(document.text)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding document: {str(e)}"
        )

@app.post("/documents/batch", status_code=status.HTTP_201_CREATED, tags=["Documents"])
def add_documents_batch(documents: List[Document]):
    """
    Add multiple documents at once (Exercise 8).
    
    Example request:
    [
        {
            "doc_id": "doc_006",
            "text": "First document...",
            "metadata": {"category": "test"}
        },
        {
            "doc_id": "doc_007",
            "text": "Second document...",
            "metadata": {"category": "test"}
        }
    ]
    """
    results = {
        "successful": [],
        "failed": [],
        "total_processed": len(documents)
    }
    
    for doc in documents:
        try:
            # Check if document already exists
            if doc.doc_id in documents_db:
                results["failed"].append({
                    "doc_id": doc.doc_id,
                    "error": f"Document {doc.doc_id} already exists"
                })
                continue
            
            # Add to database
            documents_db[doc.doc_id] = doc
            results["successful"].append({
                "doc_id": doc.doc_id,
                "text_length": len(doc.text)
            })
            
        except Exception as e:
            results["failed"].append({
                "doc_id": doc.doc_id,
                "error": str(e)
            })
    
    return {
        "message": f"Batch upload completed: {len(results['successful'])} successful, {len(results['failed'])} failed",
        "successful_count": len(results["successful"]),
        "failed_count": len(results["failed"]),
        "results": results
    }

@app.get("/documents", tags=["Documents"])
def list_documents(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """
    List all documents with pagination, optionally filtered by category.
    
    Parameters:
    - category: Filter by category (optional)
    - skip: Number of documents to skip (default: 0)
    - limit: Maximum number of documents to return (default: 10, max: 100)
    
    Examples:
    - GET /documents?skip=0&limit=5  (first 5 documents)
    - GET /documents?skip=5&limit=5  (next 5 documents)
    - GET /documents?category=programming&limit=3
    """
    # Validate pagination parameters
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip must be >= 0"
        )
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be between 1 and 100"
        )
    
    docs = list(documents_db.values())
    
    # Filter by category if provided
    if category:
        docs = [d for d in docs if d.metadata.get("category") == category]
    
    total = len(docs)
    
    # Apply pagination
    paginated_docs = docs[skip:skip + limit]
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "count": len(paginated_docs),
        "documents": [
            {
                "doc_id": doc.doc_id,
                "text_preview": doc.text[:100] + "...",
                "metadata": doc.metadata
            }
            for doc in paginated_docs
        ]
    }

@app.get("/documents/{doc_id}", tags=["Documents"])
def get_document(doc_id: str):
    """Get a specific document by ID"""
    if doc_id not in documents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {doc_id} not found"
        )
    
    return documents_db[doc_id]

@app.delete("/documents/{doc_id}", tags=["Documents"])
def delete_document(doc_id: str):
    """Delete a document"""
    if doc_id not in documents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {doc_id} not found"
        )
    
    deleted_doc = documents_db.pop(doc_id)
    return {
        "message": "Document deleted successfully",
        "doc_id": doc_id
    }

@app.put("/documents/{doc_id}", tags=["Documents"])
def update_document(doc_id: str, document: Document):
    """
    Update an existing document.
    
    Parameters:
    - doc_id: The ID of the document to update (in URL path)
    - document: The new document data (in request body)
    
    Note: The doc_id in the URL must match the doc_id in the request body.
    
    Example:
    PUT /documents/doc_001
    {
        "doc_id": "doc_001",
        "text": "Updated text content...",
        "metadata": {"category": "updated"}
    }
    """
    # Check if document exists
    if doc_id not in documents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {doc_id} not found"
        )
    
    # Verify doc_id in body matches URL parameter
    if document.doc_id != doc_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document ID in body ({document.doc_id}) must match URL parameter ({doc_id})"
        )
    
    # Store old document for response
    old_doc = documents_db[doc_id]
    
    # Update the document
    documents_db[doc_id] = document
    
    return {
        "message": "Document updated successfully",
        "doc_id": doc_id,
        "old_text_length": len(old_doc.text),
        "new_text_length": len(document.text),
        "metadata_updated": old_doc.metadata != document.metadata
    }

@app.post("/query", response_model=Answer, tags=["RAG"])
def query_documents(query: Query):
    """
    Main RAG endpoint: Query documents and get AI-generated answer.
    With caching: Results are cached for 5 minutes (Exercise 7).
    
    Example request:
    {
        "question": "What is FastAPI?",
        "top_k": 3,
        "include_sources": true
    }
    """
    start_time = datetime.now()
    
    # LOG: Query received
    print(f"\n{'='*60}")
    print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] NEW QUERY RECEIVED")
    print(f"Question: {query.question}")
    print(f"Top K: {query.top_k}")
    print(f"{'='*60}")
    
    # CACHE: Check if result is cached (Exercise 7)
    cache_key = generate_cache_key(query.question, query.top_k)
    cached_result = get_cached_result(cache_key)
    
    if cached_result:
        print(f"[CACHE HIT] Returning cached result")
        print(f"{'='*60}\n")
        # Return cached result (update timestamp to current)
        cached_result["timestamp"] = datetime.now().isoformat()
        return Answer(**cached_result)
    
    try:
        # Validate input
        if not documents_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No documents in database. Please add documents first."
            )
        
        # STEP 1: Retrieve relevant documents
        relevant_docs = retrieve_documents(query.question, query.top_k)
        
        if not relevant_docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant documents found for this query"
            )
        
        # STEP 2: Generate answer using context
        answer_text = generate_answer(query.question, relevant_docs)
        
        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        # LOG: Query completed
        print(f"\n[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] QUERY COMPLETED")
        print(f"Processing Time: {round(processing_time, 2)} ms")
        print(f"Documents Retrieved: {len(relevant_docs)}")
        print(f"Answer Length: {len(answer_text)} characters")
        print(f"{'='*60}\n")
        
        # Prepare response
        sources = relevant_docs if query.include_sources else []
        
        result = Answer(
            question=query.question,
            answer=answer_text,
            sources=sources,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
        
        # CACHE: Store result in cache (Exercise 7)
        set_cached_result(cache_key, result.dict())
        print(f"[CACHE STORED] Result cached for {CACHE_TTL_MINUTES} minutes")
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/search", tags=["Search"])
def semantic_search(
    q: str,
    limit: int = 5,
    min_score: float = 0.0
):
    """
    Simple semantic search without answer generation.
    
    Parameters:
    - q: Search query (minimum 3 characters)
    - limit: Maximum number of results (default: 5)
    - min_score: Minimum similarity score threshold (0.0 to 1.0, default: 0.0)
    
    Examples:
    - GET /search?q=docker&limit=3
    - GET /search?q=python&min_score=0.7  (only results with score >= 0.7)
    - GET /search?q=fastapi&limit=5&min_score=0.5
    """
    try:
        if not q or len(q) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query must be at least 3 characters"
            )
        
        # Validate min_score
        if min_score < 0.0 or min_score > 1.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_score must be between 0.0 and 1.0"
            )
        
        results = retrieve_documents(q, top_k=limit)
        
        # Filter by minimum similarity score
        filtered_results = [
            result for result in results
            if result.similarity_score >= min_score
        ]
        
        return {
            "query": q,
            "min_score": min_score,
            "total_results": len(filtered_results),
            "results": filtered_results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}"
        )


