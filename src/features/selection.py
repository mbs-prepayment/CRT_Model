"""
特征选择
"""
import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from typing import List, Optional

from ..config import (
    HIGH_MISSING_THRESHOLD, HIGH_CORRELATION_THRESHOLD,
    LOW_VARIANCE_THRESHOLD, MUST_KEEP_FEATURES,
    OPTIONAL_KEEP_FEATURES, LEAKAGE_COLUMNS, TARGET_COLUMN
)


class FeatureSelector:
    """特征选择器"""
    
    def __init__(self):
        self.dropped_features = {
            'high_missing': [],
            'high_correlation': [],
            'low_variance': [],
            'leakage': []
        }
    
    def remove_high_missing(
        self, 
        df: pd.DataFrame,
        threshold: float = HIGH_MISSING_THRESHOLD,
        must_keep: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """删除高缺失率特征"""
        must_keep = must_keep or (MUST_KEEP_FEATURES + OPTIONAL_KEEP_FEATURES)
        
        missing_rate = df.isnull().mean()
        high_missing_cols = missing_rate[missing_rate > threshold].index.tolist()
        high_missing_cols = [col for col in high_missing_cols if col not in must_keep]
        
        if high_missing_cols:
            self.dropped_features['high_missing'] = high_missing_cols
            df = df.drop(columns=high_missing_cols)
            print(f"删除高缺失率特征 (>{threshold*100}%): {len(high_missing_cols)} 个")
        
        return df
    
    def remove_high_correlation(
        self,
        df: pd.DataFrame,
        threshold: float = HIGH_CORRELATION_THRESHOLD,
        must_keep: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """删除高相关特征"""
        must_keep = must_keep or (MUST_KEEP_FEATURES + OPTIONAL_KEEP_FEATURES)
        
        # 只对数值列计算相关性
        numeric_cols = [
            col for col in df.select_dtypes(include=[np.number]).columns 
            if col != TARGET_COLUMN
        ]
        
        if len(numeric_cols) < 2:
            return df
        
        corr_matrix = df[numeric_cols].corr()
        drop_corr = set()
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    col_name = corr_matrix.columns[i]
                    if col_name not in must_keep:
                        drop_corr.add(col_name)
        
        if drop_corr:
            self.dropped_features['high_correlation'] = list(drop_corr)
            df = df.drop(columns=list(drop_corr))
            print(f"删除高相关特征 (>{threshold}): {len(drop_corr)} 个")
        
        return df
    
    def remove_low_variance(
        self,
        df: pd.DataFrame,
        threshold: float = LOW_VARIANCE_THRESHOLD,
        must_keep: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """删除低方差特征"""
        must_keep = must_keep or (MUST_KEEP_FEATURES + OPTIONAL_KEEP_FEATURES)
        
        numeric_cols = [
            col for col in df.select_dtypes(include=[np.number]).columns 
            if col != TARGET_COLUMN
        ]
        
        if not numeric_cols:
            return df
        
        selector = VarianceThreshold(threshold=threshold)
        try:
            selector.fit(df[numeric_cols])
            low_var_cols = [
                col for col, var in zip(numeric_cols, selector.variances_) 
                if var < threshold and col not in must_keep
            ]
            
            if low_var_cols:
                self.dropped_features['low_variance'] = low_var_cols
                df = df.drop(columns=low_var_cols)
                print(f"删除低方差特征 (<{threshold}): {len(low_var_cols)} 个")
        except Exception as e:
            print(f"低方差特征选择警告: {e}")
        
        return df
    
    def remove_leakage_features(
        self,
        df: pd.DataFrame,
        leakage_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """删除数据泄露特征"""
        leakage_cols = leakage_cols or LEAKAGE_COLUMNS
        
        cols_to_drop = [col for col in leakage_cols if col in df.columns]
        
        if cols_to_drop:
            self.dropped_features['leakage'] = cols_to_drop
            df = df.drop(columns=cols_to_drop)
            print(f"删除数据泄露特征: {len(cols_to_drop)} 个")
        
        return df
    
    def fill_missing_values(self, df: pd.DataFrame, target_col: str = TARGET_COLUMN) -> pd.DataFrame:
        """填充缺失值"""
        df = df.copy()
        
        for col in df.columns:
            if col == target_col:
                continue
            
            if df[col].isnull().any():
                if df[col].dtype == "object":
                    # 类别特征用众数填充
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    # 数值特征用中位数填充
                    df[col].fillna(df[col].median(), inplace=True)
        
        print("缺失值填充完成")
        return df
    
    def select_features(
        self,
        df: pd.DataFrame,
        remove_missing: bool = True,
        remove_correlation: bool = True,
        remove_variance: bool = True,
        remove_leakage: bool = True,
        fill_missing: bool = True
    ) -> pd.DataFrame:
        """
        完整的特征选择流程
        
        Args:
            df: DataFrame
            remove_missing: 是否删除高缺失率特征
            remove_correlation: 是否删除高相关特征
            remove_variance: 是否删除低方差特征
            remove_leakage: 是否删除数据泄露特征
            fill_missing: 是否填充缺失值
        
        Returns:
            特征选择后的 DataFrame
        """
        print("开始特征选择...")
        print(f"初始特征数: {df.shape[1]}")
        
        if remove_missing:
            df = self.remove_high_missing(df)
        
        if remove_correlation:
            df = self.remove_high_correlation(df)
        
        if remove_variance:
            df = self.remove_low_variance(df)
        
        if remove_leakage:
            df = self.remove_leakage_features(df)
        
        if fill_missing:
            df = self.fill_missing_values(df)
        
        print(f"最终特征数: {df.shape[1]}")
        print(f"特征选择完成: {df.shape}")
        
        return df
    
    def get_dropped_features_summary(self) -> dict:
        """获取被删除特征的汇总"""
        return {
            category: len(features) 
            for category, features in self.dropped_features.items()
        }

