import datetime as dt
from pathlib import Path

import ics

dates = Path("data/easter.txt").read_text()
easter_dates = [dt.datetime.fromisoformat(line) for line in dates.splitlines()]

lent_days = dt.timedelta(days=49)
cv_dates = [easter - lent_days for easter in easter_dates]

themefile = Path("data/themes.txt").read_text()
themes = {}
for line in themefile.splitlines():
    year, theme = line.split(' - ')
    themes[int(year)] = theme

cal = ics.Calendar()

for cv in cv_dates:
    theme = themes.get(cv.year)
    title = theme and f'Carnaval: {theme}' or 'Carnaval'
    event = ics.Event(
        name=title,
        begin=cv,
        location="Oeteldonk",
        duration=dt.timedelta(days=2),
        transparent=True,
    )
    event.make_all_day()
    cal.events.add(event)

    elfelf = dt.datetime(cv.year, 11, 11)
    event = ics.Event(
        name="D’n Elfde van d’n Elfde",
        begin=elfelf,
        location="Oeteldonk",
        transparent=True,
    )
    event.make_all_day()
    cal.events.add(event)

    kwek = elfelf
    while kwek.weekday() != 5:
        kwek += dt.timedelta(days=1)

    event = ics.Event(
        name="Kwekfestijn",
        begin=kwek,
        location="Oeteldonk",
        transparent=True,
    )
    event.make_all_day()
    cal.events.add(event)

ics_contents = cal.serialize_iter()
Path("public").mkdir(exist_ok=True)
Path("public/calendar.ics").write_text("".join(ics_contents))
