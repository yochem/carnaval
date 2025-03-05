import sys
import datetime as dt
from pathlib import Path

import ics
import requests
from bs4 import BeautifulSoup


def scrape_themes():
    url = "https://www.oeteldonk.org/over-oeteldonk/thema-en-symboliek/thema-oeteldonk"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("main ul li")
    themes = [item.get_text(strip=True) for item in items]

    try:
        return dict([line.split(" - ") for line in themes])
    except ValueError:
        print(
            "Warning: One or more lines do not match 'year - theme' format:",
            *themes,
            sep="\n",
            file=sys.stderr,
        )


def dates():
    dates = Path("data/easter.txt").read_text()
    easter_dates = [dt.date.fromisoformat(line) for line in dates.splitlines()]

    lent_days = dt.timedelta(days=49)
    cv_dates = [easter - lent_days for easter in easter_dates]

    themes = scrape_themes()

    cal = ics.Calendar()
    two_days = dt.timedelta(days=2)

    for cv in cv_dates:
        theme = themes.get(str(cv.year))
        event = ics.Event(
            name=f"Carnaval{': ' + theme if theme else ''}",
            begin=cv,
            location="Oeteldonk",
            duration=two_days,
            transparent=True,
        )
        event.make_all_day()
        cal.events.add(event)

        event = ics.Event(
            name="D’n Elfde van d’n Elfde",
            begin=dt.date(cv.year, 11, 11),
            location="Oeteldonk",
            transparent=True,
        )
        event.make_all_day()
        cal.events.add(event)

    ics_contents = cal.serialize_iter()
    Path("calendar.ics").write_text("".join(ics_contents))


if __name__ == "__main__":
    dates()
