import ast
import os

# Конфігурація - що включати в скелетон
INCLUDE_DOCSTRINGS = False      # пункт 1: докстрінги функцій
INCLUDE_ERROR_HANDLING = True  # пункт 2: обробка помилок (try/except)
INCLUDE_COMMENTS = False        # пункт 3: коментарі
INCLUDE_MAIN_GUARD = False      # пункт 4: if __name__ == "__main__"
INCLUDE_PRINT_STATEMENTS = False # пункт 5: print statements

def get_skeleton_from_file(filepath: str) -> str:
    """Парсить Python файл і повертає його структуру у вигляді псевдокоду."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        if INCLUDE_ERROR_HANDLING:
            return f"# {filepath} [SyntaxError: {e}]"
        else:
            return f"# {filepath} [SyntaxError]"

    lines = [f"# --- {filepath} ---"]

    for node in tree.body:
        # Пропускаємо if __name__ == "__main__", якщо вимкнено
        if not INCLUDE_MAIN_GUARD and isinstance(node, ast.If):
            if (isinstance(node.test, ast.Compare) and 
                isinstance(node.test.left, ast.Name) and 
                node.test.left.id == '__name__'):
                continue
        
        if isinstance(node, ast.ClassDef):
            lines.append(f"class {node.name}:")
            if INCLUDE_DOCSTRINGS:
                doc = ast.get_docstring(node)
                if doc:
                    lines.append(f'    """{doc}"""')
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    args = [a.arg for a in sub.args.args]
                    lines.append(f"    def {sub.name}({', '.join(args)}): ...")
        elif isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            lines.append(f"def {node.name}({', '.join(args)}): ...")
        elif isinstance(node, ast.Import):
            names = ", ".join([alias.name for alias in node.names])
            lines.append(f"import {names}")
        elif isinstance(node, ast.ImportFrom):
            names = ", ".join([alias.name for alias in node.names])
            lines.append(f"from {node.module} import {names}")
        elif INCLUDE_COMMENTS and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            # Додаємо коментарі (вони зберігаються як рядкові вирази)
            lines.append(f"# {node.value.value}")

    return "\n".join(lines)


def get_project_skeleton(root_folder: str, output_folder: str) -> None:
    """Створює скелет у вигляді одного текстового файлу."""
    skeleton_parts = []
    for subdir, _, files in os.walk(root_folder):
        # Пропускаємо папку, куди будемо зберігати результат
        if output_folder in subdir:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                skeleton_parts.append(get_skeleton_from_file(path))

    skeleton_text = "\n\n".join(skeleton_parts)

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "project_skeleton.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(skeleton_text)

    if INCLUDE_PRINT_STATEMENTS:
        print(f"✅ Скелет збережено у {output_file}")


if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_path, "_skeleton")
    get_project_skeleton(project_path, output_path)
    
    if INCLUDE_PRINT_STATEMENTS:
        print("Генерація завершена")