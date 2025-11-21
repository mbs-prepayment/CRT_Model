"""
检查所有必需的Python包是否已安装
"""
import sys

print("=" * 70)
print("检查 CRT Model 项目所需的 Python 包")
print("=" * 70)

# 定义所有需要的包
required_packages = {
    'pandas': 'pandas',
    'numpy': 'numpy', 
    'sklearn': 'scikit-learn',
    'supabase': 'supabase',
    'pygam': 'pygam',
    'matplotlib': 'matplotlib',
    'scipy': 'scipy',
}

missing_packages = []
installed_packages = []

print("\n检查中...\n")

for import_name, package_name in required_packages.items():
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', '未知版本')
        print(f"✅ {package_name:20s} - 已安装 (版本: {version})")
        installed_packages.append(package_name)
    except ImportError:
        print(f"❌ {package_name:20s} - 未安装")
        missing_packages.append(package_name)

print("\n" + "=" * 70)
print("检查结果")
print("=" * 70)

print(f"\n✅ 已安装: {len(installed_packages)}/{len(required_packages)} 个包")
print(f"❌ 缺失: {len(missing_packages)} 个包")

if missing_packages:
    print("\n⚠️  需要安装以下包:")
    print("\n运行以下命令安装:")
    print(f"\npip3 install {' '.join(missing_packages)}")
    print("\n或一次性安装所有依赖:")
    print(f"\npip3 install pandas numpy scikit-learn supabase pygam matplotlib scipy")
    sys.exit(1)
else:
    print("\n🎉 所有必需的包都已安装！")
    print("\n✅ 项目可以正常运行")
    print("\n下一步:")
    print("  1. 运行测试: python3 utils/quick_test.py")
    print("  2. 打开 Notebook: jupyter notebook notebooks/model_training.ipynb")
    sys.exit(0)

