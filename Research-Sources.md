# Research Sources — Eggplant Fruit & Shoot Borer (EFSB) Simulator

All numbers used in the simulator's biology model, spray/lure mechanics, harvest timing and
report recommendations are drawn from the sources and figures below. Links verified
September 2026.

Pest: **Leucinodes orbonalis Guenée** (Lepidoptera: Crambidae) — eggplant fruit and shoot borer (EFSB / BFSB / brinjal).

---

## 1. Life Cycle & Biology

| Source | Link | Key data used |
|---|---|---|
| EFSA PLH Panel — Pest categorisation of *Leucinodes orbonalis* (EFSA Journal 2021;19(11):6890) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8586846/ · DOI: [10.2903/j.efsa.2021.6890](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2021.6890) | Egg 3–6 days; larva 12–15 d (summer) / 22 d (winter); egg→adult 17–44 d. Thermal minimum ~14.6 °C; thermal constant ~444.3 degree-days for complete development. 1.1–4.4 larvae per infested shoot; 1.3–5.0 per infested fruit. |
| EFSA PLH Panel — Pest risk assessment of *L. orbonalis* (EFSA Journal 2024;22(3):8498) | https://pmc.ncbi.nlm.nih.gov/articles/PMC10928798/ · DOI: [10.2903/j.efsa.2024.8498](https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2024.8498) | Confirms biology/thermal parameters above; key pest of eggplant in South Asia. |
| Yadav R — Effects of temperature on development & population parameters (2014) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4212862/ | Highest egg→adult emergence **67.7–78.75 %** in the range **25–31 °C** (basis for our TOPT ≈ 28 °C; mortality at T < 20 °C / T ≥ 33 °C). |
| Navasero MV & Calilung VJ — Biology of the eggplant fruit and shoot borer in the Philippines | https://agris.fao.org/search/en/providers/122430/records/6471e6d22a40512c710e9535 | Philippine conditions: larval period **9–14 d (mean 10.85)**; egg 4.12 d; pupa 9.44 d; adult 5.84 d; fecundity **8–295 eggs (mean 118)**; mating 1 d after emergence, oviposition 2–3 d after mating; one larva can move between plants / infest several fruits; infestation starts ~3 weeks after transplanting. |
| Jat HK, Shrivastava VK, Dubey R — Biology of BSB (Int. J. Curr. Microbiol. App. Sci. 2020;9(9):2475–2479) | https://www.ijcmas.com/9-9-2020/H.%20K.%20Jat,%20et%20al.pdf DOI: 10.20546/ijcmas.2020.909.309 | Egg **4.95 d**, larva **11.25 d**, pupa **7.18 d**, adult **4.92 d**, total **27.08 d**; sex ratio ≈ 1:2 (male:female) in lab. |
| CABI Compendium — *Leucinodes orbonalis* (eggplant fruit borer) | https://www.cabidigitallibrary.org/doi/abs/10.1079/cabicompendium.30498 | Biology, distribution, damage and management overview. |

> Simulator stage durations used (warm-day units): egg 4, larva 11, pupa 8, adult lifespan 5 d —
> consistent with the EFSA/Navasero ranges above.

---

## 2. Weather / Seasonality Effects

| Source | Link | Key data used |
|---|---|---|
| Population dynamics of BSB during cropping season & correlation with weather (J. Entomology and Zoology Studies 2019;7(1):1571–1575) | https://www.entomoljournal.com/archives/2019/vol7issue1/PartZ/7-1-307-302.pdf | Infestation starts low (**2.73 %**, ~4 weeks after transplanting / flowering), rises to a peak (**19.36 %** at 47th SMW), then declines with cooler temps/RH. Negative correlation with minimum temperature and evening RH. |
| ARCC / Agricultural Science Digest (IPM threshold review) | https://arccjournals.com/journal/agricultural-science-digest/D-6500 | IPM recommends beginning control when **shoot damage ≈ 5 %** and fruit damage ≈ 10 % to prevent economic loss (basis for our SPRAY_THRESHOLD = 5 % and report action threshold). |

---

## 3. Pesticide Management

