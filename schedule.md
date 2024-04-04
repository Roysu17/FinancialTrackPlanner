# Project Roles and Schedule

## Roles

### Roy - Focused on SQL Database and Project Lead

- **`app/database.py`**: Handle all the database interactions, including setting up the database schema and implementing CRUD operations.
- **Documentation**: Focus on the parts that deal with database setup and any configurations related to database interactions in `config.py`.
- **Final Testing and Debugging**: Oversee and participate in the final testing phase, especially focusing on database integrity and performance.
- **`app/login.py`**: Handle the login interface's frontend and backend authentication logic.
- **`app/main.py`**: Set up the application's main window and ensure that the navigation flows correctly between different parts of the application.

### Sean - Focused on the Frame and Menu Components

- **`app/__init__.py`**: Set up the application's main window and ensure that the navigation flows correctly between different parts of the application.
- **`app/dashboard.py`**: Work on the dashboard's layout and how it presents the overview of the user's finances.
- **UI/UX Design**: Given the focus on the frame and menus, ensuring a user-friendly interface would naturally fall under Sean's responsibilities.

### Adam - Working on the Rest of the Application

- **`app/transactions.py`, `app/budget.py`, and `app/reports.py`**: These components involve a mix of frontend and backend work but are less focused on the core database interactions. Start with transactions.
- **Tests**: Responsible for writing tests for his components, ensuring that transactions, budgeting, and reports work as expected.
- **Documentation**: Contribute to the `docs/` folder by documenting the usage, setup, and features related to transactions, budgeting, and reporting.
- **UI/UX Design**: Help with the focus on the frame and menus, ensuring a user-friendly interface.

## Suggested Schedule

### Week 1

- **Days 1-2**: Project setup (everyone) - Setting up the project environment, reviewing the project structure, and initial planning.
- **Days 3-5**: Core development starts - Roy focuses on `database.py`, Roy and Sean on `main.py` and `login.py`, Adam on starting `transactions.py`.

### Week 2

- **Days 6-7**: Continue development - Sean moves to `dashboard.py`, Adam continues on `transactions.py`, Roy supports database integration.
- **Days 8-9**: Initial integration - Begin integrating the developed parts, identify any major issues.
- **Days 10-11**: Development on remaining components – Roy and Sean move to `reports.py` and `budget.py`, Sean and Roy polish UI/UX, Roy focuses on any remaining database issues and starts on final testing preparations.
- **Day 12**: Testing - Everyone tests their components, identifying bugs.
- **Day 13**: Debugging and documentation - Fix identified bugs, and everyone contributes to the documentation.
- **Day 14**: Final review and submission - Final integration testing, review documentation, and submit the project.
