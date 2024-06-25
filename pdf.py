import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader


def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


# Đường dẫn đến tệp PDF
pdf_path = os.path.join("data", "Canada.pdf")

# Kiểm tra xem tệp PDF có tồn tại hay không
if not os.path.exists(pdf_path):
    print(f"Tệp {pdf_path} không tồn tại.")
else:
    # Sử dụng PDFReader để đọc tệp PDF
    parser = PDFReader()
    file_extractor = {".pdf": parser}

    # Sử dụng SimpleDirectoryReader để đọc tệp PDF
    documents = SimpleDirectoryReader("data", file_extractor=file_extractor).load_data()

    # Kiểm tra xem dữ liệu đã được tải thành công hay chưa
    if not documents:
        print("Không tìm thấy tài liệu nào. Vui lòng kiểm tra đường dẫn tệp.")
    else:
        # Xây dựng hoặc tải chỉ mục
        canada_index = get_index(documents, "canada")
        canada_engine = canada_index.as_query_engine()
