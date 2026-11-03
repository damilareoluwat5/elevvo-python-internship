from typing import List, Dict, Any, Tuple


class InvalidScoreError(Exception):
    """Custom exception raised when a student's score is outside 0 to 100."""
    pass


def validate_score(score: float) -> float:
    """Validates that a score is numeric and between 0 and 100."""
    if not isinstance(score, (int, float)) or score < 0 or score > 100:
        raise InvalidScoreError(f"Invalid score: {score}. Must be between 0 and 100.")
    return float(score)


def calculate_average(records: List[Dict[str, Any]]) -> float:
    """Calculates the average score for a list of student dictionaries."""
    if not records:
        return 0.0
    scores = [validate_score(r["score"]) for r in records]
    return round(sum(scores) / len(scores), 2)


def get_highest_and_lowest(records: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Returns the student dictionaries with the highest and lowest scores."""
    if not records:
        return {}, {}
    for r in records:
        validate_score(r["score"])
    return max(records, key=lambda x: x["score"]), min(records, key=lambda x: x["score"])


def evaluate_students(records: List[Dict[str, Any]], pass_mark: float = 50.0) -> List[Dict[str, Any]]:
    """Determines pass/fail status for each student record."""
    results = []
    for r in records:
        score = validate_score(r["score"])
        results.append({
            "name": r["name"],
            "score": score,
            "status": "Pass" if score >= pass_mark else "Fail"
        })
    return results
