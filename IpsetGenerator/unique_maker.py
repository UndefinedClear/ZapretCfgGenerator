def remove_duplicates(input_file, output_file=None):
    """
    Удаляет дубликаты строк из текстового файла.

    :param input_file: Путь к входному файлу (.txt)
    :param output_file: Путь к выходному файлу. Если не указан, перезаписывает входной.
    """
    # Читаем все строки
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Убираем символы новой строки, оставляем уникальные, сохраняя порядок
    seen = set()
    unique_lines = []
    for line in lines:
        stripped = line.strip()  # Убираем \n и пробелы по краям
        if stripped not in seen:
            seen.add(stripped)
            unique_lines.append(line)  # Сохраняем оригинал (с \n)

    # Определяем, куда записывать
    output_path = output_file if output_file else input_file

    # Записываем уникальные строки
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(unique_lines)

    print(f"Обработка завершена. Результат сохранён в: {output_path}")


if __name__ == "__main__":
    input_path = input("Введите путь к файлу (.txt): ").strip().strip('"\'')
    output_choice = input("Перезаписать файл? (y/n): ").lower()

    if output_choice == 'y':
        remove_duplicates(input_path)
    else:
        output_path = input("Введите путь для нового файла: ").strip().strip('"\'')
        remove_duplicates(input_path, output_path)
