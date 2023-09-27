import datetime as dt

import ics


def carnaval_sunday_dates():
    with open("easter.txt", "r", encoding="utf-8") as f:
        easter_dates = [dt.date.fromisoformat(x) for x in f.read().splitlines()]

    # lent means 'vasten'
    lent_time = dt.timedelta(days=49)
    return [easter - lent_time for easter in easter_dates]


def oeteldonk_themes():
    with open("themes.txt", "r", encoding="utf-8") as f:
        splits = [line.split(" - ") for line in f.read().splitlines()]

    return dict(splits)


def create_ics():
    cal = ics.Calendar()

    themes = oeteldonk_themes()

    for cv in carnaval_sunday_dates():
        theme = themes.get(str(cv.year))
        event = ics.Event(
            name=f"Carnaval{': ' + theme if theme else ''}",
            begin=cv,
            location="Oeteldonk",
            duration=dt.timedelta(days=2),
            transparent=True,
            created=dt.datetime.now(),
            last_modified=dt.datetime.now(),
        )
        event.make_all_day()
        cal.events.add(event)

    with open("carnaval.ics", "w", encoding="utf-8") as f:
        f.writelines(cal.serialize_iter())


if __name__ == "__main__":
    create_ics()
    print("Don't forget to push it to your website ;)")
