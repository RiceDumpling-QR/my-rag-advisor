# my-rag-advisor

## Introduction

This project is a RAG chatbot agent for influencer. If you are a new influencer who wants to build up your fan community, the chatbot will be able to answer your questions from the command line. It takes data from multiple sources such as academic papers and past instagram posts.

## Usage

1. Install all necessary requirements

```sh
pip install -r requirements.txt
```

2. Run pipeline.py with the command 

```sh
python3 pipeline.py "The question I want to ask"
```


## Results

If your question can be answered from a relevant source, it will provide the answer and the referecen from the sources. If your question is irrelevant to anything from the database, it will just retrieve response from general knowledge.

