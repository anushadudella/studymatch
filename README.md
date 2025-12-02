## StudyMatch: Intelligent Peer Matching System

## Overview

StudyMatch is a Python-based application designed to intelligently match students for collaborative study sessions. It utilizes an enhanced scoring algorithm and a Max-Heap data structure to efficiently find the most compatible study partner for a given user.

The system incorporates comprehensive scoring based on shared courses, mutual availability, topic needs, and study style preferences, leveraging the power of Python's built-in data structures.

-----

## Algorithms and Data Structures Used

The core of StudyMatch relies on efficiency and structured data management:

| Component | Data Structure/Algorithm | Purpose |
| :--- | :--- | :--- |
| **Matching Score Retrieval** | **Max-Heap** (via `heapq`) | Stores all potential matches prioritized by their compatibility score. The best match is retrieved in $O(1)$ time after the scoring process. |
| **Scoring Process** | **Set Operations** | Used extensively to calculate overlaps (shared courses, mutual availability, shared topic needs) in $O(1)$ expected time per factor. |
| **Student Data Management** | **Dictionary** (`self.student_index`) | Provides $O(1)$ average time access to student profiles using their `ut_eid` (unique identifier) as the key. |
| **Compatibility Comparison** | **`__lt__` Dunder Method** | Implemented within the `Student` class to enable the Max-Heap to correctly prioritize the student object with the *highest* compatibility score. |

-----

## Features

  * **Intelligent Matching:** Calculates a comprehensive compatibility score using multiple weighted factors (courses, confidence levels, availability, topics, study style, workload).
  * **Efficient Retrieval:** Uses a Python `heapq` (Max-Heap) to store and retrieve the best match in $O(1)$ time after the initial scoring process ($O(N \log N)$ total time for $N$ candidates).
  * **Data Loading:** Imports student data from a structured CSV file (`students.csv`).
  * **Detailed Output:** Provides the best partner's contact information, shared courses, mutual meeting times, and resources.

-----

## Compatibility Scoring Factors

The algorithm weights the following factors to determine compatibility:

| Factor | Description | Weight/Calculation |
| :--- | :--- | :--- |
| **Course Overlap** | Primary shared classes. | $\text{Count} \times 10$ |
| **Topic Needs Overlap** | Shared need for specific concepts (e.g., 'Heaps', 'Trees'). | $\text{Count} \times 15$ |
| **Time Slot Overlap** | Mutual availability slots (e.g., 'Mon 3pm'). | $\text{Count} \times 5$ |
| **Study Style** | Match on preferred study life (e.g., 'quiet' vs 'group'). | $+12$ if styles match |
| **Confidence Mismatch** | Difference in confidence level (1-5). | $\text{Absolute Difference} \times 3$ |
| **Workload Similarity** | Similarity in estimated weekly work hours. | $\max(0, 10 - \text{Difference})$ |

-----

## Installation

StudyMatch is a pure Python script and requires no external packages beyond the standard library.

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/studymatch.git
    cd studymatch
    ```

2.  **Prepare Data:** Ensure you have a `students.csv` file in the root directory formatted with the required columns (`ut_eid`, `name`, `courses`, `confidence_level`, `availability`, `email`, `topics_need`, `study_life`, `work_hours`).

-----

## Usage

The script automatically generates a `students.csv` file with sample data and then runs the matching algorithm for the defined seeker (`SEEKER_EID = 'aavila'`).

```bash
python studymatch.py
```

### Example Output

The output reflects the data loading, resource management, and the final match found:

```
'students.csv' created successfully
Loading data from students.csv...
Loaded 4 students
Students in Dictionary: ['jsmith', 'aavila', 'bchen', 'ajones']
Resource added to Alex (ajones): GOV310 Final Review.pdf

Ana's Resources: 
[]
Note: Global queue is being used, but matching now relies on individual availability.
Open Slots (Queue - No longer affects scoring directly): ['Mon 3pm']

Finding Match for 'aavila' (Ana)

--- Match Found! ---
Seeker's Contact: ana.avila@utexas.edu
Best match is: Student(Name: Alex, EID: ajones, Score: 49, Confidence: 4/5, Email: alex.jones@utexas.edu)
Common Courses: CS 313E, GOV 310
Mutual Meeting Times: Tue 10am
Partner's Resources:
['GOV310 Final Review.pdf']
```

-----

## Code Structure

The core functionality is contained within two classes:

  * **`Student`:** Holds all attributes for a single student and implements the **`__lt__` method** to enable the Max-Heap to prioritize students by their `compatibility_score`.
  * **`StudyMatch`:** The main manager class responsible for `load_data`, managing the `self.student_index` (Dictionary), implementing the comprehensive `find_matches` scoring algorithm, and retrieving the `get_best_match` using the Max-Heap (`self.match_heap`).

-----

## Citations and Acknowledgements

This project was developed with the assistance of an artificial intelligence model, which provided the structural foundation, the compatibility scoring algorithm, and debugging/refinement of the Max-Heap implementation.

### AI Model Citation

The core Python code in this repository was generated and refined by Google's Gemini large language model (LLM) in response to a user request for a student matching system.

> Gemini. (2025, December). *StudyMatch: Intelligent Peer Matching System* [Computer software]. Google.

### Library Citation

The project relies solely on standard, built-in Python modules.

  * **`csv`**: Used for reading and parsing student data from the `students.csv` file.
  * **`heapq`**: Essential for implementing the Max-Heap data structure to prioritize and retrieve the best match efficiently.
  * **`typing`**: Used for type hinting to improve code readability and maintainability.

-----

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.
