"""
模型训练相关的工具函数
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_curve, f1_score
from pygam import s, f
from typing import Tuple, Dict


def fit_label_encoders(X: pd.DataFrame) -> Tuple[pd.DataFrame, Dict, list, Dict]:
    """
    训练 Label Encoders
    
    Args:
        X: DataFrame
    
    Returns:
        (编码后的DataFrame, 编码器字典, 类别列列表, 众数字典)
    """
    obj_cols = X.select_dtypes(include=["object"]).columns.tolist()
    encs = {}
    modes = {}
    X2 = X.copy()
    
    for c in obj_cols:
        le = LabelEncoder()
        tr_codes = le.fit_transform(X2[c].astype(str)) + 1
        X2[c] = tr_codes
        encs[c] = le
        modes[c] = int(pd.Series(tr_codes).mode().iloc[0])
    
    return X2, encs, obj_cols, modes


def transform_with_encoders(
    X: pd.DataFrame,
    encs: Dict,
    obj_cols: list,
    modes: Dict
) -> pd.DataFrame:
    """
    使用已有的 Label Encoders 转换数据
    
    Args:
        X: DataFrame
        encs: 编码器字典
        obj_cols: 类别列列表
        modes: 众数字典
    
    Returns:
        编码后的 DataFrame
    """
    X2 = X.copy()
    
    for c in obj_cols:
        le = encs[c]
        mode_code = modes[c]
        classes = set(le.classes_)
        
        def map_one(s):
            s = str(s)
            return int(le.transform([s])[0]) + 1 if s in classes else mode_code
        
        X2[c] = X2[c].astype(str).map(map_one).astype(int)
    
    return X2


def build_terms(cols: list, obj_cols: list, n_splines: int = 8, spline_order: int = 3):
    """
    构建 GAM 模型的 terms
    
    Args:
        cols: 所有列名
        obj_cols: 类别列名
        n_splines: 样条数量
        spline_order: 样条阶数
    
    Returns:
        GAM terms
    """
    terms = None
    for i, c in enumerate(cols):
        t = f(i) if c in obj_cols else s(i, n_splines=n_splines, spline_order=spline_order)
        terms = t if terms is None else terms + t
    return terms


def class_weights(y: np.ndarray) -> Tuple[float, float]:
    """
    计算类别权重
    
    Args:
        y: 标签数组
    
    Returns:
        (w0, w1) - 类别0和类别1的权重
    """
    bc = np.bincount(y)
    w0 = bc.sum() / (2.0 * bc[0]) if len(bc) > 0 and bc[0] > 0 else 1.0
    w1 = bc.sum() / (2.0 * bc[1]) if len(bc) > 1 and bc[1] > 0 else 1.0
    return w0, w1


def best_threshold(y_true: np.ndarray, proba: np.ndarray) -> Tuple[float, float]:
    """
    找到最佳阈值（基于 F1 Score）
    
    Args:
        y_true: 真实标签
        proba: 预测概率
    
    Returns:
        (best_threshold, best_f1)
    """
    fpr, tpr, thr = roc_curve(y_true, proba)
    f1s = [f1_score(y_true, (proba >= t).astype(int)) for t in thr]
    j = int(np.argmax(f1s))
    return float(thr[j]), float(f1s[j])

