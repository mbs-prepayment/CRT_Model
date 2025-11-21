"""
特征工程
"""
import pandas as pd
import numpy as np
import re
from typing import List, Optional


class FeatureEngineer:
    """特征工程器"""
    
    @staticmethod
    def extract_time_features(df: pd.DataFrame, period_col: str = 'period') -> pd.DataFrame:
        """提取时间特征"""
        df = df.copy()
        df[period_col] = df[period_col].astype(str)
        df['year'] = df[period_col].str[:4].astype(int)
        df['month'] = df[period_col].str[4:6].astype(int)
        return df
    
    @staticmethod
    def looks_like_yyyymm(series: pd.Series) -> bool:
        """检查序列是否像 YYYYMM 格式"""
        if not np.issubdtype(series.dtype, np.number):
            return False
        v = pd.Series(series).dropna().astype(int)
        if v.empty:
            return False
        mn, mx = v.min(), v.max()
        if mn < 190001 or mx > 210012:
            return False
        mm = v % 100
        return bool(((mm >= 1) & (mm <= 12)).all())
    
    @staticmethod
    def is_time_like(name: str, series: pd.Series) -> bool:
        """判断是否是时间相关字段"""
        name_l = str(name).lower()
        if re.search(r"(period|yyyymm|ym|yearmon|asof|report|month|mon|mth|date|dt)$", name_l):
            return True
        if FeatureEngineer.looks_like_yyyymm(series):
            return True
        return False
    
    @staticmethod
    def identify_time_columns(df: pd.DataFrame, exclude_cols: Optional[List[str]] = None) -> List[str]:
        """识别所有时间相关列"""
        exclude_cols = exclude_cols or []
        time_cols = []
        
        for col in df.columns:
            if col in exclude_cols:
                continue
            if FeatureEngineer.is_time_like(col, df[col]):
                time_cols.append(col)
        
        return time_cols

