# Secret santa attributions

Make random attributions of people for a secret santa-style gift exchange. Results will always be a loop (fully connected graph) and no similar attribution will be made twice.

# Run

Create your `people.csv` file (see `people.csv.example`), then run:

`python tirage.py`

Attributions are stored in `tuples.csv` and similar ones will not be made in subsequent runs.

# Example run

```
Elsa -> Doug
Doug -> Casey
Casey -> Zahid
Zahid -> Evan
Evan -> Paige
Paige -> Izzie
Izzie -> Sam
Sam -> Julia
Julia -> Gretchen
Gretchen -> Elsa
```
