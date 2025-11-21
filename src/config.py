"""
配置文件 - 集中管理所有配置项
"""
import os

# Supabase 配置
SUPABASE_URL = os.getenv(
    "SUPABASE_URL", 
    "https://ptukzshzuloxipzwycte.supabase.co"
)
SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0dWt6c2h6dWxveGlwend5Y3RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxNjg0OTMsImV4cCI6MjA2Nzc0NDQ5M30.MAnlnrt0traaFjE-QV3jSKETU6woZJ8LcVIqjrAIiQ4"
)

# 数据库表名
TABLE_MODEL_DATA = "freddie_mac_delinquency_30_model_2013_2025"
TABLE_RAW_DATA = "freddie_mac_crt_raw_2023_2023"
TABLE_CLEAN_DATA = "freddie_mac_crt_raw_clean1"

# 数据配置
BATCH_SIZE = 1000
MAX_ROWS = 40000

# 目标变量
TARGET_COLUMN = "delinquency_30d_label"

# 文件路径
DATA_DIR = "data"
RAW_DATA_FILE = "freddie_mac_delinquency_balanced.csv"
PROCESSED_DATA_FILE = "freddie_mac_delinquency_strict_predict_ready_GAM.csv"

# 模型配置
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# GAM 模型参数
GAM_LAM_CANDIDATES = [10, 20, 40, 80, 120, 160, 240, 320, 480, 640]
GAM_N_SPLINES = 8
GAM_SPLINE_ORDER = 3

# 特征工程配置
HIGH_MISSING_THRESHOLD = 0.4
HIGH_CORRELATION_THRESHOLD = 0.9
LOW_VARIANCE_THRESHOLD = 0.01

# 必须保留的特征
MUST_KEEP_FEATURES = [
    "period_year", "period_month",
    "credit_score", "original_loan_to_value_ltv",
    "original_debt_to_income_dti_ratio", "current_interest_rate",
    "loan_age_years", "interest_rate_diff"
]

# 可选保留的特征
OPTIONAL_KEEP_FEATURES = [
    "state_default_rate", "msa_default_rate", "modification_history_flag"
]

# 数据泄露字段（需要删除）
LEAKAGE_COLUMNS = [
    "loan_identifier", "first_payment_date", "maturity_date",
    "loan_age", "remaining_months_to_legal_maturity",
    "current_loan_delinquency_status", "payment_history",
    "loan_to_value_ratio_bucket", "credit_score_bucket",
    "high_dti_flag", "loan_size_bucket", "interest_rate_bucket",
    "seasonality_flag"
]

