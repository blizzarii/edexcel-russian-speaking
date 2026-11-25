import random
import time
from pathlib import Path

QUESTION_FILE = Path(__file__).with_name("questions.txt")


def load_questions(path):
    """Read 'theme | question' lines into a dict: {theme: [questions]}."""
    bank = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            theme, question = (part.strip() for part in line.split("|", 1))
            bank.setdefault(theme, []).append(question)
    return bank


def choose_questions(bank):
    """Let the user pick one theme or all of them."""
    themes = list(bank)
    print("\nPick a theme:")
    for i, theme in enumerate(themes, start=1):
        print(f"  {i}. {theme} ({len(bank[theme])} questions)")
    print("  0. All themes")
    while True:
        choice = input("> ").strip()
        if choice == "0":
            return [q for qs in bank.values() for q in qs]
        if choice.isdigit() and 1 <= int(choice) <= len(themes):
            return list(bank[themes[int(choice) - 1]])
        print("Type a number from the list.")


def ask(question):
    """Show one question, time the answer, return the self-rating."""
    print(f"\n{question}")
    start = time.time()
    input("Answer out loud, then press Enter... ")
    print(f"You spoke for about {int(time.time() - start)} seconds.")
    while True:
        rating = input("How did it go? 1 = bad, 2 = ok, 3 = good (q to quit): ").strip().lower()
        if rating in ("1", "2", "3", "q"):
            return rating
        print("Type 1, 2, 3 or q.")


def run_round(questions):
    """Ask every question once. Return the ones rated below 3, or None if quit."""
    random.shuffle(questions)
    retry = []
    for question in questions:
        rating = ask(question)
        if rating == "q":
            return None
        if rating != "3":
            retry.append(question)
    return retry


def main():
    if not QUESTION_FILE.exists():
        print(f"Can't find {QUESTION_FILE.name}. Put it in the same folder as this script.")
        return

    bank = load_questions(QUESTION_FILE)
    if not bank:
        print("No questions found. Check the 'theme | question' format.")
        return

    questions = choose_questions(bank)
    round_number = 1
    while questions:
        print(f"\n--- Round {round_number}: {len(questions)} questions ---")
        questions = run_round(questions)
        if questions is None:
            print("\nStopped. Good session.")
            return
        round_number += 1
        if questions:
            print(f"\n{len(questions)} to retry.")

    print("\nEvery question rated 3. Done.")


if __name__ == "__main__":
    main()
