APPLICATIONS = {
    "APP1001": {
        "student_name": "Rahul",
        "course": "B.Tech",
        "status": "Under Review",
    },
    "APP1002": {
        "student_name": "Amit",
        "course": "B.Tech",
        "status": "Approved",
    },
}


def check_application_status(application_number: str) -> dict:
    application = APPLICATIONS.get(application_number)

    if not application:
        return {
            "found": False,
            "message": "Application not found.",
        }

    return {
        "found": True,
        "application_number": application_number,
        "student_name": application["student_name"],
        "course": application["course"],
        "status": application["status"],
    }