| Source | Link | Key data used |
|---|---|---|
| Cornell / Feed the Future Bt Eggplant Partnership — "Pesticide use in the Philippines provides a strong justification for Bt eggplant" (2022) | https://bteggplant.cornell.edu/2022/08/16/pesticide-use-in-the-philippines-provides-a-strong-justification-for-bt-eggplant | Philippine growers spray **at least 2×/week, some every other day = 60–80 sprays in a 4-month season**. **Larvae are susceptible to sprays only a few hours after hatching** — once they bore into fruit/shoot they are sheltered (basis for our stage-limited spray: high kill on exposed eggs/neonates, low kill on bored larvae). |
| Cornell Bt Eggplant — field research on non-target arthropods (2016) | https://bteggplant.cornell.edu/2016/11/10/philippines-field-research-shows-no-negative-impacts-from-bt-eggplant-on-non-target-arthropods | Conventional eggplant sprayed up to **72 times / 180-day season**. Broad-spectrum actives: profenofos, triazophos, chlorpyrifos, cypermethrin, malathion. |
| Sowmya K. et al. — Field Efficacy of Different Insecticides Against BSB (Int. J. Plant & Soil Science 2023;35(18):418–422) | https://journalijpss.com/index.php/IJPSS/article/view/3305 DOI: 10.9734/ijpss/2023/v35i183305 | Post-spray infestation (%): **Chlorantraniliprole 12.45**, Spinosad 13.56, Emamectin benzoate 14.68, Indoxacarb 15.34, Flubendiamide 16.26, Beauveria bassiana 16.84, Neem oil 19.46 vs control. Best yield & economics = **Chlorantraniliprole 220.5 q/ha (1:8.3)**. |
| Biswas M. et al. — Newer molecules against EFSB (J. Entomology & Zoology Studies 2020;8(2)145–414) | https://www.entomoljournal.com/archives/2020/vol8issue2/PartZ/8-2-145-414.pdf | **Flubendiamide** best reduction over control: **87.46 % shoot, 81.43 % fruit**; highest B:C 1:11.74; low damage persisting 7–14 days (residual ~5–7 days window). |
| Jat HK & Shrivastava VK — Management through Newer Insecticides (Int. J. Plant & Soil Science 2022;34(24):996–1004) | https://journalijpss.com/index.php/IJPSS/article/view/2729 | Spinosad 45 SC & Indoxacarb 14.5 SC most effective (3.42–3.58 % shoot; 3.11–3.28 % fruit). |
| EJAFSS — A Comprehensive Analysis of Chemical Applications for Brinjal Crop (JEAI 2024;46(7):53–63) | https://journaljeai.com/index.php/JEAI/article/view/2557 DOI: 10.9734/jeai/2024/v46i72557 | Optimized pesticide scheduling + IPM to minimise residues; strategic applications at flowering/fruiting stages. |
| IJACR — Sustainable management of BSB in Bangladesh (2021) | https://ijacr.net/upload/ijacr/2021-13-1014.pdf | **Voliam flexi + hand removal + pheromone trap + nappy trap** best package: **95.96 % shoot / 94.85 % fruit reduction** over control; pheromone traps lower male catch over season. |
| Taiwan/EPA — Flubendiamide fact sheet | https://www3.epa.gov/pesticides/chem_search/reg_actions/registration/fs_PC-027602_01-Aug-08.pdf | Flubendiamide registered for lepidopteran pests on fruiting vegetables; residual efficacy profile. |

> Spray model: residual window DAYS = 5; **stage-limited kill** — EGG_KILL = 0.80, NEONATE_KILL = 0.85,
> PROTECTED_MORT = 0.10 (older larvae are sheltered inside shoots/fruit), RESIDUAL_MORT = 0.30/day on the
> exposed (egg/neonate) window — calibrated against the chlorantraniliprole/flubendiamide "best persistence, ~7-day interval" results.

---

## 4. Pheromone Lures & Mass Trapping

