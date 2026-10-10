# Additional Exercise No. 1: Engineering Test Data Organizer
# Student-specific inputs
LAST_NAME = "PENA"
SEED_NUM = 8
FAVORITE_ARTIST = "LANY"

from collections import defaultdict

CATEGORIES = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]
MULTIPLIERS = {
    "TEMPERATURE": 1.0,
    "VOLTAGE": 0.1,
    "CURRENT": 0.01,
    "PRESSURE": 1.5,
    "SPEED": 2.0,
}

def generate_records():
    # Alphabet positions: L=12, A=1, N=14, Y=25
    artist_positions = [ord(char.upper()) - ord("A") + 1
                        for char in FAVORITE_ARTIST if char.isalpha()]
    records = []

    for source_index in range(1, 6):
        source = f"{LAST_NAME}_T{source_index}"
        for category_index, category in enumerate(CATEGORIES, start=1):
            position = artist_positions[
                (source_index + category_index - 2) % len(artist_positions)
            ]
            raw_value = SEED_NUM * 2 + position + source_index * 3 + category_index * 2
            value = round(raw_value * MULTIPLIERS[category], 2)
            records.append({
                "Source": source,
                "Category": category,
                "Value": value
            })

    # Required repeated source-category record
    records.append(records[0].copy())

    # Required incomplete record (missing measurement value)
    records.append({
        "Source": f"{LAST_NAME}_T5",
        "Category": "SPEED",
        "Value": None
    })
    return records

def show_records(records):
    print("\n1. GENERATED TEST DATA")
    print(f"{'SOURCE':<12} {'CATEGORY':<15} {'VALUE':>8}")
    print("-" * 38)
    for record in records:
        value = "MISSING" if record["Value"] is None else f'{record["Value"]:.2f}'
        print(f'{record["Source"]:<12} {record["Category"]:<15} {value:>8}')

def analyze(records):
    valid_records = [r for r in records if r["Value"] is not None]
    missing_records = [r for r in records if r["Value"] is None]

    # Find duplicate source-category pairs
    pair_counts = defaultdict(int)
    for record in records:
        # Count repeated completed source-category records; missing-value rows
        # are reported separately as incomplete, not as repeated purchases.
        if record["Value"] is not None:
            pair_counts[(record["Source"], record["Category"])] += 1
    repeated_pairs = {pair: count for pair, count in pair_counts.items() if count > 1}

    print("\n2. DATA QUALITY AND DISTINCT RECORDS")
    print(f"Total records: {len(records)}")
    print(f"Records with values: {len(valid_records)}")
    print(f"Incomplete records: {len(missing_records)}")
    print(f"Distinct sources: {len(set(r['Source'] for r in records))}")
    print(f"Distinct categories: {len(set(r['Category'] for r in records))}")
    print("Repeated source-category pairs:")
    for (source, category), count in repeated_pairs.items():
        print(f" {source} - {category}: appears {count} times")
    print("Incomplete records:")
    for record in missing_records:
        print(f" {record['Source']} - {record['Category']}: value missing")

    overall_total = sum(r["Value"] for r in valid_records)
    overall_average = overall_total / len(valid_records) if valid_records else 0

    print("\n3. NUMERICAL SUMMARY")
    print(f"Valid measurement total: {overall_total:.2f}")
    print(f"Valid measurement average: {overall_average:.2f}")
    print(f"Minimum value: {min(r['Value'] for r in valid_records):.2f}")
    print(f"Maximum value: {max(r['Value'] for r in valid_records):.2f}")

    # Group by source
    source_groups = defaultdict(list)
    for record in valid_records:
        source_groups[record["Source"]].append(record["Value"])

    print("\n4. SOURCE SUMMARY")
    print(f"{'SOURCE':<12} {'RECORDS':>7} {'TOTAL':>10} {'AVERAGE':>10}")
    for source in sorted(source_groups):
        values = source_groups[source]
        print(f"{source:<12} {len(values):>7} {sum(values):>10.2f} {sum(values)/len(values):>10.2f}")

    # Group by category
    category_groups = defaultdict(list)
    for record in valid_records:
        category_groups[record["Category"]].append(record["Value"])

    print("\n5. CATEGORY SUMMARY")
    print(f"{'CATEGORY':<15} {'RECORDS':>7} {'TOTAL':>10} {'AVERAGE':>10} {'MIN':>8} {'MAX':>8}")
    for category in sorted(category_groups):
        values = category_groups[category]
        print(f"{category:<15} {len(values):>7} {sum(values):>10.2f} "
              f"{sum(values)/len(values):>10.2f} {min(values):>8.2f} {max(values):>8.2f}")

    print("\n6. ORDERED RESULTS (highest source total to lowest)")
    for source, values in sorted(source_groups.items(),
                                 key=lambda item: sum(item[1]), reverse=True):
        print(f"{source}: total={sum(values):.2f}, average={sum(values)/len(values):.2f}")

    print("\n7. FINAL CONSOLIDATED REPORT")
    print(f"Student: {LAST_NAME}")
    print(f"Seed number: {SEED_NUM}")
    print(f"Favorite artist: {FAVORITE_ARTIST}")
    print(f"Sources generated: {len(set(r['Source'] for r in records))}")
    print(f"Measurement categories: {len(set(r['Category'] for r in records))}")
    print(f"Raw records: {len(records)}; valid values: {len(valid_records)}; missing values: {len(missing_records)}")
    print(f"Repeated source-category pair(s): {len(repeated_pairs)}")
    print(f"Overall valid-value total: {overall_total:.2f}")
    print(f"Overall valid-value average: {overall_average:.2f}")
    print("Note: totals combine different measurement categories and are for this exercise's data-processing demonstration.")

if __name__ == "__main__":
    data = generate_records()
    print("ENGINEERING TEST DATA ORGANIZER")
    print(f"Student input: LAST_NAME={LAST_NAME}, SEED_NUM={SEED_NUM}, FAVORITE_ARTIST={FAVORITE_ARTIST}")
    print("Artist character positions:", [ord(c) - ord("A") + 1 for c in FAVORITE_ARTIST])
    show_records(data)
    analyze(data)

