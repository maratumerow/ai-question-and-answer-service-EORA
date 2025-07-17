## ➡️ [ссылка для проверяющего ТЗ. (Описание тестового задания)](docs/DESCRIPTION.md) ⬅️

# EORA Q&A Сервис


 ИИ-сервис для вопросов и ответов по кейсам и проектам компании EORA.


## 🚀 Features

- **Интеллектуальные Q&A**: Задавайте вопросы и получайте контекстные ответы на основе корпоративных знаний
- **Управление источниками**: Загружайте и обрабатывайте контент с URL для построения базы знаний
- **Умный поиск источников**: Автоматически находите релевантные источники для каждого вопроса
- **RESTful API**: Чистый, хорошо документированный API
- **Асинхронная обработка**: Оптимальная производительность в реальном времени
- **Комплексное логирование**: Детальное логирование для мониторинга и отладки

## 🏗️ Архитектура

Проект следует принципам **Clean Architecture** с четким разделением задач:

- **Доменный слой**: Бизнес-сущности, интерфейсы и доменная логика
- **Слой приложения**: Use cases, DTO и сервисы приложения
- **Инфраструктурный слой**: Внешние интеграции, базы данных и сторонние сервисы
- **Слой представления**: HTTP API, контроллеры и внедрение зависимостей

Подробную документацию по архитектуре см. в [ARCHITECTURE.md](ARCHITECTURE.md).

## 🛠️ Tech Stack

- **Фреймворк**: FastAPI
- **Язык**: Python 3.12+
- **База данных**: PostgreSQL с async SQLAlchemy
- **ИИ/LLM**: Anthropic Claude API
- **Парсинг**: httpx + BeautifulSoup4
- **Валидация**: Pydantic
- **Миграции**: Alembic
- **Контейнеризация**: Docker и Docker Compose

## 📋 Предварительные требования

- Python 3.12 или выше
- Docker и Docker Compose
- Ключ Anthropic API
- uv package manager (будет установлен автоматически если отсутствует)

> **Важно**: Docker должен быть запущен перед началом установки, так как setup автоматически поднимает PostgreSQL в контейнере.

## ⚙️ Установка и настройка

### 🚀 Быстрый старт с Makefile

1. **Клонируйте репозиторий**
```bash
git clone git@github.com:maratumerow/ai-question-and-answer-service-EORA.git
cd ai-question-and-answer-service-EORA
```

2. **Убедитесь, что Docker запущен**
```bash
docker --version
docker-compose --version
```

3. **Запустите полную настройку одной командой**
```bash
cd scripts && make setup
```

**Что делает `make setup`:**
- Создает Python виртуальное окружение
- Устанавливает все зависимости
- Копирует `.env.example` в `.env` (если не существует)
- **Автоматически запускает PostgreSQL в Docker**
- Ожидает готовности базы данных
- Применяет все миграции базы данных

4. **Отредактируйте .env файл** с вашими настройками (обязательно укажите ANTHROPIC_API_KEY)

5. **Запустите приложение**
```bash
make run
```

6. **Когда закончите работу**, остановите сервисы
```bash
make docker-down
```

> **Примечание**: Все команды Makefile находятся в папке `scripts/`. После setup доступны команды: `make run`, `make check`, `make docker-setup`, `make docker-up` и другие.

### 🐳 Альтернативный способ: Полное развертывание в Docker

Если вы предпочитаете запустить все приложение в Docker:

```bash
cd scripts
make docker-setup  # Настройка окружения
make docker-up     # Запуск всех сервисов в Docker
```

### 🛠️ Ручная установка (без Makefile)

<details>
<summary>Развернуть инструкции по ручной установке</summary>

1. **Создайте виртуальное окружение**
```bash
uv venv
uv sync
```

2. **Настройте переменные окружения**
```bash
cp config/.env.example .env
# Отредактируйте .env файл
```

3. **Запустите PostgreSQL**
```bash
docker-compose -f docker/docker-compose.yml up -d postgres
```

4. **Примените миграции**
```bash
uv run alembic upgrade head
```

5. **Запустите приложение**
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

</details>


## 🎯 Использование API

### Health Check
```bash
curl http://localhost:8000/api/v1/health/
```