| Source | Link | Key data used |
|---|---|---|
| Krishna Kumar NK et al. — Pheromone Trapping Protocols for BSB (J. Hortic. Sci. 2006;1(1)) | https://jhs.iihr.res.in/index.php/jhs/article/view/671 · full PDF: https://jhs.iihr.res.in/index.php/jhs/article/download/671/484 DOI: 10.24154/jhs.v1i1.671 | Water trap = plastic container **20 cm dia × 7.5 cm deep**, attraction higher than delta trap; **4 mg pheromone load** best (37.0 ± 1.52 moths/trap over 6 months); **rubber septum** superior dispenser; traps placed and leveled weekly **at/between crop canopy heights**. |
| Mazumder F & Khalequzzaman M — Male moth catch in sex pheromone trap w.r.t. lure elevation & IPM (J. Bio-Science 2010;18:9–15) | https://www.banglajol.info/index.php/JBS/article/view/8768 DOI: 10.3329/jbs.v18i0.8768 | Lure blend E11-16:Ac:E11-16:OH (100:1). Male catches 1.7–4.5 to **14.95 ± 0.34 catch/trap** at 1 m; ~**4.54/trap at 1 m vs ~1.76 at 0.5 m** (basis for trap height/RADIUS). |
| Nusra MSF et al. — Pheromone baited biopesticide for control of *L. orbonalis* (Front. Biosci. (Elite Ed.) 2020;12(1)) | https://pubmed.ncbi.nlm.nih.gov/31585868/ · full: https://www.imrpress.com/journal/FBE/12/1/10.2741/E856 | Sex pheromone, alone or blended, in traps suppresses population growth — supports **mass-trapping of males to reduce mating/egg-laying** (our CATCH_MALE 0.60, MATE_SUPPRESS 0.50). |
| Cork A et al. — Female sex pheromone of EFSB blend optimization (J. Chem. Ecol. 2001;27(9):1867–1877) | https://pubmed.ncbi.nlm.nih.gov/11545376/ DOI: 10.1023/a:1010416927282 | Identified/optimised pheromone blend for synthetic lures. |
| Thomas G, Thakur V, Sharma S, Azizi S et al. — Strategic implementation of conventional and advanced approaches to combat BSFB (Discover Applied Sciences 2025;7:232) | https://link.springer.com/article/10.1007/s42452-025-06670-6 DOI: 10.1007/s42452-025-06670-6 | IPM review: "a single approach cannot be found effective"; a combination of **sex pheromones + mechanical/physical barriers + biocontrol + bio-pesticides + synthetic insecticides** gave effective control. Pheromone mass trapping alone lowered fruit infestation vs pesticide-only plots; **combined** treatments (botanicals + pesticides + pheromones/cultural) gave the lowest shoot/fruit damage and highest yield. Farmers may spray **~140×/season** (Bangladesh survey up to 180×). |
| EPPO Standard PP 1/264 (2) — Principles of efficacy evaluation for mating disruption pheromones (2019) | https://pp1.eppo.int/standards/PP1-264-2-en.pdf · https://pp1.eppo.int/standards/PP1-264-2 | Defines the **"combined programme"** concept: mating disruption evaluated *together with a reduced insecticide programme*, compared against the same reduced insecticide treatments alone. Establishes pheromone + insecticide integration as standard IPM practice. |
| Sarr M, et al. — Concerted action needed among smallholders when using mass trapping of insect pests (Agriculture, Ecosystems & Environment 2024) | https://www.sciencedirect.com/science/article/pii/S016788092400121X | Bangladesh field trial on eggplant *L. orbonalis*: **4 traps (2×2 grid) did NOT reduce infestation** (comparable to no-trap), while **24 traps (4×6 grid, ~10 m spacing)** cut fruit infestation by **25 percentage points**; networks of 22–40 scattered traps were equally effective. → mass trapping needs an **even grid at ~10 m spacing** and a sufficient trap density; edge/clustered placement under-covers the field. |
| Groot AT, et al. — Technical efficacy and practicability of mass trapping for insect control (Agron. Sustain. Dev. 2020) | https://link.springer.com/article/10.1007/s13593-020-00623-6 | Mass trapping efficacy for *L. orbonalis* depends on trap **density and uniform coverage**, combined with sanitation (removal of infested shoots/fruits); reinforces grid placement over perimeter-only traps. |

> Combined-IPM model (new 🪤💧 "Run + Lure & Spray" mode): pheromone traps (4 mg lure, mass-trapping of
> males + ~50 % mating disruption) **plus** whole-farm threshold sprays every **~10 days** (fewer sprays than
> the spray-only 7-day schedule). This mirrors the research best package — IJACR 2021: spray @10-day interval
> + pheromone trap + hand removal → **95.96 % shoot / 94.85 % fruit reduction**, the best of all treatments.

> Lure model: 4 water traps auto-deployed in an **even 2×2 grid across the plot** (or placed with the 🪤
> tool), RADIUS 3 cells, 60 % chance to catch a male moth per night in range, plus 50 % mating-disruption
> reduction in egg counts. Placement follows the 2024 mass-trapping trial (even grid, ~10 m spacing);
> note that 4 traps is a *monitoring* density — the same trial found mass trapping only suppressed
> infestation with ~24 traps (4×6) or a network of 22–40 traps.

---

## 5. Harvest Timing (Eggplant in the Philippines)

