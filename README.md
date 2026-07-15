# Book Recommendation Engine

A Python desktop app that recommends books to users based on 
purchase similarity, using the Jaccard similarity algorithm.

## How it works
- Each user's purchase history is stored as a set of book IDs
- Jaccard similarity (|A ∩ B| / |A ∪ B|) is calculated between 
  the target user and every other user
- The most similar user's unique purchases become the recommendations

## Tech
- Python (OOP)
- Tkinter (GUI)
- JSON (data export)

## Run it
```bash
python book_recommender.py
```

## Example
Select a user from the dropdown, click "Generate Recommendations" 
to see their purchase history and personalized book suggestions 
based on the most similar user.
