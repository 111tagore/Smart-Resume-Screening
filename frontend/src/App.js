import React, { useState } from "react";
import AuthPage from "./components/AuthPage1";
import Dashboard from "./components/Dashboard";

function App() {
  // Get current session user from localStorage (optional)
  const [user, setUser] = useState(() => {
    const savedUser = JSON.parse(localStorage.getItem("currentUser"));
    return savedUser || null;
  });

  // Handle login
  const handleLogin = (loggedInUser) => {
    setUser(loggedInUser);
    localStorage.setItem("currentUser", JSON.stringify(loggedInUser));
  };

  // Handle logout
  const handleLogout = () => {
    setUser(null); // clear session only
    localStorage.removeItem("currentUser"); // optional: clear only session, not all users
  };

  return (
    <>
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <AuthPage onLogin={handleLogin} />
      )}
    </>
  );
}

export default App;
