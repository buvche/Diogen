from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from api.routes import ingest, verify
from core.config import settings
from core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(ingest.router, prefix="/api", tags=["ingestion"])
app.include_router(verify.router, prefix="/api", tags=["verification"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diogen</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh;padding:2rem}
  .container{max-width:800px;margin:0 auto}
  h1{font-size:1.8rem;margin-bottom:.25rem}
  .subtitle{color:#94a3b8;margin-bottom:2rem;font-size:.9rem}
  .card{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:1.25rem;margin-bottom:1rem}
  .card h2{font-size:1rem;color:#94a3b8;margin-bottom:.75rem;
    text-transform:uppercase;letter-spacing:.05em;font-weight:500}
  .status{display:flex;align-items:center;gap:.5rem}
  .dot{width:10px;height:10px;border-radius:50%;background:#ef4444}
  .dot.ok{background:#22c55e}
  .dot.loading{background:#eab308;animation:pulse 1s infinite}
  @keyframes pulse{50%{opacity:.5}}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
  @media(max-width:600px){.grid{grid-template-columns:1fr}}
  .stat{text-align:center;padding:.5rem}
  .stat .num{font-size:2rem;font-weight:700;color:#f8fafc}
  .stat .label{font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em}
  form{display:flex;flex-direction:column;gap:.75rem}
  label{font-size:.85rem;color:#94a3b8}
  select,textarea{background:#0f172a;border:1px solid #334155;border-radius:6px;
    padding:.5rem .75rem;color:#e2e8f0;font-family:inherit;font-size:.85rem;resize:vertical}
  select:focus,textarea:focus{outline:none;border-color:#3b82f6}
  button{background:#3b82f6;color:#fff;border:none;border-radius:6px;
    padding:.6rem 1.2rem;cursor:pointer;font-size:.85rem;font-weight:500;align-self:flex-start}
  button:hover{background:#2563eb}
  button:disabled{background:#334155;cursor:not-allowed}
  .result{font-family:'SF Mono',Monaco,Consolas,monospace;font-size:.8rem;padding:.75rem;
    background:#0f172a;border-radius:6px;border:1px solid #334155;white-space:pre-wrap;display:none}
  .result.show{display:block}
  .result.err{border-color:#ef4444;color:#fca5a5}
  .result.ok{border-color:#22c55e;color:#86efac}
  .endpoints{list-style:none;font-family:monospace;font-size:.85rem}
  .endpoints li{padding:.35rem 0;display:flex;gap:.75rem;align-items:center}
  .method{background:#22c55e20;color:#22c55e;padding:.15rem .4rem;
    border-radius:4px;font-size:.75rem;font-weight:600;min-width:3rem;text-align:center}
  .method.post{background:#3b82f620;color:#60a5fa}
  a{color:#60a5fa;text-decoration:none}
  a:hover{text-decoration:underline}
</style>
</head>
<body>
<div class="container">
  <h1>Diogen</h1>
  <p class="subtitle">DevOps Metrics Tracker &mdash; Medallion Architecture</p>

  <div class="grid">
    <div class="card">
      <h2>Health</h2>
      <div class="status">
        <div class="dot loading" id="healthDot"></div>
        <span id="healthText">Checking...</span>
      </div>
    </div>
    <div class="card">
      <h2>API</h2>
      <ul class="endpoints">
        <li><span class="method">GET</span> <a href="/health">/health</a></li>
        <li><span class="method post">POST</span> /api/ingest/{source}</li>
        <li><span class="method">GET</span> <a href="/api/v1/openapi.json">/docs (json)</a></li>
      </ul>
    </div>
  </div>

  <div class="card">
    <h2>Test Ingestion</h2>
    <form id="ingestForm">
      <label for="source">Source</label>
      <select id="source">
        <option value="github">github</option>
        <option value="jira">jira</option>
        <option value="aws">aws</option>
        <option value="manual">manual</option>
      </select>
      <label for="payload">Payload (JSON)</label>
      <textarea id="payload" rows="4">{"event": "test", "message": "Hello from Diogen UI"}</textarea>
      <button type="submit" id="sendBtn">Send</button>
      <div class="result" id="result"></div>
    </form>
  </div>
</div>
<script>
(async()=>{
  const dot=document.getElementById('healthDot'),txt=document.getElementById('healthText');
  try{
    const r=await fetch('/health');
    const d=await r.json();
    dot.className='dot '+(d.status==='ok'?'ok':'');
    txt.textContent=d.status==='ok'?'All systems operational':'Degraded';
  }catch(e){
    dot.className='dot';txt.textContent='Unreachable';
  }
})();
document.getElementById('ingestForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('sendBtn'),res=document.getElementById('result');
  const src=document.getElementById('source').value;
  let body;
  try{body=JSON.parse(document.getElementById('payload').value)}catch(err){
    res.className='result show err';res.textContent='Invalid JSON: '+err.message;return;
  }
  btn.disabled=true;btn.textContent='Sending...';
  try{
    const h={'Content-Type':'application/json'};
    const r=await fetch('/api/ingest/'+src,{method:'POST',headers:h,body:JSON.stringify(body)});
    const d=await r.json();
    res.className='result show '+(r.ok?'ok':'err');
    res.textContent=JSON.stringify(d,null,2);
  }catch(err){
    res.className='result show err';res.textContent='Error: '+err.message;
  }
  btn.disabled=false;btn.textContent='Send';
});
</script>
</body>
</html>"""
