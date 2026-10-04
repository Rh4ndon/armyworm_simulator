# Eggplant Worm Simulator
### (how a tiny moth can destroy an eggplant field — and how farmers stop it)

A single-page web app that simulates the **eggplant fruit and shoot borer**
(*Leucinodes orbonalis*) — the main worm pest of eggplant in the Philippines and
across South Asia. You watch a small farm of 200 eggplants day by day, and see
how weather, a few starting worms, and the farmer's choices (spraying, pheromone
traps, hand-picking) decide whether the harvest survives or not.

Everything runs in your browser — open `index.html` and it just works. No
install, no build, no internet needed (you can also run `./venv/bin/python
server.py` and open the page at `http://localhost:8765`).

## What you can do

- Watch the farm day by day: play/pause, change speed, or step **one day at a time**.
- **Seed the farm** with a few worms (4 by default) on one eggplant and see the outbreak spread.
- **Take control of the weather** — raise the temperature, change humidity, or make it rain — and see how the pest reacts.
- Try **tools**: pheromone traps, whole-farm spraying, or both together.
- **Load a real farm layout** (a CSV where each cell is "plant" or "path").
- **Load a scenario CSV** — a real 120-day record of weather and treatments — and replay it to compare "real life" with the simulation.
- Get a **report at the end**: peak infestation day, rate of spread, how many eggplants got eaten, sprays and trap events, and advice on what might have worked better.

## How the math works (in plain words)

The simulation moves **one day at a time**. On every day, the computer looks at
**each worm** on **every plant** and makes a decision using **chance**. Think of
it as rolling a die for each worm: the numbers below are just the odds of each
event happening to one worm in one day.

### 1. Warmth makes worms grow faster (temperature model)

Worms gain "growth points" every day, but only if it's warm enough:

