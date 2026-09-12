from fastapi import APIRouter, HTTPException

from rules import dsng_tree as tree
from schemas.diagnostic import CategoryOut, NodeOut, OptionOut

router = APIRouter(prefix="/api/diagnostic", tags=["diagnostic"])


@router.get("/categories", response_model=list[CategoryOut])
def list_categories():
    """All fault categories -- equivalent to the home-screen grid in the frontend."""
    return [
        CategoryOut(id=c.id, title=c.title, description=c.description, root=c.root)
        for c in tree.CATEGORIES
    ]


@router.get("/node/{node_id}", response_model=NodeOut)
def get_node(node_id: str):
    """
    A single diagnostic-tree node: either a question with options, or a
    terminal result with severity + recommended steps. The frontend walks
    this graph one call at a time so the decision logic lives in exactly
    one place (this module), never duplicated client-side.
    """
    try:
        node = tree.get_node(node_id)
    except tree.UnknownNodeError:
        raise HTTPException(status_code=404, detail=f"Unknown diagnostic node: {node_id}")

    return NodeOut(
        id=node.id,
        is_result=node.is_result,
        question=node.question,
        options=[OptionOut(label=o.label, next=o.next) for o in node.options],
        severity=node.severity,
        title=node.title,
        steps=node.steps,
    )


@router.get("/stats")
def stats():
    return {
        "categories": len(tree.CATEGORIES),
        "scenarios": tree.total_scenarios(),
    }


@router.get("/_integrity")
def integrity_check():
    """
    Not part of the public product surface -- a diagnostic-of-the-diagnostics
    endpoint used by CI / the test suite to catch a broken tree edit
    (e.g. an option pointing at a typo'd node id) before it ships.
    """
    problems = tree.validate_tree_integrity()
    return {"healthy": len(problems) == 0, "problems": problems}
