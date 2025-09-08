import math

# ТОЛЬКО для варинтов с ЦЕНОЙ ДЕЛЕНИЯ. Если она не указана, то программа не подходит. 

# Исходные данные
x = [50.1, 50.0, 50.0, 50.1, 50.0]
c = 0.1                          # цена деления
delta_sys = c / 2                # систематическая погрешность
t = 2.776                        # t-критерий для n=5, α=0.05
G_critical = 1.764               # критерий Граббса для n=5, α=0.05

def recalc(values):
    """Возвращает (среднее, стандартное отклонение, стандартное отклонение среднего)."""
    n = len(values)
    avg = sum(values) / n
    s = math.sqrt(sum((xi - avg) ** 2 for xi in values) / (n - 1)) if n > 1 else 0
    s_avg = s / math.sqrt(n) if n > 0 else 0
    return avg, s, s_avg

def grubbs_test(values, Gcrit):
    """Удаляет промахи по критерию Граббса, пока они есть."""
    changed = True
    values = values.copy()
    while changed and len(values) > 2:
        changed = False
        avg, s, _ = recalc(values)
        if s == 0:  # все значения равны
            break
        Gmax = abs(max(values) - avg) / s
        Gmin = abs(avg - min(values)) / s
        if Gmax > Gcrit:
            values.remove(max(values))
            changed = True
        elif Gmin > Gcrit:
            values.remove(min(values))
            changed = True
    return values

def round_uncertainty(value):
    """
    Округляет погрешность до 1–2 значащих цифр
    и возвращает (округленная погрешность, порядок, мантисса, экспонента).
    """
    if value == 0:
        return 0, 0, 0, 0
    exp = math.floor(math.log10(value))
    digits = 1 if value / 10**exp >= 2 else 2   # если >2 → 1 цифра, иначе 2
    rounded = round(value, -exp + (digits - 1))
    return rounded, digits, exp, None

def format_result(avg, delta):
    """Форматирует результат в виде (X ± Δ) × 10^exp"""
    if avg == 0:
        return "0 ± ?"
    exp = math.floor(math.log10(abs(avg)))
    mantissa = avg / (10 ** exp)

    # округляем погрешность
    delta_rounded, _, _, _ = round_uncertainty(delta)

    # количество значащих знаков в мантиссе определяется разрядом погрешности
    digits = int(-math.floor(math.log10(delta_rounded)))

    # форматируем строки с фиксированным количеством знаков
    mantissa_str = f"{mantissa:.{digits}f}"
    delta_str = f"{delta_rounded / 10**exp:.{digits}f}"

    return f"({mantissa_str} ± {delta_str}) × 10^{exp}"


# === Основной код ===

# 1. Удаляем промахи
x_clean = grubbs_test(x, G_critical)

# 2. Пересчитываем статистики
x_avg, s, s_avg = recalc(x_clean)

# 3. Доверительные границы случайной погрешности
epsilon = t * s_avg

# 4. Полная погрешность
delta = math.sqrt(delta_sys**2 + epsilon**2)

# 5. Форматируем результат
result = format_result(x_avg, delta)

# Вывод
print("Очищенные данные:", x_clean)
print("Среднее значение:", x_avg)
print("СКО (Среднее квадратическое отклонение):", s)
print("СКО среднего (Среднее квадратическое отклонение среднего):", s_avg)
print("Случайная погрешность:", epsilon)
print("Полная погрешность:", delta)
print("Результат:", result)