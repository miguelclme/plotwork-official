import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import { currentUser } from "./auth.js";
import ToolList from "./pages/ToolList.jsx";
import ToolDetail from "./pages/ToolDetail.jsx";
import LendTool from "./pages/LendTool.jsx";
import MyLoans from "./pages/MyLoans.jsx";
import Deposit from "./pages/Deposit.jsx";
import Messages from "./pages/Messages.jsx";
import Login from "./pages/Login.jsx";
import "./styles.css";

function SignedIn({ children }) {
  return currentUser() ? children : <Navigate to="/login" replace />;
}

function Nav() {
  return (
    <nav className="nav">
      <Link to="/tools">Tools</Link>
      <Link to="/tools/new">Lend a tool</Link>
      <Link to="/loans">My loans</Link>
      <Link to="/messages">Messages</Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/tools" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/tools" element={<SignedIn><ToolList /></SignedIn>} />
        <Route path="/tools/new" element={<SignedIn><LendTool /></SignedIn>} />
        <Route path="/tools/:id" element={<SignedIn><ToolDetail /></SignedIn>} />
        <Route path="/loans" element={<SignedIn><MyLoans /></SignedIn>} />
        <Route path="/loans/:id/deposit" element={<SignedIn><Deposit /></SignedIn>} />
        <Route path="/messages" element={<SignedIn><Messages /></SignedIn>} />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
