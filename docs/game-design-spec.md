# Plaza Game Design Spec v0.1

Nov 26, 2026 · @Reece DeHaan

**Status: ACCEPTED by Reece (2026-11-26).** Third deliverable of PL-D0; destined for `docs/game-design-spec.md`. Structured like Partner Track's spec. It follows the accepted roadmap, reuse map and ADRs PL-0001 to PL-0008, and every section is bound by the content rules (PL-0008). All numbers are balance-tuned placeholders.

## 1. Vision and pillars

Plaza is Football Manager for a cartel. The squad is the organisation, the fixtures are shipments and turf, and the league table is market share against rival organisations and the state. The player builds a structure of people, holds territory, runs a supply chain from precursors to street markets, moves money from the dirty book to the clean one, and survives a state that learns.

**Pillars:** people are the game; the council is the boss; every number reconciles; heat is the counterweight; the state adapts; deterministic, seeded and nothing is lost; play at any depth.

**Tone.** The game is a management sim about an organisation, told through reports, ledgers and briefings. It is specific about structure, people, territory, money and risk, and says nothing operational (PL-0008).

## 2. The player: the leader

### 2.1 Who they are

A mid-level lieutenant who breaks away in January 2006 with a crew of 6–10, one plaza and one product line. The player builds the leader at the start: name, age (28–45), a **background** and a persona.

| Background | Starting lean |
| --- | --- |
| Smuggler | logistics skills, a route partner, lower transit risk |
| Producer | production skills, a better first site |
| Enforcer | security skills, higher control, more heat |
| Accountant | finance skills, a first front, lower laundering loss |
| Fixer | influence skills, a contact in local politics, more council confidence |

### 2.2 The leader's time

