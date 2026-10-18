#!/usr/bin/env bash
# Каскадное сжатие статьи: parts -> L1 -> L2 -> L3.
# Каждая часть сжимается отдельным запуском ai4science (своё окно).
set -e
cd "$(dirname "$0")"
mkdir -p memory/L1

# 1. Сжатие каждой части в L1/part_NN.md
for f in paper/parts/part_*.md; do
  [ -e "$f" ] || continue
  n=$(basename "$f" .md)          # part_01
  out="memory/L1/${n}.md"
  if [ -s "$out" ]; then
    echo "skip $out"
    continue
  fi
  echo "=== compress $f -> $out ==="
  ai4science run "Прочитай файл $f. Сожми его в реферат 100–150 слов.
Числа и единицы — дословно, из текста. Каждое утверждение завершай меткой
вида [с. N], где N — номер страницы из метки [с. N] внутри файла.
Запиши результат в $out. Больше ничего не делай."
done

# 2. Склейка L1
cat memory/L1/part_*.md > memory/L1.md
echo "L1 готов: $(wc -l < memory/L1.md) строк"

# 3. L2 из L1
if [ ! -s memory/L2.md ]; then
  echo "=== L2 из L1 ==="
  ai4science run "Прочитай memory/L1.md. Создай memory/L2.md — 5–10 тезисов
всей статьи. Каждый тезис — проверяемое утверждение (число, условие или
ограничение), со меткой [с. N]. Никаких общих фраз. В конце добавь пустую
таблицу сверки со столбцами: | № | Страница | Цитата | Итог |."
fi

# 4. L3 из L2
if [ ! -s memory/L3.md ]; then
  echo "=== L3 из L2 ==="
  ai4science run "Прочитай memory/L2.md. Создай memory/L3.md — одна строка:
главный результат статьи. Название статьи результатом не является."
fi

echo "Готово: memory/L1.md, memory/L2.md, memory/L3.md"
