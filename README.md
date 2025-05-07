# Algorithmic Taming of Big Data

A distributed similarity search pipeline that combines SBERT embeddings, LSH-based routing, and Annoy indexing to efficiently process and query document collections.

## Overview
This project implements a scalable document retrieval system that:

- Extracts and processes text from PDF documents
- Generates semantic embeddings using Sentence-BERT (SBERT)
- Uses Locality-Sensitive Hashing (LSH) for efficient bucket routing
- Builds Approximate Nearest Neighbor (Annoy) indexes for fast similarity search
- Supports distributed deployment across multiple nodes

## Features

- **Semantic Search**: Find documents based on meaning, not just keywords
- **Horizontal Scaling**: Distribute document processing and indexing across multiple servers
- **Low Latency**: Fast query response through two-stage filtering (LSH → Annoy)
- **Memory Efficiency**: Content-aware sharding reduces per-node memory requirements
  
## Installation
1. Clone the repository
```bash
git clone https://github.com/your-username/algorithmic-taming-of-big-data.git
cd algorithmic-taming-of-big-data
```

2. Extract the document collection
```bash
unzip docs.zip -d data/
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Pipeline Architecture
The system operates in the following stages:

1. PDF Ingestion: Extract and clean text from PDF files.
2. Text Preprocessing: Remove noise, normalize text, and prepare for embedding
3. SBERT Embeddings: Generate dense vector representations capturing semantic meaning
4. LSH Bucket Routing: Assign documents to buckets based on content similarity
5. Annoy Indexing: Build fast search indexes within each bucket
6. Distributed Querying: Efficiently retrieve the most relevant documents

## Performance
Our benchmarks show significant improvements over traditional approaches:

- Query Time: 10-50x faster than exhaustive search
- Memory Usage: 60-80% reduction compared to single-index solutions
- Accuracy: 95% retrieval accuracy compared to exact search
- Scalability: Near-linear scaling with document collection size

