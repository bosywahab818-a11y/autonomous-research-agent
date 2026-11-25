from src.research_tools import deduplicate_text_results, limit_result_text


def test_deduplicate_text_results_removes_repeated_blocks():
    text = "First result\n\nSecond result\n\nFirst result"
    assert deduplicate_text_results(text) == "First result\n\nSecond result"


def test_deduplicate_text_results_keeps_empty_input():
    assert deduplicate_text_results("") == ""


def test_limit_result_text_keeps_short_text_unchanged():
    assert limit_result_text("short result", 20) == "short result"


def test_limit_result_text_truncates_long_text():
    result = limit_result_text("word " * 100, 80)
    assert len(result) <= 130
    assert "result shortened" in result
