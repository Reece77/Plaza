# Plaza Research Dossier v1 (2006–2016)

Nov 26, 2026 · @Reece DeHaan

**Status: ACCEPTED by Reece (2026-11-26); A-tagged items still to verify.** Destined for `docs/research/dossier-v1.md`. Public macro sources only, per PL-0008: market sizes, seizure trends, policy and enforcement timelines. Every fact is tagged **S** (sourced), **D** (derived from sourced figures) or **A** (assumed, to verify or tune). No individuals are named; no operational detail is recorded.

## 1. US consumer market size, 2006–2016 (S)

Retail spending by US users, billions of 2018 dollars, best estimates (RAND, 2019):

| Year | Cocaine | Heroin | Cannabis | Methamphetamine | Total |
| --- | --- | --- | --- | --- | --- |
| 2006 | 58 | 31 | 34 | 22 | 145 |
| 2007 | 48 | 29 | 33 | 18 | 128 |
| 2008 | 39 | 31 | 37 | 15 | 122 |
| 2009 | 35 | 36 | 39 | 16 | 126 |
| 2010 | 31 | 35 | 42 | 16 | 124 |
| 2011 | 29 | 35 | 42 | 15 | 121 |
| 2012 | 27 | 37 | 42 | 17 | 123 |
| 2013 | 24 | 40 | 44 | 21 | 129 |
| 2014 | 24 | 42 | 54 | 23 | 143 |
| 2015 | 24 | 41 | 51 | 29 | 145 |
| 2016 | 24 | 43 | 52 | 27 | 146 |

Notes (S): methamphetamine estimates carry the most uncertainty; the report could not fully separate fentanyl's effect on heroin estimates; by 2016 the cannabis market was roughly the size of the cocaine and methamphetamine markets combined.

## 2. Demand indexes for v1 products (D)

Indexed to 2006 = 100 from section 1, for `markets.yaml` (national; the US Southwest share is an assumption in section 5):

| Year | Cannabis | Methamphetamine |
| --- | --- | --- |
| 2006 | 100 | 100 |
| 2008 | 109 | 68 |
| 2010 | 124 | 73 |
| 2012 | 124 | 77 |
| 2014 | 159 | 105 |
| 2016 | 153 | 123 |

**Important (D):** national cannabis spending rose, but the share supplied by imports fell after legal domestic production began (section 3). The game models the **imported** cannabis market, so its demand must fall from 2014 even as the national index rises.

**Fentanyl (D):** no market-size estimate exists for 2006–2016. Its emergence is anchored to the US death rate involving synthetic opioids other than methadone: 1.0 per 100,000 in 2013, 1.8 in 2014, 3.1 in 2015, 6.2 in 2016, an average rise of 88% a year (S, CDC). Game rule: fentanyl unlocks as a product in 2013 with demand growing about 80–90% a year to 2016 (D), with extreme heat.

## 3. Policy and enforcement timeline, 2005–2016 (S unless tagged)

