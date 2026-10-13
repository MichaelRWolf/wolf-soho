# AT&T Billing Export - April 2023

## Source & Consolidation

- **Original location**: `~/AT&T/` (home directory)
- **Consolidated to project**: October 13, 2026
- **Export date**: April 17, 2023
- **Data scope**: AT&T mobile data usage records (granular, ~2-hour intervals)

## Phone Number Mapping

| Phone Number | Context                                                 |
|--------------|---------------------------------------------------------|
| 2066797941   | Primary line (Michael)                                  |
| 2068538603   | Secondary line (Michael's device)                       |
| 9197465174   | Wendy's second line (was on Wendy's phone for a period) |

## Files

- `2023-04-17_XXXXX_data.csv` - Individual usage records per phone number
- `2023-04-17_combined.csv` - Merged records from all three numbers
- `csv_reformatter.pl` - Perl script to normalize CSV format (converts usage strings KB/MB/GB to decimal bytes, appends phone number to each row)

## Notes

These are historical billing extracts. The 919 number (9197465174) was a temporary secondary line on Wendy's device during this period.
