"""
快速测试Supabase数据获取
"""
import sys

print("=" * 70)
print("Supabase 数据获取测试")
print("=" * 70)

# 1. 检查supabase是否已安装
print("\n[1/3] 检查依赖...")
try:
    from supabase import create_client, Client
    print("  ✅ supabase 库已安装")
except ImportError:
    print("  ❌ supabase 库未安装")
    print("  请运行: pip install supabase")
    sys.exit(1)

# 2. 测试连接
print("\n[2/3] 测试数据库连接...")
url = "https://ptukzshzuloxipzwycte.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0dWt6c2h6dWxveGlwend5Y3RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxNjg0OTMsImV4cCI6MjA2Nzc0NDQ5M30.MAnlnrt0traaFjE-QV3jSKETU6woZJ8LcVIqjrAIiQ4"

try:
    supabase: Client = create_client(url, key)
    print("  ✅ 连接创建成功")
except Exception as e:
    print(f"  ❌ 连接失败: {e}")
    sys.exit(1)

# 3. 测试数据获取
print("\n[3/3] 测试数据获取...")

tables_to_test = [
    "freddie_mac_delinquency_30_model_2013_2025",
    "freddie_mac_crt_raw_2023_2023",
    "freddie_mac_crt_raw_clean1"
]

results = {}

for table_name in tables_to_test:
    print(f"\n  测试表: {table_name}")
    try:
        # 尝试获取1条数据
        response = supabase.table(table_name).select("*").limit(1).execute()
        
        if response.data:
            print(f"    ✅ 表存在且有数据")
            
            # 尝试获取总数
            try:
                count_response = supabase.table(table_name).select("*", count="exact").limit(1).execute()
                if hasattr(count_response, 'count') and count_response.count is not None:
                    print(f"    📊 总记录数: {count_response.count:,}")
                    results[table_name] = {
                        "status": "success",
                        "count": count_response.count,
                        "columns": len(response.data[0].keys()) if response.data else 0
                    }
                else:
                    print(f"    📊 有数据，但无法获取精确计数")
                    results[table_name] = {
                        "status": "success",
                        "count": "unknown",
                        "columns": len(response.data[0].keys())
                    }
            except Exception as e:
                print(f"    ⚠️  无法获取计数: {e}")
                results[table_name] = {
                    "status": "success",
                    "count": "error",
                    "columns": len(response.data[0].keys())
                }
            
            # 显示字段信息
            if response.data:
                columns = list(response.data[0].keys())
                print(f"    📋 字段数: {len(columns)}")
                
                # 检查关键字段
                key_fields = ["delinquency_30d_label", "credit_score", "period", "loan_identifier"]
                found_keys = [k for k in key_fields if k in columns]
                if found_keys:
                    print(f"    🔑 关键字段: {', '.join(found_keys[:3])}...")
                    
        else:
            print(f"    ⚠️  表存在但没有数据")
            results[table_name] = {"status": "empty"}
            
    except Exception as e:
        error_msg = str(e)
        if "relation" in error_msg.lower() or "does not exist" in error_msg.lower():
            print(f"    ❌ 表不存在")
            results[table_name] = {"status": "not_found"}
        elif "permission" in error_msg.lower() or "denied" in error_msg.lower():
            print(f"    ❌ 权限不足")
            results[table_name] = {"status": "permission_denied"}
        else:
            print(f"    ❌ 错误: {error_msg[:100]}")
            results[table_name] = {"status": "error", "message": error_msg[:100]}

# 4. 总结
print("\n" + "=" * 70)
print("测试结果总结")
print("=" * 70)

success_count = sum(1 for r in results.values() if r.get("status") == "success")
total_count = len(results)

print(f"\n✅ 成功访问: {success_count}/{total_count} 个表")

if success_count > 0:
    print("\n📊 数据详情:")
    for table, result in results.items():
        if result.get("status") == "success":
            count = result.get("count", "unknown")
            cols = result.get("columns", "unknown")
            print(f"  • {table}")
            print(f"    记录数: {count}")
            print(f"    字段数: {cols}")

# 5. 特别测试模型训练表
print("\n" + "=" * 70)
print("模型训练表详细测试")
print("=" * 70)

model_table = "freddie_mac_delinquency_30_model_2013_2025"
if results.get(model_table, {}).get("status") == "success":
    print(f"\n正在测试 {model_table}...")
    
    try:
        # 获取样本数据
        sample = supabase.table(model_table).select("*").limit(5).execute()
        
        if sample.data and len(sample.data) > 0:
            print(f"  ✅ 成功获取 {len(sample.data)} 条样本数据")
            
            # 检查目标变量
            first_row = sample.data[0]
            if "delinquency_30d_label" in first_row:
                print(f"  ✅ 目标变量 'delinquency_30d_label' 存在")
                
                # 统计标签分布
                try:
                    pos_res = supabase.table(model_table).select("*", count="exact").eq("delinquency_30d_label", 1).limit(1).execute()
                    neg_res = supabase.table(model_table).select("*", count="exact").eq("delinquency_30d_label", 0).limit(1).execute()
                    
                    if hasattr(pos_res, 'count') and hasattr(neg_res, 'count'):
                        print(f"\n  📊 标签分布:")
                        print(f"    正样本 (违约=1): {pos_res.count:,}")
                        print(f"    负样本 (正常=0): {neg_res.count:,}")
                        
                        if pos_res.count and neg_res.count:
                            total = pos_res.count + neg_res.count
                            ratio = pos_res.count / total * 100
                            print(f"    违约率: {ratio:.1f}%")
                            
                            if abs(pos_res.count - neg_res.count) < 1000:
                                print(f"  ✅ 数据集平衡良好")
                            else:
                                print(f"  ⚠️  数据集不平衡")
                except Exception as e:
                    print(f"  ⚠️  无法统计标签分布: {e}")
            
            # 显示关键特征
            key_features = [
                "credit_score", "original_loan_to_value_ltv", 
                "current_interest_rate", "loan_age_years",
                "period_year", "period_month"
            ]
            
            available_features = [f for f in key_features if f in first_row]
            if available_features:
                print(f"\n  🔑 关键特征可用: {len(available_features)}/{len(key_features)}")
                for feat in available_features[:5]:
                    print(f"    ✓ {feat}")
    
    except Exception as e:
        print(f"  ❌ 详细测试失败: {e}")
else:
    print(f"\n⚠️  模型训练表 '{model_table}' 不可用")
    print("   可能需要先运行 SQL 脚本创建表并导入数据")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)

# 给出建议
print("\n💡 建议:")
if success_count == 0:
    print("  ❌ 无法访问任何表，可能的原因:")
    print("    1. 表尚未创建 - 需要运行 SQL 脚本")
    print("    2. 网络连接问题")
    print("    3. API密钥权限不足")
elif success_count < total_count:
    print("  ⚠️  部分表不可用:")
    for table, result in results.items():
        if result.get("status") != "success":
            print(f"    • {table}: {result.get('status')}")
else:
    print("  ✅ 所有表都可以正常访问！")
    print("  ✅ 可以开始运行 Notebook 进行模型训练")

print()

