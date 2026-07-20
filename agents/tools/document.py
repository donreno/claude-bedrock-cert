from markitdown import MarkItDown, StreamInfo
from io import BytesIO
import os

SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(file_path: str) -> str:
    """Converts a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path and converts its contents to
    markdown. Supports PDF and DOCX files, identified by their file
    extension.

    When to use:
    - When you have a filesystem path to a PDF or DOCX document and need
      its contents as markdown.
    - When you don't already have the file's binary data in memory (if
      you do, use `binary_document_to_markdown` instead).

    When not to use:
    - For file types other than PDF or DOCX — this will raise a
      ValueError.

    Examples:
    >>> document_path_to_markdown("report.pdf")
    '# Report\\n\\n...'
    >>> document_path_to_markdown("notes.docx")
    '# Notes\\n\\n...'
    """
    file_type = os.path.splitext(file_path)[1].lstrip(".").lower()
    if file_type not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{file_type}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}."
        )

    with open(file_path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, file_type)
