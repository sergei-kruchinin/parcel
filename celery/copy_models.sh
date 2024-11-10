#!/bin/bash

echo "Пытаемся скопировать models из webapp/src"

MY_PATH="$(dirname "$(readlink -f "$0")")"

SRC_DIR="$MY_PATH/../webapp/src/models"
DST_DIR="$MY_PATH/src"

if [ ! -d "$SRC_DIR" ]; then
  echo "Исходный каталог не существует: $SRC_DIR"
  exit 1
fi

mkdir -p "$DST_DIR"

# Копируем содержимое из webapp/src/models в src/models
if cp -r "$SRC_DIR" "$DST_DIR"; then
  echo "Успешно скопировано"
else
  echo "Не удалось скопировать"
fi