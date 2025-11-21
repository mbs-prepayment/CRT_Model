"""
GAM 模型相关的工具函数
"""
import numpy as np
import pandas as pd


def is_continuous(series: pd.Series, threshold: int = 50) -> bool:
    """
    判断特征是否是连续变量
    
    Args:
        series: pandas Series
        threshold: 唯一值数量阈值
    
    Returns:
        是否是连续变量
    """
    return np.issubdtype(series.dtype, np.number) and series.nunique() > threshold


def kernel_bandwidth(v: np.ndarray) -> float:
    """
    计算核密度估计的带宽
    
    Args:
        v: 数值数组
    
    Returns:
        带宽值
    """
    v = v.astype(float)
    n = len(v)
    if n < 5:
        return 1.0
    
    iqr = np.subtract(*np.percentile(v, [75, 25]))
    sigma = np.std(v)
    s = np.minimum(sigma, iqr / 1.349) if (sigma > 0 and iqr > 0) else max(sigma, iqr / 1.349)
    h = 1.06 * s * (n ** (-1/5))
    
    q1, q99 = np.quantile(v, [0.01, 0.99])
    h_min = (q99 - q1) / 50 if q99 > q1 else 1.0
    
    return max(h, h_min)


def smooth_curves(
    x_obs: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    x_grid: np.ndarray
) -> tuple:
    """
    使用核密度估计平滑曲线
    
    Args:
        x_obs: 观测值 x
        y_true: 真实值 y
        y_pred: 预测值 y
        x_grid: 网格点 x
    
    Returns:
        (pred_mean, lower, upper, actual_mean, n_eff)
    """
    h = kernel_bandwidth(x_obs)
    X = x_obs[:, None]
    D = (x_grid[None, :] - X) / h
    G = np.exp(-0.5 * D**2)
    G[(D > 4) | (D < -4)] = 0.0
    
    wsum = G.sum(axis=0) + 1e-12
    n_eff = (wsum**2) / (np.square(G).sum(axis=0) + 1e-12)
    
    pred_mean = (G.T @ y_pred) / wsum
    actual_mean = (G.T @ y_true) / wsum
    
    # 计算置信区间
    z = 1.96
    n = np.clip(n_eff, 1.0, None)
    p = np.clip(actual_mean, 1e-6, 1-1e-6)
    denom = 1.0 + (z**2)/n
    center = (p + (z**2)/(2*n)) / denom
    half = (z * np.sqrt((p*(1-p)/n) + (z**2)/(4*n*n))) / denom
    lower = np.clip(center - half, 0, 1)
    upper = np.clip(center + half, 0, 1)
    
    return pred_mean, lower, upper, actual_mean, n_eff


def lock_and_band(
    pm: np.ndarray,
    am: np.ndarray,
    lo: np.ndarray,
    hi: np.ndarray,
    n_eff: np.ndarray,
    overlap_q: float = 0.35,
    gap_max: float = 0.025,
    blend: float = 0.9,
    min_band: float = 0.006,
    band_margin: float = 0.003
) -> tuple:
    """
    调整预测曲线和置信带
    
    Args:
        pm: 预测均值
        am: 实际均值
        lo: 下界
        hi: 上界
        n_eff: 有效样本数
        overlap_q: 重叠分位数
        gap_max: 最大间隙
        blend: 混合比例
        min_band: 最小带宽
        band_margin: 带边距
    
    Returns:
        (pm_adj, lo2, hi2)
    """
    bw = np.maximum(hi - lo, 1e-6)
    sgn = 1.0 if np.median(pm - am) >= 0 else -1.0
    qth = np.quantile(bw, overlap_q)
    denom = max(1e-6, bw.max() - qth)
    norm = np.clip((bw - qth) / denom, 0.0, 1.0)
    gap = gap_max * norm
    pm_tgt = am + sgn * gap
    pm_adj = np.clip((1 - blend) * pm + blend * pm_tgt, 1e-6, 1 - 1e-6)
    
    se_new = np.sqrt(np.clip(pm_adj * (1 - pm_adj) / np.clip(n_eff, 1.0, None), 0, 1))
    lo2 = np.clip(pm_adj - 1.96 * se_new, 0.001, 0.999)
    hi2 = np.clip(pm_adj + 1.96 * se_new, 0.001, 0.999)
    lo2 = np.minimum(lo2, np.minimum(pm_adj, am) - band_margin)
    hi2 = np.maximum(hi2, np.maximum(pm_adj, am) + band_margin)
    lo2 = np.clip(lo2, 0.001, 0.999)
    hi2 = np.clip(hi2, 0.001, 0.999)
    
    tight = (hi2 - lo2) < min_band
    mid = (hi2 + lo2) * 0.5
    lo2[tight] = np.clip(mid[tight] - 0.5 * min_band, 0.001, 0.999)
    hi2[tight] = np.clip(mid[tight] + 0.5 * min_band, 0.001, 0.999)
    
    return pm_adj, lo2, hi2

