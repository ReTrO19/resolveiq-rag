from langchain_chroma import Chroma
from config import Config
import constants as const
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tenacity import retry, wait_fixed
from prompts import SystemPrompts
from typing import List
from pydantic_store import Result, RankOrder
from dotenv import load_dotenv
import os


load_dotenv(override=True)


embeddings = OpenAIEmbeddings(model=const.EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=Config.DB_NAME, embedding_function=embeddings)

vectorstore = Chroma(
    persist_directory="./preprocess_db",
    embedding_function=embeddings
)

llm = ChatOpenAI(
	model=const.MODEL_NAME,
	temperature=0
)

def make_rag_message(question, history, chunks):
	try:
		print("Starting Make Rag message")
		rag_prompt = ChatPromptTemplate.from_messages([
			("system", SystemPrompts.CORE_SYSTEM_PROMPT),
			MessagesPlaceholder(variable_name="history"),
			("human", question)
		])

		context = "\n\n".join(
			f"Extract from {chunk.metadata.get('source', 'Unknown')}:\n{chunk.page_content}" for chunk in chunks
		)

		messages = rag_prompt.format_messages(
			context=context,
			history=history,
			question=question
		)

		return messages
	except Exception as err:
		raise RuntimeError(f"Error in make rag message module : {err}")
		


# @retry(wait=wait_fixed(2))
def rerank(question:str, chunk: list[Result]):
	ranked_chunks = []
	try:
		print("Start Reranked")
		if len(chunk) > 0:
			structured_llm = llm.with_structured_output(RankOrder)
			# parser = PydanticOutputParser(pydantic_object=RankOrder)
			chunk_block = ""
			chunk_block = f"The user has asked the following question:\n\n{question}\n\nOrder all the chunks of text by relevance to the question, from most relevant to least relevant. Include all the chunk ids you are provided with, reranked. \n\n"
			chunk_block += f"Here are the chunks:\n\n"
			for idx, chuk in enumerate(chunk):
				chunk_block += f"""\n\n#Chunk ID: {idx + 1}:\n\n{chuk.page_content}"""
			chunk_block += "Reply only with the list of ranked chunk ids, noting else. If no chunk detail was provided you can reply with an empty list."

			print("Chunk Block :", chunk_block)

			prompt = ChatPromptTemplate.from_messages([
				("system", SystemPrompts.RERANK_SYSTEM_PROMPT),
				("human", chunk_block)
			])

			chain = prompt | structured_llm

			response: RankOrder = chain.invoke({})

			print("Response :", response, response.order)
			# print("Chunks :", chunk)
			ranked_chunks = [chunk[i-1] for i in response.order]

		return ranked_chunks
	except Exception as err:
		raise RuntimeError(f"Error in rerank module : {err}")

def rewrite_query(question: str, history: list=[]) -> str:
	try:
		print("Started Rewrite Query")
		user_prompt = """This is the history of your conversation so far with user:
		{history}
		And this is the user's current question:
		{question}"""

		print("Rewrite User Prompt:",question, history)

		prompt = ChatPromptTemplate.from_messages([
			("system", SystemPrompts.REWRITE_QUERY_PROMPT),
			("human", user_prompt)
		])

		chain = prompt | llm

		response = chain.invoke({
			"question":question,
			"history":history
		})

		return response.content.strip()
	except Exception as err:
		raise RuntimeError(f"Error in rewrite query module : {err}")
		

def merge_chunks(chunks, reranked):
	try:
		print("Started Merge Chunks")
		merged = chunks[:]
		existing = [chunk.page_content for chunk in chunks]
		for chunk in reranked:
			if chunk.page_content not in existing:
				merged.append(chunk)
		return merged
	except Exception as err:
		raise RuntimeError(f"Error in merge chunk module : {err}")

def fetch_context_unranked(question: str) -> List[Result]:
	print("Started Fetch Context Unranked")
	try:
		retriever = vectorstore.as_retriever(
			search_kwargs={"k": const.RETRIEVAL_K}
		)
		# print("Retriever :", retriever)
		docs = retriever.invoke(question)
		# print("Docs :", docs)
		chunks = []

		for idx, doc in enumerate(docs):
			print("Chunk idx :", idx)
			print("Page Content :", type(doc.page_content))
			print("Metadata :", type(doc.metadata))
			chunks.append(
				
				Result(
					page_content=doc.page_content,
					metadata=doc.metadata
				)
			)
		# print("Chunks :", chunks)
		return chunks
	except Exception as err:
		raise RuntimeError(f"Error in fetch context unranked module : {err}")

def fetch_context(original_question):
	try:
		print("Starting Fetching Context")
		rewritten_question = rewrite_query(original_question)
		# print("Rewritten Question :",rewritten_question)
		chunk_og_question = fetch_context_unranked(original_question)
		# print("Og Chunks :", chunk_og_question)
		chunk_re_question = fetch_context_unranked(rewritten_question)
		# print("Re Chunks :", chunk_re_question)
		final_chunks = merge_chunks(chunk_og_question, chunk_re_question)
		# print("Final Chunks :", final_chunks)
		reranked = rerank(original_question, final_chunks)

		return reranked[:const.FINAL_K]
	except Exception as err:
		raise RuntimeError(f"Error in fetch context module : {err}")

def main_runner(question: str, history: list[dict] = []) -> tuple[str, list]:
	try:
		print("Question :", question)
		print("History :", history)
		chunks = fetch_context(question)
		messages = make_rag_message(question, history, chunks)
		response = llm.invoke(messages)
		return response.content, chunks
	except Exception as err:
		raise RuntimeError(f"Error in main_runner module : {err}")

