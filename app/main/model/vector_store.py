import chromadb

class VectorStore:
    def __init__(self,app=None, persist_dir = "./chroma_data",collection_name = "document"):
        self.client = chromadb.PersistentClient(persist_dir)
        self.collection = self.client.get_or_create_collection(collection_name)
        print("established chromadb connection successfully")
    
    def add_document(self, doc_id, text, embedding, metadata):
        if metadata is None:
            metadata = {}
        
        self.collection.add(
            ids = [doc_id],
            documents = [text],
            embeddings = [embedding],
            metadatas = [metadata]
        )
    
    def query(self, query_embedding, top_k: int = 5):
        return self.collection.query(
            query_embeddings = [query_embedding],
            n_results= top_k
        )