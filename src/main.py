"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for several diverse "taste profiles" so we can compare
how the scoring logic behaves for different kinds of listeners.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


# Three (plus one adversarial) distinct taste profiles used for stress testing.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    # Adversarial / conflicting profile: wants calm mood but very high energy.
    "Conflicted (sad but high energy)": {"genre": "edm", "mood": "sad", "energy": 0.95},
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a clean, readable block of the top k recommendations for a profile."""
    print("=" * 60)
    print(f"Profile: {name}")
    print(f"Preferences: {user_prefs}")
    print("-" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']} "
              f"({song['genre']}/{song['mood']}) - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()
