# Data in this repository

Everything under `data/raw/` is real, public data, committed on purpose and **never edited**. Where it came from, its license, and exactly what was changed for this course:

The names of places in these files are their publishers'. Their use in this course says nothing about the political status of any place.

## Online Retail II (UCI), sheet “Year 2009-2010”

**Source:** Daqing Chen, *Online Retail II*, UCI Machine Learning Repository, https://doi.org/10.24432/C5CG6D —
`https://archive.ics.uci.edu/dataset/502/online+retail+ii (sheet 'Year 2009-2010')` (fetched 2026-09-19, SHA-256 `17181af53059386e…`).

**License:** **CC BY 4.0** (as stated on the UCI dataset page).

**What it is:** every invoice line of a UK-based online retailer of gifts, 1 December 2009 to 9 December 2010:
525,461 rows, one row per product on an invoice. The UCI page documents that an invoice number starting with `C`
is a cancellation. It does not say why some lines have no `Customer ID`.

**Changes made for this course:** the 2009–2010 sheet only (the second sheet, 2010–2011, is not included);
converted from CSV to Parquet with the column types DuckDB inferred from the CSV (`Customer ID` is a `DOUBLE`
because that is what inference produced — part of Block 1). No rows or values were changed.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `online_retail.parquet` | 3,218,445 | `4f7f7bc8788b32e7…` |
