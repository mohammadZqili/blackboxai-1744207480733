import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Retriever:
    def __init__(self):
        # Initialize the sentence transformer model for encoding text
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize storage paths
        self.storage_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.index_path = os.path.join(self.storage_dir, 'faiss_index')
        self.documents_path = os.path.join(self.storage_dir, 'documents.json')
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Initialize or load the FAISS index and documents
        self.initialize_storage()

    def initialize_storage(self):
        """Initialize or load the FAISS index and documents."""
        if os.path.exists(self.documents_path):
            with open(self.documents_path, 'r') as f:
                self.documents = json.load(f)
        else:
            self.documents = []

        # Initialize FAISS index
        self.dimension = 384  # Dimension of sentence embeddings
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def save_storage(self):
        """Save the current state of the index and documents."""
        with open(self.documents_path, 'w') as f:
            json.dump(self.documents, f)
        faiss.write_index(self.index, self.index_path)

    def add_interaction(self, query, response, feedback=None):
        """Add a new interaction to the knowledge base."""
        document = {
            'text': f"Query: {query}\nResponse: {response}",
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback
        }
        
        # Add to documents list
        self.documents.append(document)
        
        # Add to FAISS index
        embedding = self.model.encode([document['text']])[0]
        self.index.add(np.array([embedding]).astype('float32'))
        
        # Save the updated storage
        self.save_storage()

    def retrieve(self, user_input, k=3):
        """Retrieve relevant documents based on user input."""
        if self.index.ntotal == 0:
            return "No previous interactions available."

        # Encode the user input
        query_vector = self.model.encode([user_input])[0]
        
        # Search the FAISS index
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), k)
        
        # Retrieve the most relevant documents
        relevant_docs = [self.documents[i] for i in indices[0]]
        
        # Format the context
        context = "\n\n".join([doc['text'] for doc in relevant_docs])
        
        return context

    def get_interaction_history(self):
        """Return the full interaction history."""
        return self.documents
