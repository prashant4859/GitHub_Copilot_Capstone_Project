from pathlib import Path
import argparse

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def table_to_markdown(table: Table) -> list[str]:
    rows = []

    for row in table.rows:
        rows.append([escape_cell(cell.text) for cell in row.cells])

    if not rows:
        return []

    width = max(len(row) for row in rows)

    normalized_rows = [
        row + [""] * (width - len(row))
        for row in rows
    ]

    output = []

    first = normalized_rows[0]
    output.append("| " + " | ".join(first) + " |")
    output.append("| " + " | ".join(["---"] * width) + " |")

    for row in normalized_rows[1:]:
        output.append("| " + " | ".join(row) + " |")

    return output


def paragraph_to_markdown(paragraph: Paragraph) -> list[str]:
    text = paragraph.text.strip()

    if not text:
        return []

    style_name = paragraph.style.name if paragraph.style else ""

    if style_name.startswith("Heading"):
        try:
            level = int(style_name.split()[-1])
            level = min(max(level, 1), 6)
            return [f"{'#' * level} {text}", ""]
        except ValueError:
            pass

    if style_name.startswith("List"):
        return [f"- {text}"]

    return [text, ""]


def convert_docx(input_path: Path, output_path: Path) -> None:
    document = Document(input_path)

    output = [
        "# Extracted Word Source",
        "",
        f"Source File: {input_path.name}",
        "",
        "---",
        "",
    ]

    for block in document.iter_inner_content():
        if isinstance(block, Paragraph):
            output.extend(paragraph_to_markdown(block))

        elif isinstance(block, Table):
            output.extend(table_to_markdown(block))
            output.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(output).rstrip() + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Extract a Word .docx source into Markdown."
    )

    parser.add_argument(
        "input",
        help="Path to the Word .docx file.",
    )

    parser.add_argument(
        "--output",
        default=".sdlc/input/raw/word-extracted.md",
        help="Markdown output path.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Word document does not exist: {input_path}"
        )

    if input_path.suffix.lower() != ".docx":
        raise ValueError(
            "Only .docx Word documents are supported."
        )

    convert_docx(input_path, output_path)

    print(f"WORD_EXTRACTION_COMPLETE: {output_path}")


if __name__ == "__main__":
    main()