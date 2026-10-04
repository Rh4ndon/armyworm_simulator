# Armyworm (Leucinodes orbonalis) Field Simulator

An agent-based, daily-timestep simulation of eggplant fruit & shoot borer (EFSB,
*Leucinodes orbonalis*) infestation on a grid of eggplant plants, driven by real
weather, with optional control strategies (pheromone mass-trapping, pesticide
sprays, sanitation) and CSV-scenario replay.

Open `index.html` in a browser (or serve it with `./venv/bin/python server.py`
for the local file-based data loading). Everything runs client-side — no build
step.

## Mathematical model

The simulation advances **one day at a time**. Every event is a stochastic
**Bernoulli trial** (`Math.random() < p`): the numbers below are daily per-individual
probabilities, not deterministic rates.

### 1. Temperature-driven development (degree-day linear)

```
g(T) = 0                                              for T <= Tmin
g(T) = min( (T - Tmin) / (Topt - Tmin), 1.6 )         for T >  Tmin
```

| Parameter | Value | Meaning |
|---|---|---|
| `TMIN` | 14.6 °C | development stops below this |
| `TOPT` | 28.0 °C | thermal optimum (denominator) |

Each stage accumulates `progress += g` per day and advances when
`progress >= DUR` (`egg: 4`, `larva: 11`, `pupa: 8` thermal days). Adults do not
grow; they age once per day and die at `ADULT_LIFE = 5` days.

### 2. Daily environmental mortality

```
m = M0(stage)
  + MR(stage) * [rainy]
  + 0.12 * [T >= 33]
  + 0.05 * [T < 20]
  + ( 0.10 if H < 50   else 0.03 if H < 60 )
m = min(m, 0.95)
```

| Stage | M0 (base) | MR (rain) |
|---|---|---|
| egg | 0.03 | 0.10 |
| larva | 0.02 | 0.05 |
| pupa | 0.015 | 0.03 |

**Larval crowding:** each larva beyond `LARVA_CAP = 5` on a plant adds `+0.05`
to death probability.

### 3. Reproduction (oviposition)

A gravid female aged `age` lays `W = EGG_NIGHTS[age]` eggs per night:

| age | 0 | 1 | 2 | 3 | 4+ |
|---|---|---|---|---|---|
| eggs | 0 | 20 | 14 | 14 | 0 (dead at 5) |

Under pheromone **mating disruption** `W` is multiplied by `MATE_SUPPRESS = 0.50`.
Eggs per plant are capped at `EGG_CAP = 30`.

### 4. Dispersal

- **Larval crawl:** move to the least-crowded plant within Manhattan distance
  `CRAWL_DIST = 3`. Larvae are *forced* to leave when the plant exceeds
  `LARVA_CAP`; otherwise each larva crawls with probability
  `min(0.35, 0.04 + 0.06 * (excess / LARVA_CAP))`.
- **Adult flight:** newly emerged adults relocate to a plant at Manhattan
  distance `6..16` (`FLIGHT_MIN..FLIGHT_MAX`), falling back to a random plant.

### 5. Pesticide spray

- **Instant kill on application:**
  - egg: `EGG_KILL = 0.80`
  - exposed neonate (larva progress < `EXPOSED_DAYS = 0.5`): `NEONATE_KILL = 0.85`
  - sheltered older larva: `PROTECTED_MORT = 0.10`
- **Residue:** lasts `SPRAY.DAYS = 5` days; while active, egg/neonate daily
  mortality gets `+RESIDUAL_MORT = 0.30`.
- **Auto mode** (Spray / Combine runs): fires when cooldown is 0 and infestation
  `>= SPRAY_THRESHOLD = 5%`; resets a 7-day (spray) or 10-day (combine) cooldown.

### 6. Pheromone lure (mass trapping)

- **Trapping:** each adult male within Manhattan radius `RADIUS = 3` of a trap is
  removed with `CATCH_MALE = 0.60`/night; males elsewhere on the plot with
  `CATCH_FAR = 0.15`.
- **Mating disruption:** `MATE_SUPPRESS = 0.50` reduces field-wide oviposition.
- Placement: `NAT = 4` traps on an even, aspect-ratio-matched grid across the
  farm's bounding box.

### 7. Sanitation (Combine mode)

Every `SANITATION.INTERVAL = 7` days, each sheltered larva (progress >= 0.5) is
removed with `FRACTION = 0.45`.

### 8. Harvest

```
marketable per plant = max(0, PER_PLANT - min(PER_PLANT, larvae * DAMAGE))
```

with `PER_PLANT = 3`, `DAMAGE = 0.4`. First picking Day `FIRST = 48`, then every
`EVERY = 4` days; the profitable season runs to `SEASON = 120` days.

### 9. Aggregate metrics & stop rules

```
infestation %  P = (infested plants / total plants) * 100
rate of spread = (I_last - I_first) / max(1, day_last - day_first)  # new plants/day
```

A run stops when: no borers remain; `P >= 80%` or total worms `>= 2500`
("out of control"); or `day >= 120`. CSV-scenario runs instead replay every day
of the scenario (waiting for its starting-infestation day, then running through
to its last day, ignoring the out-of-control cap).

## Run modes

| Mode | Control |
|---|---|
| Daily (plain) | no control |
| + Pheromone Lure | mass trapping + mating disruption |
| + Pesticide Spray | threshold-triggered whole-farm spraying |
| + Lure & Spray (combine) | traps + less frequent sprays + weekly sanitation |
| Scenario | replays a user CSV day-by-day (weather, treatments, infestation) |

## Scenario CSV format

Columns: `Day, Infestation, Weather, Temperature (°C), Humidity (%), Treatment`.

- Temperature/humidity/rain drive the biology that day.
- `Treatment` values `Spray` or `Lure` are applied on exactly that day.
- A non-empty `Infestation` cell (e.g. `20,4 Worms Started`) starts the outbreak.
- A trailing row `,,,,,Interval=7` sets the re-spray interval note.

Example:

```
Day,Infestation,Weather,Temperature (°C),Humidity (%),Treatment
1,,Sunny,30°C,76%,None
20,4 Worms Started,Sunny,31°C,75%,None
55,,Sunny,31°C,72%,Lure
120,,Sunny,31°C,84%,None
,,,,,Interval=7
```

## Files

- `index.html` — full simulation (model, UI, reports).
- `generated_data.py` — model reference implementation used for validation.
- `leucinodes_orbonalis_simulation.csv` / `farm.csv` — climate record and farm layout.
- `Research-Sources.md` — literature basis for the parameter values.
- `server.py` — optional local HTTP server (avoids browser file-access limits).