"""
Research-based population model for eggplant fruit & shoot borer
(Leucinodes orbonalis) on the farm layout.

Regenerates leucinodes_orbonalis_simulation.csv with observed borer counts,
infested units and infestation rate predicted by the biology:

Life cycle (research):
  egg 3-6 d, larva ~11 d (PH study 9-14), pupa ~8 d, adult ~5 d
  => ~23 warm days egg->adult ; total life cycle 25-40 d
  Tmin = 14.6 C, thermal sum ~444 DD ; optimal 25-31 C
  Favourable RH 60-90% ; rain washes eggs/young larvae ; >33 C kills
  Female lays 8-295 eggs (PH mean 118), mostly night 2-4
  Larvae crawl to nearby plants ; adults (moths) fly far at night

The generated CSV keeps the original observation weather (temperature,
humidity, weather) so the simulation and dataset stay consistent.
"""

import csv
import random
from collections import defaultdict

SEED = 42
random.seed(SEED)

# ---- biology parameters (must mirror the JS simulation) ----
T_MIN = 14.6
T_OPT = 28.0
STAGE_DUR = {'egg': 4, 'larva': 11, 'pupa': 8}   # warm-day durations
ADULT_LIFE = 5                                    # days adults live
EGG_NIGHTS = [0, 20, 14, 14]                      # eggs/female by adult age; total 48
EGG_CAP = 30                                      # max eggs/plant (fruit sites)
LARVA_CAP = 5                                     # larvae/plant before dispersal (avg ~4)
CRAWL_DIST = 3                                    # larvae crawl to plants within this distance
FLIGHT_MIN, FLIGHT_MAX = 6, 16                    # moth long-range flight distance (cells)
BASE_MORT = {'egg': 0.03, 'larva': 0.02, 'pupa': 0.015}
RAIN_MORT = {'egg': 0.10, 'larva': 0.05, 'pupa': 0.03}
ACTIVITY = {'6:00 AM': 0.55, '5:00 PM': 0.20, '6:00 PM': 0.95}  # observed fraction of larvae

P_AMBIENT_CRAWL = 0.04   # per-larva daily chance to wander to a neighbour


def growth(T):
    """Daily development progress (1.0 = one warm day)."""
    if T <= T_MIN:
        return 0.0
    g = (T - T_MIN) / (T_OPT - T_MIN)
    return max(0.0, min(g, 1.6))


class Plant:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.worms = []  # list of dicts {stage, progress, age, sex}


def load_farm(path):
    with open(path) as f:
        rows = [r for r in csv.reader(f) if r and any(v.strip() for v in r)]
    plants = []
    idx = {}
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if 'plant' in v.lower():
                p = Plant(r, c)
                plants.append(p)
                idx[(r, c)] = p
    return rows, plants, idx


def load_original(path):
    """Return (header, rows) keeping weather columns from the existing dataset."""
    with open(path) as f:
        return list(csv.reader(f))


def mortality(stage, T, H, rainy):
    m = BASE_MORT[stage]
    if rainy:
        m += RAIN_MORT[stage]
    if T >= 33:
        m += 0.12
    if T < 20:
        m += 0.05
    if H < 50:
        m += 0.10
    elif H < 60:
        m += 0.03
    return min(m, 0.95)


def lay_eggs(p, count, egg_cap=EGG_CAP):
    eggs = sum(1 for w in p.worms if w['stage'] == 'egg')
    room = max(0, egg_cap - eggs)
    for _ in range(min(count, room)):
        p.worms.append({'stage': 'egg', 'progress': 0.0, 'age': 0})


def pick_flight_target(src, idx, dist_range):
    """Long-range moth flight: random plant at distance in [lo, hi]."""
    lo, hi = dist_range
    far = []
    for (r, c), p in idx.items():
        d = abs(r - src.r) + abs(c - src.c)
        if lo <= d <= hi:
            far.append((d, r, c, p))
    if not far:
        far = [((abs(p.r - src.r) + abs(p.c - src.c)), p.r, p.c, p)
               for p in idx.values()]
    return far[random.randrange(len(far))][3]


def crawl_neighbour(src, idx, lo=1, hi=CRAWL_DIST):
    """Pick a nearby uncrowded plant for a larva to crawl to."""
    cands = []
    for (r, c), p in idx.items():
        d = abs(r - src.r) + abs(c - src.c)
        if lo <= d <= hi:
            larva = sum(1 for w in p.worms if w['stage'] == 'larva')
            cands.append((larva - LARVA_CAP, d, r, c, p))
    if not cands:
        return None
    random.shuffle(cands)
    cands.sort(key=lambda x: (max(0, x[0]), x[1]))
    return cands[0][4]


