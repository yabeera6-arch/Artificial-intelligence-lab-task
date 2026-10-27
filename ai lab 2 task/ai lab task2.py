class ClassroomAgent:
    """Choose a target mode and avoid resending an unchanged command."""

    def __init__(self):
        self.previous_mode = None
        self.previous_percept = None

    def act(self, temperature, occupied):
        percept = (temperature, occupied)
        previous_mode = self.previous_mode

        # Occupancy has priority: an empty classroom always goes to ECO.
        if not occupied:
            target = "ECO"
        elif temperature > 26:
            target = "COOL"
        elif temperature < 20:
            target = "WARM"
        else:
            target = "IDLE"

        command = target if target != previous_mode else "NO COMMAND"
        self.previous_mode = target
        self.previous_percept = percept
        return previous_mode, percept, target, command


def main():
    # Includes repeats, exact thresholds, transitions, and empty-room priority.
    percepts = [
        (24, True), (24, True), (27, True), (27, True),
        (20, True), (19, True), (19, False), (19, False),
        (26, True), (27, True), (26, True),
    ]
    agent = ClassroomAgent()
    print(f"{'#':>2}  {'Previous':<9} {'Percept (°C, occupied)':<25} {'Target':<7} Command")
    print("-" * 71)
    for step, (temperature, occupied) in enumerate(percepts, start=1):
        previous, percept, target, command = agent.act(temperature, occupied)
        print(f"{step:>2}  {(previous or '—'):<9} {str(percept):<25} {target:<7} {command}")


if __name__ == "__main__":
    main()
