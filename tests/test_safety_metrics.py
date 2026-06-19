from storygen.metrics import lexical_diversity, repetition_rate, score_story
from storygen.safety import has_repetitive_loop, trim_repetitive_tail, validate_prompt
from backend.ai_engine import StoryCraftEngine


def test_validate_prompt_rejects_empty_short_and_long_inputs():
    assert not validate_prompt("").ok
    assert not validate_prompt("dragon").ok
    assert not validate_prompt("word " * 1000, max_chars=100).ok


def test_validate_prompt_accepts_story_beginning():
    result = validate_prompt("A lonely astronaut found a garden under the moon.")
    assert result.ok
    assert result.cleaned_prompt.startswith("A lonely astronaut")


def test_repetitive_loop_detection_and_trim():
    text = "blue door opens. blue door opens. blue door opens. blue door opens."
    assert has_repetitive_loop(text, min_phrase_words=2, threshold=3)
    assert trim_repetitive_tail(text) == "blue door opens."


def test_metrics_are_stable():
    story = "The city woke slowly. The river carried silver lights."
    assert lexical_diversity(story) > 0
    assert repetition_rate(story) >= 0
    scores = score_story("city river mystery", story)
    assert {"word_count", "lexical_diversity", "repetition_rate", "prompt_coherence"} <= set(scores)


def test_story_engine_prefers_coherent_non_repetitive_candidate():
    prompt = "Mira entered the clock tower to find the missing inventor."
    repetitive = "Mira waited by the door. Mira waited by the door. Mira waited by the door."
    coherent = "Mira climbed the tower and found the inventor's journal beneath a stopped clock."
    assert StoryCraftEngine._candidate_score(prompt, coherent) > StoryCraftEngine._candidate_score(prompt, repetitive)


def test_story_engine_uses_story_seed_instead_of_instruction_prompt():
    prompt = "A cartographer saw the mountain move at dawn."
    assert StoryCraftEngine._prompt_template(prompt, "Fantasy", "generation") == f"Fantasy story:\n{prompt}\n"
    assert StoryCraftEngine._prompt_template(prompt, "Fantasy", "completion") == f"{prompt}\n"


def test_story_engine_ignores_common_words_when_scoring_relevance():
    prompt = "The cartographer entered the mountain archive."
    unrelated = "The river moved through the valley at dawn."
    relevant = "The cartographer found a map in the mountain archive."
    assert StoryCraftEngine._candidate_score(prompt, relevant) > StoryCraftEngine._candidate_score(prompt, unrelated)
