
# Buddle sort
def sort_time(events: list):
    sorted_event: list = events.copy()
    n: int = len(events)
    for i in range(n):
        for j in range(n - 1 - i):
            event: tuple = sorted_event[j]
            next_event: tuple = sorted_event[j+1]
            current_time  = event[0]
            current_type = event[1]   # +1 arrival, -1 departure
            next_time = next_event[0]
            next_type = next_event[1]
            if (current_time, current_type) > (next_time, next_type):
                sorted_event[j], sorted_event[j+1] = sorted_event[j+1], sorted_event[j]
    return sorted_event



def min_gates(arrivals: list[int], departures: list[int]) -> int:
    events = []
    for t in arrivals:
        events.append((t, 1))   # 1 = arrival (+1 plane)
    for t in departures:
        events.append((t, -1))  # -1 = departure (-1 plane)

    print(events)
    sorted_event = sort_time(events)
    print(sorted_event)
    events.sort(key=lambda x: (x[0], x[1]))  # sort by time; same time: -1 before 1
    print(events)

    count = 0
    max_plane_presents = 0
    for time, delta in events:
        count += delta
        max_plane_presents = max(max_plane_presents, count)
    print(f"minimum of gate: {max_plane_presents}")

min_gates(
     [150, 100, 200, 400, 215, 140],
     [220, 110, 230, 600, 315, 300]
)