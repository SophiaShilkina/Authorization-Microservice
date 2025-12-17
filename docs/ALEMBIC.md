# Работа с миграциями
Скрипты запускать из корня проекта.

## Создание миграций 

```bash
  alembic revision --autogenerate -m "Описание миграции"
```

## Применение миграций

```bash
  alembic upgrade head
```

## Откат на одну миграцию

```bash
  alembic downgrade -1
```

## Откат до конкретной миграции

```bash
  alembic downgrade айди_миграции
```

## Откат всех миграций 

```bash
  alembic downgrade base
```

## Удаление миграции
Откатить до нужной миграции и удалить файл лишней миграции в alembic/versions.

## Просмотр истории миграций

```bash
  alembic history
```