- Below **14.6 °C** — growth stops completely (too cold to develop).
- Between **14.6 °C and 28 °C** — the warmer it gets, the faster they grow.
- **28 °C is the "perfect" temperature** — worms grow at their fastest here.
- Above that, growth is capped (they can't grow faster than a maximum speed).

When a worm has collected enough growth points to finish its stage, it changes:
**egg → larva (caterpillar) → pupa → adult (moth)**.
An egg needs 4 "warm days", a larva 11, and a pupa 8.

### 2. Bad weather kills worms (death by chance)

Every worm has a **base chance of dying** each day, plus extra chances when the
weather is stressful. The computer rolls a die; if the number comes up below the
total chance, the worm dies.

| Weather condition | Extra death chance |
|---|---|
| It's raining 🌧 | + 10% for eggs, + 5% for larvae, + 3% for pupae |
| Very hot (33 °C or higher) | + 12% |
| Too cold (below 20 °C) | + 5% |
| Very dry (humidity below 50%) | + 10% |
| A bit dry (humidity between 50–60%) | + 3% |

Even with no bad weather, worms have a small base chance of dying each day:
eggs 3%, larvae 2%, pupae 1.5%. No worm ever has more than a 95% chance of dying
in one day (nothing is guaranteed).

**Crowding kills too:** an eggplant can only feed about **5 larvae**. Every larva
above that limit adds another **+5% death chance** each (they compete for food).

### 3. Moths lay eggs (how the pest multiplies)

A female moth lives about **5 days**. She starts laying eggs on her 2nd day and
lays:

| Age of female moth | 1st day | 2nd | 3rd |
|---|---|---|---|
| Eggs laid that night | 0 | **20** | **14** |

(A 4th day gives 14 more, then she's too old and dies.) One plant can hold at
most **30 eggs** — extra eggs don't fit.

### 4. Worms spread (moving to new plants)

- **Babies crawl:** young caterpillars can move up to **3 plants away** (counting
  squares across the grid). They leave when their plant is too crowded and prefer
  to move to a plant with fewer worms.
- **Moths fly:** when a new adult moth comes out, it flies **6–16 plants away**
  to start a "colony" somewhere far from where it was born.

This is how one infested plant becomes a whole infested field.

### 5. Pesticide spray (chemistry with chance)

When the farmer sprays, the whole farm gets a chemical layer for **5 days**.

- **Right away (the instant spray):** eggs have an **80%** chance of dying,
  tiny fresh larvae (**less than half a day old**) have an **85%** chance,
  but older hidden larvae have only a **10%** chance (they're sheltered inside
  the fruit/shoots).
- **While the layer lasts:** every day, eggs and fresh babies get an extra
  **+30%** death chance.

**Auto-spray mode:** the farmer automatically sprays when **5% of plants** are
infested, then waits **7 days** (or 10 for the combined method) before spraying
again.

### 6. Pheromone traps (a love trick)

A pheromone trap smells like a female moth, so it **lures male moths away**:

- Males within **3 plants** of a trap: **60%** chance of being trapped each night.
- Males further away: **15%** chance (the smell reaches the whole small field).
- The fake smell also **confuses the whole field** — real males can't find
  females as easily, so females lay **half** the eggs they normally would.

Traps are placed in a neat **grid** across the farm (4 traps by default).

### 7. Hand-picking (cleaning up, used in the combined method)

Every **7 days**, the farmer visits each plant and removes **45%** of the hidden
larvae by hand — removing the ones the spray can't reach.

### 8. Harvesting the eggplants

Each picking day, a healthy plant gives **3 fruits**. Every larva damages
**0.4 fruits** (it eats into the fruit). So:

```
fruits you get = 3 − (larva damage), but never less than 0
```

The first picking is Day 48, then every 4 days, and the growing season lasts
**120 days**.

### 9. The numbers in the report

- **Infestation %** = the share of plants that have at least one worm, in percent.
- **Rate of spread** = (infested plants at the end − at the start) ÷ days in between —
  "how many new plants get infected each day, on average". The report also shows
  the single fastest daily jump.
- The run ends when worms die out, when **80% of plants** are infested (or **2500 worms**), or after **120 days**.

## Try it — the four "strategies"

| Strategy | What happens |
|---|---|
| **Daily (no control)** | Watch the pest do whatever it wants. |
| **+ Pheromone traps** | Traps catch males and reduce egg-laying. |
| **+ Pesticide spray** | Farmer sprays when 5% of plants are infested. |
| **+ Lure & Spray (combined)** | Traps + less frequent sprays + hand-picking every 7 days. |
| **Scenario** | Replays a CSV record — real weather and treatments, day by day. |

## Make your own scenario file (optional)

A scenario is just a spreadsheet (CSV) with these columns:

```
Day, Infestation, Weather, Temperature (°C), Humidity (%), Treatment
1,,Sunny,30°C,76%,None
20,4 Worms Started,Sunny,31°C,75%,None
55,,Sunny,31°C,72%,Lure
120,,Sunny,31°C,84%,None
,,,,,Interval=7
```

- **Temperature** and **humidity** tell the simulation what the weather was each day.
- **Treatment**: `Spray` or `Lure` means that tool was used *that day*.
- **Infestation**: a written note like `4 Worms Started` on a day tells the
  simulation a farmer found 4 worms on that day.
- **Interval=7** (bottom row) just writes how often a farmer would re-spray.
- Missing days keep the weather of the previous day.

Sample files for real 120-day records (no treatment, spray, lure, both) are in
your `Downloads` folder if you want to try one.

## Where do the numbers come from?

The temperature limits, egg and larvae counts, trap catch rates, and other
values come from published field studies on eggplant fruit and shoot borer —
see **`Research-Sources.md`** in this folder for the full list of sources.

## Files in this folder

| File | What it is |
|---|---|
| `index.html` | The whole simulation (page + math + charts). |
| `farm.csv` | The default farm layout ("plant" cells and cleared paths). |
| `leucinodes_orbonalis_simulation.csv` | A 15-day weather/climate record. |
| `Research-Sources.md` | The scientific sources behind the numbers. |
| `generate_data.py` | The reference model (used to double-check the browser version). |
| `server.py` | Optional little local web server. |