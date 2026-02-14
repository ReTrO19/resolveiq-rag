from pydantic import BaseModel, Field
from langchain_core.documents import Document

class Result(BaseModel):
    page_content: str
    metadata: dict

class Chunk(BaseModel):
    headline: str = Field(
        description="A brief heading for this chunk, typically a few words, that" \
        "is most likely to be surfaced in a query"
    )
    summary: str = Field(
        description="A few sentence summarizing the content of this chunk to answer" \
        "common questions"
    )
    original_text: str = Field(
        description="The orignal text of the chunk from the document, exactly as is," \
        "not changed in any way"
    )

    def as_result(self, document):
        metadata = {"source":document.metadata["source"], "type":document.metadata["type"]}

        return Document(
            page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata
        )
    
class Chunks(BaseModel):
    chunks: list[Chunk]

class RankOrder(BaseModel):
	order: list[int] = Field(
		description="The order of releavence of chunks, from most relevent to least relevant, by chunk id number"
	)