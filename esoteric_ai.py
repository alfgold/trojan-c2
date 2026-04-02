#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔮 ЭЗОТЕРИЧЕСКИЙ AI АССИСТЕНТ 🔮
Автоматизированная система эзотерических расчетов и консультаций
Зодиак | Нумерология | Матрица Судьбы
"""

import datetime
import json
import math
import sys
import os
from typing import Dict, List, Tuple, Optional

class EsotericAI:
    def __init__(self):
        self.name = "Эзотерический AI Ассистент"
        self.version = "1.0"
        
        # Зодиакальные знаки
        self.zodiac_signs = {
            "Овен": (datetime.datetime(2024, 3, 21), datetime.datetime(2024, 4, 19)),
            "Телец": (datetime.datetime(2024, 4, 20), datetime.datetime(2024, 5, 20)),
            "Близнецы": (datetime.datetime(2024, 5, 21), datetime.datetime(2024, 6, 20)),
            "Рак": (datetime.datetime(2024, 6, 21), datetime.datetime(2024, 7, 22)),
            "Лев": (datetime.datetime(2024, 7, 23), datetime.datetime(2024, 8, 22)),
            "Дева": (datetime.datetime(2024, 8, 23), datetime.datetime(2024, 9, 22)),
            "Весы": (datetime.datetime(2024, 9, 23), datetime.datetime(2024, 10, 22)),
            "Скорпион": (datetime.datetime(2024, 10, 23), datetime.datetime(2024, 11, 21)),
            "Стрелец": (datetime.datetime(2024, 11, 22), datetime.datetime(2024, 12, 21)),
            "Козерог": (datetime.datetime(2024, 12, 22), datetime.datetime(2024, 12, 31)),
            "Козерог": (datetime.datetime(2024, 1, 1), datetime.datetime(2024, 1, 19)),
            "Водолей": (datetime.datetime(2024, 1, 20), datetime.datetime(2024, 2, 18)),
            "Рыбы": (datetime.datetime(2024, 2, 19), datetime.datetime(2024, 3, 20))
        }
        
        # Планеты-управители
        self.planetary_rulers = {
            "Овен": "Марс",
            "Телец": "Венера",
            "Близнецы": "Меркурий",
            "Рак": "Луна",
            "Лев": "Солнце",
            "Дева": "Меркурий",
            "Весы": "Венера",
            "Скорпион": "Плутон/Марс",
            "Стрелец": "Юпитер",
            "Козерог": "Сатурн",
            "Водолей": "Уран/Сатурн",
            "Рыбы": "Нептун/Юпитер"
        }
        
        # Значения чисел в нумерологии
        self.numerology_meanings = {
            1: "Лидерство, независимость, инициатива, сила воли",
            2: "Сотрудничество, дипломатичность, чувствительность, гармония",
            3: "Творчество, коммуникация, оптимизм, самовыражение",
            4: "Стабильность, практичность, дисциплина, организация",
            5: "Свобода, приключения, разнообразие, адаптивность",
            6: "Любовь, семья, ответственность, забота о других",
            7: "Духовность, интуиция, анализ, мудрость",
            8: "Власть, материальный успех, амбиции, карма",
            9: "Гуманитаризм, завершение, духовное пробуждение",
            11: "Интуиция, духовное просветление, вдохновение",
            22: "Мастер-число, большие достижения, реализация идей",
            33: "Мастер-число, учитель, духовное служение"
        }
        
        # Элементы знаков
        self.elements = {
            "Овен": "Огонь",
            "Лев": "Огонь", 
            "Стрелец": "Огонь",
            "Телец": "Земля",
            "Дева": "Земля",
            "Козерог": "Земля",
            "Близнецы": "Воздух",
            "Весы": "Воздух",
            "Водолей": "Воздух",
            "Рак": "Вода",
            "Скорпион": "Вода",
            "Рыбы": "Вода"
        }
        
    def print_header(self):
        print("🔮" * 50)
        print(f"🔮 {self.name} v{self.version} 🔮")
        print("🔮 Эзотерические расчеты и консультации 🔮")
        print("🔮" * 50)
        
    def get_zodiac_sign(self, day: int, month: int) -> str:
        """Определение знака зодиака по дате рождения"""
        try:
            birth_date = datetime.datetime(2024, month, day)
            for sign, (start, end) in self.zodiac_signs.items():
                if start <= birth_date <= end:
                    return sign
        except:
            pass
        return "Неопределено"
    
    def calculate_zodiac_analysis(self, day: int, month: int, year: int) -> Dict:
        """Полный анализ зодиакального знака"""
        sign = self.get_zodiac_sign(day, month)
        element = self.elements.get(sign, "Неизвестно")
        ruler = self.planetary_rulers.get(sign, "Неизвестно")
        
        # Расчет транзитов (упрощенный)
        current_date = datetime.datetime.now()
        birth_date = datetime.datetime(year, month, day)
        age = current_date.year - birth_date.year
        
        # Солнечный возврат
        solar_return = datetime.datetime(current_date.year, month, day)
        days_to_solar = (solar_return - current_date).days
        if days_to_solar < 0:
            solar_return = datetime.datetime(current_date.year + 1, month, day)
            days_to_solar = (solar_return - current_date).days
            
        return {
            "sign": sign,
            "element": element,
            "ruler": ruler,
            "age": age,
            "days_to_solar_return": days_to_solar,
            "solar_return_date": solar_return.strftime("%d.%m.%Y"),
            "description": self.get_zodiac_description(sign)
        }
    
    def get_zodiac_description(self, sign: str) -> str:
        """Описание знака зодиака"""
        descriptions = {
            "Овен": "Энергичный, смелый, инициативный лидер. Путь воина и первопроходца.",
            "Телец": "Стабильный, практичный, чувственный. Путь земного изобилия.",
            "Близнецы": "Интеллектуальный, коммуникационный, adaptable. Путь знания и общения.",
            "Рак": "Эмоциональный, заботливый, интуитивный. Путь семьи и защиты.",
            "Лев": "Творческий, щедрый, харизматичный лидер. Путь самовыражения и славы.",
            "Дева": "Аналитичный, perfectionistic, служебный. Путь healers и организаторов.",
            "Весы": "Гармоничный, дипломатичный, справедливый. Путь партнерства и красоты.",
            "Скорпион": "Интенсивный, трансформирующий, мистический. Путь возрождения.",
            "Стрелец": "Оптимистичный, философский, свободный. Путь знаний и путешествий.",
            "Козерог": "Амбициозный, дисциплинированный, статусный. Путь достижения и мастерства.",
            "Водолей": "Инновационный, гуманитарный, свободомыслящий. Путь будущего.",
            "Рыбы": "Духовный, сострадательный, художественный. Путь слияния и transцendence."
        }
        return descriptions.get(sign, "Уникальная личность со своим особенным путем.")
    
    def calculate_numerology(self, day: int, month: int, year: int) -> Dict:
        """Полный нумерологический расчет"""
        # Число жизненного пути
        life_path = self.reduce_number(day + month + year)
        
        # Число дня рождения
        birth_day = self.reduce_number(day)
        
        # Число судьбы (сумма всех цифр)
        destiny = self.reduce_number(int(str(day) + str(month) + str(year)))
        
        # Число души (гласные в полном имени - упрощено)
        soul_number = self.reduce_number(day + month)  # Упрощенный расчет
        
        # Персональный год
        current_year = datetime.datetime.now().year
        personal_year = self.reduce_number(day + month + current_year)
        
        return {
            "life_path_number": life_path,
            "birth_day_number": birth_day,
            "destiny_number": destiny,
            "soul_number": soul_number,
            "personal_year": personal_year,
            "life_path_meaning": self.numerology_meanings.get(life_path, "Уникальное число"),
            "personal_year_meaning": self.get_personal_year_meaning(personal_year)
        }
    
    def reduce_number(self, number: int) -> int:
        """Сведение чисел к однозначным (мастер-числа сохраняются)"""
        while number > 9 and number not in [11, 22, 33]:
            sum_digits = 0
            for digit in str(number):
                sum_digits += int(digit)
            number = sum_digits
        return number
    
    def get_personal_year_meaning(self, year_number: int) -> str:
        """Значение персонального года"""
        meanings = {
            1: "Новые начинания, независимость, лидерство",
            2: "Сотрудничество, отношения, дипломатия",
            3: "Творчество, общение, самовыражение",
            4: "Работа, стабильность, строительство фундамента",
            5: "Изменения, свобода, приключения",
            6: "Любовь, семья, ответственность",
            7: "Духовность, introspection, мудрость",
            8: "Успех, власть, материальные достижения",
            9: "Завершения, гуманитаризм, духовный рост",
            11: "Духовное пробуждение, интуиция",
            22: "Большие возможности, мастерство",
            33: "Служение, учительство, любовь"
        }
        return meanings.get(year_number, "Особый год с уникальными возможностями")
    
    def calculate_matrix_of_destiny(self, day: int, month: int, year: int) -> Dict:
        """Расчет Матрицы Судьбы"""
        # Создание матрицы 3x3
        birth_date_str = f"{day:02d}{month:02d}{year}"
        
        matrix = [[0 for _ in range(3)] for _ in range(3)]
        
        # Заполнение матрицы по методу Пифагора
        digits = [int(d) for d in birth_date_str]
        
        # Первая строка - характер, интеллект, энергия
        matrix[0][0] = digits[0] if len(digits) > 0 else 0
        matrix[0][1] = digits[1] if len(digits) > 1 else 0
        matrix[0][2] = digits[2] if len(digits) > 2 else 0
        
        # Вторая строка - здоровье, логика, труд
        matrix[1][0] = digits[3] if len(digits) > 3 else 0
        matrix[1][1] = digits[4] if len(digits) > 4 else 0
        matrix[1][2] = digits[5] if len(digits) > 5 else 0
        
        # Третья строка - память, интуиция, цель
        matrix[2][0] = digits[6] if len(digits) > 6 else 0
        matrix[2][1] = digits[7] if len(digits) > 7 else 0
        matrix[2][2] = sum(digits) % 9 or 9  # Цель жизни
        
        # Расчет дополнительных параметров
        character = sum(matrix[0]) % 9 or 9
        health = sum(matrix[1]) % 9 or 9
        purpose = sum(matrix[2]) % 9 or 9
        
        return {
            "matrix": matrix,
            "character_number": character,
            "health_number": health,
            "purpose_number": purpose,
            "interpretation": self.interpret_matrix(matrix)
        }
    
    def interpret_matrix(self, matrix: List[List[int]]) -> Dict:
        """Интерпретация Матрицы Судьбы"""
        interpretation = {}
        
        # Характер (первая строка)
        character_sum = sum(matrix[0])
        interpretation["характер"] = {
            "число": character_sum % 9 or 9,
            "описание": f"Сила характера: {self.get_strength_description(character_sum)}"
        }
        
        # Здоровье (вторая строка)
        health_sum = sum(matrix[1])
        interpretation["здоровье"] = {
            "число": health_sum % 9 or 9,
            "описание": f"Энергия здоровья: {self.get_health_description(health_sum)}"
        }
        
        # Цель (третья строка)
        purpose_sum = sum(matrix[2])
        interpretation["цель"] = {
            "число": purpose_sum % 9 or 9,
            "описание": f"Жизненная цель: {self.get_purpose_description(purpose_sum)}"
        }
        
        return interpretation
    
    def get_strength_description(self, strength: int) -> str:
        """Описание силы характера"""
        if strength >= 20:
            return "Очень сильный характер, лидерские качества"
        elif strength >= 15:
            return "Сильный характер, уверенность в себе"
        elif strength >= 10:
            return "Средняя сила характера, адаптивность"
        else:
            return "Мягкий характер, гибкость"
    
    def get_health_description(self, health: int) -> str:
        """Описание здоровья"""
        if health >= 20:
            return "Хорошая жизненная энергия, крепкое здоровье"
        elif health >= 15:
            return "Средняя энергия, нужно заботиться о здоровье"
        else:
            return "Требуется внимание к здоровью, энергия ниже нормы"
    
    def get_purpose_description(self, purpose: int) -> str:
        """Описание жизненной цели"""
        if purpose >= 20:
            return "Высокая цель, большие амбиции, духовный рост"
        elif purpose >= 15:
            return "Ясная цель, стабильное развитие"
        else:
            return "Поиск цели, духовное самопознание"
    
    def generate_full_report(self, name: str, day: int, month: int, year: int) -> Dict:
        """Генерация полного эзотерического отчета"""
        report = {
            "имя": name,
            "дата_рождения": f"{day:02d}.{month:02d}.{year}",
            "возраст": (datetime.datetime.now() - datetime.datetime(year, month, day)).days // 365,
            "зодиак": self.calculate_zodiac_analysis(day, month, year),
            "нумерология": self.calculate_numerology(day, month, year),
            "матрица_судьбы": self.calculate_matrix_of_destiny(day, month, year),
            "прогноз": self.generate_prediction(day, month, year)
        }
        return report
    
    def generate_prediction(self, day: int, month: int, year: int) -> Dict:
        """Генерация предсказания"""
        current_date = datetime.datetime.now()
        personal_year = self.reduce_number(day + month + current_date.year)
        
        predictions = {
            "персональный_год": personal_year,
            "основные_темы": self.get_year_themes(personal_year),
            "рекомендации": self.get_year_recommendations(personal_year),
            "благоприятные_периоды": self.get_favorable_periods(personal_year)
        }
        return predictions
    
    def get_year_themes(self, year_number: int) -> List[str]:
        """Основные темы года"""
        themes = {
            1: ["Новые проекты", "Независимость", "Лидерство"],
            2: ["Отношения", "Сотрудничество", "Гармония"],
            3: ["Творчество", "Общение", "Самовыражение"],
            4: ["Работа", "Стабильность", "Дисциплина"],
            5: ["Изменения", "Путешествия", "Свобода"],
            6: ["Семья", "Любовь", "Ответственность"],
            7: ["Духовность", "Учеба", "Интроспекция"],
            8: ["Карьера", "Деньги", "Власть"],
            9: ["Завершения", "Мудрость", "Гуманитаризм"],
            11: ["Интуиция", "Духовность", "Вдохновение"],
            22: ["Большие проекты", "Мастерство", "Достижения"],
            33: ["Служение", "Учительство", "Любовь"]
        }
        return themes.get(year_number, ["Уникальные возможности", "Рост", "Трансформация"])
    
    def get_year_recommendations(self, year_number: int) -> List[str]:
        """Рекомендации на год"""
        recommendations = {
            1: ["Начинайте новое", "Будьте лидером", "Действуйте решительно"],
            2: ["Развивайте отношения", "Будьте дипломатичны", "Ищите гармонию"],
            3: ["Творите", "Общайтесь", "Выражайте себя"],
            4: ["Работайте усердно", "Создавайте фундамент", "Будьте дисциплинированы"],
            5: ["Принимайте изменения", "Путешествуйте", "Будьте гибкими"],
            6: ["Заботьтесь о близких", "Создайте любовь", "Будьте ответственны"],
            7: ["Учитесь", "Медитируйте", "Развивайте интуицию"],
            8: ["Стройте карьеру", "Управляйте финансами", "Проявляйте амбиции"],
            9: ["Завершайте старое", "Помогайте другим", "Растите духовно"],
            11: ["Доверяйте интуиции", "Ищите мудрость", "Будьте вдохновителем"],
            22: ["Реализуйте большие идеи", "Проявляйте мастерство", "Думайте масштабно"],
            33: ["Служите другим", "Учите", "Проявляйте любовь"]
        }
        return recommendations.get(year_number, ["Следуйте интуиции", "Развивайтесь", "Будьте открыты"])
    
    def get_favorable_periods(self, year_number: int) -> List[str]:
        """Благоприятные периоды"""
        months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        
        # Упрощенный расчет благоприятных периодов
        favorable = []
        for i, month in enumerate(months, 1):
            if (i + year_number) % 3 == 0:  # Каждые 3 месяца
                favorable.append(month)
        
        return favorable[:4]  # Возвращаем до 4 благоприятных месяцев
    
    def print_report(self, report: Dict):
        """Вывод красивого отчета"""
        print("\n" + "🌟" * 60)
        print(f"🌟 ЭЗОТЕРИЧЕСКИЙ ОТЧЕТ ДЛЯ: {report['имя'].upper()} 🌟")
        print("🌟" * 60)
        
        print(f"\n📅 ДАТА РОЖДЕНИЯ: {report['дата_рождения']}")
        print(f"🎂 ВОЗРАСТ: {report['возраст']} лет")
        
        # Зодиак
        zodiac = report['зодиак']
        print(f"\n🦁 ЗОДИАК: {zodiac['sign']}")
        print(f"   🔥 Элемент: {zodiac['element']}")
        print(f"   🪐 Управитель: {zodiac['ruler']}")
        print(f"   ✨ Описание: {zodiac['description']}")
        print(f"   📅 Солнечный возврат через: {zodiac['days_to_solar_return']} дней")
        
        # Нумерология
        numerology = report['нумерология']
        print(f"\n🔢 НУМЕРОЛОГИЯ:")
        print(f"   🛤️ Число жизненного пути: {numerology['life_path_number']} - {numerology['life_path_meaning']}")
        print(f"   🎯 Число судьбы: {numerology['destiny_number']}")
        print(f"   💫 Число души: {numerology['soul_number']}")
        print(f"   📅 Персональный год: {numerology['personal_year']} - {numerology['personal_year_meaning']}")
        
        # Матрица Судьбы
        matrix = report['матрица_судьбы']
        print(f"\n🔮 МАТРИЦА СУДЬБЫ:")
        print("   ┌───┬───┬───┐")
        for i, row in enumerate(matrix['matrix']):
            print(f"   │ {row[0]} │ {row[1]} │ {row[2]} │")
            if i == 0: print("   ├───┼───┼───┤")
        print("   └───┴───┴───┘")
        
        interpretation = matrix['interpretation']
        print(f"   💪 Характер: {interpretation['характер']['описание']}")
        print(f"   ❤️ Здоровье: {interpretation['здоровье']['описание']}")
        print(f"   🎯 Цель: {interpretation['цель']['описание']}")
        
        # Прогноз
        prediction = report['прогноз']
        print(f"\n🔮 ПРОГНОЗ НА ГОД:")
        print(f"   📊 Персональный год: {prediction['персональный_год']}")
        print(f"   🌟 Основные темы: {', '.join(prediction['основные_темы'])}")
        print(f"   💡 Рекомендации: {', '.join(prediction['рекомендации'])}")
        print(f"   🗓️ Благоприятные периоды: {', '.join(prediction['благоприятные_периоды'])}")
        
        print("\n" + "🌟" * 60)
        print("🌟 БЛАГОСЛОВЕНИЯ НА ВАШ ПУТЬ! 🌟")
        print("🌟" * 60)
    
    def save_report(self, report: Dict, filename: str = None):
        """Сохранение отчета в файл"""
        if not filename:
            name = report['имя'].replace(' ', '_')
            date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"esoteric_report_{name}_{date}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Отчет сохранен: {filename}")
    
    def interactive_mode(self):
        """Интерактивный режим"""
        self.print_header()
        
        while True:
            print("\n" + "="*50)
            print("🔮 МЕНЮ ЭЗОТЕРИЧЕСКОГО AI 🔮")
            print("="*50)
            print("1. 🌟 Полный эзотерический анализ")
            print("2. 🦁 Анализ зодиака")
            print("3. 🔢 Нумерологический расчет")
            print("4. 🔮 Матрица Судьбы")
            print("5. 📅 Прогноз на год")
            print("6. 🚪 Выход")
            print("="*50)
            
            choice = input("\nВыберите опцию (1-6): ").strip()
            
            if choice == '1':
                self.full_analysis_interactive()
            elif choice == '2':
                self.zodiac_analysis_interactive()
            elif choice == '3':
                self.numerology_interactive()
            elif choice == '4':
                self.matrix_interactive()
            elif choice == '5':
                self.prediction_interactive()
            elif choice == '6':
                print("\n🌟 Благодарю за использование! До встречи! 🌟")
                break
            else:
                print("\n❌ Неверный выбор. Попробуйте снова.")
    
    def full_analysis_interactive(self):
        """Интерактивный полный анализ"""
        print("\n🌟 ПОЛНЫЙ ЭЗОТЕРИЧЕСКИЙ АНАЛИЗ 🌟")
        name = input("Введите ваше имя: ").strip()
        
        try:
            day = int(input("День рождения (1-31): "))
            month = int(input("Месяц рождения (1-12): "))
            year = int(input("Год рождения (например, 1990): "))
            
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2024):
                raise ValueError("Некорректная дата")
                
            report = self.generate_full_report(name, day, month, year)
            self.print_report(report)
            
            save = input("\nСохранить отчет в файл? (да/нет): ").strip().lower()
            if save in ['да', 'д', 'yes', 'y']:
                self.save_report(report)
                
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")
    
    def zodiac_analysis_interactive(self):
        """Интерактивный анализ зодиака"""
        print("\n🦁 АНАЛИЗ ЗОДИАКА 🦁")
        try:
            day = int(input("День рождения (1-31): "))
            month = int(input("Месяц рождения (1-12): "))
            year = int(input("Год рождения: "))
            
            analysis = self.calculate_zodiac_analysis(day, month, year)
            print(f"\n🦁 Ваш знак: {analysis['sign']}")
            print(f"🔥 Элемент: {analysis['element']}")
            print(f"🪐 Управитель: {analysis['ruler']}")
            print(f"✨ {analysis['description']}")
            
        except ValueError:
            print("\n❌ Некорректная дата")
    
    def numerology_interactive(self):
        """Интерактивная нумерология"""
        print("\n🔢 НУМЕРОЛОГИЧЕСКИЙ РАСЧЕТ 🔢")
        try:
            day = int(input("День рождения (1-31): "))
            month = int(input("Месяц рождения (1-12): "))
            year = int(input("Год рождения: "))
            
            numerology = self.calculate_numerology(day, month, year)
            print(f"\n🛤️ Число жизненного пути: {numerology['life_path_number']}")
            print(f"   {numerology['life_path_meaning']}")
            print(f"🎯 Число судьбы: {numerology['destiny_number']}")
            print(f"💫 Число души: {numerology['soul_number']}")
            print(f"📅 Персональный год: {numerology['personal_year']}")
            print(f"   {numerology['personal_year_meaning']}")
            
        except ValueError:
            print("\n❌ Некорректная дата")
    
    def matrix_interactive(self):
        """Интерактивная Матрица Судьбы"""
        print("\n🔮 МАТРИЦА СУДЬБЫ 🔮")
        try:
            day = int(input("День рождения (1-31): "))
            month = int(input("Месяц рождения (1-12): "))
            year = int(input("Год рождения: "))
            
            matrix = self.calculate_matrix_of_destiny(day, month, year)
            print("\n🔮 ВАША МАТРИЦА СУДЬБЫ:")
            print("   ┌───┬───┬───┐")
            for i, row in enumerate(matrix['matrix']):
                print(f"   │ {row[0]} │ {row[1]} │ {row[2]} │")
                if i == 0: print("   ├───┼───┼───┤")
            print("   └───┴───┴───┘")
            
            interpretation = matrix['interpretation']
            print(f"\n💪 {interpretation['характер']['описание']}")
            print(f"❤️ {interpretation['здоровье']['описание']}")
            print(f"🎯 {interpretation['цель']['описание']}")
            
        except ValueError:
            print("\n❌ Некорректная дата")
    
    def prediction_interactive(self):
        """Интерактивный прогноз"""
        print("\n📅 ПРОГНОЗ НА ГОД 📅")
        try:
            day = int(input("День рождения (1-31): "))
            month = int(input("Месяц рождения (1-12): "))
            
            prediction = self.generate_prediction(day, month, 2000)  # Год не важен для прогноза
            print(f"\n📊 Персональный год: {prediction['персональный_год']}")
            print(f"🌟 Темы года: {', '.join(prediction['основные_темы'])}")
            print(f"💡 Рекомендации: {', '.join(prediction['рекомендации'])}")
            print(f"🗓️ Благоприятные периоды: {', '.join(prediction['благоприятные_периоды'])}")
            
        except ValueError:
            print("\n❌ Некорректная дата")

def main():
    """Главная функция"""
    esoteric = EsotericAI()
    
    if len(sys.argv) > 1:
        # Командная строка
        if len(sys.argv) >= 5:
            try:
                name = sys.argv[1]
                day = int(sys.argv[2])
                month = int(sys.argv[3])
                year = int(sys.argv[4])
                
                report = esoteric.generate_full_report(name, day, month, year)
                esoteric.print_report(report)
                
                if len(sys.argv) > 5 and sys.argv[5] == '--save':
                    esoteric.save_report(report)
                    
            except ValueError:
                print("❌ Неверный формат даты")
                print("Использование: python3 esoteric_ai.py \"Имя\" день месяц год [--save]")
        else:
            print("Использование: python3 esoteric_ai.py \"Имя\" день месяц год [--save]")
    else:
        # Интерактивный режим
        esoteric.interactive_mode()

if __name__ == "__main__":
    main()
