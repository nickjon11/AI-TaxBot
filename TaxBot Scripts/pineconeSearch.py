from ChunkVector2 import getIndex, getIndexName

#Main RAG class. Search vector store for relevant info

#do a quick scan of vectors to check if any have helpful data
def pineconeQuickSearch(query):
    index = getIndex() #pinecone vector index
    results = index.search(
        namespace=getIndexName(),
        query={
            "top_k": 1, #only check the best doc
            "inputs": {
                'text': query
            }
        }
    )
    score = results.result['hits'][0]['_score']
    #Score cut off at 0.4 means commonly search, but not always
    if(score > 0.4):
        return pineconeSearch(query)#do deeper search

#Search for the best 5 documents, return those with scores within range
def pineconeSearch(query):
    index = getIndex()
    # Find the top 10 documents
    results = index.search(
        namespace=getIndexName(),
        query={
            "top_k": 10,
            "inputs": {
                'text': query
            }
        },
        rerank={#rank by relevance of each other, return top 5 only
        "model": "bge-reranker-v2-m3",
        "top_n": 5,
        "rank_fields": ["chunk_text"]
        }   
    )
    highscore = 0 #score of most relevant chunk
    answers = [] #chunk text collection from results
    for result in results['result']['hits']:
        resultScore = result['_score']
        if resultScore > highscore:
            highscore=resultScore
        if result['_score'] >= highscore-0.01:#Scores range from .00-.02 usually. Only return chunks with at least half the score of the best chunk
            answers.append(result['fields']['chunk_text'])

    return answers

#if you run this file ask a simple question and print the answer.
if __name__ == '__main__':
    answers = pineconeQuickSearch("How often are taxes filed?")

    for answer in answers:
        print(answer)