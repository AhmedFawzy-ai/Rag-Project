"""
Script to create Chroma vector database from Excel data
Run this once to prepare your museum data for the chatbot
"""

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import pandas as pd
import os

def create_database():
    print("📊 Reading Excel file...")
    
    # Read the Excel file
    try:
        df = pd.read_excel("dataset.xlsx")
        print(f"✅ Found {len(df)} rows in the dataset")
        print(f"📋 Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return
    
    # Convert DataFrame to documents
    print("\n🔄 Converting data to documents...")
    documents = []
    
    # Option 1: Combine all columns into one document per row
    for idx, row in df.iterrows():
        # Create a text representation of the row
        content_parts = []
        for col in df.columns:
            if pd.notna(row[col]):  # Skip NaN values
                content_parts.append(f"{col}: {row[col]}")
        
        content = "\n".join(content_parts)
        documents.append(Document(
            page_content=content,
            metadata={"row_id": idx}
        ))
    
    print(f"✅ Created {len(documents)} documents")
    
    # Initialize embeddings
    print("\n🤖 Initializing embedding model...")
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("✅ Embedding model loaded")
    
    # Create vector database
    print("\n💾 Creating Chroma vector database...")
    try:
        # Remove old database if exists
        if os.path.exists("./chroma_db"):
            import shutil
            shutil.rmtree("./chroma_db")
            print("🗑️  Removed old database")
        
        vdb = Chroma.from_documents(
            documents=documents,
            embedding=embedding,
            persist_directory="./chroma_db"
        )
        
        print("✅ Database created successfully!")
        print(f"📍 Location: ./chroma_db")
        
        # Test the database
        print("\n🧪 Testing database with a sample query...")
        retriever = vdb.as_retriever(search_kwargs={"k": 3})
        test_results = retriever.invoke("museum")
        print(f"✅ Retrieved {len(test_results)} documents")
        
        print("\n✨ All done! You can now run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return

if __name__ == "__main__":
    create_database()
