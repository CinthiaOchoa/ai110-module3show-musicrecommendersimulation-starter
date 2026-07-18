# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is a classroom simulation, not a real product. It suggests songs from a
small fixed catalog that match a listener's stated taste (a favorite genre, a favorite
mood, and how energetic they want the music to be). It assumes the user can describe
their taste up front and that the catalog is small enough to score in full. It is meant
for learning how recommenders turn data into ranked predictions — not for real users or
any decision that matters.

---

## 3. How the Model Works

Every song carries a few labels: its genre, its mood, and numbers between 0 and 1 for
things like energy. The user says what they like. For each song the model adds up points:
2 points if the genre matches, 1 point if the mood matches, and up to 2 more points
depending on how close the song's energy is to what the user wants. A song whose energy is
exactly right gets the full bonus, and the bonus shrinks the further off it is. Then it
sorts all the songs by their total points and shows the top five, along with a short
sentence explaining where the points came from. Compared to the starter code, I filled in
the empty scoring and ranking functions, made energy reward *closeness* instead of just
high numbers, and added the plain-English "reasons."

---

## 4. Data

The catalog has **18 songs**. Each song has: id, title, artist, genre, mood, energy,
tempo_bpm, valence, danceability, and acousticness. I expanded the original 10 songs by
adding 8 more to cover genres and moods the starter file was missing — punk, folk, edm,
blues, world, hip hop, classical, and reggae, with moods like aggressive, nostalgic,
euphoric, melancholy, peaceful, and dramatic. It is still tiny and English/Western-leaning,
and it has no `sad` songs even though a user can ask for that mood, so parts of real
musical taste are simply missing.

---

## 5. Strengths

- For clear, consistent profiles (e.g. "Chill Lofi") the top results are exactly the songs
  a person would expect — the two lofi/chill tracks score highest.
- The energy-closeness rule works well: it correctly separates "intense rock" from
  "chill lofi" instead of always preferring the loudest song.
- The reasons make every ranking transparent — you can always see why a song scored what
  it did, which matched my intuition when I checked results by hand.

---

## 6. Limitations and Bias

The biggest weakness is that **genre is weighted highest (+2.0)**, so the system leans
toward the user's stated genre and can hide great cross-genre songs that match their mood —
a classic filter bubble. It also ignores preferences it can't satisfy: the "Conflicted"
profile asked for a `sad` mood, but since no song is tagged `sad`, that rule silently does
nothing and ranking falls back to genre + energy. Features like valence, danceability, and
acousticness are stored but not scored, so listeners who care about those get no benefit.
Finally, with only 18 songs, popular genres crowd the top of many lists and there just
isn't enough variety to serve unusual tastes.

---

## 7. Evaluation

I tested four profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and an
adversarial **Conflicted** profile (sad mood but very high energy). I looked at whether the
top 5 for each felt right and whether different profiles produced genuinely different lists.

Profile comparisons:

- **Chill Lofi vs. Deep Intense Rock:** completely different tops — Lofi surfaces
  low-energy lofi/chill tracks (Library Rain, 5.00), while Rock surfaces high-energy
  intense tracks (Storm Runner, 4.98). This makes sense: the energy-closeness rule pulls
  each list toward opposite ends of the energy scale, exactly what those profiles test for.
- **High-Energy Pop vs. Deep Intense Rock:** both want high energy, so they *share* songs
  like Gym Hero and Storm Runner, but genre flips the winner — Pop puts Sunrise City first,
  Rock puts Storm Runner first. This shows genre acting as the tie-breaker among similarly
  energetic songs.
- **Conflicted vs. the rest:** the surprise was that a "sad" request had no effect at all,
  because the dataset has no sad songs, so the profile behaved like a plain edm/high-energy
  request. That revealed the "silently ignored preference" limitation above.

---

## 8. Future Work

- Score the unused numeric features (valence, danceability, acousticness) so more of a
  user's taste actually counts.
- Add a diversity penalty so the same artist/genre can't dominate the whole top-5.
- Warn the user when a requested genre or mood doesn't exist in the catalog instead of
  silently ignoring it, and grow the dataset so rarer tastes have real options.

---

## 9. Personal Reflection

My biggest learning moment was realizing a recommender is just a scoring function plus a
sort — once each song has a number, "recommending" is only ranking. AI tools were most
helpful for brainstorming the energy-closeness formula and for suggesting adversarial
profiles I wouldn't have thought of, but I had to double-check the math and the weights
myself, and I caught the "no sad songs" gap by reading the actual output rather than
trusting it. What surprised me most is how a handful of simple weighted rules can feel like
the app "gets" you — and how the invisible choice of those weights is exactly where bias
sneaks into real recommendation systems.
