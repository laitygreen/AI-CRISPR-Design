"""B1: Whole-genome CRISPR site scanning for E. coli MG1655.

Pipeline: PAM search (NGG / Cas12a TTTV) -> candidate gRNA enumeration -> feature engineering -> off-target candidate scan.
Reference: DeepCRISPR encoding scheme, CRISPOR methodology.
TODO: implement scan_pams(), extract_features(), find_offtarget_candidates().
"""
