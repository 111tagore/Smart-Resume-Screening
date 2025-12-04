import React from "react";

export default function Sidebar({onLogout}){
  return (
    <div className="sidebar">
      <div style={{fontWeight:600, marginBottom:10}}>Menu</div>
      <div className="menu-item">Dashboard</div>
      <div className="menu-item">Settings</div>
      <div className="menu-item" onClick={onLogout}>Logout</div>
    </div>
  );
}
