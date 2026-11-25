from src.research_tools import deduplicate_text_results


def test_deduplicate_text_results_removes_repeated_blocks():
    text = "First result\\n\\nSecond result\\n\\nFirst result"
    assert deduplicate_text_results(text) == "First result\\n\\nSecond result"


def test_deduplicate_text_results_keeps_empty_input():
    assert deduplicate_text_results("") == ""
