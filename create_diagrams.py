import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(base_dir, "screenshot")
os.makedirs(screenshot_dir, exist_ok=True)

# 1. FLOWCHART HTML
flowchart_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #FFFFFF;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1E293B;
    padding: 40px;
    width: 950px;
    margin: 0 auto;
  }
  .header {
    text-align: center;
    margin-bottom: 35px;
  }
  .univ {
    font-size: 14px;
    font-weight: 700;
    color: #800020;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }
  .title {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    margin: 6px 0;
  }
  .subtitle {
    font-size: 14px;
    color: #64748B;
  }
  .flow-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }
  .node {
    width: 320px;
    padding: 14px 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 13.5px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    position: relative;
    z-index: 2;
  }
  .node-start {
    background: #0F172A;
    color: #FFFFFF;
    border-radius: 30px;
    width: 220px;
    font-weight: 700;
    letter-spacing: 1px;
  }
  .node-process {
    background: #F8FAFC;
    border: 2px solid #CBD5E1;
    color: #1E293B;
  }
  .node-auth {
    background: #EFF6FF;
    border: 2px solid #3B82F6;
    color: #1E3A8A;
  }
  .decision {
    width: 220px;
    height: 100px;
    background: #FEF3C7;
    border: 2px solid #F59E0B;
    transform: rotate(45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    z-index: 2;
    margin: 25px 0;
  }
  .decision-inner {
    transform: rotate(-45deg);
    text-align: center;
    font-size: 12px;
    font-weight: 700;
    color: #92400E;
    line-height: 1.3;
    padding: 10px;
  }
  .node-pass {
    background: #ECFDF5;
    border: 2px solid #10B981;
    color: #065F46;
  }
  .node-fail {
    background: #FEF2F2;
    border: 2px solid #EF4444;
    color: #991B1B;
    border-radius: 20px;
    width: 200px;
    padding: 8px 12px;
    font-size: 11.5px;
  }
  .arrow-down {
    width: 2px;
    height: 30px;
    background: #94A3B8;
    position: relative;
  }
  .arrow-down::after {
    content: '';
    position: absolute;
    bottom: -6px;
    left: -4px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #94A3B8;
  }
  .branch-row {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    gap: 60px;
    margin: 10px 0;
  }
  .services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    width: 860px;
    margin: 10px 0;
  }
  .service-card {
    background: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px;
    font-size: 12px;
  }
  .service-card strong {
    display: block;
    color: #0F172A;
    font-size: 13px;
    margin-bottom: 4px;
  }
  .tag {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    margin-top: 4px;
  }
  .tag-auth { background: #DBEAFE; color: #1E40AF; }
  .tag-trip { background: #D1FAE5; color: #065F46; }
  .tag-weather { background: #FEF3C7; color: #92400E; }
</style>
</head>
<body>

<div class="header">
  <div class="univ">ITM Skills University • School of Future Tech</div>
  <div class="title">TripCraft Backend API — Request & Security Flowchart</div>
  <div class="subtitle">Complete Execution Lifecycle from Client Ingestion to Persistence</div>
</div>

<div class="flow-container">
  <!-- START -->
  <div class="node node-start">START: CLIENT REQUEST</div>
  <div class="arrow-down"></div>

  <!-- EXPRESS APP -->
  <div class="node node-process">
    <strong>Express Server & Security Pipeline</strong><br>
    <span style="font-size: 11.5px; color: #64748B;">Port 8000 • Helmet Hardening • CORS • express.json()</span>
  </div>
  <div class="arrow-down"></div>

  <!-- ROUTE DISPATCHER -->
  <div class="node node-process">
    <strong>Express Router Dispatcher</strong><br>
    <span style="font-size: 11.5px; color: #64748B;">Inspects URL: /api/auth, /api/trips, /api/weather</span>
  </div>
  <div class="arrow-down"></div>

  <!-- DECISION 1: PROTECTED ROUTE? -->
  <div class="decision">
    <div class="decision-inner">Protected<br>Route?</div>
  </div>

  <div class="branch-row">
    <!-- YES BRANCH -->
    <div style="display: flex; flex-direction: column; align-items: center;">
      <div style="font-size: 12px; font-weight: 700; color: #16A34A; margin-bottom: 6px;">[ YES: Requires Auth ]</div>
      <div class="node node-auth">
        <strong>authMiddleware Verification</strong><br>
        <span style="font-size: 11.5px;">Validates JWT Bearer Token / Firebase Token</span>
      </div>
    </div>

    <!-- NO BRANCH -->
    <div style="display: flex; flex-direction: column; align-items: center;">
      <div style="font-size: 12px; font-weight: 700; color: #2563EB; margin-bottom: 6px;">[ NO: Public ]</div>
      <div class="node node-process" style="width: 240px;">
        <strong>Public Route Allowed</strong><br>
        <span style="font-size: 11.5px;">Register, Login, Swagger Docs, Weather</span>
      </div>
    </div>
  </div>

  <div class="arrow-down"></div>

  <!-- DECISION 2: TOKEN & VALIDATION VALID? -->
  <div class="decision">
    <div class="decision-inner">Validation &<br>Token Valid?</div>
  </div>

  <div class="branch-row">
    <div class="node node-pass" style="width: 380px;">
      <strong>✓ Passed: User Injected into req.user</strong><br>
      <span style="font-size: 11.5px;">express-validator checks sanitize body & params</span>
    </div>
    <div class="node node-fail">
      <strong>✗ Error Intercepted</strong><br>
      400 Bad Request / 401 Unauthorized
    </div>
  </div>

  <div class="arrow-down"></div>

  <!-- CONTROLLERS LAYER -->
  <div style="font-weight: 800; font-size: 14px; color: #0F172A; margin: 10px 0 6px 0; text-transform: uppercase; letter-spacing: 0.5px;">
    Controller Business Logic Execution Layer
  </div>

  <div class="services-grid">
    <div class="service-card">
      <strong>Auth Controller</strong>
      Bcrypt hash generation (cost 10) & JWT token signing.
      <div><span class="tag tag-auth">POST /register</span> <span class="tag tag-auth">POST /login</span></div>
    </div>

    <div class="service-card">
      <strong>Trip Controller</strong>
      Ownership verification, collaborator sharing & regex search.
      <div><span class="tag tag-trip">CRUD /trips</span> <span class="tag tag-trip">/share</span> <span class="tag tag-trip">/search</span></div>
    </div>

    <div class="service-card">
      <strong>Itinerary Controller</strong>
      Day-by-day scheduling, activity updates, compound indexing.
      <div><span class="tag tag-trip">POST /itinerary</span> <span class="tag tag-trip">GET /itinerary</span></div>
    </div>

    <div class="service-card">
      <strong>Expense & Budget</strong>
      Total spent aggregation, balance deduction, category map.
      <div><span class="tag tag-auth">POST /expenses</span> <span class="tag tag-auth">GET /expenses</span></div>
    </div>

    <div class="service-card">
      <strong>Weather Telemetry</strong>
      Open-Meteo geocoding & live 7-day meteorological forecast.
      <div><span class="tag tag-weather">GET /weather</span> <span class="tag tag-weather">GET /trips/:id/weather</span></div>
    </div>

    <div class="service-card">
      <strong>Media Pipeline</strong>
      Multer memory buffer streaming to Firebase / Local disk.
      <div><span class="tag tag-trip">POST /trips/:id/photos</span></div>
    </div>
  </div>

  <div class="arrow-down"></div>

  <!-- MONGODB PERSISTENCE -->
  <div class="node node-process" style="width: 500px; background: #F1F5F9; border: 2px solid #0F172A;">
    <strong>MongoDB Document Persistence (Mongoose ODM)</strong><br>
    <span style="font-size: 12px; color: #475569;">Atomic Operations • Cascade Itinerary Clean-up • Schema Virtuals</span>
  </div>

  <div class="arrow-down"></div>

  <!-- END RESPONSE -->
  <div class="node node-start" style="background: #16A34A; width: 340px;">
    END: HTTP JSON RESPONSE (200 / 201)
  </div>
</div>

</body>
</html>
"""

# 2. MIND MAP HTML
mindmap_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #FFFFFF;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1E293B;
    padding: 35px 25px;
    width: 1050px;
    margin: 0 auto;
  }
  .header {
    text-align: center;
    margin-bottom: 30px;
  }
  .univ {
    font-size: 13px;
    font-weight: 700;
    color: #800020;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }
  .title {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    margin: 4px 0;
  }
  .subtitle {
    font-size: 13.5px;
    color: #64748B;
  }
  .map-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    padding: 20px 0;
  }
  .center-core {
    background: linear-gradient(135deg, #800020 0%, #4A0012 100%);
    color: #FFFFFF;
    padding: 26px 20px;
    border-radius: 50%;
    width: 220px;
    height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: 0 10px 25px rgba(128, 0, 32, 0.3);
    border: 5px solid #F8FAFC;
    z-index: 10;
  }
  .center-core h2 {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 0.5px;
    line-height: 1.2;
  }
  .center-core span {
    font-size: 11px;
    font-weight: 500;
    color: #FED7D7;
    margin-top: 6px;
  }
  .col {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 360px;
  }
  .branch-card {
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.04);
    position: relative;
    border-left: 5px solid #3B82F6;
  }
  .branch-security { border-left-color: #8B5CF6; }
  .branch-trips { border-left-color: #10B981; }
  .branch-collab { border-left-color: #F59E0B; }
  .branch-storage { border-left-color: #06B6D4; }
  .branch-weather { border-left-color: #EC4899; }
  .branch-devops { border-left-color: #64748B; }

  .branch-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .branch-title {
    font-size: 13.5px;
    font-weight: 700;
    color: #0F172A;
  }
  .badge {
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .badge-purple { background: #EDE9FE; color: #6D28D9; }
  .badge-green { background: #D1FAE5; color: #047857; }
  .badge-amber { background: #FEF3C7; color: #B45309; }
  .badge-cyan { background: #CFFAFE; color: #0E7490; }
  .badge-pink { background: #FCE7F3; color: #BE185D; }
  .badge-gray { background: #F1F5F9; color: #475569; }

  .sub-list {
    list-style: none;
    font-size: 11.5px;
    color: #334155;
    line-height: 1.6;
  }
  .sub-list li {
    position: relative;
    padding-left: 14px;
    margin-bottom: 3px;
  }
  .sub-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #94A3B8;
    font-weight: bold;
    font-size: 14px;
  }
</style>
</head>
<body>

<div class="header">
  <div class="univ">ITM Skills University • School of Future Tech</div>
  <div class="title">TripCraft Backend Architecture Mind Map</div>
  <div class="subtitle">Taxonomy of System Capabilities, Cryptographic Security & RESTful Services</div>
</div>

<div class="map-wrapper">
  <!-- LEFT COLUMN BRANCHES -->
  <div class="col">
    <!-- BRANCH 1: AUTH & SECURITY -->
    <div class="branch-card branch-security">
      <div class="branch-header">
        <div class="branch-title">1. Authentication & Security</div>
        <span class="badge badge-purple">Core Guard</span>
      </div>
      <ul class="sub-list">
        <li><strong>JWT Stateless Bearer Token:</strong> HMAC-SHA256 signature with 7-day expiration.</li>
        <li><strong>Bcrypt Salting & Hashing:</strong> Blowfish key derivation with 10 salt rounds.</li>
        <li><strong>Dual Auth Support:</strong> Native JWT + Firebase Admin ID Token validation.</li>
        <li><strong>OWASP Hardening:</strong> Helmet security headers & CORS policy enforcement.</li>
      </ul>
    </div>

    <!-- BRANCH 2: TRIP & ITINERARY CORE -->
    <div class="branch-card branch-trips">
      <div class="branch-header">
        <div class="branch-title">2. Trip & Itinerary Engine</div>
        <span class="badge badge-green">Resource Hub</span>
      </div>
      <ul class="sub-list">
        <li><strong>Lifecycle Management:</strong> Full CRUD operations (Planning, Ongoing, Completed).</li>
        <li><strong>Day-by-Day Scheduling:</strong> Chronological daily activity timetables.</li>
        <li><strong>Bookings Subdocs:</strong> Flight, hotel, and transport tracking.</li>
        <li><strong>Atomic Cascading Cleanup:</strong> Deleting trip purges all linked itineraries.</li>
      </ul>
    </div>

    <!-- BRANCH 3: COLLABORATION & SEARCH -->
    <div class="branch-card branch-collab">
      <div class="branch-header">
        <div class="branch-title">3. Collaborators & Search</div>
        <span class="badge badge-amber">Multi-User</span>
      </div>
      <ul class="sub-list">
        <li><strong>Role-Based Access Control:</strong> Distinct 'viewer' and 'editor' collaborator roles.</li>
        <li><strong>Partner Invitations:</strong> Email verification & prevention of self-collaboration.</li>
        <li><strong>Multi-Dimensional Search:</strong> Regex scanning titles, cities, countries & activities.</li>
        <li><strong>Route Ordering Optimization:</strong> /search placed before /:id parameter interceptor.</li>
      </ul>
    </div>
  </div>

  <!-- CENTER CORE NODE -->
  <div class="center-core">
    <h2>TripCraft API Core</h2>
    <span>Node.js v22 LTS<br>Express.js 5.x<br>MongoDB 9.x<br>Port 8000</span>
  </div>

  <!-- RIGHT COLUMN BRANCHES -->
  <div class="col">
    <!-- BRANCH 4: BUDGET & FINANCIALS -->
    <div class="branch-card branch-storage">
      <div class="branch-header">
        <div class="branch-title">4. Budget & Expense Tracking</div>
        <span class="badge badge-cyan">Advanced</span>
      </div>
      <ul class="sub-list">
        <li><strong>Budget Ceilings:</strong> Multi-currency allocation (USD, EUR, INR).</li>
        <li><strong>Expense Logging:</strong> Title, cost, category (food, lodging, transit), & payer attribution.</li>
        <li><strong>Automated Computation:</strong> Total spent & remaining balance calculation on-the-fly.</li>
        <li><strong>Category Breakdown:</strong> Functional reduction generating aggregated spending metrics.</li>
      </ul>
    </div>

    <!-- BRANCH 5: METEOROLOGICAL TELEMETRY -->
    <div class="branch-card branch-weather">
      <div class="branch-header">
        <div class="branch-title">5. Weather & Media Services</div>
        <span class="badge badge-pink">External APIs</span>
      </div>
      <ul class="sub-list">
        <li><strong>Open-Meteo REST Client:</strong> Free global geocoding & live weather telemetry.</li>
        <li><strong>7-Day Meteorological Forecast:</strong> Daily temperature extrema & precipitation codes.</li>
        <li><strong>Multer Image Streamer:</strong> Memory buffer processing for cover & memory snapshots.</li>
        <li><strong>Dual Storage Strategy:</strong> Firebase Cloud Storage + automatic local disk fallback.</li>
      </ul>
    </div>

    <!-- BRANCH 6: DEVOPS & DOCUMENTATION -->
    <div class="branch-card branch-devops">
      <div class="branch-header">
        <div class="branch-title">6. Documentation & DevOps</div>
        <span class="badge badge-gray">Deployment</span>
      </div>
      <ul class="sub-list">
        <li><strong>OpenAPI 3.0 Swagger UI:</strong> Live interactive browser testing at <code>/api-docs</code>.</li>
        <li><strong>Postman Collection (v2.1):</strong> Pre-configured tests with automatic token persistence.</li>
        <li><strong>Docker Containerization:</strong> Alpine-based lightweight production container.</li>
        <li><strong>Cloud Blueprints:</strong> Render (render.yaml) & Heroku (Procfile) deployment configs.</li>
      </ul>
    </div>
  </div>
</div>

</body>
</html>
"""

flowchart_html_path = os.path.join(base_dir, "temp_flowchart.html")
mindmap_html_path = os.path.join(base_dir, "temp_mindmap.html")

with open(flowchart_html_path, "w", encoding="utf-8") as f:
    f.write(flowchart_html)
with open(mindmap_html_path, "w", encoding="utf-8") as f:
    f.write(mindmap_html)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
flowchart_png = os.path.join(screenshot_dir, "tripcraft_flowchart.png")
mindmap_png = os.path.join(screenshot_dir, "tripcraft_mindmap.png")

print("Rendering TripCraft Flowchart image...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--screenshot={flowchart_png}",
    "--window-size=1000,1500",
    flowchart_html_path
], check=True)

print("Rendering TripCraft Mind Map image...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--screenshot={mindmap_png}",
    "--window-size=1150,1100",
    mindmap_html_path
], check=True)

print(f"Flowchart saved at: {flowchart_png} ({os.path.getsize(flowchart_png)} bytes)")
print(f"Mind map saved at: {mindmap_png} ({os.path.getsize(mindmap_png)} bytes)")

# Cleanup temporary html files
if os.path.exists(flowchart_html_path): os.remove(flowchart_html_path)
if os.path.exists(mindmap_html_path): os.remove(mindmap_html_path)
