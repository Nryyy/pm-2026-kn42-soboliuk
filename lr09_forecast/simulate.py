"""Monte Carlo прогноз кількості спринтів за історією velocity (ЛР9).

Приклади:
    python lr09_forecast/simulate.py lr09_forecast/velocity.csv 50
    python lr09_forecast/simulate.py lr09_reference_velocity.csv 220 --sprints 1,2
"""
import argparse
import csv
import math
import random


def load_velocity(path, sprints=None):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if sprints:
        rows = [r for r in rows if int(r["sprint"]) in sprints]
    return [float(r["points_done"]) for r in rows]


def simulate(velocity, remaining, runs, rng):
    if max(velocity) <= 0:
        raise ValueError("усі спринти закрили 0 points: прогноз нескінченний")
    results = []
    for _ in range(runs):
        left, sprints = remaining, 0
        while left > 0:
            left -= rng.choice(velocity)
            sprints += 1
        results.append(sprints)
    return sorted(results)


def percentile(sorted_results, p):
    # Найменше значення, нижче або на рівні якого лежить p частка прогонів.
    index = math.ceil(p * len(sorted_results)) - 1
    return sorted_results[index]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("velocity_csv")
    parser.add_argument("remaining_points", type=float)
    parser.add_argument("--sprints", help="номери спринтів через кому, за замовчуванням усі")
    parser.add_argument("--runs", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    sprints = {int(s) for s in args.sprints.split(",")} if args.sprints else None
    velocity = load_velocity(args.velocity_csv, sprints)
    results = simulate(velocity, args.remaining_points, args.runs, random.Random(args.seed))
    p50, p85 = percentile(results, 0.50), percentile(results, 0.85)
    print(f"velocity={velocity} points={args.remaining_points:g} runs={args.runs}")
    print(f"P50={p50} P85={p85} ширина={p85 - p50}")


if __name__ == "__main__":
    main()
