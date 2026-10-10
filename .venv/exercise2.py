# ADDITIONAL EXERCISE NO. 2
# Student Performance Data Analyzer

# STUDENT-SPECIFIC INPUTS
LAST_NAME = "PENA"
SEED_NUM = 8
FAVORITE_ARTIST = "LANY"

from collections import defaultdict

student_labels = [f"{LAST_NAME}_{i+1}" for i in range(5)]
subjects = [
    "PROGRAMMING",
    "MATHEMATICS",
    "ELECTRONICS",
    "PHYSICS",
    "ENGLISH",
]


def generate_score(char_pos, seed):
    base = ord(FAVORITE_ARTIST.upper()[char_pos % len(FAVORITE_ARTIST)])
    score = (base + seed * 7 + char_pos * 11) % 41 + 60
    return score


# Generate student performance records
records = []
idx = 0

for student in student_labels:
    for subject in subjects:
        score = generate_score(idx, SEED_NUM)
        records.append({
            "student": student,
            "subject": subject,
            "score": score,
        })
        idx += 1

# Add one repeated record and one incomplete record
records.append(records[0].copy())
records.append({
    "student": f"{LAST_NAME}_5",
    "subject": "PHYSICS",
    "score": None,
})

print(f"=== Generated Performance Records ({len(records)}) ===")
for record in records:
    print(record)

# Organize records by student and subject
organized = defaultdict(dict)

for record in records:
    if record["score"] is not None:
        organized[record["student"]][record["subject"]] = record["score"]

print("\n=== Organized Student/Subject Data ===")
for student, subject_data in organized.items():
    print(f"{student}: {subject_data}")


def get_category(score):
    if score is None:
        return "INCOMPLETE"
    elif score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Very Good"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Passed"
    else:
        return "Failed"


# Categorize each record
for record in records:
    record["category"] = get_category(record["score"])

print("\n=== Performance Categories ===")
for record in records:
    print(
        f"{record['student']}-{record['subject']}: "
        f"{record['score']} -> {record['category']}"
    )

# Detect repeated and incomplete records
seen = set()
repeated = []
incomplete = []

for record in records:
    key = (record["student"], record["subject"])

    if record["score"] is None:
        incomplete.append(record)
    elif key in seen:
        repeated.append(record)
    else:
        seen.add(key)

print("\n=== Repeated/Incomplete Records ===")
print("Repeated:", repeated)
print("Incomplete:", incomplete)

# Calculate each student's average using organized subject scores
print("\n=== Student Averages ===")
for student in student_labels:
    scores = list(organized[student].values())
    average = sum(scores) / len(scores) if scores else 0
    print(f"{student} Average: {average:.2f}")

# Calculate each subject's average from valid records
print("\n=== Subject Averages ===")
subject_averages = {}

for subject in subjects:
    scores = [
        record["score"]
        for record in records
        if record["subject"] == subject and record["score"] is not None
    ]
    average = sum(scores) / len(scores) if scores else 0
    subject_averages[subject] = average
    print(f"{subject} Average: {average:.2f}")

# Sort valid records from highest to lowest score
valid_records = [
    record for record in records if record["score"] is not None
]
ordered = sorted(
    valid_records,
    key=lambda record: record["score"],
    reverse=True,
)

print("\n=== Ordered Results (Highest to Lowest) ===")
for record in ordered:
    print(record)

# Print the final report
overall_average = (
    sum(record["score"] for record in valid_records) / len(valid_records)
    if valid_records else 0
)

print("\n=== FINAL STUDENT PERFORMANCE REPORT ===")
print(f"Student: {LAST_NAME}")
print(f"Seed Number: {SEED_NUM}")
print(f"Favorite Artist: {FAVORITE_ARTIST}")
print(f"Total Records Generated: {len(records)}")
print(f"Valid Records: {len(valid_records)}")
print(f"Repeated Records Found: {len(repeated)}")
print(f"Incomplete Records Found: {len(incomplete)}")
print(f"Overall Average: {overall_average:.2f}")

if ordered:
    print(f"Top Performer Record: {ordered[0]}")
    print(f"Lowest Valid Score Record: {ordered[-1]}")
else:
    print("No valid score records available.")