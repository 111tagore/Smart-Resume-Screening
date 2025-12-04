import React, { useState } from "react";
import axios from "axios";

export default function Login({ onSwitch, onLoginSuccess }){
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async () => {
    setErr("");
    try {
      const res = await axios.post("http://localhost:5000/login", { email, password });
      if(res.data.success){
        onLoginSuccess(res.data.user);
      } else {
        setErr(res.data.message || "Login failed");
      }
    } catch(e){
      setErr(e.response?.data?.message || "Server error");
    }
  };

  return (
    <div className="card">
      <div className="header">
        <h2>Smart Resume Screening</h2>
        <div className="small">Login</div>
      </div>
      <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="input" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      {err && <div style={{color:"red"}}>{err}</div>}
      <div style={{display:"flex",gap:10, marginTop:8}}>
        <button className="btn" onClick={submit}>Login</button>
        <button className="btn" style={{background:"transparent", color:"#333", border:"1px solid rgba(0,0,0,0.06)"}} onClick={onSwitch}>Don't have an account? Register</button>
      </div>
    </div>
  );
}
