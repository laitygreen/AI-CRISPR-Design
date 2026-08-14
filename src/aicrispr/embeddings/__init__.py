"""C: DNA foundation model embeddings.

Models: DNABERT-2 (mean pooling, recommended), Nucleotide Transformer, HyenaDNA.
Usage: extract embeddings for gRNA sequences, then feed to M1 classifier/regressor.
Reference: RouteC method package (mean pooling > CLS by 1.4-8.7% AUC).
TODO: implement load_model(), embed_sequences().
"""
