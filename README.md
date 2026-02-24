# Exam Session Management System

A simple Django-based web application for managing university exam sessions, including majors, exams, and exam halls.

## Features

*   **Majors Management**: Create, read, update, and delete (CRUD) majors. View details and associated exams.
*   **Exam Halls Management**: Manage exam halls with capacity and computer availability. Includes validation to prevent deletion or modification of halls that are currently hosting exams.
*   **Exam Scheduling**:
    *   **Wizard-based Creation**: A 2-step wizard for scheduling exams.
        *   Step 1: Define exam details (subject, major, date, time, examinees, computer needs).
        *   Step 2: Select available exam halls based on capacity and availability.
    *   **Conflict Detection**: Automatically filters out exam halls that are already booked for the selected time slot.
    *   **Validation**: Ensures exams are scheduled within valid hours (8:00 - 20:00), have sufficient duration, and do not exceed hall capacities.
    *   **Unique Constraints**: Prevents duplicate exams for the same subject and major.
*   **Search Functionality**: Search for exams by subject and date. Search for exam halls by name and computer availability.
*   **Responsive Design**: Built with Bootstrap 5 for a mobile-friendly interface.

---

## Database Structure

| Table Name | Fields | Relations |
| :--- | :--- | :--- |
| **Major** | `id` (PK)<br>`name`<br>`slug`<br>`created_at`<br>`updated_at` | **One-to-Many** with `Exam` (via `exam` related name) |
| **ExamHall** | `id` (PK)<br>`name`<br>`capacity`<br>`is_computer_room`<br>`created_at`<br>`updated_at` | **Many-to-Many** with `Exam` (via `hosted_exams` related name) |
| **Exam** | `id` (PK)<br>`subject`<br>`major_id` (FK)<br>`needs_computers`<br>`number_of_examinees`<br>`date`<br>`start_time`<br>`end_time`<br>`created_at`<br>`updated_at` | **ForeignKey** to `Major` (field: `major`)<br>**ManyToManyField** to `ExamHall` (field: `exam_halls`) |

---

## Project Structure

*   `common`: Base templates, home page, and shared utilities.
*   `majors`: Models and views for handling academic majors.
*   `exam_halls`: Models and views for managing physical exam locations.
*   `exams`: Core logic for exam scheduling, including the creation wizard and validation forms.

---

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd exam_session
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up database** (Using PostgreSQL):
    In exam_session\settings.py enter your Postgre user credentials.
    Create a database with the corresponding name ("exam_session_db")

4.  **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Populate initial data** (Optional):
    ```bash
    python main.py
    ```

6.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7.  **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Usage

*   **Home**: Dashboard with quick stats and recent activity.
*   **Majors**: List of all majors. Click "Create New Major" to add one.
*   **Exam Halls**: List of halls. Use the search bar to filter by computer availability.  
    *Note: You are not allowed to delete exam halls or edit their capacity and computer availability fields, if there is already an exam hosted in them!*
*   **Exams**: List of scheduled exams. Use the "Create New Exam" button to start the scheduling wizard.
*   All models feature Edit and Delete functions.
---

## License

This project is open source and available under the [MIT License](LICENSE).