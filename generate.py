import datetime as dt
from pathlib import Path

import ics


def carnaval_sunday_dates() -> list[dt.date]:
    dates = Path("easter.txt").read_text()
    easter_dates = [dt.date.fromisoformat(line) for line in dates.splitlines()]

    # lent means 'vasten'. It is the time between carnaval and Easter
    lent_days = dt.timedelta(days=49)
    carnaval_start_dates = [easter - lent_days for easter in easter_dates]

    return carnaval_start_dates


def oeteldonk_themes() -> dict[str, str]:
    theme_lines = Path("themes.txt").read_text()

    # [(year, theme), ...]
    splits = [line.split(" - ") for line in theme_lines.splitlines()]

    return dict(splits)


def create_ics(elfelf: bool = True) -> None:
    cal = ics.Calendar()
    two_days = dt.timedelta(days=2)
    now = dt.datetime.now()

    themes = oeteldonk_themes()
    cv_dates = carnaval_sunday_dates()

    for cv in cv_dates:
        theme = themes.get(str(cv.year))
        event = ics.Event(
            name=f"Carnaval{': ' + theme if theme else ''}",
            begin=cv,
            location="Oeteldonk",
            duration=two_days,
            transparent=True,
            last_modified=now,
        )
        event.make_all_day()
        cal.events.add(event)

        if elfelf:
            event = ics.Event(
                name="D’n Elfde van d’n Elfde",
                begin=dt.date(cv.year, 11, 11),
                location="Oeteldonk",
                transparent=True,
                last_modified=now,
            )
            event.make_all_day()
            cal.events.add(event)

    ics_contents = cal.serialize_iter()
    Path("calendar.ics").write_text("".join(ics_contents))


if __name__ == "__main__":
    create_ics()
    print("Don't forget to push it to your website ;)")
