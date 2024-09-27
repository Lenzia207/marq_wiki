import os

class Config:
    DATA_PATH = os.getenv('DATA_PATH', './src/data')
    CHROMA_PATH = os.getenv('CHROMA_PATH', './src/db/chroma')