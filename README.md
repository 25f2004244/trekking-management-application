# Trekking Management Application

A web-based trekking management system built with Flask and SQLAlchemy, developed as a MAD1 project for the IIT Madras BS Degree program.

## Overview

This application allows users to browse and book treks, staff to manage treks assigned to them by the admin, and an admin to oversee the entire platform — managing treks, staff, users, and bookings.

## Features

- Role-based registration and login (User, Staff, Admin)
- Staff signup requires admin approval before login
- Admin: create, edit, delete treks; assign staff; manage trek status
- Admin: approve/reject staff requests; blacklist/reactivate staff and users
- User: browse, search, and book available treks with live slot availability
- Staff: manage assigned treks (update slots, status); approve/decline booking requests
- Search functionality across treks, staff, and users
- Profile settings (username, email, password) for staff and users

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite3 with SQLAlchemy ORM
- **Frontend:** Jinja2 templates, HTML, CSS
- **Session Management:** Flask sessions

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

The database is created automatically on first run and pre-filled with demo accounts, so no manual signup is needed.

## Demo Accounts

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| Admin | admin@trek | admin | Predefined |
| Staff | s1@trek, s2@trek, s3@trek | s1, s2, s3 | Approved |
| Staff | sr1@trek, sr2@trek | sr1, sr2 | Pending approval (can't log in until approved) |
| Staff | sb1@trek, sb2@trek | sb1, sb2 | Blocked |
| User | u1@trek, u2@trek, u3@trek | u1, u2, u3 | Active |
| User | ub1@trek, ub2@trek | ub1, ub2 | Blocked |

## Notes

- Passwords are stored in plaintext because this is a demo/college project.
- Trek status: `Open`, `Ongoing`, `Closed`, `Completed`.
- Booking status: `pending`, `approved`, `cancelled`.