| Source | Link | Key data used |
|---|---|---|
| Department of Agriculture — Region 02 "Eggplant Production Guide" (Cagayan Valley) | https://cagayanvalley.da.gov.ph/wp-content/uploads/2018/02/Eggplant.pdf | Transplant seedlings **30–35 days after sowing**; **harvest starts 46–50 DAT** depending on variety; harvest fruit early morning, preferably double-row planting; use only 1 seedling/hill. |
| DA-ATI — Techno Guide on Organic Eggplant Production | https://ati2.da.gov.ph/ati-7/content/sites/default/files/users/user18/eggplant_final.pdf | Harvest **60–80 DAT** (organic); harvest **twice a week over 3–5 months**; store 10 d at 85–90 % RH, 10–13 °C. |
| Hautea DM et al. — Field Performance of Bt Eggplants (Cry1Ac) in the Philippines (PLOS ONE 2016;11:e0157498) | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0157498 | Growing season **≈ 120 days**; **harvest every 3–4 days**; data collected over **10–17 harvest periods**; Bt lines: <1 % shoot damage, <2 % fruit damage. |
| ISAAA Crop Biotech Update — Bt eggplant performance (2016) | https://www.isaaa.org/kc/cropbiotechupdate/article/default.asp?ID=14513 | Confirms harvest frequency & season length from the PLOS ONE trial. |
| Cornell Bt Eggplant — Philippines approves Bt eggplant for commercial cultivation (2023) | https://bteggplant.cornell.edu/2023/02/01/philippines-approves-bt-eggplant-for-commercial-cultivation | South-Asian/PH farmers spray **80–100× per season**; even with spraying EFSB can cause **up to 80 % crop loss**. |
| USDA-FAS — Agricultural Biotechnology Annual, Philippines (2023) | https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Agricultural%20Biotechnology%20Annual_Manila_Philippines_RP2023-0065.pdf | **Bt eggplant approved for commercial propagation 18 Oct 2022** (3rd GE crop in PH after Bt corn & Golden Rice); developed by UPLB-IPB. |

> Harvest model: FIRST = 48 DAT, EVERY = 4 days (≈2×/week), SEASON = 120 days, PER_PLANT = 3 fruits/picking,
> DAMAGE = 0.4 fruit destroyed per larva per picking.

---

## Simulation Datasets (local, generated from the model above + published weather)

- `leucinodes_orbonalis_simulation.csv` — 15-day observation table (8 columns: Initial Number;
  Observation Period; Temperature; Humidity; Weather; Number of Observed Units; Number of Infested
  Units; Infestation Rate), 3 observations/day. Regenerated by `generate_data.py` from the research
  biology + weather mortality model so the "real" dataset is consistent with the interactive sim.
- `farm.csv` — 23×21 farm layout, 200 plant cells, with path-blocked rows (0/11/22) that force
  near-distance spread to crawl/flight across gaps.

## Notes / Caveats
- Field efficacy numbers vary with season, location and cultivar; the simulator converts research
  figures (reduction over control %) into per-stage kill probabilities.
- "Peromone" in some earlier UI labels is a typo for **pheromone**.
- Spray is modelled **per plot**: a farmer sprays every plant on the whole field in a single day
  (no small spray radius), matching real practice — so the day counter advances one day per spray event.
- Spray **efficacy is stage-limited (realistic)**: contact spray kills ~80 % of *exposed eggs* and ~85 %
  of *neonates* (larvae only a few hours old), but only ~10 % of older larvae that have bored into
  shoots/fruit, and it does not reach pupae in the soil. The ~5-day residue keeps killing new hatchlings
  in that window. Consequence: a single spray **cannot wipe out** an established borer population —
  IPM (traps + repeated threshold sprays) only *suppresses* it, and moths reinfest from neighbouring
  fields. This matches the research: even the best package gave ~95 % *reduction*, not eradication.
- Combined-IPM mode models all **three legs** of the IJACR 2021 best package: (1) pheromone traps —
  4 mg lures, nightly male catch higher near a trap, and field-wide mating disruption (~50 % fewer
  viable eggs, since a 4 mg lure saturates a small plot); (2) reduced insecticide programme —
  threshold sprays every ~10 days; (3) **weekly hand removal (sanitation)** of damaged shoots/fruit,
  which is the only leg that reaches larvae sheltered inside the plant. Result in the sim: combined
  > spray-only > lure-only (matching the literature). A true **wipe-out is rare (~10–15 % of runs)**,
  needs months of sustained IPM in an isolated plot, and is a legitimate outcome — not the norm.
- Philippine farmer spray frequencies (60–100×/season) are far above recommended IPM levels —
  the simulator's recommended schedule follows the research (threshold-triggered, ~7-day interval).