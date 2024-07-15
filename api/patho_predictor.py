import pandas as pd
from Bio import SeqIO
from itertools import product
from joblib import load


def encode_sequence(sequence, k):
    all_kmers = [''.join(p) for p in product('ATCG', repeat=k)]
    kmer_counts = {kmer: 0 for kmer in all_kmers}
    sequence = ''.join(char for char in sequence if char in ['A', 'T', 'C', 'G'])
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer in kmer_counts:
            kmer_counts[kmer] += 1
    encoded_df = pd.DataFrame([kmer_counts.values()], columns=all_kmers)
    sum_counts = encoded_df.sum(axis=1)
    encoded_df = encoded_df.divide(sum_counts, axis=0)
    encoded_df = encoded_df.fillna(0)
    return encoded_df


def read_fasta_to_kmers(file_path, k_mers):
    dfs_per_sequence = []
    for record in SeqIO.parse(file_path, "fasta"):
        sequence = str(record.seq)
        encoded_sequence_dfs = [encode_sequence(sequence, k) for k in k_mers]
        merged_sequence_df = pd.concat(encoded_sequence_dfs, axis=1)
        merged_sequence_df.insert(0, 'sequence_id', record.id)
        dfs_per_sequence.append(merged_sequence_df)
    final_df = pd.concat(dfs_per_sequence, ignore_index=True) if dfs_per_sequence else pd.DataFrame()
    return final_df


def patho_predict(model_path, input_fasta, k_mers=None):
    if k_mers is None:
        k_mers = [3]
    df = read_fasta_to_kmers(input_fasta, k_mers)
    model = load(model_path)
    y_pred = model.predict_proba(df.iloc[:, 1:])[:, 1]  # Predict probabilities for the positive class
    results_df = pd.DataFrame({
        'sequence_id': df['sequence_id'],
        'prediction_value': y_pred,
        'label': ['pathogenic' if pred >= 0.5 else 'non-pathogenic' for pred in y_pred]
    })
    return results_df


def run(model_path, input_fasta):
    return patho_predict(model_path, input_fasta)