### Загрузка источников
```bash
curl -X POST "http://localhost:8000/api/v1/sources/load" \
     -H "Content-Type: application/json" \
     -d '{
      "urls": [
            "https://eora.ru/cases/promyshlennaya-bezopasnost",
            "https://eora.ru/cases/lamoda-systema-segmentacii-i-poiska-po-pohozhey-odezhde",
            "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/karas-golosovoy-assistent",
            "https://eora.ru/cases/assistenty-dlya-gorodov",
            "https://eora.ru/cases/avtomatizaciya-v-promyshlennosti/chemrar-raspoznovanie-molekul",
            "https://eora.ru/cases/zeptolab-skazki-pro-amnyama-dlya-sberbox",
            "https://eora.ru/cases/goosegaming-algoritm-dlya-ocenki-igrokov",
            "https://eora.ru/cases/dodo-pizza-robot-analitik-otzyvov",
            "https://eora.ru/cases/ifarm-nejroset-dlya-ferm",
            "https://eora.ru/cases/zhivibezstraha-navyk-dlya-proverki-rodinok",
            "https://eora.ru/cases/sportrecs-nejroset-operator-sportivnyh-translyacij",
            "https://eora.ru/cases/avon-chat-bot-dlya-zhenshchin",
            "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/navyk-dlya-proverki-loterejnyh-biletov",
            "https://eora.ru/cases/computer-vision/iss-analiz-foto-avtomobilej",
            "https://eora.ru/cases/purina-master-bot",
            "https://eora.ru/cases/skinclub-algoritm-dlya-ocenki-veroyatnostej",
            "https://eora.ru/cases/skolkovo-chat-bot-dlya-startapov-i-investorov",
            "https://eora.ru/cases/purina-podbor-korma-dlya-sobaki",
            "https://eora.ru/cases/purina-navyk-viktorina",
            "https://eora.ru/cases/dodo-pizza-pilot-po-avtomatizacii-kontakt-centra",
            "https://eora.ru/cases/dodo-pizza-avtomatizaciya-kontakt-centra",
            "https://eora.ru/cases/icl-bot-sufler-dlya-kontakt-centra",
            "https://eora.ru/cases/s7-navyk-dlya-podbora-aviabiletov",
            "https://eora.ru/cases/workeat-whatsapp-bot",
            "https://eora.ru/cases/absolyut-strahovanie-navyk-dlya-raschyota-strahovki",
            "https://eora.ru/cases/kazanexpress-poisk-tovarov-po-foto",
            "https://eora.ru/cases/kazanexpress-sistema-rekomendacij-na-sajte",
            "https://eora.ru/cases/intels-proverka-logotipa-na-plagiat",
            "https://eora.ru/cases/karcher-viktorina-s-voprosami-pro-uborku",
            "https://eora.ru/cases/chat-boty/purina-friskies-chat-bot-na-sajte",
            "https://eora.ru/cases/nejroset-segmentaciya-video",
            "https://eora.ru/cases/chat-boty/essa-nejroset-dlya-generacii-rolikov",
            "https://eora.ru/cases/qiwi-poisk-anomalij",
            "https://eora.ru/cases/frisbi-nejroset-dlya-raspoznavaniya-pokazanij-schetchikov",
            "https://eora.ru/cases/skazki-dlya-gugl-assistenta",
            "https://eora.ru/cases/chat-boty/hr-bot-dlya-magnit-kotoriy-priglashaet-na-sobesedovanie"
        ]
    }'
```

### Ask Question
```bash
curl -X POST "http://localhost:8000/api/v1/questions/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Какие основные услуги предоставляет EORA?"
     }'
```

### Интерактивная документация API

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 🚨 Устранение неполадок

### Проблемы с setup

**Ошибка: "could not connect to server: Connection refused"**
- Убедитесь, что Docker запущен: `docker --version`
- Проверьте, что порт 5432 свободен: `lsof -i :5432`
- Попробуйте перезапустить setup: `make docker-down && make setup`

**Ошибка: "timeout waiting for PostgreSQL"**
- Увеличьте время ожидания в Makefile или запустите вручную:
```bash
docker-compose -f docker/docker-compose.yml up -d postgres
# Подождите 30-60 секунд
make setup
```

**Проблемы с портами**
- PostgreSQL использует порт 5432
- Приложение использует порт 8000
- Убедитесь, что эти порты свободны

### Проблемы с API
- Проверьте, что ANTHROPIC_API_KEY установлен в .env
- Убедитесь, что база данных запущена: `docker ps`
- Проверьте логи: `tail -f logs/eora_errors.log`

## 🗂️ Project Structure

```
src/
├── domain/              # Domain layer (entities, interfaces)
│   ├── entities/        # Business entities
│   ├── repositories/    # Repository interfaces
│   ├── services/        # Domain service interfaces
│   └── exceptions/      # Domain exceptions
├── application/         # Application layer (use cases, DTOs)
│   ├── use_cases/       # Business use cases
│   └── dto/            # Data transfer objects
├── infrastructure/     # Infrastructure layer (implementations)
│   ├── database/       # Database models & connections
│   ├── repositories/   # Repository implementations
│   └── services/       # External service implementations
├── presentation/       # Presentation layer (API)
│   ├── api/           # API controllers
│   ├── dependencies/  # Dependency injection
│   └── setup/         # Application setup
└── core/              # Core utilities
    ├── config/        # Configuration
    ├── logging/       # Logging setup
    └── middleware/    # Middleware
```

## 🧪 Testing (проект еще не покрыт тестами)


## 🔧 Development

### Инструменты качества кода

Проект включает автоматизированный скрипт для проверки качества кода:

```bash
# Запуск всех проверок одной командой
./scripts/check_code.sh

# Или из папки scripts с помощью Makefile
make check
```

Скрипт выполняет:
- 📝 Форматирование кода с Ruff
- 🔧 Автоисправление проблем
- 🔍 Проверку типов с Ty и MyPy
- 🚀 Pre-commit проверки

> Все инструменты настроены с конфигурационными файлами в папке `tools/`

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## 📊 Мониторинг и логирование

Приложение включает комплексное логирование:

- **Application logs**: `logs/eora.log`
- **Error logs**: `logs/eora_errors.log`
- **Request/Response logging**: Via middleware
- **Database query logging**: When DEBUG=true

## 🚀 Deployment

### Production Environment (Не готов к продакшену)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow Clean Architecture principles
- Write comprehensive tests
- Use type hints everywhere
- Add docstrings for public methods
- Follow PEP 8 style guide

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support:
- Create an issue in the repository
- Contact the development team
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

**Made with ❤️ for EORA Company**
