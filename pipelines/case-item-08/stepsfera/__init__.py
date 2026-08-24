"""Catálogo de Steps modulares no padrão Stepsfera / Dadosfera."""
from .step_01_ingest_bronze import run_step as run_step_01_ingest
from .step_02_validate_qualify import run_step as run_step_02_qualify
from .step_03_enrich_genai import run_step as run_step_03_enrich
from .step_04_transform_gold_kimball import run_step as run_step_04_gold
from .step_05_train_churn_model import run_step as run_step_05_train_ml
