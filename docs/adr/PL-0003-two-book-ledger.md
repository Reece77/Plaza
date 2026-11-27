## PL-0003: The two-book ledger

- Inherits: TST ADR-0003 (integer cents, double entry, cash from the ledger); PT-0003 §6's client money kept apart

**Decision.**

1. One double-entry ledger with two **books**: **dirty** (all trafficking income and costs) and **clean** (fronts, legitimate assets, the leader's lawful wealth). Every entry belongs to one book; only a **laundering transfer** may cross them.
2. **Laundering** moves value from dirty to clean through a front, at a loss: `clean = dirty × (1 − fee) − leakage`, limited by the front's monthly **capacity**. Fee, leakage and capacity are balance-tuned fictions set by front type and research; no method detail appears anywhere.
3. **Fronts** are clean-book businesses with their own lawful revenue, which sets their capacity and their audit risk. Running a front above its plausible capacity raises its heat.
4. **Seizure** removes dirty cash, product or clean assets through enforcement outcomes; seized clean assets are lost from the clean book with a court record.
5. Dirty cash pays crews, suppliers and tribute; clean cash buys fronts, legitimate assets and, at the end, the legitimacy exit. Dirty cash held in quantity carries its own heat and theft risk.
6. Chart of accounts in `accounts.yaml`, by book: assets (cash, product inventory, sites, fronts, receivables from distributors), liabilities (owed to suppliers, loans from financiers), equity, income (sales by market, plaza tax), costs (payroll, supply, logistics, protection, tribute, losses).

**Consequences.** "Every number reconciles" holds across both books; the player always sees how much of their wealth is spendable where.

