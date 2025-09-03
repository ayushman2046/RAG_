

from app.config import get_config_by_name
import openai,os


class Embeddings:
    def __init__(self,app):
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = "text-embedding-3-small"
    
    def generate_embeddings(self,text = None):
        response = self.client.embeddings.create(
            input = text,
            model = self.model_name
        )
        return response.data[0].embedding