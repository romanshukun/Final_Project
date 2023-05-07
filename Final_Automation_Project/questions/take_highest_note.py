# Create a list of dictionaries representing students and their notes.
students_list = [
    {"name": "Avi", "notes": [3, 5, 4]},
    {"name": "Moshe", "notes": [-1, 3, 5.5]},
    {"name": "Roman", "notes": []}
]


# Define a function that takes a list of students and returns a new list of dictionaries,
# where each dictionary contains the student's name and their highest note (or 0 if they have no notes).
def highest_note(students):
    return [
        {
            "name": student["name"],
            "top_note": max(student["notes"], default=0),
        } for student in students
    ]


# Call the highest_note function with the students_list argument and store the result in a variable.
result = highest_note(students_list)

# Print the resulting list of dictionaries.
print(result)
