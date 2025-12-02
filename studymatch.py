import csv
import json
import heapq
from typing import Dict, List, Set, Tuple, Optional

# 1 Student Class
class Student:
    # Definition: Initializes a new Student object
    def __init__(self, ut_eid: str, name: str, courses: List[str], confidence: int, availability: List[str], email: str, topics_need: List[str], study_life: str, work_hours: int):
        self.ut_eid = ut_eid
        self.name = name
        self.courses = set(courses)
        self.compatibility_score = 0
        self.confidence_level = confidence
        self.individual_availability: Set[str] = set(availability)
        self.email = email
        self.topics_need = set(topics_need)
        self.study_life = study_life.lower()
        self.work_hours = work_hours

    # Definition: Compares this student to another for the Max-Heap
    # NOTE: Since the heap stores (-score, Student), this __lt__ is primarily for 
    # tie-breaking when the scores are identical.
    def __lt__(self, other):
        # Tie-break by EID to ensure consistent ordering if scores are identical
        return self.ut_eid < other.ut_eid

    # Definition: Provides a string representation of the Student
    def __repr__(self):
        return f"Student(Name: {self.name}, EID: {self.ut_eid}, Score: {self.compatibility_score}, Confidence: {self.confidence_level}/5, Email: {self.email})"


# 2 StudyMatch Class
class StudyMatch:
    # Definition: Initializes the StudyMatch manager
    def __init__(self):
        self.student_index: Dict[str, Student] = {}
        self.open_slots_queue: List[str] = []
        # Max-Heap stores: (-score, Student object)
        self.match_heap: List[Tuple[int, Student]] = [] 
        # tie_break_heap is not used in the final matching logic
        self.tie_break_heap: List[Tuple[int, str]] = [] 

    # Data Structure Methods

    # Load course data from a file (Currently loads into an unused attribute)
    def load_course_data(self, file_path: str):
        try:
            # NOTE: self.course_topic_path is not used in the matching logic below
            with open(file_path, "r") as file:
                self.course_topic_path = json.load(file)
            print(f"Loaded course data topics from {file_path}")
        except Exception as e:
            print("Error loading course data topics:", e)

    # Definition: Loads student data from a file
    def load_data(self, file_path: str):
        print(f"Loading data from {file_path}...")

        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    ut_eid = row['ut_eid']
                    name = row['name']
                    # Handle multiple courses
                    courses_list = [c.strip() for c in row['courses'].split(',')]

                    try:
                        confidence = int(row.get('confidence_level', 1))
                    except ValueError:
                        confidence = 1

                    # Handle multiple availability slots separated by a semicolon
                    availability_list = [t.strip() for t in row['availability'].split(';')] if row.get('availability') else []

                    email = row.get('email', '')

                    # Handle multiple topics separated by a comma
                    topics = [t.strip() for t in row.get('topics_need', '').split(',')] if row.get('topics_need') else []

                    study_life = row.get('study_life', 'none')

                    try:
                        work_hours = int(row.get('work_hours', 5))
                    except ValueError:
                        work_hours = 5 # Default if conversion fails

                    student = Student(ut_eid, name, courses_list, confidence, availability_list, email, topics, study_life, work_hours)
                    self.student_index[ut_eid] = student

        except Exception as e:
            print(f"An error occurred during file loading: {e}")

        print(f"Loaded {len(self.student_index)} students")

    # Definition: Adds a time slot to the availability queue (retained but unused in scoring)
    def post_availability(self, time_slot: str):
        print(f"Note: Global queue is being used, but matching now relies on individual availability.")
        self.open_slots_queue.append(time_slot)

    # Algorithm Method

    # Definition: Finds matches for a given student with enhanced scoring (FIXED)
    def find_matches(self, seeker_eid: str):
        seeker = self.student_index.get(seeker_eid)
        if not seeker:
            print("Seeker not found")
            return

        self.match_heap = [] # Reset heap

        for candidate_eid, candidate in self.student_index.items():
            if candidate_eid == seeker_eid:
                continue

            score = 0

            # 1. Course Overlap Score (Primary Factor)
            shared_courses = seeker.courses.intersection(candidate.courses)
            score += len(shared_courses) * 10

            # 2. Confidence Mismatch Score (Complexity Factor)
            # Penalizes the match if confidence levels are too different
            confidence_diff = abs(seeker.confidence_level - candidate.confidence_level)
            score += confidence_diff * 3

            # 3. Time Slot Overlap Score (Individual Availability Match)
            shared_slots = seeker.individual_availability.intersection(candidate.individual_availability)
            score += len(shared_slots) * 5

            # 4. Topics Need Overlap (High Value)
            if seeker.topics_need and candidate.topics_need:
                shared_topics = seeker.topics_need & candidate.topics_need
                score += len(shared_topics) * 15

            # 5. Study Style Compatibility
            if seeker.study_life != 'none' and candidate.study_life != 'none':
                if seeker.study_life == candidate.study_life:
                    score += 12

            # 6. Workload Similarity
            # Reward smaller difference in work hours (max 10 points)
            difference = abs(seeker.work_hours - candidate.work_hours)
            work_score = max(0, 10 - difference)
            score += work_score

            # 7. Set final score and push to Max-Heap
            candidate.compatibility_score = score
            
            # Use negative score for Max-Heap behavior: (-score, Student object)
            heapq.heappush(self.match_heap, (-candidate.compatibility_score, candidate))

            # The tie_break_heap logic from the original code is redundant and removed.


    # Definition: Gets the best match, shared times, AND shared courses (FIXED)
    def get_best_match(self, seeker_eid: str) -> Optional[Tuple[Student, Set[str], Set[str]]]:
        # Return type: (Best Student, Shared Times, Shared Courses)
        if not self.match_heap:
            return None

        seeker = self.student_index.get(seeker_eid)
        if not seeker:
             return None

        # Pop the element with the highest score (the one with the smallest negative value)
        # best_match_tuple is: (-score, Student)
        best_match_tuple = heapq.heappop(self.match_heap)
        best_partner = best_match_tuple[1] # Extract the Student object

        # Calculate the required intersection data
        shared_slots = seeker.individual_availability.intersection(best_partner.individual_availability)
        shared_courses = seeker.courses.intersection(best_partner.courses)

        # Return a tuple containing all match details
        return (best_partner, shared_slots, shared_courses)

