CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'student',
    is_active BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE Folder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE CoursePDF (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT DEFAULT 'Général',
    file TEXT NOT NULL,
    summary TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    folder_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (folder_id) REFERENCES Folder(id)
);

CREATE TABLE Deck (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    course_pdf_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (course_pdf_id) REFERENCES CoursePDF(id)
);

CREATE TABLE Flashcard (
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
    subject TEXT DEFAULT 'Général',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (deck_id) REFERENCES Deck(id)
);

CREATE TABLE QuizQuestion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    choices TEXT,
    quiz_id INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);

CREATE TABLE QuizResult (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    passed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE RevisionPlan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE RevisionSession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    revision_date DATE NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status TEXT NOT NULL,
    revision_plan_id INTEGER NOT NULL,
    deck_id INTEGER NOT NULL,
    FOREIGN KEY (revision_plan_id) REFERENCES RevisionPlan(id),
    FOREIGN KEY (deck_id) REFERENCES Deck(id)
);

CREATE TABLE Todo (
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

CREATE TABLE ForumPost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE ForumComment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (post_id) REFERENCES ForumPost(id)
);

CREATE TABLE AIConversation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    scope TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    course_pdf_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (course_pdf_id) REFERENCES CoursePDF(id)
);

CREATE TABLE AIMessage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    conversation_id INTEGER NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES AIConversation(id)
);