| Date | Event | Game effect (D/A) |
| --- | --- | --- |
| 2005 | Mexico begins phasing in tighter limits on imports of pseudoephedrine and ephedrine | precursor scheduling risk rises (A) |
| Mar 2006 | US Combat Methamphetamine Epidemic Act signed (behind-the-counter sales, purchase limits, logbooks), fully in force by Sep 2006 | US small-scale supply squeezed; demand shifts to imported product (D) |
| Dec 2006 | Mexico's federal government launches the first major military operation against trafficking organisations, widely treated as the start of the drug war | the game's opening shock: state pressure and agency budget up (D) |
| Jan 2007 onward | Large-scale extraditions to the US begin and continue | extradition era begins: higher cost of a leader's capture (A) |
| 2007 | Mexico announces a ban on pseudoephedrine and ephedrine imports for 2008 and on their use by 2009 | substitution race event (D) |
| Oct 2007 / Jun 2008 | Mérida Initiative announced (about US$1.6bn) and signed into law | agency research and budget boost from 2008 (A) |
| 2007–2008 | Mexican methamphetamine production falls; US availability declines; US small-scale production rises to fill the gap | methamphetamine demand dips 2007–2008, as in section 2 (D) |
| Late 2008–2009 | Producers adapt with substitute chemicals and new methods; Mexican production rebounds in 2009 | substitution research pays off after about 12–18 months (A) |
| 2007–2010 | Reported drug-related deaths in Mexico: 2,477 (2007), 6,290 (2008), 7,724 (2009), 15,273 (2010) | violence index for rival aggression and fragmentation (D) |
| 2010–2011 | Organisations fragment; open conflict between former allies; violence peaks in 2011 | splinter-group rate peaks 2010–2012 (A) |
| Nov 2012 | Colorado and Washington vote to legalise recreational cannabis | first legalisation shock (D) |
| 2014 | Oregon, Alaska and the District of Columbia vote to legalise; retail sales begin in Colorado and Washington (A: verify dates) | imported cannabis demand falls (D) |
| FY2009–FY2016 | Border Patrol cannabis seizures fall by more than half, attributed to less trafficking as legal domestic production fills the market | calibration target for imported cannabis decline (D) |
| Nov 2016 | California, Nevada, Massachusetts and Maine vote to legalise | second legalisation shock (D) |
| 2013–2016 | Synthetic-opioid deaths rise sharply (section 2); 63,632 total US overdose deaths in 2016 | fentanyl era and a large rise in agency priority on synthetics (D) |

## 4. Proposed game anchors (D/A)

- **Total addressable market** in v1: the US Southwest share of the national market for the three products, roughly US$8–12bn a year in 2006 (A: from section 1 times the share in section 5).
- **The player's ceiling** by 2016: a successful organisation holds 10–20% of its corridor's supply (A, tune).
- **Cannabis:** imported demand index follows section 2 to 2013, then falls about 10–15% a year after each legalisation wave (A, calibrated to the seizure decline).
- **Methamphetamine:** follows section 2, including the 2007–2008 dip from precursor controls.
- **Fentanyl:** unlocks 2013, grows 80–90% a year, carries the highest heat.

## 5. Gaps and next research

- **US Southwest share** of national demand (A: 15–20% pending a better source).
- **Price and purity series** by product (ONDCP and DEA price and purity reports).
- **Seizure tonnage by year** at the southwest border before FY2012 (CBP's public tables start later).
- **Retail cannabis start dates** for Colorado and Washington (marked A above).
- **v2 entries** to verify: China's class-wide scheduling of fentanyl-related substances (2019), sanctions on organisations, encrypted-phone takedowns.

## Sources

- RAND, What America's Users Spend on Illegal Drugs, 2006–2016 (2019): [PDF](https://www.issup.net/files/2019-08/What%20America%27s%20Users%20Spend%20on%20Illegal%20Drugs%2C%202006%E2%80%932016.pdf)
- US Department of Justice, NDIC methamphetamine assessment (2010): [justice.gov](https://www.justice.gov/archive/ndic/pubs38/38661/meth.htm)
- Combat Methamphetamine Epidemic Act of 2005: [Wikipedia](https://en.wikipedia.org/wiki/Combat_Methamphetamine_Epidemic_Act_of_2005)
- Timeline of the Mexican drug war: [Wikipedia](https://en.wikipedia.org/wiki/Timeline_of_the_Mexican_drug_war)
- Timeline of cannabis laws in the United States: [Wikipedia](https://en.wikipedia.org/wiki/Timeline_of_cannabis_laws_in_the_United_States)
- Texas Tribune on Border Patrol cannabis seizures (2016): [texastribune.org](https://www.texastribune.org/2016/12/09/marijuana-legalization-texas)
- CDC NCHS Data Brief 294, Drug Overdose Deaths 1999–2016: [cdc.gov](https://cdc.gov/nchs/products/databriefs/db294.htm)
- CDC MMWR, Drug and Opioid-Involved Overdose Deaths 2013–2017: [cdc.gov](https://www.cdc.gov/mmwr/volumes/67/wr/mm675152e1.htm)

## Ideas to expand

- Replace the Wikipedia-sourced violence figures with official Mexican statistics (INEGI homicide data) before pinning.
- Add a v2 section on producing-region and transit-country trends from UNODC's World Drug Reports.