The leader has monthly energy (TST's model). Personal attention (a sit-down, inspecting a site, a council lobby) is stronger than delegated action but exposes the leader to personal heat.

### 2.3 The leader's life (TST founder, CHANGED lightly)

Stress and burnout, persona traits, and a personal account held in the clean book. Conspicuous spending raises personal heat; security spending lowers capture risk.

### 2.4 Family (v2)

Partner, children, heirs; family can be a pressure point for rivals and the agency, shown only as outcomes.

### 2.5 Succession

On capture, death or deposition the council chooses a successor (PL-0007); the player may continue as that successor. Game over only when no successor exists or the organisation collapses.

## 3. Player journey and organisation stages

| Stage | Typical size | What unlocks |
| --- | --- | --- |
| 1. Crew | 6–20 members, 1 plaza | recruitment, one site, flows to one market |
| 2. Network | 20–60, 3–6 plazas | cells, a front, named shipments, the first council seat |
| 3. Organisation | 60–200, a corridor | the full council, a second product, rival wars, the agency's attention |
| 4. Cartel | 200+ | delegation everywhere, multiple corridors (v2), alliances, legitimacy exit (v2) |

The campaign ends in December 2035 (v1 balance targets stop at December 2016). Score: revenue, territory, survival and clean wealth, plus the leader's legacy. The **legitimacy exit** (v2) is scored as a win.

## 4. Core loop and time model

### 4.1 Turn pipeline (PL-0002)

World and policy shocks → agency → rivals → production → logistics → markets and sales → laundering → heat → people (morale, growth, informants) → council → events → snapshot. December adds the council meeting, tribute settlement, the agency's budget and rivals' yearly decisions.

### 4.2 What the player does in a month

Review the inbox and digest; recruit and assign members to cells and plazas; set production levels and buy supply; plan named shipments and pick routes; set laundering through fronts; respond to events; lobby the council; decide on conflict or truce. Most of it can be delegated (§11.3).

## 5. People

### 5.1 Attribute model

Attributes 1–20 (shown as ranges until revealed), in groups:

| Group | Attributes |
| --- | --- |
| Operations | production, logistics, negotiation, finance, security |
| Discretion | discretion, counter-surveillance, composure |
| Leadership | leadership, management, judgement, charisma |
| Mental | loyalty, ambition, greed, temperament, adaptability, risk appetite |
| Hidden | consistency, **informant risk**, poachability, big moments |

Personality and interests come from TST's data as is. **Informant risk** is hidden (TST ADR-0023): it never reaches the API or a prompt until an event reveals it.

### 5.2 Roles and ranks

Roles: lieutenant (plaza holder), cell leader, producer, courier and driver, distributor, accountant, fixer, enforcer, lookout, recruiter. Ranks: associate → member → cell leader → lieutenant → council. Promotion raises pay expectations and exposure.

### 5.3 How people change

Growth by doing (TST growth with PT's learning term, here from months worked in a role), morale from pay, fairness, heat and leadership, strain from pressure (PT-0006).

### 5.4 Pay

Monthly pay in dirty cash, by role and rank, against a regional market rate. Underpaying raises desertion and informant risk; overpaying raises cost and conspicuous spending.

### 5.5 Loyalty, desertion and informants

Loyalty drifts with pay, treatment, the leader's success and rival offers. A member can desert, defect to a rival with their contacts, or **flip** for the agency (§13.4). Members can also be lost to arrest or conflict.

### 5.6 Recruitment

Regional pools with a **sponsor** who vouches for the recruit; a sponsor's reputation shades the recruit's revealed ranges. Rivals and the agency both work the same pools.

## 6. Products and markets

### 6.1 Products (v1)

| Product | Kind | Role in v1 |
| --- | --- | --- |
| Cannabis | plant-based | the starting line; margin erodes with US state legalisation from 2012 |
| Methamphetamine | synthetic | the growth line; shaped by precursor controls |
| Fentanyl | emerging synthetic | arrives in the late 2010s; high margin, extreme heat |

Each product has margin, bulk, a heat profile and demand by market. Cocaine and heroin enter with v2 corridors.

### 6.2 Markets

A market is a region with wholesale and street price indexes (TST commodity pattern), demand by product, a quality preference and saturation. Selling more lowers price; rivals' supply competes.

### 6.3 Quality tiers

Four tiers set by equipment and research; higher quality sells higher and builds a brand reputation in a market.

## 7. Supply and production

### 7.1 The supply graph (PL-0008)

Nodes linked by "requires", never "how": products require precursors (named as in public control lists, verified in the dossier) and reagent categories (bulk solvents, industrial acids and bases, controlled reagents). Each supply node has a source region, cost, scheduling risk, substitutes and a tracking level.

### 7.2 Process families

Named, news-level production approaches as research nodes, each with the precursors it accepts, a cost multiplier, a quality ceiling and heat. Precursor controls make a family more expensive; substitution research opens another.

### 7.3 Sites

A site has a kind (field, small lab, industrial lab), an **equipment tier** (makeshift, small lab, industrial, pharmaceutical-grade) setting capacity, quality ceiling, footprint and detectability, a crew and a plaza. Bigger sites mean more heat; redundancy across sites limits a raid's damage.

### 7.4 Suppliers

Precursor and equipment suppliers are generated counterparties with contracts (TST contracts pattern) and memory. Imports are traceable and raise route heat.

## 8. Logistics and shipments

### 8.1 Routes

A route joins plazas along map edges using a method category (maritime, semi-submersible, tunnel, cross-border trucking, mail and parcel, air, cash smuggling) with abstract capacity, cost, transit time, heat and seizure risk.

### 8.2 Flow and named shipments (PL-0002)

Routine volume moves as monthly flow. Shipments above a threshold are **named**: a route, a crew, a cargo, a departure month and an outcome (arrived, delayed, partly seized, seized, stolen). They are the season's fixtures and are reported like results.

### 8.3 Transit partners

Passing through another organisation's plaza means a toll, a deal (§11.4) or a risk of conflict.

### 8.4 Cash home

Sales in the consumer market produce dirty cash that must travel back; cash shipments have their own seizure risk.

## 9. Territory (PL-0004)

### 9.1 The map

About 20–30 plazas across the v1 producing region, the northern border crossings and the US Southwest market, joined by edges. Each plaza: kind, holder, control, tax yield, local loyalty, contested status.

### 9.2 Holding a plaza

Control drifts toward a target from presence, spending, loyalty and rival pressure. A plaza pays **tax yield** (from local trade passing through) into the dirty book.

### 9.3 Local loyalty

Patronage spending and restraint raise it; violence outcomes and seizures lower it. Low loyalty feeds informants and the press.

### 9.4 Contests

Below a control threshold a plaza is contested; the contest resolves by the conflict rules (§12.3).

## 10. Money: the two books (PL-0003)

### 10.1 The books

Dirty book: sales, plaza tax, payroll, supply, logistics, protection, tribute, losses. Clean book: fronts' lawful revenue and costs, legitimate assets, the leader's lawful wealth.

### 10.2 Fronts and laundering

Front types (for example retail, hospitality, construction, transport, property) each with plausible capacity, a laundering fee, leakage and audit risk, all abstract. Running above plausible capacity raises the front's heat.

### 10.3 KPIs

Revenue by product and market; margin; dirty and clean cash; laundering capacity used; seizure losses; payroll; tribute; months of cash.

### 10.4 Financiers

Generated lenders who advance dirty cash at a price and remember defaults.

## 11. Leadership, the council and automation

### 11.1 The council (PL-0007)

Plaza holders with confidence 0–100; tribute rules; the December council's votes; deposition after six months under 30; splits into rival crews.

### 11.2 Seats

Second-in-command, chief accountant, head of security, head of logistics: TST seats with authority and guardrails.

### 11.3 Automation

Areas (production, logistics, laundering, security, recruitment) with an owner, money limits, one-offs as proposals and a monthly digest (TST §40).

### 11.4 Sit-downs

Negotiations (TST negotiation, CHANGED) with suppliers, transit partners, rivals and local power brokers: terms, a hidden zone, patience and rounds.

## 12. Rivals and conflict

### 12.1 Rival organisations

Generated organisations of every size, with leaders, councils, products, territory and books, run by utility AI with personalities (PT rivals, CHANGED). New organisations form from splinters.

### 12.2 Rival decisions

Expand, contest a plaza, ally, truce, poach members, inform on a rival, go quiet, launder.

### 12.3 Conflict (ADR PL-0010, to come)

Wars and alliances resolve abstractly from strength (members, security skill), morale, money and intelligence. Outcomes appear as reports: plazas changing hands, members lost, heat for both sides. No scenes.

## 13. Heat and law enforcement

### 13.1 Heat (PL-0005)

Person, site, route and organisation heat, bands with Explain breakdowns, slow decay.

### 13.2 The agency (PL-0006)

One fictional agency in v1 with a budget, priorities, a research tree and a political cycle; it chooses targets each December.

### 13.3 Cases

Surveillance → investigation → raid or arrest → indictment → trial or plea, with odds as ranges and warnings ahead. Outcomes: seizures, arrests, asset seizure, extradition (by era).

### 13.4 Informants

Recruited from members by heat, loyalty and pressure; a flipped member raises a case's odds. Counter-intelligence research and the head of security can surface suspicions as ranges, never certainties.

### 13.5 Corruption and influence (v2 depth)

Protection and influence as abstract reach with cost and informant risk; never a named real official.

## 14. Press and reputation

Press attention raises organisation heat and shifts political pressure on the agency. Reputation by plaza (fear and respect) affects recruitment, control and rival behaviour.

## 15. Research and eras

### 15.1 Research branches

Production, logistics, concealment and counter-surveillance, finance, security and influence, organisation; nodes are names and modifiers.

### 15.2 Eras (history pinned to 2025 at news level, then seeded)

The 2006 escalation of state military operations; precursor controls tightening from 2005; the kingpin strategy and extraditions in the 2010s; US state cannabis legalisation from 2012; the shift to synthetics and China's class-wide scheduling of fentanyl-related substances (2019); crypto laundering, drones, encrypted-phone takedowns and sanctions in the 2020s. The dossier verifies every dated entry before it is pinned.

## 16. Events and the LLM

TST's director, slots, severity caps and storylines (PT version). Text kinds: field report, council minutes, informant tip, year-end report. The validator enforces PL-0008; every event has an offline template; outcomes, never scenes.

## 17. Interface

TST's dark, dense, keyboard-first shell. Screens: Overview, Inbox, Organisation (cell diagram), People, Person, Recruitment, Territory map, Supply chain, Sites, Shipments, Markets, Books, Heat, Investigations, Council, Rivals, World news, Automation, History. Every number has an Explain breakdown.

## 18. Balance and tuning

TST's balance runner and strategy scripts (cautious, aggressive, launderer, warlord). v1 targets to December 2016: a competent cautious strategy survives in most seeds; an aggressive one grows faster but is captured or deposed more often; heat bites by the third year.

## 19. Scope by release

v1 (2006–2016, one corridor), v2 (to 2035, depth), v3 (the world), as in the accepted roadmap.

## 20. Ideas for expanding the design

- Street-price league table per market beside market share.
- Planting informants in rivals and the agency.
- A "what brought us down" retrospective after game over, built from the event log.
- A shared-world link where TST's companies and PT's firms appear as fronts and counterparties.

## 21. Open questions

Kept in `docs/questions.md` (the next deliverable), each with a proposed default.
