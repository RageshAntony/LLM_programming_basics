from colorama import Fore
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

if __name__ == '__main__':
    print("status: loading document")

    loader = TextLoader("../docs/doc.txt")
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    docs = text_splitter.split_documents(pages)

    # Split documents into chunks
    gds_data_split = docs
    print(len(gds_data_split))

    # Define embedding model
    OPENAI_API_KEY = "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"

    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    support_data = gds_data_split
    support_store = Chroma.from_documents(
        support_data, embeddings, collection_name="support"
    )
    print("status: configure llm")
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
        max_tokens=1024,
    )

    sales_template = """As a TechSamurai marketing bot, your goal is to provide accurate and helpful information about
     TechSamurai products. You should answer user inquiries based on the context provided .

    {context}

    Question: {question}"""
    SALES_PROMPT = PromptTemplate(
        template=sales_template, input_variables=["context", "question"]
    )
    sales_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=support_store.as_retriever(),
        chain_type_kwargs={"prompt": SALES_PROMPT},
    )

    while True:
        query = input(" > ")
        result = sales_qa.run(query)
        print(result)