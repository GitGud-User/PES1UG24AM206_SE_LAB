"""School bus transport register: enrol riders, list rosters and total fees."""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE riders (id INTEGER PRIMARY KEY, "
             "student TEXT, route TEXT, stop TEXT, fee INTEGER)")


def enroll_rider(student, route, stop, fee):
    """Add a student to a bus route at the given stop with the given fee."""
    conn.execute("INSERT INTO riders (student, route, stop, fee) "
                 "VALUES (?, ?, ?, ?)", (student, route, stop, fee))
    conn.commit()


def route_roster(route):
    """Return the names of all students enrolled on a route."""
    rows = conn.execute("SELECT student FROM riders WHERE route = ?",
                        (route,))
    return [r[0] for r in rows]


def export_roster(path, route):
    """Write the roster for a route to a text file, one name per line."""
    with open(path, "w", encoding="utf-8") as out:
        for name in route_roster(route):
            out.write(name + "\n")


def dispatch_alert(route):
    """Announce that the bus for a route is being dispatched."""
    print("dispatching bus " + route)


def fee_collected(route):
    """Return the total fee collected for a route (0 if none or on error)."""
    try:
        total = conn.execute("SELECT SUM(fee) FROM riders WHERE route = ?",
                             (route,)).fetchone()[0]
    except sqlite3.Error:
        return 0
    return total or 0


def main():
    """Run a short demonstration of the register."""
    enroll_rider("Tara", "R1", "Lake Road", 1800)
    enroll_rider("Kabir", "R1", "Mill Street", 1800)
    enroll_rider("Zoya", "R2", "Fort Gate", 2100)
    if fee_collected("R1") != 3600:
        raise ValueError("Unexpected fee total for route R1")
    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2"))


if __name__ == "__main__":
    main()
