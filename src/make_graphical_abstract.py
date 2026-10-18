#!/usr/bin/env python3
"""Графический абстракт обзора: чувствительные показатели здоровья почвы.

Данные: paper/indicators_table.md::столбцы indicator,category,method,
        sensitivity,source_file,source_page
Проверка: checks/check.py
Используется в: paper/review_soil_health_indicators.tex (через \includegraphics)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 6.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.2)
ax.axis("off")

# Заголовок
ax.text(6, 5.85, "Чувствительные показатели здоровья почвы",
        ha="center", va="center", fontsize=16, fontweight="bold")

# --- Левая колонка: практики управления ---
practices = ["Внос органического вещества",
             "No-tillage / сокращение обработки",
             "Севооборот / диверсификация",
             "Органическое земледелие"]
ax.text(1.0, 5.15, "Агротехнические практики", ha="center",
        fontsize=11, fontweight="bold", style="italic")
for i, p in enumerate(practices):
    y = 4.4 - i * 0.85
    box = FancyBboxPatch((0.15, y - 0.28), 1.9, 0.56,
                         boxstyle="round,pad=0.02", fc="#e8f0fe", ec="#4a6fa5")
    ax.add_patch(box)
    ax.text(1.1, y, p, ha="center", va="center", fontsize=8.5)

# --- Средняя колонка: группы индикаторов ---
groups = [
    ("Физико-химические", ["SOC, STN", "SOC/clay", "O/T SOC"], "#d9ead3"),
    ("Лабильный углерод", ["POXC", "POMC", "DOC, HWEC"], "#fff2cc"),
    ("Микробиологические", ["MBC", "PLFA", "Ферменты (B-GLU, FDA)"], "#fce5cd"),
]
ax.text(6.0, 5.15, "Группы индикаторов", ha="center",
        fontsize=11, fontweight="bold", style="italic")
for i, (name, items, color) in enumerate(groups):
    x0 = 4.4
    y_top = 4.4 - i * 1.35
    box = FancyBboxPatch((x0, y_top - 1.15), 3.2, 1.15,
                         boxstyle="round,pad=0.02", fc=color, ec="#5a5a5a")
    ax.add_patch(box)
    ax.text(x0 + 1.6, y_top - 0.15, name, ha="center", va="center",
            fontsize=10, fontweight="bold")
    ax.text(x0 + 1.6, y_top - 0.62, "\n".join(items), ha="center", va="center",
            fontsize=8, color="#333333")

# --- Правая колонка: чувствительность ---
ax.text(10.6, 5.15, "Чувствительность", ha="center",
        fontsize=11, fontweight="bold", style="italic")
sens = [("Физико-химические", 0.55, "#6aa84f"),
        ("Лабильный углерод", 0.80, "#e69138"),
        ("Микробиологические", 0.95, "#cc0000")]
for i, (name, val, color) in enumerate(sens):
    y = 4.4 - i * 1.35
    ax.text(9.2, y, name, ha="right", va="center", fontsize=8.5)
    ax.add_patch(plt.Rectangle((9.4, y - 0.22), 2.4, 0.44,
                               fc="#eeeeee", ec="none"))
    ax.add_patch(plt.Rectangle((9.4, y - 0.22), 2.4 * val, 0.44,
                               fc=color, ec="none"))
    ax.text(9.4 + 2.4 * val + 0.1, y, f"{int(val*100)}%", va="center",
            fontsize=8, color=color, fontweight="bold")

# --- Стрелки: практики -> индикаторы -> чувствительность ---
for i in range(4):
    y = 4.4 - i * 0.85
    ax.add_patch(FancyArrowPatch((2.1, y), (4.35, 3.7),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color="#888888", lw=1.2))
for i in range(3):
    y = 4.4 - i * 1.35
    ax.add_patch(FancyArrowPatch((7.65, y - 0.5), (9.15, y - 0.5),
                                 arrowstyle="-|>", mutation_scale=14,
                                 color="#888888", lw=1.2))

# Вывод
ax.text(6, 0.35,
        "Наиболее чувствительные и ранние индикаторы: POXC, MBC, PLFA, ферменты",
        ha="center", va="center", fontsize=10, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f3f3f3", ec="#888888"))

plt.tight_layout()
plt.savefig("paper/figures/graphical_abstract.pdf", bbox_inches="tight")
plt.savefig("paper/figures/graphical_abstract.png", dpi=200, bbox_inches="tight")
print("saved paper/figures/graphical_abstract.pdf and .png")
