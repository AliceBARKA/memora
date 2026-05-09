import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Courses from "../pages/Courses/Courses";
import Flashcards from "../pages/Flashcards/Flashcards";
import Quiz from "../pages/Quiz/Quiz";
import Planning from "../pages/Planning/Planning";
import Todo from "../pages/Todo/Todo";
import AppLayout from "../layouts/AppLayout";


function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />

      <Route element={<AppLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/flashcards" element={<Flashcards />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/planning" element={<Planning />} />
        <Route path="/todo" element={<Todo />} />

      </Route>
    </Routes>
  );
}

export default AppRoutes;



