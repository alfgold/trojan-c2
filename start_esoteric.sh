#!/bin/bash
# Эзотерический AI Ассистент - Скрипт запуска

echo "🔮 Эзотерический AI Ассистент 🔮"
echo "=================================="

# Проверка виртуального окружения
if [ ! -d "foxemp_env" ]; then
    echo "❌ Виртуальное окружение не найдено. Создание..."
    python3 -m venv foxemp_env
    source foxemp_env/bin/activate
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение найдено"
fi

# Активация виртуального окружения
source foxemp_env/bin/activate

# Запуск эзотерического AI
if [ $# -eq 0 ]; then
    echo ""
    echo "🔮 Запуск в интерактивном режиме..."
    echo ""
    python3 esoteric_ai.py
else
    echo ""
    echo "🔮 Запуск с параметрами: $@"
    echo ""
    python3 esoteric_ai.py "$@"
fi
