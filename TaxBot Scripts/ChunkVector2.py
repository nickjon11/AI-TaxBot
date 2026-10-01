import os, re
import pinecone 
from openai import OpenAI
from constants import *
from connect import getModelEmbeddings

#Creates Pinecone Index with connection to cloud vector store
#Run this file to load from chunks to pinecone


# Get Pinecone Key from vault
with open(getSecretStuff(), "r") as file:
    for line in file:
        name, value = line.split("=")
        if name.strip() == "pinecone_key":
            pinecone_api_key = value.strip()

# Initialization
pc = pinecone.Pinecone(api_key=pinecone_api_key)

# Pinecone Index Initialization
index_name = getPineconeIndexName() #from constants
#create index if it does not exist
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":getModelEmbeddings(),
            "field_map":{"text": "chunk_text"}
        }
    )

#Set index. This entire script has built up to this moment
index = pc.Index(index_name)

def getIndex():
    return index

def getIndexName():
    return index_name

#Load from chunked data into pinecone
def loadChunks():
    # Path to chunks outer folder
    chunks_root = os.path.join(getUploadFolder(), "chunked_data")#from constants

    # PDF Subfolder List.
    subfolders = [
        "Form 8917 (Rev. January 2020) - f8917",
        "i1040gi",
        "i1040x",
        "i1042s",
        "i1098et",
        "i1099mec",
        "i8863",
        "iw2w3",
        "PATaxLaws"
    ]   


    # Chunk Processing/Uploading
    for subfolder in subfolders: # Loop through subfolders
        subfolder_path = os.path.join(chunks_root, subfolder)
        #if no folder exists, state and skip folder
        if not os.path.isdir(subfolder_path):
            print(f"[SKIP] Folder not found: {subfolder_path}")
            continue

        #get all chunk files, sort them so _001 is first
        chunk_files = sorted([f for f in os.listdir(subfolder_path) if f.endswith(".txt")]) #
        print(f"\nProcessing folder: {subfolder} ({len(chunk_files)} chunks)")

        #Begin processing
        for i, filename in enumerate(chunk_files):
            # Loop through chunk files
            file_path = os.path.join(subfolder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.read().strip().splitlines()

            chunk_name = ""
            summary = ""
            chunk_text = ""

            # Set Meta Data
            for x, line in enumerate(lines):
                if line.startswith("Chunk Name:"):
                    chunk_name = line.replace("Chunk Name:", "").strip()
                elif line.startswith("Summary:"):
                    summary = line.replace("Summary:", "").strip()
                elif line.startswith("Chunk Content:"):
                    chunk_text = "\n".join(lines[x+1:]).strip()
                    break
            
            #If the chunk has no text, skip the file and print the error
            if not chunk_text.strip():
                print(f"  [SKIP] Empty file: {filename}")
                continue
            
            # ID Creation
            folder_id = subfolder.replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("-", "") #remove special characters
            vector_id = f"{folder_id}_chunk_{i+1}"
            #add to the collection of records to be uploaded to pinecone
            records = [
                {"_id":vector_id, "chunk_text":chunk_text, 'chunk_name': chunk_name, 'summary':summary}
            ]

            # Upload to Pinecone
            index.upsert_records(index_name, records) #This could be moved if records were changed to collect multiple values. Can update for speed. Unneccessary for now.
            print(f"  [OK] Uploaded {vector_id}")
        print(f"Finished {filename}")
    print("\n✅ All chunks uploaded successfully.")

#Run this file to load from chunks to pinecone
if __name__ == '__main__':
    loadChunks()