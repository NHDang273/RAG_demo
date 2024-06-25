import os
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from IPython.display import Markdown, display
from llama_index.readers.web import FireCrawlWebReader

# Initialize FireCrawlWebReader to crawl a website
firecrawl_reader = FireCrawlWebReader(
    api_key="fc-1359b3ce751942cd99ab44adecc9e398",  # Replace with your actual API key from https://www.firecrawl.dev/
    mode="crawl",  # Choose between "crawl" and "scrape" for single page scraping
    params={"additional": "parameters"}  # Optional additional parameters
)

def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = SummaryIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index

# Load documents from a single page URL
documents = firecrawl_reader.load_data(url="https://docs.python.org/3/tutorial/controlflow.html#for-statements")
website_index = get_index(documents, "website-1")
website_engine = website_index.as_query_engine()

# Set Logging to DEBUG for more detailed outputs
# user_query = input("Enter your query: ")
# response = website_engine.query(user_query)
# display(Markdown(f"<b>{response}</b>"))
# print(response)
