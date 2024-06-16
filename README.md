# Tinkoff Payment Parser

## Usage

1. Navigate to [https://www.tinkoff.ru/events/feed](https://www.tinkoff.ru/events/feed)
2. Select desired month in UI
3. Tap "Показать еще" until all transactions are loaded
4. Open browser console (F12 -> Console)
5. Outer-copy all the contents of html page with `<div data-qa-type="timeline-operations-list">`
6. Paste this html into input file (by default `./input/input.html`)
7. Run the script `poetry run python main.py`
8. You should see csv formatted output in `./output/output.csv`
