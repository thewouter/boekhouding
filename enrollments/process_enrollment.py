import os
from typing import List

from enrollments.enrollment.enrollment import Enrollment
from enrollments.enrollment.load_json import load_json


def load_new_enrollments():
    """Load all new enrollments into a list."""
    new_enrollments : List[Enrollment] = []
    directory = "/onedrive/data/exchange_folder/inschrijvingen"
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            data = load_json(os.path.join(directory, filename))
            new_enrollments.append(Enrollment.from_json(data, filename))
    return new_enrollments


def main():
    """Main enrollment loop."""
    new_enrollments = load_new_enrollments()
    for enrollment in new_enrollments:
        print(f"processing enrollment {enrollment}")
        enrollment.write_to_file(folder="/onedrive/data/exchange_folder/inschrijfformulieren")
        enrollment.send_email_enrollment_confirmation()
        os.remove(f"/onedrive/data/exchange_folder/inschrijvingen/{enrollment.filename}")


if __name__ == "__main__":
    main()