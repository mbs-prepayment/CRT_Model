"""
显示Supabase数据库连接信息
"""
import base64
import json

print("=" * 70)
print("Supabase 数据库连接信息")
print("=" * 70)

# 数据库URL
url = "https://ptukzshzuloxipzwycte.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB0dWt6c2h6dWxveGlwend5Y3RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxNjg0OTMsImV4cCI6MjA2Nzc0NDQ5M30.MAnlnrt0traaFjE-QV3jSKETU6woZJ8LcVIqjrAIiQ4"

print("\n📊 数据库基本信息:")
print(f"  • 数据库URL: {url}")
print(f"  • 项目引用ID (Reference ID): ptukzshzuloxipzwycte")
print(f"  • 区域: 根据URL推测可能在美国")
print(f"  • API端点: {url}/rest/v1/")

print("\n🔑 API密钥信息:")
try:
    # 手动解析JWT token (不验证签名)
    parts = key.split('.')
    if len(parts) == 3:
        # 解码payload部分 (第二部分)
        payload = parts[1]
        # 添加padding如果需要
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded = json.loads(decoded_bytes)
        
        print(f"  • 密钥类型: {decoded.get('role', 'unknown')}")
        print(f"  • 发行者: {decoded.get('iss', 'unknown')}")
        print(f"  • 项目引用: {decoded.get('ref', 'unknown')}")
        
        # 时间戳
        iat = decoded.get('iat')
        exp = decoded.get('exp')
        
        if iat:
            from datetime import datetime
            iat_date = datetime.fromtimestamp(iat)
            print(f"  • 创建时间: {iat_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if exp:
            exp_date = datetime.fromtimestamp(exp)
            now = datetime.now()
            days_remaining = (exp_date - now).days
            
            print(f"  • 过期时间: {exp_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if days_remaining > 0:
                print(f"  • 状态: ✅ 有效 (剩余 {days_remaining} 天)")
            else:
                print(f"  • 状态: ❌ 已过期 ({abs(days_remaining)} 天前)")
    else:
        print(f"  • 密钥格式: JWT")
        print(f"  • 密钥长度: {len(key)} 字符")
        
except Exception as e:
    print(f"  • 密钥格式: JWT (无法解析详情)")
    print(f"  • 密钥长度: {len(key)} 字符")

print("\n📋 项目中使用的数据表:")
tables = [
    {
        "name": "freddie_mac_crt_raw_2023_2023",
        "description": "原始CRT数据表 (2013-2023)",
        "fields": "86个字段",
        "purpose": "存储从文本文件导入的原始数据",
        "used_in": "CRT_Data_Inserting.ipynb"
    },
    {
        "name": "freddie_mac_delinquency_30_model_2013_2025",
        "description": "30天违约模型训练表 (2013-2025)",
        "fields": "~56个字段",
        "purpose": "特征工程后的平衡数据集 (40,000条记录)",
        "used_in": "30_days_delinquency_2013_2025.ipynb"
    },
    {
        "name": "freddie_mac_crt_raw_clean1",
        "description": "清洗后的原始数据表",
        "fields": "86个字段",
        "purpose": "SQL特征工程的数据源表",
        "used_in": "SQL脚本"
    }
]

for i, table in enumerate(tables, 1):
    print(f"\n  [{i}] {table['name']}")
    print(f"      描述: {table['description']}")
    print(f"      字段: {table['fields']}")
    print(f"      用途: {table['purpose']}")
    print(f"      使用: {table['used_in']}")

print("\n🔗 访问和管理:")
print(f"  • Supabase Dashboard:")
print(f"    https://supabase.com/dashboard/project/ptukzshzuloxipzwycte")
print(f"  • 数据库直接连接 (PostgreSQL):")
print(f"    在 Dashboard > Settings > Database 中查看连接字符串")
print(f"  • REST API 端点:")
print(f"    {url}/rest/v1/[table_name]")

print("\n📝 项目文件使用情况:")
files = [
    ("CRT_Data_Inserting.ipynb", "数据导入 (从Google Drive)", "✅ 使用此数据库"),
    ("CRT_Data_Inserting (1).ipynb", "数据导入 (备份版本)", "✅ 使用此数据库"),
    ("30_days_delinquency_2013_2025 (1).ipynb", "GAM模型训练和评估", "✅ 使用此数据库"),
    ("30 Days Delinquency... (SQL)", "特征工程SQL脚本", "✅ 针对此数据库"),
]

for filename, purpose, status in files:
    print(f"\n  • {filename}")
    print(f"    功能: {purpose}")
    print(f"    状态: {status}")

print("\n" + "=" * 70)
print("💡 重要提示:")
print("=" * 70)
print("  ✓ 所有项目文件都连接到同一个 Supabase 数据库实例")
print("  ✓ 项目ID: ptukzshzuloxipzwycte")
print("  ✓ 使用的是 'anon' (匿名) 密钥 - 用于客户端访问")
print("  ✓ 建议在 Supabase Dashboard 中配置 Row Level Security (RLS)")
print("  ✓ 如需完整管理权限，使用 'service_role' 密钥 (在Dashboard中获取)")
print("\n  ⚠️  注意: 不要在公开的代码库中暴露 API 密钥!")
print("=" * 70)
