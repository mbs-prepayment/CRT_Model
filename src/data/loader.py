"""
数据加载器 - 从 Supabase 加载数据
"""
import pandas as pd
import time
from supabase import create_client, Client
from typing import Optional
import os

from ..config import (
    SUPABASE_URL, SUPABASE_KEY, TABLE_MODEL_DATA,
    BATCH_SIZE, MAX_ROWS, RAW_DATA_FILE
)


class SupabaseLoader:
    """Supabase 数据加载器"""
    
    def __init__(self, url: str = SUPABASE_URL, key: str = SUPABASE_KEY):
        """
        初始化 Supabase 客户端
        
        Args:
            url: Supabase 项目 URL
            key: Supabase API 密钥
        """
        self.url = url
        self.key = key
        self.client: Client = create_client(url, key)
    
    def load_data(
        self,
        table_name: str = TABLE_MODEL_DATA,
        max_rows: int = MAX_ROWS,
        batch_size: int = BATCH_SIZE,
        cache_file: Optional[str] = None
    ) -> pd.DataFrame:
        """
        从 Supabase 加载数据
        
        Args:
            table_name: 表名
            max_rows: 最大行数
            batch_size: 批次大小
            cache_file: 缓存文件路径（如果存在则从缓存加载）
        
        Returns:
            DataFrame
        """
        # 检查缓存
        if cache_file and os.path.exists(cache_file):
            print(f"从缓存加载数据: {cache_file}")
            return pd.read_csv(cache_file, low_memory=False)
        
        # 从 API 下载
        print(f"从 Supabase 下载数据: {table_name}")
        rows = []
        offset = 0
        
        while offset < max_rows:
            print(f"获取行 {offset} - {offset + batch_size - 1} ...")
            try:
                res = self.client.table(table_name).select("*").range(
                    offset, offset + batch_size - 1
                ).execute()
                
                if not res.data:
                    print("数据读取完成")
                    break
                
                rows.extend(res.data)
                offset += batch_size
                print(f"进度: {offset}/{max_rows} ({(offset/max_rows)*100:.1f}%)")
                
            except Exception as e:
                print(f"请求失败: {e}，5秒后重试...")
                time.sleep(5)
                continue
        
        df = pd.DataFrame(rows)
        
        # 保存缓存
        if cache_file:
            df.to_csv(cache_file, index=False)
            print(f"数据已缓存: {cache_file}")
        
        print(f"加载完成: {df.shape[0]} 行, {df.shape[1]} 列")
        return df
    
    def load_training_data(self, use_cache: bool = True) -> pd.DataFrame:
        """
        加载训练数据（便捷方法）
        
        Args:
            use_cache: 是否使用缓存
        
        Returns:
            DataFrame
        """
        cache_file = RAW_DATA_FILE if use_cache else None
        return self.load_data(
            table_name=TABLE_MODEL_DATA,
            max_rows=MAX_ROWS,
            cache_file=cache_file
        )

