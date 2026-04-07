# Exam Session Management System

A Django-based web application for managing university exam sessions, including users, majors, faculties, exams, and exam halls.

## Features

* **Authentication and User Accounts**
  * User registration, login, logout, and profile page
  * Custom user model
  * Admin/user role separation
  * API access for user management

* **Faculties and Majors Management**
  * Create, read, update, and delete faculties and majors
  * Detail pages with related data
  * Automatic slug generation
  * Search and filtering support for majors

* **Exam Halls Management**
  * Manage exam halls with capacity and computer-room flags
  * Validation for hall capacity
  * Prevent duplicate hall names within the same faculty
  * Custom delete/edit handling for halls with related exams

* **Exam Scheduling**
  * 2-step wizard-based exam creation and editing
  * Step 1: define exam details
  * Step 2: select available exam halls
  * Automatic filtering of halls by date, time, capacity, and computer-room requirement
  * Validation for exam duration and duplicate exams
  * Search by subject and date

* **Shared Pages**
  * Home page
  * Dashboard/about page with summary statistics
  * Custom error pages for `400`, `403`, `404`, `405`, and `500`

* **Responsive Design**
  * Built with Bootstrap 5 for a mobile-friendly interface

## Project Structure

* `accounts`: Authentication, profile, custom user model, and API user management
* `common`: Base templates, home page, dashboard, and shared utilities
* `faculties`: Faculty models, forms, views, and CRUD operations
* `majors`: Major models, forms, views, and CRUD operations
* `exam_halls`: Exam hall models, forms, views, and CRUD operations
* `exams`: Core scheduling logic, validation forms, and wizard views
* `templates`: Shared templates and custom error pages
* `tests`: Automated tests for the application

## Database Structure

| Table Name | Fields | Relations |
| :--- | :--- | :--- |
| **ExamSessionUser** | `id` (PK)<br>`email`<br>`username`<br>`first_name`<br>`last_name`<br>`academic_rank`<br>`is_active`<br>`is_staff` | **Many-to-Many** with `Major` |
| **Faculty** | `id` (PK)<br>`name`<br>`description`<br>`location`<br>`slug`<br>`created_at`<br>`updated_at` | **One-to-Many** with `Major` |
| **Major** | `id` (PK)<br>`name`<br>`description`<br>`slug`<br>`faculty_id`<br>`created_at`<br>`updated_at` | **ForeignKey** to `Faculty`<br>**One-to-Many** with `Exam` |
| **ExamHall** | `id` (PK)<br>`name`<br>`capacity`<br>`is_computer_room`<br>`faculty_id`<br>`created_at`<br>`updated_at` | **Many-to-Many** with `Exam` |
| **Exam** | `id` (PK)<br>`subject`<br>`major_id`<br>`needs_computers`<br>`number_of_examinees`<br>`date`<br>`start_time`<br>`end_time`<br>`created_at`<br>`updated_at` | **ForeignKey** to `Major`<br>**Many-to-Many** with `ExamHall` |

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

3.  **Configure environment variables**
   * Copy `.env.template` to `.env`
   * Set values for:
     * `SECRET_KEY`
     * `DEBUG`
     * `ALLOWED_HOSTS`
     * `DB_NAME`
     * `DB_USER`
     * `DB_PASS`
     * `DB_HOST`
     * `DB_PORT`

4.  **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Populate initial data** (Optional):
    ```bash
    python main.py
    ```

6.  **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Usage

* **Home**: Overview page with faculty-related data
* **Dashboard**: Summary statistics and project info
* **Accounts**: Register, log in, log out, and view profile
* **Faculties**: Manage faculties and view their related majors, exams, and halls
* **Majors**: Browse, search, and manage majors
* **Exam Halls**: Manage halls and their capacity/computer-room settings
* **Exams**: Create and edit exams using the scheduling wizard
* **Error Pages**: Friendly custom pages for common HTTP errors

## Testing

Run the test suite with:
```bash
python manage.py test
```

---

## Notes

* Link to the deployed project: exam-session-fnf4evc2csgce3d6.francecentral-01.azurewebsites.net
* The project uses a custom user model.
* Project depends on superuser to manage user groups.
* Some views require authentication and/or permissions.
* Exam scheduling includes validation to avoid conflicts and capacity issues.
* Custom error pages are available when `DEBUG = False`.

---

## License

This project is open source and available under the [MIT License](LICENSE).