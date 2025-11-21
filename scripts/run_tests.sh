#!/bin/bash

# CRT Model 自动化测试脚本
# 使用方法: bash run_tests.sh [stage]
# 例如: bash run_tests.sh 1  (只运行阶段1)
#      bash run_tests.sh     (运行所有阶段)

echo "════════════════════════════════════════════════════════════════════════"
echo "                    CRT Model 自动化测试"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试结果记录
PASSED=0
FAILED=0

# 函数: 打印阶段标题
print_stage() {
    echo ""
    echo "════════════════════════════════════════════════════════════════════════"
    echo "  阶段 $1: $2"
    echo "════════════════════════════════════════════════════════════════════════"
    echo ""
}

# 函数: 运行测试
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo "▶ 测试: $test_name"
    echo "  命令: $test_cmd"
    echo ""
    
    if eval "$test_cmd"; then
        echo -e "${GREEN}✅ 通过${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ 失败${NC}"
        ((FAILED++))
    fi
    echo ""
}

# 阶段选择
STAGE=${1:-all}

# ═══════════════════════════════════════════════════════════════════════
# 阶段 1: 环境验证
# ═══════════════════════════════════════════════════════════════════════
if [ "$STAGE" = "all" ] || [ "$STAGE" = "1" ]; then
    print_stage "1" "环境验证"
    
    run_test "Python包检查" "python3 check_packages.py"
    
    run_test "数据库连接测试" "python3 utils/quick_test.py"
    
    echo "▶ 检查项目结构"
    if [ -f "notebooks/model_training.ipynb" ] && \
       [ -f "notebooks/data_importing.ipynb" ] && \
       [ -d "utils" ] && \
       [ -d "sql_scripts" ]; then
        echo -e "${GREEN}✅ 项目结构完整${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ 项目结构不完整${NC}"
        ((FAILED++))
    fi
    echo ""
fi

# ═══════════════════════════════════════════════════════════════════════
# 总结
# ═══════════════════════════════════════════════════════════════════════
echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "                    测试结果总结"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}通过: $PASSED${NC}"
echo -e "${RED}失败: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！可以开始运行 Notebook${NC}"
    echo ""
    echo "下一步:"
    echo "  1. 打开 notebooks/model_training.ipynb"
    echo "  2. 按顺序运行 Cell 0-6"
    echo "  3. 参考 TEST_PLAN.txt 记录结果"
    exit 0
else
    echo -e "${RED}⚠️  有测试失败，请检查并修复问题${NC}"
    exit 1
fi

