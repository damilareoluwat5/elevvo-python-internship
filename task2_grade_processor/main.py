from grade_processor import (
    InvalidScoreError,
    calculate_average,
    get_highest_and_lowest,
    evaluate_students
)


def main():
    students = [
        {"name": "Mathias Oluwatoyin", "score": 95.0},
        {"name": "Sara Ahmed", "score": 88.5},
        {"name": "Youssef Ibrahim", "score": 72.0},
        {"name": "Tariq Mansoor", "score": 44.0}
    ]

    print("--- Student Grade Report ---")
    for s in evaluate_students(students):
        print(f"{s['name']:<20} | Score: {s['score']:>5.1f} | Status: {s['status']}")

    avg = calculate_average(students)
    high, low = get_highest_and_lowest(students)
    print(f"\nAverage: {avg} | Highest: {high['name']} ({high['score']}) | Lowest: {low['name']} ({low['score']})")

    # Demonstrate custom exception for invalid score
    try:
        evaluate_students([{"name": "Test User", "score": 120}])
    except InvalidScoreError as e:
        print(f"Validation Check Passed -> {e}")


if __name__ == "__main__":
    main()
