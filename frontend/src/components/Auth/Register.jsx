import React, { useState } from "react";
import axios from "axios";

export default function Register({ onSwitch, onRegisterSuccess }){
  const [step,setStep]=useState(1);
  const [form,setForm]=useState({
    first_name:"", last_name:"", employee_role:"", employee_id:"", department:"",
    email:"", password:"", confirm_password:""
  });
  const [err,setErr]=useState("");

  const next = () => {
    setErr("");
    if(step===1){
      const needed = ["first_name","last_name","employee_role","employee_id","department"];
      for(let k of needed) if(!form[k]) { setErr("Please fill all fields"); return; }
      setStep(2);
    } else {
      if(!form.email || !form.password || !form.confirm_password) { setErr("Please fill all fields"); return; }
      if(form.password !== form.confirm_password){ setErr("Passwords don't match"); return; }
      axios.post("http://localhost:5000/register", {
        first_name: form.first_name,
        last_name: form.last_name,
        employee_role: form.employee_role,
        employee_id: form.employee_id,
        department: form.department,
        email: form.email,
        password: form.password
      }).then(res=>{
        if(res.data.success){
          onRegisterSuccess();
        } else setErr(res.data.message || "Registration failed");
      }).catch(err=>{
        setErr(err.response?.data?.message || "Server error");
      });
    }
  };

  return (
    <div className="card">
      <div className="header"><h2>Register</h2><div className="small">Create your HR account</div></div>
      {step===1 ? (
        <>
        <div className="auth-grid">
          <input className="input" placeholder="First Name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})}/>
          <input className="input" placeholder="Last Name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})}/>
          <input className="input" placeholder="Employee Role" value={form.employee_role} onChange={e=>setForm({...form, employee_role:e.target.value})}/>
          <input className="input" placeholder="Employee ID" value={form.employee_id} onChange={e=>setForm({...form, employee_id:e.target.value})}/>
          <input className="input" placeholder="Department" value={form.department} onChange={e=>setForm({...form, department:e.target.value})}/>
        </div>
        <div style={{display:"flex",gap:10, marginTop:8}}>
          <button className="btn" onClick={next}>Continue</button>
          <button className="btn" style={{background:"transparent"}} onClick={onSwitch}>Back to Login</button>
        </div>
        </>
      ) : (
        <>
          <input className="input" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/>
          <input className="input" placeholder="Create Password" type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})}/>
          <input className="input" placeholder="Re-enter Password" type="password" value={form.confirm_password} onChange={e=>setForm({...form, confirm_password:e.target.value})}/>
          {err && <div style={{color:"red"}}>{err}</div>}
          <div style={{display:"flex",gap:10, marginTop:8}}>
            <button className="btn" onClick={next}>Register</button>
            <button className="btn" style={{background:"transparent"}} onClick={()=>setStep(1)}>Back</button>
          </div>
        </>
      )}
    </div>
  );
}
