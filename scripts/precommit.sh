#!/bin/bash
# ============================================================================
# СКРИПТ ДЛЯ УПРАВЛЕНИЯ PRE-COMMIT
# ============================================================================

set -e  # Остановка при ошибках

cd "$(dirname "$0")/.."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовков
print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo
}

# Функция для проверки успешности выполнения
check_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        exit 1
    fi
}

# Функция для поиска pre-commit
find_precommit() {
    # Попробуем разные варианты запуска pre-commit
    if command -v uv >/dev/null 2>&1; then
        # Если есть uv, используем его
        echo "uv run pre-commit"
    elif [ -f ".venv/bin/pre-commit" ]; then
        # Если есть локальный .venv
        echo "$(pwd)/.venv/bin/pre-commit"
    elif [ -f "venv/bin/pre-commit" ]; then
        # Если есть venv
        echo "$(pwd)/venv/bin/pre-commit"
    elif command -v pre-commit >/dev/null 2>&1; then
        # Если pre-commit установлен глобально
        echo "pre-commit"
    else
        echo ""
    fi
}

# Найдем pre-commit
PRECOMMIT=$(find_precommit)

if [ -z "$PRECOMMIT" ]; then
    echo -e "${RED}❌ Pre-commit не найден! Установите его через:${NC}"
    echo -e "${YELLOW}  uv add --dev pre-commit${NC}"
    echo -e "${YELLOW}  или${NC}"
    echo -e "${YELLOW}  pip install pre-commit${NC}"
    exit 1
fi

# Показываем какой метод используется (только в debug режиме)
if [ "$DEBUG" = "true" ]; then
    echo -e "${BLUE}🔧 Используется: $PRECOMMIT${NC}"
fi

case "$1" in
    "install")
        print_header "УСТАНОВКА PRE-COMMIT HOOKS"
        $PRECOMMIT install
        check_success "Pre-commit hooks установлены"
        ;;

    "run")
        print_header "ЗАПУСК ВСЕХ PRE-COMMIT ПРОВЕРОК"
        $PRECOMMIT run --all-files
        check_success "Все проверки прошли успешно"
        ;;

    "ruff")
        print_header "ПРОВЕРКА И ИСПРАВЛЕНИЕ КОДА (RUFF)"
        $PRECOMMIT run ruff --all-files
        check_success "Ruff проверка завершена"
        ;;

    "format")
        print_header "ФОРМАТИРОВАНИЕ КОДА"
        $PRECOMMIT run ruff-format --all-files
        check_success "Код отформатирован"
        ;;

    "mypy")
        print_header "ПРОВЕРКА ТИПОВ (MYPY)"
        $PRECOMMIT run mypy --all-files
        check_success "MyPy проверка завершена"
        ;;

    "update")
        print_header "ОБНОВЛЕНИЕ PRE-COMMIT HOOKS"
        $PRECOMMIT autoupdate
        check_success "Hooks обновлены"
        ;;

    "clean")
        print_header "ОЧИСТКА PRE-COMMIT КЭША"
        $PRECOMMIT clean
        check_success "Кэш очищен"
        ;;

    *)
        echo -e "${YELLOW}Использование: ./scripts/precommit.sh [команда]${NC}"
        echo
        echo "Доступные команды:"
        echo -e "  ${GREEN}install${NC}  - Установить pre-commit hooks"
        echo -e "  ${GREEN}run${NC}      - Запустить все проверки"
        echo -e "  ${GREEN}ruff${NC}     - Проверить код с Ruff"
        echo -e "  ${GREEN}format${NC}   - Отформатировать код"
        echo -e "  ${GREEN}mypy${NC}     - Проверить типы с MyPy"
        echo -e "  ${GREEN}update${NC}   - Обновить hooks"
        echo -e "  ${GREEN}clean${NC}    - Очистить кэш"
        ;;
esac
