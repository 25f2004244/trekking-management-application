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

