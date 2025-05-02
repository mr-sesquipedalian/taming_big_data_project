import fitz  
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text.lower())
    text = re.sub(r'[^\w\s]', '', text)  
    return text.strip()

def get_pdf_texts(pdf_directory):
    pdf_texts = []
    pdf_names = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = preprocess_text(text)
            pdf_texts.append(cleaned_text)
            pdf_names.append(filename)
    return pdf_texts, pdf_names

def compute_similarity_matrix(pdf_texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(pdf_texts)
    
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    n = len(pdf_texts)
    upper_triangular = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            upper_triangular[i, j] = similarity_matrix[i, j]
    
    return upper_triangular


def save_to_csv(similarity_matrix, pdf_names, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    matrix_df = pd.DataFrame(similarity_matrix, index=pdf_names, columns=pdf_names)
    matrix_csv_path = os.path.join(output_dir, "similarity_matrix.csv")
    matrix_df.to_csv(matrix_csv_path)
    print(f"Similarity matrix saved to: {matrix_csv_path}")
    
    pairwise_data = []
    n = len(pdf_names)
    for i in range(n):
        for j in range(i + 1, n):
            pairwise_data.append({
                "Document_1": pdf_names[i],
                "Document_2": pdf_names[j],
                "Similarity_Score": similarity_matrix[i, j]
            })
    pairwise_df = pd.DataFrame(pairwise_data)
    pairwise_csv_path = os.path.join(output_dir, "pairwise_similarities.csv")
    pairwise_df.to_csv(pairwise_csv_path, index=False)
    print(f"Pairwise similarities saved to: {pairwise_csv_path}")

def main(pdf_directory, output_dir="output"):
    pdf_texts, pdf_names = get_pdf_texts(pdf_directory)
    if not pdf_texts:
        print("No PDFs found in the directory.")
        return
    
    similarity_matrix = compute_similarity_matrix(pdf_texts)
    
    print("PDF Documents:", pdf_names)
    print("\nUpper Triangular Similarity Matrix:")
    print(similarity_matrix)
    
    save_to_csv(similarity_matrix, pdf_names, output_dir)
    
    print("\nSimilarity Scores (Upper Triangular):")
    n = len(pdf_names)
    for i in range(n):
        for j in range(i + 1, n):
            print(f"Similarity between {pdf_names[i]} and {pdf_names[j]}: {similarity_matrix[i, j]:.4f}")

# Example usage
if _name_ == "_main_":
    pdf_directory = "Required Data"  
    output_dir = "similarity_output" 
    main(pdf_directory, output_dir)