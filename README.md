# 🎵 Music Recommender Simulation

## Project Summary

This project is a small, content-based music recommender called **VibeFinder 1.0**.
It represents each song as a set of attributes (genre, mood, energy, and more) and
represents a listener as a "taste profile." For any profile it scores every song in
the catalog, ranks them, and prints the top matches together with a plain-English
reason for each score. The goal is not to build a production system but to *simulate*
and *explain* how a simple recommender turns data into predictions.

---

## How The System Works

Real platforms like Spotify or TikTok mostly blend two ideas:

- **Collaborative filtering** — "people who liked what you liked also liked X." It uses
  the behavior of *other users* (likes, skips, playlists, listening history) and needs
  no knowledge of what a song actually sounds like.
- **Content-based filtering** — "this song is similar to songs you like." It uses the
  *attributes of the song itself* (genre, tempo, mood, energy) and compares them to a
  profile of the user's taste.

My version is **content-based only**. It has no user history, so it prioritizes matching
song attributes to a stated taste profile.

**Features each `Song` uses:** `genre`, `mood`, `energy`, plus extra numeric attributes in
the dataset (`tempo_bpm`, `valence`, `danceability`, `acousticness`).

**What the `UserProfile` stores:** a `favorite_genre`, a `favorite_mood`, a numeric
`target_energy` (0.0–1.0), and a `likes_acoustic` flag. In the CLI the same idea is
expressed as a simple dictionary: `{"genre": ..., "mood": ..., "energy": ...}`.

**Algorithm Recipe (how a score is computed):**

| Rule | Points |
|------|--------|
| Genre match | **+2.0** |
| Mood match | **+1.0** |
| Energy closeness | **+2.0 × (1 − \|song energy − target energy\|)** |

Energy is scored by *closeness*, not size: a song whose energy exactly equals the target
earns the full +2.0, and the reward shrinks as the gap grows. This rewards "the right
vibe" instead of just always favoring the loudest track.

**Scoring Rule vs. Ranking Rule:** the *Scoring Rule* (`score_song`) judges one song in
isolation and produces a number plus a list of reasons. The *Ranking Rule*
(`recommend_songs`) applies the scoring rule to every song, sorts the whole catalog from
high to low, and returns the top `k`. You need both: scoring answers "how good is this
song for you?" and ranking answers "out of everything, which few should I actually show?"

**Data flow:** Input (user prefs) → Process (loop over every song, score each one) →
Output (sort and return the top K recommendations with reasons).

**Expected bias:** because a genre match is worth the most points, the system likely
over-prioritizes genre and can bury great songs that match the user's *mood* but not
their genre.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` loads the 18-song catalog and ranks it for each profile:

```
Loaded songs: 18

============================================================
Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
------------------------------------------------------------
1. Sunrise City by Neon Echo (pop/happy) - Score: 4.84
   Because: genre match (+2.0); mood match (+1.0); energy close to target (+1.84)
2. Gym Hero by Max Pulse (pop/intense) - Score: 3.94
   Because: genre match (+2.0); energy close to target (+1.94)
3. Rooftop Lights by Indigo Parade (indie pop/happy) - Score: 2.72
   Because: mood match (+1.0); energy close to target (+1.72)
4. Storm Runner by Voltline (rock/intense) - Score: 1.98
   Because: energy close to target (+1.98)
5. Neon Dancefloor by Pulse Theory (edm/euphoric) - Score: 1.90
   Because: energy close to target (+1.9)

============================================================
Profile: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
------------------------------------------------------------
1. Library Rain by Paper Lanterns (lofi/chill) - Score: 5.00
   Because: genre match (+2.0); mood match (+1.0); energy close to target (+2.0)
2. Midnight Coding by LoRoom (lofi/chill) - Score: 4.86
   Because: genre match (+2.0); mood match (+1.0); energy close to target (+1.86)
