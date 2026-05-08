CREATE TABLE COURSE_PDF (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    file TEXT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)

);

CREATE TABLE Deck(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT ,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    course_pdf_id INTEGER,
    FOREIGN KEY (course_pdf_id) REFERENCES Courses(id)
    FOREIGN KEY (user_id) REFERENCES Users(id)
);


CREATE TABLE Flashcard(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES Deck(id)
);

CREATE TABLE Quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES Deck(id)
);

CREATE TABLE Availability(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)

);

CREATE TABLE QuizResult(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    passed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE RevisionPlan(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE RevisionSession(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status TEXT NOT NULL,
    revision_plan_id INTEGER NOT NULL,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (revision_plan_id) REFERENCES RevisionPlan(id),
    FOREIGN KEY (deck_id) REFERENCES Deck(id)

);

CREATE TABLE Todo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    revision_session_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (revision_session_id) REFERENCES RevisionSession(id)
);