# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
TRY THESE MODIFICATIONS:

BEGINNER:
1. Add a new endpoint: GET /stats that returns total documents and categories
2. Add input validation: question must not contain special characters
3. Add logging: print query and processing time to console

INTERMEDIATE:
4. Implement pagination for /documents endpoint (skip, limit parameters)
5. Add a filter by similarity_score threshold in search
6. Create an endpoint to update existing documents (PUT /documents/{doc_id})

ADVANCED:
7. Add caching: store query results for 5 minutes
8. Implement batch document upload (accept list of documents)
9. Add authentication: require API key in headers
10. Create a simple HTML frontend that calls this API

DEBUGGING CHALLENGES:
- What happens if you query with an empty string?
- How does the API handle very long documents (10,000+ characters)?
- Test concurrent requests (use threading or asyncio)
- What happens if documents_db is deleted during a query?
"""