3. Focus Flow by LoRoom (lofi/focused) - Score: 3.90
   Because: genre match (+2.0); energy close to target (+1.9)
4. Spacewalk Thoughts by Orbit Bloom (ambient/chill) - Score: 2.86
   Because: mood match (+1.0); energy close to target (+1.86)
5. Coffee Shop Stories by Slow Stereo (jazz/relaxed) - Score: 1.96
   Because: energy close to target (+1.96)

============================================================
Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
------------------------------------------------------------
1. Storm Runner by Voltline (rock/intense) - Score: 4.98
   Because: genre match (+2.0); mood match (+1.0); energy close to target (+1.98)
2. Gym Hero by Max Pulse (pop/intense) - Score: 2.94
   Because: mood match (+1.0); energy close to target (+1.94)
3. Neon Dancefloor by Pulse Theory (edm/euphoric) - Score: 1.90
   Because: energy close to target (+1.9)
4. Basement Riot by Static Fury (punk/aggressive) - Score: 1.86
   Because: energy close to target (+1.86)
5. Sunrise City by Neon Echo (pop/happy) - Score: 1.84
   Because: energy close to target (+1.84)

============================================================
Profile: Conflicted (sad but high energy)
Preferences: {'genre': 'edm', 'mood': 'sad', 'energy': 0.95}
------------------------------------------------------------
1. Neon Dancefloor by Pulse Theory (edm/euphoric) - Score: 4.00
   Because: genre match (+2.0); energy close to target (+2.0)
2. Gym Hero by Max Pulse (pop/intense) - Score: 1.96
   Because: energy close to target (+1.96)
3. Basement Riot by Static Fury (punk/aggressive) - Score: 1.96
   Because: energy close to target (+1.96)
4. Storm Runner by Voltline (rock/intense) - Score: 1.92
   Because: energy close to target (+1.92)
5. Sunrise City by Neon Echo (pop/happy) - Score: 1.74
   Because: energy close to target (+1.74)
```

---

## Experiments You Tried

- **Weight shift (genre 2.0 → 0.5):** dropping the genre weight let mood/energy matches
  compete. "Off-genre" songs that share the user's mood climbed the list — the results
  felt more varied but less "on theme."
- **Feature removal (comment out mood):** rankings barely changed for genre-heavy
  profiles, which confirmed that genre + energy do most of the work; mood is only a
  tie-breaker at its current +1.0 weight.
- **Adversarial / conflicting profile** (`edm` + `sad` + `energy 0.95`): because no song is
  tagged `sad`, the mood rule never fires and ranking collapses to genre + energy. This
  exposed that the system silently ignores preferences it can't satisfy instead of
  flagging them.

---

## Limitations and Risks

- It only works on a tiny 18-song catalog, so variety is limited.
- It does not understand lyrics, language, or *why* someone likes a song.
- Genre is worth the most points, so it can create a "filter bubble" that over-favors the
  user's stated genre and hides good cross-genre matches.
- A mood the dataset doesn't contain (e.g. `sad`) is silently ignored rather than handled.

You will go deeper on this in the model card.

---

## Reflection

Building this made the "data → prediction" pipeline concrete: a recommendation is really
just a scoring function applied to every item and then sorted. Once each song has a
number attached, "recommending" is nothing more than ranking and slicing the top few.
Watching the same recipe produce sensible, different lists for the Lofi vs. Rock profiles
made a very simple algorithm *feel* intelligent, even though it's just weighted addition.

The clearest lesson about bias was how much the choice of weights matters. By making
genre worth twice a mood match, I quietly told the system that genre is what counts most —
so it will keep suggesting in-genre songs and rarely surprise the user. In a real product
that same design choice, scaled up, is exactly how filter bubbles form: the system keeps
showing you more of what you already said you liked. Small, invisible decisions in the
scoring rule turn into real fairness and diversity problems at scale.

See the full [**Model Card**](model_card.md) for intended use, biases, and future work.
