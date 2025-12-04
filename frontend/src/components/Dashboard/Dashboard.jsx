import React, { useState } from "react";
import Sidebar from "./Sidebar";
import axios from "axios";

export default function Dashboard({user, onLogout}){
  const [files, setFiles] = useState([]);
  const [jobRole, setJobRole] = useState("");
  const [openings, setOpenings] = useState(1);
  const [results, setResults] = useState([]);
  const [selected, setSelected] = useState([]);
  const [analysisId, setAnalysisId] = useState(null);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const upload = async () => {
    if(!files || files.length===0) return alert("Choose files");
    const form = new FormData();
    for(let i=0;i<files.length;i++) form.append("files", files[i]);
    try {
      const res = await axios.post("http://localhost:5000/upload_resumes", form, {
        headers: {"Content-Type":"multipart/form-data"}
      });
      if(res.data.success) alert("Uploaded");
    } catch (e){
      alert("Upload failed");
    }
  };

  const analyze = async () => {
    if(!jobRole) return alert("Type job role");
    try {
      const res = await axios.post("http://localhost:5000/analyze", { job_role: jobRole, openings });
      if(res.data.success){
        setAnalysisId(res.data.analysis_id);
        setResults(res.data.ranked_results);
        setSelected(res.data.selected);
      }
    } catch (e){
      alert("Analysis failed");
    }
  };

  return (
    <div className="card app-grid" style={{alignItems:"flex-start"}}>
      <Sidebar onLogout={onLogout} />
      <div style={{flex:1}}>
        <div className="header">
          <div>
            <h3>Dashboard</h3>
            <div className="small">Welcome, {user.first_name}</div>
          </div>
        </div>

        <div className="upload-area">
          <div style={{display:"flex",gap:10, alignItems:"center"}}>
            <input type="file" multiple onChange={handleFileChange} />
            <button className="btn" onClick={upload}>Upload Resumes</button>
          </div>

          <div style={{marginTop:12, display:"flex", gap:10}}>
            <input className="input" placeholder="Type job role (e.g. Python Developer)" value={jobRole} onChange={e=>setJobRole(e.target.value)} />
            <input className="input" placeholder="Number of openings" type="number" value={openings} onChange={e=>setOpenings(e.target.value)} style={{width:140}} />
            <button className="btn" onClick={analyze}>Start Analysis</button>
          </div>

          <div style={{marginTop:20}}>
            <h4>Results</h4>
            <table className="results-table">
              <thead><tr><th>Filename</th><th>Score (0-10)</th></tr></thead>
              <tbody>
                {results.map((r, i) => (
                  <tr key={i}>
                    <td>{r.filename}</td>
                    <td>{r.score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{marginTop:12}}>
              <strong>Selected Candidates (top {openings})</strong>
              <ul>
                {selected.map((s, idx) => <li key={idx}>{s.filename} — {s.score}</li>)}
              </ul>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
