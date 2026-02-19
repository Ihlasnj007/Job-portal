# 💼 TalentHire – Django Job Portal

TalentHire is a fully-featured Job Portal built with Django. It allows employers to post jobs, and jobseekers to find and apply to jobs that match their skills. The portal includes role-based dashboards, smart recommendations, application tracking, and profile management.

---

## 🚀 Features

### ✅ Authentication & Authorization
- Separate registration for **Jobseekers** and **Employers**
- **Email-based login** (no usernames)
- Session-based authentication
- Role-based dashboard redirection

### 👤 Jobseeker Module
- Register & log in using email
- Create and manage profile with:
  - Phone number
  - Profession
  - Education
  - Skills (comma-separated)
  - Work experience
  - Resume upload & view
- **Recommended Jobs page**:
  - Jobs filtered by profession and skills
  - Excludes already applied jobs
- Apply to jobs (only once per job)
- Track application statuses: Pending, Shortlisted, Rejected
- View current resume and edit profile anytime

### 🧑‍💼 Employer Module
- Register & log in as company
- Post new job listings with:
  - Job title, description, type, department, experience level, location, etc.
- View all posted jobs with pagination and search
- View applicants per job with status filter
- Shortlist or reject applications
- One-click **Send Mail to shortlisted applicants**
  - Opens Gmail with pre-filled email
  - Tracks mail sent (hides button after click)

### 📊 Dashboards
- **Jobseeker Dashboard**:
  - See recommended jobs
  - Track your applications
- **Employer Dashboard**:
  - Manage job postings
  - View and filter job applicants

### 📄 Additional Features
- Smart job filtering by:
  - Job title
  - Job type
  - Experience level
  - Date posted
- Clean and responsive UI using **HTML + CSS**
- Protected views using `@login_required`
- Pagination across job listings & applicant list
- Error handling with styled messages
- Fully working logout system

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Font Awesome
- **Database**: PostgreSQL (or default SQLite during dev)
- **Authentication**: Django’s session framework
- **File Uploads**: Django’s media file handling (resumes)

---

## 🔑 Setup Instructions

### Clone the repo:
```
git clone https://github.com/Ihlasnj007/Job-portal.git
cd Job-portal
```

## 🧑‍💻 Developed By
- Ihlas N J
- A full-fledged Django web application project focused on real-world job portal workflows.

>>>>>>> 45ca5dc941d3ce8faadcd8c84067b21fd11184fd
