def test_package_imports():
    import src

    assert hasattr(src, "OMLRetriever")
    assert hasattr(src, "EmbeddingManager")
    assert hasattr(src, "create_instruction_prompt")
    assert hasattr(src, "extract_oml_code")
    assert hasattr(src, "ExamplesProcessor")
    assert hasattr(src, "DependencyExtractor")