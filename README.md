# 🧭 IITP Companion

**IITP Companion+** is a comprehensive web platform built for the students of **IIT Patna**, aiming to streamline daily campus life through smart digital solutions. It integrates food ordering, transportation tracking, event notifications, and more — all under one roof.

## 🚀 Features

### 🍽️ Food Ordering System
- Order food from campus canteens or nearby restaurants
- View dynamic menus and place orders in real-time

### 🚌 Transport Tracker
- Real-time tracking of campus buses or local transport
- Estimate arrival times and plan your journey effectively

### 📝 Event & Assignment Notifier
- Syncs with Moodle to fetch upcoming events and assignments
- Provides reminders and alerts for deadlines

### 📺 Virtual Event Viewer
- Watch live or recorded fests, seminars, and webinars
- Enhances student participation and accessibility

### ✍️ Blog System
- Platform for students to publish and read blogs
- Covers tech, college life, academics, and more

### 📬 Complaint / Feedback System
- Submit complaints, suggestions, and feedback
- Ensures two-way communication with authorities

---

## 🛠️ Tech Stack

| Component        | Technology          |
|------------------|---------------------|
| **Frontend**     | HTML, CSS, JavaScript, Tailwind/Bootstrap |
| **Backend**      | Django (Python)     |
| **Database**     | SQLite3 / MySQL     |
| **APIs**         | Django REST Framework (optional) |
| **Integration**  | Moodle API (for notifications) |

---

## 📸 Screenshots

> Include screenshots of:
> - Dashboard/Homepage  
> - Food Ordering Page  
> - Event Notifier  
> - Virtual Event Player  
> - Blog or Feedback UI

*(Add them here using: `![Alt text](screenshots/home.png)`)*

---

## 🧑‍💻 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/ankitkushwaha-ank/iitpcompanion.git
cd iitpcompanion

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver