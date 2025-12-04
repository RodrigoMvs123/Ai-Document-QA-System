# ============================================================================
# HOW TO RUN THIS CODE
# ============================================================================

"""
SETUP INSTRUCTIONS:

1. Install dependencies:
   pip install fastapi uvicorn pydantic

2. Run the server:
   uvicorn filename:app --reload --host 0.0.0.0 --port 8000

3. Open API documentation:
   http://localhost:8000/docs

4. Test with curl:
   # Query documents
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Python?", "top_k": 2}'
   
   # Add document
   curl -X POST "http://localhost:8000/documents" \
     -H "Content-Type: application/json" \
     -d '{"doc_id": "doc_006", "text": "New document text..."}'
   
   # List documents
   curl "http://localhost:8000/documents"

5. Test with Python:
   import requests
   
   response = requests.post(
       "http://localhost:8000/query",
       json={"question": "What is FastAPI?", "top_k": 3}
   )
   print(response.json())
"""