def step_day(plants, idx, T, H, rainy):
    """Advance one day. Returns nothing; mutates plant worm lists."""
    g = growth(T)
    moves = []  # (worm, target_plant)

    for p in plants:
        dead = []
        for w in p.worms:
            if w['stage'] != 'adult' and random.random() < mortality(w['stage'], T, H, rainy):
                dead.append(w)
                continue
            s = w['stage']
            if s == 'egg':
                w['progress'] += g
                if w['progress'] >= STAGE_DUR[s]:
                    w['stage'] = 'larva'
                    w['progress'] = 0.0
            elif s == 'larva':
                w['progress'] += g
                if w['progress'] >= STAGE_DUR[s]:
                    w['stage'] = 'pupa'
                    w['progress'] = 0.0
            elif s == 'pupa':
                w['progress'] += g
                if w['progress'] >= STAGE_DUR[s]:
                    w['stage'] = 'adult'
                    w['age'] = 0
                    w['sex'] = 'f' if random.random() < 0.5 else 'm'
                    # newly eclosed moths fly far: long-distance spread
                    target = pick_flight_target(p, idx, (FLIGHT_MIN, FLIGHT_MAX))
                    moves.append((w, target))
            else:  # adult
                w['age'] += 1
                if w['age'] > ADULT_LIFE:
                    dead.append(w)
                    continue
                if w['sex'] == 'f' and 0 <= w['age'] < len(EGG_NIGHTS):
                    if EGG_NIGHTS[w['age']] > 0:
                        lay_eggs(p, EGG_NIGHTS[w['age']])
        for w in dead:
            if w in p.worms:
                p.worms.remove(w)

    for w, target in moves:
        if w in p.worms:
            p.worms.remove(w)
        target.worms.append(w)

    # larval dispersal: overcrowding forces crawling, plus ambient wander
    mover_worms = []
    for p in plants:
        larvae = [w for w in p.worms if w['stage'] == 'larva']
        excess = max(0, len(larvae) - LARVA_CAP)
        prob = min(0.35, P_AMBIENT_CRAWL + 0.06 * (excess / LARVA_CAP))
        for w in larvae:
            if random.random() < prob or excess > 0:
                excess = max(0, excess - 1)
                mover_worms.append((p, w))
    for src, w in mover_worms:
        if w not in src.worms:
            continue
        target = crawl_neighbour(src, idx)
        if target and target is not src:
            src.worms.remove(w)
            target.worms.append(w)


def observe(plants, total_plants, time_label, jitter=True):
    larvae = sum(1 for p in plants for w in p.worms if w['stage'] == 'larva')
    obs = round(larvae * ACTIVITY[time_label])
    if jitter:
        obs = max(0, obs + random.randint(-1, 1))
    infested = sum(1 for p in plants
                   if any(w['stage'] in ('larva', 'pupa') for w in p.worms))
    if jitter:
        infested = max(0, min(total_plants, infested + random.randint(-1, 1)))
    return obs, infested


def main():
    rows, plants, idx = load_farm('farm.csv')
    orig = load_original('leucinodes_orbonalis_simulation.csv')
    header = orig[0]
    data = orig[1:]
    total = len(plants)

    # summary column index in written file (to update col 5,6,7)
    out = [row[:5] + [''] * 3 for row in data]  # keep cols 0-4, blank 5-7 for now
    col_idx = {0: 'init', 1: 'period', 2: 'temp', 3: 'hum', 4: 'weather',
               5: 'obs', 6: 'units', 7: 'rate'}

    # build per-day weather keyed by Day N using the 5:00 PM reading
    day_weather = {}
    for row in data:
        m = row[1].split('(')[0].strip()  # "Day N"
        if m not in day_weather and '5:00 PM' in row[1]:
            day_weather[m] = (float(row[2]), float(row[3]), row[4])

    # initial cohort: 4 borers with overlapping life stages on one plant
    # (research: continuously breeding pest with overlapping generations)
    seed_plant = plants[len(plants) // 2]
    seed_plant.worms.append({'stage': 'adult', 'progress': 0.0,
                             'age': 1, 'sex': 'f'})          # gravid female moth
    seed_plant.worms.append({'stage': 'larva', 'progress': 9.0, 'age': 9})   # near-mature larva
    seed_plant.worms.append({'stage': 'larva', 'progress': 3.0, 'age': 3})   # young larva
    seed_plant.worms.append({'stage': 'pupa', 'progress': 6.0, 'age': 0})    # pupa about to eclose

    # step one day, then record that day's 3 observations
    for day_i in range(1, 16):
        key = f'Day {day_i}'
        T, H, weather = day_weather.get(key, (28.5, 80, 'Cloudy'))
        rainy = 'Rainy' in weather
        step_day(plants, idx, T, H, rainy)
        for obs_slot, row in enumerate(data):
            if (obs_slot // 3 + 1) != day_i:
                continue
            time_label = ('6:00 AM' if '6:00' in row[1]
                          else '5:00 PM' if '5:00' in row[1] else '6:00 PM')
            obs, infested = observe(plants, total, time_label)
            rate = infested / total * 100
            idx_out = obs_slot
            out[idx_out][5] = str(obs)
            out[idx_out][6] = str(infested)
            out[idx_out][7] = f'{rate:.1f}%'

    with open('leucinodes_orbonalis_simulation.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in out:
            # restore any header rows already present in original data rows
            w.writerow(row)

    # summary printout
    print(f'Farm: {total} plants')
    print('Day  obs  infested  rate')
    for i in range(0, len(out), 3):
        d = i // 3 + 1
        print(f'{d:>3}  {out[i][5]:>3}      {out[i][6]:>3}      {out[i][7]}')


if __name__ == '__main__':
    main()