import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rules import dsng_tree as tree


def test_tree_integrity():
    """Every category root and every option target must resolve to a real node."""
    problems = tree.validate_tree_integrity()
    assert problems == [], f"Broken diagnostic tree: {problems}"


def test_six_categories():
    assert len(tree.CATEGORIES) == 6


def test_scenario_count_matches_frontend():
    # Kept in sync with the 26 documented scenarios in app/dsng-troubleshooter.html.
    assert tree.total_scenarios() == 26


def test_every_category_root_is_a_question_not_a_result():
    for cat in tree.CATEGORIES:
        root_node = tree.get_node(cat.root)
        assert not root_node.is_result, f"Category '{cat.id}' root should not be a terminal node"


def test_unknown_node_raises():
    import pytest
    with pytest.raises(tree.UnknownNodeError):
        tree.get_node("does_not_exist")


def test_unknown_category_raises():
    import pytest
    with pytest.raises(tree.UnknownCategoryError):
        tree.get_category("does_not_exist")


def test_walk_no_signal_happy_path_to_a_result():
    """Simulate an engineer answering 'Yes' repeatedly through the No Signal tree."""
    node = tree.get_node("ns1")
    steps = 0
    while not node.is_result and steps < 10:
        first_option = node.options[0]
        node = tree.get_node(first_option.next)
        steps += 1
    assert node.is_result
    assert node.severity in ("critical", "warning", "info")
    assert len(node.steps) > 0
