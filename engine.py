import json
import random
import time

def load_templates(path="templates.json"):
    """Loads JSON data from the specified path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_lexicon(templates, n=30):
    """
    Generates a lexicon of n words with unique forms, meanings, and glyphs.
    """
    phonemes = templates["phonemes"]
    glyph_radicals = templates["glyph_radicals"]
    # Make a copy of the meanings list to avoid modifying the original template data
    meanings = list(templates["meanings"])
    random.shuffle(meanings)

    lexicon = {}
    used_forms = set()
    used_glyphs = set()

    for i in range(n):
        # Generate a unique form
        while True:
            form = "".join(random.choices(phonemes, k=random.randint(2, 3)))
            if form not in used_forms:
                used_forms.add(form)
                break

        # Generate a unique glyph
        while True:
            glyph = "".join(random.choices(glyph_radicals, k=templates["generator_hints"]["glyph_radicals_per_glyph"]))
            if glyph not in used_glyphs:
                used_glyphs.add(glyph)
                break

        lexicon[i] = {
            "form": form,
            "glyph": glyph,
            "meaning": meanings[i]
        }
    return lexicon

def choose_grammar(templates):
    """Randomly selects a grammar system from the templates."""
    return random.choice(templates["grammar_options"])

def load_world(path="world.json"):
    """Loads a world state from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def new_world(seed=None):
    """
    Generates a new world state, including lexicon, grammar, and artifacts.
    """
    if seed is None:
        seed = int(time.time())
    random.seed(seed)

    templates = load_templates()

    lexicon_size = templates["generator_hints"]["default_lexicon_size"]
    lexicon = generate_lexicon(templates, n=lexicon_size)
    grammar = choose_grammar(templates)

    # Create a minimal set of ruins
    ruins = [
        {
            "id": 0,
            "description": random.choice(templates["room_templates"])
        }
    ]

    # Create at least one artifact with an inscription
    artifacts = []
    artifact_template = random.choice(templates["artifact_templates"])
    inscription_length = random.randint(2, 5)
    inscription = [random.choice(list(lexicon.keys())) for _ in range(inscription_length)]

    artifacts.append({
        "id": 0,
        "type": artifact_template["type"],
        "location": 0, # Belongs to the first ruin
        "inscription": inscription
    })

    world = {
        "seed": seed,
        "grammar": grammar,
        "lexicon": lexicon,
        "ruins": ruins,
        "artifacts": artifacts
    }

    with open("world.json", 'w', encoding='utf-8') as f:
        json.dump(world, f, indent=2, ensure_ascii=False)

    return seed

def save_progress(save, path="save.json"):
    """Saves the current game state to a JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(save, f, indent=2, ensure_ascii=False)

def load_progress(path="save.json"):
    """Loads a saved game state from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def recreate_world(seed):
    """Recreates a world from a specific seed."""
    return new_world(seed)

if __name__ == "__main__":
    generated_seed = new_world()
    print(f"World generated with seed: {generated_seed}")