# Main execution block 

if __name__ == "__main__":

    SEEKER_EID = 'aavila'

    csv_file_name = 'students.csv'
    sample_data = [
        {'ut_eid': 'jsmith', 'name': 'John', 'courses': 'CS 313E,M 408C', 'confidence_level': '5', 'availability': 'Mon 3pm;Wed 4pm', 'email': 'john.smith@utexas.edu', 'topics_need': 'Heaps,Trees', 'study_life': 'quiet', 'work_hours': '6'},
        {'ut_eid': 'aavila', 'name': 'Ana', 'courses': 'CS 313E,GOV 310', 'confidence_level': '1', 'availability': 'Mon 3pm;Tue 10am', 'email': 'ana.avila@utexas.edu', 'topics_need': 'Heaps', 'study_life': 'quiet', 'work_hours': '4'},
        {'ut_eid': 'bchen', 'name': 'Ben', 'courses': 'CS 313E,M 408C', 'confidence_level': '3', 'availability': 'Fri 1pm', 'email': 'ben.chen@utexas.edu', 'topics_need': 'Trees', 'study_life': 'group', 'work_hours': '3'},
        {'ut_eid': 'ajones', 'name': 'Alex', 'courses': 'CS 313E,GOV 310,PHI 301', 'confidence_level': '4', 'availability': 'Tue 10am;Wed 4pm', 'email': 'alex.jones@utexas.edu', 'topics_need': 'Heaps', 'study_life': 'quiet', 'work_hours': '4'}
    ]

    try:
        # Re-create the CSV file
        with open(csv_file_name, 'w', newline='') as f:
            fieldnames = list(sample_data[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
        print(f"'{csv_file_name}' created successfully")
    except IOError as e:
        print(f"Error creating file: {e}")

    app = StudyMatch()

    # 1 Test Dictionary
    app.load_data(csv_file_name)
    print(f"Students in Dictionary: {list(app.student_index.keys())}")

    # 2 Test Queue
    app.post_availability('Mon 3pm')
    print(f"Open Slots (Queue - No longer affects scoring directly): {app.open_slots_queue}")

    # 3 Test Algorithm
    print(f"\nFinding Match for '{SEEKER_EID}' (Ana)")
    app.find_matches(SEEKER_EID)

    match_result = app.get_best_match(SEEKER_EID)

    # Unpack the tuple: (Student, Shared Times, Shared Courses)
    if match_result:
        best_partner, shared_slots, shared_courses = match_result

        print("\n--- Match Found! ---")
        print(f"Seeker's Contact: {app.student_index[SEEKER_EID].email}")
        print(f"Best match is: {best_partner}")

        print(f"Common Courses: {', '.join(sorted(list(shared_courses)))}")

        if shared_slots:
            print(f"Mutual Meeting Times: {', '.join(sorted(list(shared_slots)))}")
        else:
            print("No immediate mutual meeting times found, but this is the best partner. Y'all should schedule a common time to meet!")
    else:
        print("Could not find a match.")