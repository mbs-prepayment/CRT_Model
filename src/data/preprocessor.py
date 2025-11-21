"""
数据预处理器
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Dict, List, Optional

from ..config import TARGET_COLUMN


class DataPreprocessor:
    """数据预处理器"""
    
    def __init__(self):
        self.label_encoders: Dict[str, LabelEncoder] = {}
    
    def remove_constant_columns(
        self, 
        df: pd.DataFrame, 
        exclude_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        删除常量列
        
        Args:
            df: DataFrame
            exclude_cols: 排除的列名列表
        
        Returns:
            处理后的 DataFrame
        """
        exclude_cols = exclude_cols or ["first_payment_date"]
        constant_cols = [
            col for col in df.columns 
            if df[col].nunique() <= 1 and col not in exclude_cols
        ]
        
        if constant_cols:
            print(f"删除常量列: {constant_cols}")
            df = df.drop(columns=constant_cols)
        
        return df
    
    def encode_categorical_features(
        self, 
        df: pd.DataFrame,
        exclude_cols: Optional[List[str]] = None,
        fit: bool = True
    ) -> pd.DataFrame:
        """
        对类别特征进行 Label Encoding
        
        Args:
            df: DataFrame
            exclude_cols: 排除的列名列表
            fit: 是否训练编码器（False 时使用已有编码器）
        
        Returns:
            编码后的 DataFrame
        """
        exclude_cols = exclude_cols or [TARGET_COLUMN, "first_payment_date"]
        df = df.copy()
        
        obj_cols = df.select_dtypes(include=['object']).columns
        
        for col in obj_cols:
            if col in exclude_cols:
                continue
            
            if fit:
                # 训练新的编码器
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                # 使用已有编码器
                if col in self.label_encoders:
                    le = self.label_encoders[col]
                    # 处理未见过的类别
                    mode_label = int(pd.Series(df[col]).mode().iloc[0])
                    classes = set(le.classes_)
                    
                    def safe_transform(val):
                        val_str = str(val)
                        return int(le.transform([val_str])[0]) if val_str in classes else mode_label
                    
                    df[col] = df[col].astype(str).map(safe_transform).astype(int)
        
        if fit:
            print(f"编码了 {len(self.label_encoders)} 个类别特征")
        
        return df
    
    def extract_time_features(self, df: pd.DataFrame, period_col: str = 'period') -> pd.DataFrame:
        """
        从 period 字段提取时间特征
        
        Args:
            df: DataFrame
            period_col: period 列名
        
        Returns:
            添加了时间特征的 DataFrame
        """
        df = df.copy()
        df[period_col] = df[period_col].astype(str)
        df['period_year'] = df[period_col].str[:4].astype(int)
        df['period_month'] = df[period_col].str[4:6].astype(int)
        
        print(f"提取时间特征: period_year, period_month")
        return df
    
    def preprocess(
        self, 
        df: pd.DataFrame,
        fit: bool = True,
        save_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        完整的预处理流程
        
        Args:
            df: 原始 DataFrame
            fit: 是否训练编码器
            save_path: 保存路径
        
        Returns:
            预处理后的 DataFrame
        """
        print("开始数据预处理...")
        
        # 1. 删除常量列
        df = self.remove_constant_columns(df)
        
        # 2. Label Encoding
        df = self.encode_categorical_features(df, fit=fit)
        
        # 3. 保存
        if save_path:
            df.to_csv(save_path, index=False)
            print(f"预处理数据已保存: {save_path}")
        
        print(f"预处理完成: {df.shape}")
        return df

