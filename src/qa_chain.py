from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import OPENAI_CHAT_MODEL, SYSTEM_PROMPT
from logger import Logger
logger = Logger.get(__name__)

def initialize_qa_chain(vector_store):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    llm       = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=0.0)
    system_prompt = (
    f"{SYSTEM_PROMPT}"
    "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(retriever, question_answer_chain)
    logger.info('🔗 QA chain triggered')
    return qa_chain