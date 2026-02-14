from pathlib import Path

class Config:
    DB_NAME = str(Path(__file__).parent / "preprocess_db")
    KNOWLEDGE_BASE_PATH = str(Path(__file__).parent / "knowledge-base")
    SUMMERIES_PATH = Path(__file__).parent / "summaries"


