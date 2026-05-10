# Florida State Parks -- Rainbow Springs Reservation Barcode

## Related skill

`/extract-rainbow-springs-reservation` -- defined in:

```text
/Users/michael/repos/claude-tools/commands/extract-rainbow-springs-reservation.md
```

Installed (symlinked) to `~/.claude/commands/extract-rainbow-springs-reservation.md`
via `make install` in claude-tools.

What it does: extracts reservation data from park confirmation screenshots → CSV →
pastes into the Reservations tab of the Google Sheet → opens that tab.

## What was built

A `Barcodes` tab in the existing Google Sheet
(`https://docs.google.com/spreadsheets/d/1wLHPw0uB7pe7hw_NJ9hPQWoQ2mt4uyv7_2YaQUt8-UU/`)
that shows today's reservation date, confirmation number, and a scannable barcode --
without needing to find the original email receipt.

## Barcode format

- **Type**: Code 128
- **Content**: Confirmation Number exactly as printed (e.g. `22572138`) -- 8 digits, no spaces
- **Verified**: human-readable text below bwipjs-generated barcode matches receipt

## Barcodes tab layout (A:B vertical)

| Row | A           | B (formula)   |
|-----|-------------|---------------|
| 1   | Date        | spill from A1 |
| 2   | Reservation | spill from A1 |
| 3   | Barcode URL | see below     |
| 4   | Barcode     | `=IMAGE(B3)`  |

### A1 spill formula (fills A1:B2)

```excel
={"Date",IFERROR(TEXT(FILTER(Reservations!A2:A,INT(Reservations!A2:A)-TODAY()=0),"yyyy-mm-dd (ddd)"),"none today");"Reservation",IFERROR(TEXT(FILTER(Reservations!B2:B,INT(Reservations!A2:A)-TODAY()=0),"0000 0000"),"none today")}
```

### B3 barcode URL formula

References the raw (unformatted) confirmation number from the Reservations tab directly,
avoiding any formatting spaces:

```excel
="https://bwipjs-api.metafloor.com/?bcid=code128&text="&IFERROR(FILTER(Reservations!B2:B,INT(Reservations!A2:A)-TODAY()=0),"")&"&scale=3&height=30&includetext"
```

## Reservations tab

Column E: days-from-today (0 = today, negative = past, positive = future):

```excel
={"DAYS";ARRAYFORMULA(IF($A2:A<>"",INT($A2:A)-TODAY(),""))}
```

## Workflow

- **Daily**: Open Barcodes tab on phone, hold barcode up to ranger's scanner
- **Weekly (batch)**: Run `/extract-rainbow-springs-reservation` with screenshots →
  paste CSV into Reservations tab → Barcodes tab auto-updates

## API

`https://bwipjs-api.metafloor.com/` -- open-source bwip-js hosted endpoint, free for
low-volume use. No key required.
