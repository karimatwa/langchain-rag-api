from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_text_splitters import HTMLSectionSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import VECTOR_SIZE
from crawler import get_all_urls
from logger import Logger
logger = Logger.get(__name__)

def load_data(engine, vector_store, embeddings, initialize_store):
    logger.info('▶ Crawling site…')
    urls = get_all_urls()
    logger.info('▶ Loading pages…')
    loader = AsyncHtmlLoader(urls)
    docs   = loader.load()
    logger.info(f'  • loaded {len(docs)} docs')

    headers_to_split_on = [
        ("h1", "Title"),
        ("h2", "Section"),
        ("h3", "Subsection")
    ]
    html_splitter = HTMLSectionSplitter(headers_to_split_on=headers_to_split_on)
    section_docs = []
    for doc in docs:
        for sec in html_splitter.split_text(doc.page_content):
            merged = {**doc.metadata, **sec.metadata}
            section_docs.append(Document(page_content=sec.page_content, metadata=merged))

    logger.info(f"→ {len(section_docs)} header-aware Documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30, add_start_index=True)
    final_chunks = []
    for sec in section_docs:
        if len(sec.page_content) > 600:
            final_chunks.extend(text_splitter.split_documents([sec]))
        else:
            final_chunks.append(sec)

    logger.info(f"→ {len(final_chunks)} total chunks ready for indexing")

    engine.init_vectorstore_table(
        table_name='documents',
        vector_size=VECTOR_SIZE,
        overwrite_existing=True
    )

    if vector_store is None:
        vector_store = initialize_store(engine, embeddings)

    logger.info('  • Adding to vector store…')
    vector_store.add_documents(final_chunks)
    logger.info('💾 Indexing completed')
    return vector_store
