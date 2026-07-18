import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# --- Algorithm Recipe (weights) ---------------------------------------------
# These constants define how many points each kind of match is worth.
# A genre match is worth the most, a mood match a bit less, and energy is
# scored by how *close* a song is to the user's target (not just how high).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 2.0


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score(fav_genre: Optional[str], fav_mood: Optional[str],
           target_energy: Optional[float], genre: str, mood: str,
           energy: float) -> Tuple[float, List[str]]:
    """Shared scoring rule used by both the dict and class based APIs."""
    score = 0.0
    reasons: List[str] = []

    if fav_genre and genre == fav_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    if fav_mood and mood == fav_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    if target_energy is not None:
        # Closeness is 1.0 when energy is identical, 0.0 when it is 1.0 apart.
        closeness = 1.0 - abs(energy - target_energy)
        points = round(ENERGY_WEIGHT * closeness, 2)
        score += points
        reasons.append(f"energy close to target (+{points})")

    if not reasons:
        reasons.append("no strong matches")

    return round(score, 2), reasons


class Recommender:
    """Object oriented wrapper that ranks Song objects for a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects sorted from best to worst match."""
        ranked = sorted(
            self.songs,
            key=lambda s: _score(user.favorite_genre, user.favorite_mood,
                                  user.target_energy, s.genre, s.mood,
                                  s.energy)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human readable explanation of a song's score."""
        score, reasons = _score(user.favorite_genre, user.favorite_mood,
                                 user.target_energy, song.genre, song.mood,
                                 song.energy)
        return f"Score {score}: " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numbers."""
    numeric_fields = ("energy", "tempo_bpm", "valence", "danceability",
                      "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in numeric_fields:
                if field in row and row[field] != "":
                    row[field] = float(row[field])
            if "id" in row and row["id"] != "":
                row["id"] = int(row["id"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song dict against user preference dict; return (score, reasons)."""
    return _score(
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        user_prefs.get("energy"),
        song.get("genre"),
        song.get("mood"),
        float(song.get("energy", 0.0)),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict],
                    k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
