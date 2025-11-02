# 📚 Library Booking System

A **Flask-based web application** that allows users to **search, reserve, and manage library books** easily.
Librarians can manage the catalog by adding or removing books, while readers can browse available titles and make bookings.

---

## 🚀 Features

### 👤 User Roles

* **Reader:** Can search, view, and book available books.
* **Librarian:** Can add or remove books and manage the library database.

### 🧩 Core Functionalities

* User registration and login system
* Role-based access control (Librarian vs Reader)
* Search and reserve books
* Manage booking history
* Cancel reservations
* Librarian dashboard for managing books
* Flash messages for feedback and validation

---

## 🏗️ Project Structure

```
library-booking-system/
│
├── app.py
├── models.py
├── forms.py
├── requirements.txt
├── .env
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│   └── librarian.html
│
└── static/
    └── (optional CSS or JS files)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MahmoudSalama7/library-booking-system.git
cd library-booking-system
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add:

```bash
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///library.db
```

### 5️⃣ Initialize the Database

Run the app once to create the database:

```bash
python app.py
```

✅ A default librarian account is automatically created:

```
Username: admin
Password: admin123
```

---

## 🖥️ Running the Application

Start the Flask development server:

```bash
flask run
```

Or simply:

```bash
python app.py
```

Then open your browser at:

```
http://127.0.0.1:5000
```

---

## 🧩 Usage Guide

### 👨‍💻 Readers

* Register as a reader.
* Log in and use the **Search** page to find books.
* Click **Reserve Now** to book an available book.
* View your bookings in **My Bookings**.
* Cancel bookings anytime.

### 📚 Librarians

* Log in as librarian (`admin / admin123`) or register as a Librarian.
* Access the **Librarian Panel**.
* Add new books or remove existing ones.

---

## 🧱 Tech Stack

| Component          | Technology                  |
| ------------------ | --------------------------- |
| Backend            | Flask (Python)              |
| Database           | SQLite (SQLAlchemy ORM)     |
| Frontend           | HTML, CSS, Jinja2 Templates |
| Authentication     | Flask-Login                 |
| Forms & Validation | Flask-WTF                   |
| Password Hashing   | Werkzeug Security           |

---

## 🧠 Future Enhancements

* Room and event booking modules
* Email notifications for reservations
* Book categories and filters
* User profile management
* Admin analytics dashboard

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push to your fork and submit a PR 🎉

---

## 👤 Author

**Mahmoud Salama**
📧 [mahmoudsalamacs@gmail.com](mailto:mahmoudsalamacs@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/mahmoud-salama-5a0525227/)

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to use and modify it for educational purposes.
