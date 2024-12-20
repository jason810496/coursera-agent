def parse_markdown_list(self, markdown: str) -> list[str]:
    """
    input example:
    ```
    - item1
    - item2
    - item3
    ```
    output:
    ['item1', 'item2', 'item3']
    """
    result = []
    for line in markdown.split("\n"):
        if line.startswith("-"):
            result.append(line[1:].strip())
    return result


__all__ = [
    "parse_markdown_list",
]
