#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import math

DATA_FILE_PATH = "./values.json"


def load_data_from_json(file_path):
    """
    Загрузка данных из JSON-файла.
    Ожидается, что файл содержит JSON-объект со всеми необходимыми параметрами.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


# Загрузка данных из JSON
data = load_data_from_json(DATA_FILE_PATH)

# Присвоение значений переменным с более понятными именами
daily_product_output = float(data["daily_product_output"])    # Суточная выработка готовой продукции (Qсут)
shift_duration = float(data["shift_duration"])                # Длительность рабочей смены (t)
dumpling_machine_capacity = float(data["dumpling_machine_capacity"])  # Производительность пельменного автомата (рпа)
dough_mass_fraction = float(data["dough_mass_fraction"])      # Массовая доля теста в готовой продукции (%)
dough_kneader_capacity = float(data["dough_kneader_capacity"])# Производительность тестомесильной машины (ртм)
cutter_capacity = float(data["cutter_capacity"])              # Производительность куттера (рк)
meat_mass_fraction = float(data["meat_mass_fraction"])        # Массовая доля мяса (%)
eggs_mass_fraction = float(data["eggs_mass_fraction"])        # Массовая доля яиц (%)
salt_mass_fraction = float(data["salt_mass_fraction"])        # Массовая доля соли (%)
spices_mass_fraction = float(data["spices_mass_fraction"])    # Массовая доля специй (%)

print(f"Суточная выработка готовой продукции (daily_product_output): {daily_product_output}")
print(f"Длительность рабочей смены (shift_duration): {shift_duration}")
print(f"Производительность пельменного автомата (dumpling_machine_capacity): {dumpling_machine_capacity}")
print(f"Массовая доля теста (%) (dough_mass_fraction): {dough_mass_fraction}")
print(f"Производительность тестомесильной машины (dough_kneader_capacity): {dough_kneader_capacity}")
print(f"Производительность куттера (cutter_capacity): {cutter_capacity}")
print(f"Массовая доля мяса (%) (meat_mass_fraction): {meat_mass_fraction}")
print(f"Массовая доля яиц (%) (eggs_mass_fraction): {eggs_mass_fraction}")
print(f"Массовая доля соли (%) (salt_mass_fraction): {salt_mass_fraction}")
print(f"Массовая доля специй (%) (spices_mass_fraction): {spices_mass_fraction}")
print()

def calculate_dumpling_machine_count(daily_output, shift_hours, machine_capacity):
    """
    Рассчитывает необходимое количество пельменных автоматов.

    :param daily_output: суточная выработка готовой продукции (Qсут)
    :param shift_hours: длительность рабочей смены (t)
    :param machine_capacity: производительность одного пельменного автомата
    :return: количество автоматов (округление вверх)
    """
    half_shift_output = daily_output / (2 * shift_hours)
    required_count = math.ceil(half_shift_output / machine_capacity)
    print("Соотношение для пельменных автоматов:", half_shift_output / machine_capacity)
    return required_count


def calculate_dough_kneaders_count(daily_output, shift_hours, dough_fraction, kneader_capacity):
    """
    Рассчитывает необходимое количество тестомесильных машин.

    :param daily_output: суточная выработка готовой продукции (Qсут)
    :param shift_hours: длительность рабочей смены (t)
    :param dough_fraction: массовая доля теста в готовой продукции (%)
    :param kneader_capacity: производительность тестомесильной машины
    :return: количество машин (округление вверх)
    """
    half_shift_output = daily_output / (2 * shift_hours)
    dough_output = half_shift_output * dough_fraction / 100.0
    required_count = math.ceil(dough_output / kneader_capacity)
    print("Соотношение для тестомесильных машин:", dough_output / kneader_capacity)
    return required_count


def calculate_cutters_count(daily_output, shift_hours, dough_fraction, cutter_capacity):
    """
    Рассчитывает необходимое количество куттеров.

    :param daily_output: суточная выработка готовой продукции (Qсут)
    :param shift_hours: длительность рабочей смены (t)
    :param dough_fraction: массовая доля теста в готовой продукции (%)
    :param cutter_capacity: производительность куттера
    :return: количество куттеров (округление вверх)
    """
    half_shift_output = daily_output / (2 * shift_hours)
    filling_output = ((100 - dough_fraction) * half_shift_output) / 100.0
    required_count = math.ceil(filling_output / cutter_capacity)
    print("Соотношение для куттеров:", filling_output / cutter_capacity)
    return required_count


def is_ingredient_composition_valid(dough, meat, eggs, salt, spices):
    """
    Проверяет, что сумма массовых долей всех ингредиентов равна 100%.

    :param dough: доля теста (%)
    :param meat: доля мяса (%)
    :param eggs: доля яиц (%)
    :param salt: доля соли (%)
    :param spices: доля специй (%)
    :return: True, если сумма равна 100%, иначе False
    """
    total_fraction = dough + meat + eggs + salt + spices
    return math.isclose(total_fraction, 100.0, rel_tol=1e-9)

# Основная логика
if is_ingredient_composition_valid(dough_mass_fraction,
                                   meat_mass_fraction,
                                   eggs_mass_fraction,
                                   salt_mass_fraction,
                                   spices_mass_fraction):
    num_dumpling_machines = calculate_dumpling_machine_count(daily_product_output, shift_duration, dumpling_machine_capacity)
    num_dough_kneaders = calculate_dough_kneaders_count(daily_product_output, shift_duration, dough_mass_fraction, dough_kneader_capacity)
    num_cutters = calculate_cutters_count(daily_product_output, shift_duration, dough_mass_fraction, cutter_capacity)

    print("Количество пельменных автоматов:", num_dumpling_machines)
    print("Количество тестомесильных машин:", num_dough_kneaders)
    print("Количество куттеров:", num_cutters)
else:
    print("Состав ингредиентов некорректен: сумма долей не равна 100%.")
