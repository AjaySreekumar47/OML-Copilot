from src.prompt_engineering import extract_oml_code


def test_extract_oml_code_from_fenced_block():
    response = """
    Here is the generated OML:

    ```oml
    vocabulary <http://example.com/test> as test {
        concept Person
    }
    ````

    """
    code = extract_oml_code(response)

    assert code is not None
    assert "vocabulary" in code
    assert "concept Person" in code


def test_extract_oml_code_returns_none_without_code_block():
    response = "No code block here."
    assert extract_oml_code(response) is None