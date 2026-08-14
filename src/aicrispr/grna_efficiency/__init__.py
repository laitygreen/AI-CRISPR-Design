"""M1: gRNA on-target efficiency prediction.

Model: DNABERT-2 embedding (mean pooling) + LoRA fine-tuning, or CRISPRon-style multi-scale CNN + dG features.
Reference: RouteA method package, DeepCRISPR (2018), CRISPRon (2021).
TODO: implement train(), predict(), evaluate().
"""
