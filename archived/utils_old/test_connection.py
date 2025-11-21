"""
测试Supabase数据库连接和数据可用性
"""
import sys

print("=" * 60)
print("CRT Model - Supabase 连接测试")
print("=" * 60)

# 1. 检查依赖包
print("\n[1/4] 检查依赖包...")
try:
    import pandas as pd
    print("  ✓ pandas:", pd.__version__)
except ImportError:
    print("  ✗ pandas 未安装，请运行: pip install pandas")
    sys.exit(1)

try:
    import sklearn
    print("  ✓ scikit-learn:", sklearn.__version__)
except ImportError:
    print("  ✗ scikit-learn 未安装，请运行: pip install scikit-learn")
    sys.exit(1)

try:
    from supabase import create_client, Client
    print("  ✓ supabase 已安装")
except ImportError:
    print("  ✗ supabase 未安装，请运行: pip install supabase")
    sys.exit(1)

# 2. 测试数据库连接
print("\n[2/4] 测试 Supabase 连接...")
url = "https://ptukzshzuloxipzwycte.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0dWt6c2h6dWxveGlwend5Y3RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxNjg0OTMsImV4cCI6MjA2Nzc0NDQ5M30.MAnlnrt0traaFjE-QV3jSKETU6woZJ8LcVIqjrAIiQ4"

try:
    supabase: Client = create_client(url, key)
    print(f"  ✓ 连接成功: {url}")
except Exception as e:
    print(f"  ✗ 连接失败: {e}")
    sys.exit(1)

# 3. 检查模型表是否存在
print("\n[3/4] 检查数据表...")
table_name = "freddie_mac_delinquency_30_model_2013_2025"
try:
    # 尝试获取前10条数据
    res = supabase.table(table_name).select("*").limit(10).execute()
    
    if res.data:
        print(f"  ✓ 表 '{table_name}' 存在")
        print(f"  ✓ 成功获取 {len(res.data)} 条样本数据")
        
        # 显示表结构
        if res.data:
            columns = list(res.data[0].keys())
            print(f"  ✓ 字段数量: {len(columns)}")
            print(f"  ✓ 关键字段检查:")
            
            key_columns = [
                "delinquency_30d_label",
                "credit_score",
                "original_loan_to_value_ltv",
                "current_interest_rate",
                "period_year",
                "loan_age_years"
            ]
            
            for col in key_columns:
                if col in columns:
                    print(f"      ✓ {col}")
                else:
                    print(f"      ✗ {col} (缺失)")
    else:
        print(f"  ⚠ 表 '{table_name}' 存在但没有数据")
        
except Exception as e:
    print(f"  ✗ 无法访问表 '{table_name}'")
    print(f"  错误信息: {e}")
    
    # 尝试检查备用表名
    alternative_tables = [
        "freddie_mac_delinquency_30_model",
        "freddie_mac_crt_raw_2023_2023",
        "freddie_mac_crt_raw_clean1"
    ]
    
    print("\n  尝试查找备用表...")
    for alt_table in alternative_tables:
        try:
            res = supabase.table(alt_table).select("*").limit(1).execute()
            if res.data:
                print(f"    ✓ 找到备用表: '{alt_table}'")
        except:
            pass

# 4. 统计数据量
print("\n[4/4] 统计数据量...")
try:
    # 统计总行数
    res = supabase.table(table_name).select("*", count="exact").limit(1).execute()
    total_count = res.count if hasattr(res, 'count') else "未知"
    print(f"  ✓ 表中总记录数: {total_count}")
    
    # 尝试统计标签分布
    try:
        res_pos = supabase.table(table_name).select("*", count="exact").eq("delinquency_30d_label", 1).limit(1).execute()
        res_neg = supabase.table(table_name).select("*", count="exact").eq("delinquency_30d_label", 0).limit(1).execute()
        
        pos_count = res_pos.count if hasattr(res_pos, 'count') else "未知"
        neg_count = res_neg.count if hasattr(res_neg, 'count') else "未知"
        
        print(f"  ✓ 正样本（违约）: {pos_count}")
        print(f"  ✓ 负样本（正常）: {neg_count}")
    except:
        print("  ⚠ 无法统计标签分布")
        
except Exception as e:
    print(f"  ✗ 统计失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)

# 给出建议
print("\n📋 建议:")
print("  1. 如果所有测试通过，可以直接运行 Notebook 文件")
print("  2. 如果表不存在，需要先运行 SQL 脚本创建表")
print("  3. 如果数据为空，需要运行 CRT_Data_Inserting.ipynb 导入数据")
print("  4. 建议的运行顺序:")
print("     a) CRT_Data_Inserting.ipynb (数据导入)")
print("     b) 30 Days Delinquency SQL (特征工程)")
print("     c) 30_days_delinquency_2013_2025.ipynb (建模)")
print()

