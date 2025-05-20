from datetime import datetime

class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []
        self._grades = {}  # Dictionary to store grades with Enrollment as key

    def enroll(self, course):
        if not isinstance(course, Course):
            raise TypeError("course must be an instance of Course")

        # Prevent duplicate enrollments
        for enrollment in self._enrollments:
            if enrollment.course == course:
                print(f"{self.name} is already enrolled in {course.title}")
                return

        enrollment = Enrollment(self, course)
        self._enrollments.append(enrollment)
        course.add_enrollment(enrollment)

    def get_enrollments(self):
        return self._enrollments.copy()

    def course_count(self):
        return len(self._enrollments)

    def set_grade(self, enrollment, grade):
        if enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Enrollment does not belong to this student")

    def aggregate_average_grade(self):
        if not self._grades:
            return None
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        return total_grades / num_courses

    def __str__(self):
        return f"Student: {self.name}"


class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        if not isinstance(enrollment, Enrollment):
            raise TypeError("enrollment must be an instance of Enrollment")
        self._enrollments.append(enrollment)

    def get_enrollments(self):
        return self._enrollments.copy()

    def student_count(self):
        return len(self._enrollments)

    def average_grade(self):
        grades = [
            enrollment.student._grades.get(enrollment)
            for enrollment in self._enrollments
            if enrollment in enrollment.student._grades
        ]
        if not grades:
            return None
        return sum(grades) / len(grades)

    def __str__(self):
        return f"Course: {self.title}"


class Enrollment:
    all = []

    def __init__(self, student, course):
        if not (isinstance(student, Student) and isinstance(course, Course)):
            raise TypeError("Invalid types for student and/or course")
        self.student = student
        self.course = course
        self._enrollment_date = datetime.now()
        Enrollment.all.append(self)

    def get_enrollment_date(self):
        return self._enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count

    def __str__(self):
        return f"Enrollment: {self.student.name} in {self.course.title} on {self._enrollment_date.date()}"
