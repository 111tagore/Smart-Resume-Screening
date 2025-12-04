import React, { useState } from "react";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Dashboard from "./components/Dashboard/Dashboard";

export default function App(){
  const [user, setUser] = useState(null);
  const [page, setPage] = useState("login");

  const onLoginSuccess = (userData) => {
    setUser(userData);
    setPage("dashboard");
  };

  return (
    <div className="app-root">
      {!user && page === "login" && <Login onSwitch={() => setPage("register")} onLoginSuccess={onLoginSuccess} />}
      {!user && page === "register" && <Register onSwitch={() => setPage("login")} onRegisterSuccess={() => setPage("login")} />}
      {user && <Dashboard user={user} onLogout={() => { setUser(null); setPage("login"); }} />}
    </div>
  );
}
