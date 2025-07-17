#!/usr/bin/env bash
# ============================================================================
# СКРИПТ ПРОВЕРКИ КОДА
# ============================================================================

set -e  # Остановка при ошибках

# Переход в папку проекта
cd "$(dirname "$0")/.."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Запуск полной проверки кода...${NC}"
echo

# Форматирование с Ruff
echo -e "${YELLOW}📝 Форматирование кода...${NC}"
uv run ruff format ./src --config tools/ruff.toml

# Проверка и автофикс с Ruff
echo -e "${YELLOW}🔧 Исправление проблем...${NC}"
uv run ruff check ./src --fix --config tools/ruff.toml

# Проверка типов с Ty
echo -e "${YELLOW}🔍 Проверка типов с Ty...${NC}"
uv run ty check ./src --config-file tools/ty.toml

# Проверка типов с MyPy
echo -e "${YELLOW}🔬 Проверка типов с MyPy...${NC}"
uv run mypy ./src --config-file tools/mypy.ini

# Запуск pre-commit проверок
echo -e "${YELLOW}🚀 Pre-commit проверки...${NC}"
uv run pre-commit run --all-files

echo
echo -e "${GREEN}✅ Все проверки завершены успешно!${NC}"
