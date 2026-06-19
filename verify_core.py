from storygen.metrics import score_story
from storygen.safety import has_repetitive_loop, validate_prompt


def main():
    prompt = "A lonely astronaut found a garden under the moon."
    story = "The garden shimmered quietly. The astronaut stepped closer and heard a voice."
    validation = validate_prompt(prompt)
    assert validation.ok
    assert score_story(prompt, story)["word_count"] > 0
    assert has_repetitive_loop("red door opens red door opens red door opens", 3, 3)
    print("Core validation, safety, and metrics checks passed.")


if __name__ == "__main__":
    main()
