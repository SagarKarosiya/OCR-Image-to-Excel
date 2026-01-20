def enrich_data(ocr_data):
    """
    STEP 3: Fetch and merge extra data from Python structures
    """

    # Example data sources
    COURSE_DB = {
        "AI & ML": "Artificial Intelligence and Machine Learning",
        "DS": "Data Science"
    }

    STUDENT_TYPE = {
        "101": "Regular",
        "102": "Lateral"
    }

    SKILLS_SET = {"Python", "ML", "Data Science"}

    final_data = ocr_data.copy()

    # Add course full name
    course = ocr_data.get("Course")
    if course in COURSE_DB:
        final_data["Course Full Name"] = COURSE_DB[course]

    # Add student type
    roll = ocr_data.get("RollNo")
    if roll in STUDENT_TYPE:
        final_data["Student Type"] = STUDENT_TYPE[roll]

    # Add skills
    final_data["Skills"] = ", ".join(SKILLS_SET)

    return final_data
