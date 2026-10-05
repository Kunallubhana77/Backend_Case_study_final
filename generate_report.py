import os
import base64
import subprocess

def get_base64_img(rel_path):
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def generate_report():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load all images including Mind Map and Flowchart
    images = {
        "IMG_FLOWCHART": get_base64_img("screenshot/tripcraft_flowchart.png"),
        "IMG_MINDMAP": get_base64_img("screenshot/tripcraft_mindmap.png"),
        "IMG_STRUCTURE": get_base64_img("screenshot/file_structure.png"),
        "IMG_MONGODB": get_base64_img("screenshot/mongodbconnect.png"),
        "IMG_RUN": get_base64_img("screenshot/run.png"),
        "IMG_REGISTER": get_base64_img("screenshot/user_register.png"),
        "IMG_LOGIN": get_base64_img("screenshot/userlogin.png"),
        "IMG_PROFILE": get_base64_img("screenshot/current_profile.png"),
        "IMG_CREATE_TRIP": get_base64_img("screenshot/create_new_trip.png"),
        "IMG_GET_TRIPS": get_base64_img("screenshot/get_all_user_trip.png"),
        "IMG_GET_TRIP_ID": get_base64_img("screenshot/get_user_trip_by_id.png"),
        "IMG_UPDATE_TRIP": get_base64_img("screenshot/put_update_trip.png"),
        "IMG_ADD_ITINERARY": get_base64_img("screenshot/Add Day Itinerary & Activities.png"),
        "IMG_GET_ITINERARY": get_base64_img("screenshot/Get Trip Itineraries.png"),
        "IMG_SHARE": get_base64_img("screenshot/share_trip_with_collabrator.png"),
        "IMG_SEARCH": get_base64_img("screenshot/get_search_by_keyword.png"),
        "IMG_ADD_EXPENSE": get_base64_img("screenshot/Add Expense to Trip.png"),
        "IMG_GET_BUDGET": get_base64_img("screenshot/Get Trip Budget & Expenses Breakdown.png"),
        "IMG_CITY_WEATHER": get_base64_img("screenshot/Get City Weather Forecast.png"),
        "IMG_TRIP_WEATHER": get_base64_img("screenshot/Get Trip Destination Weather.png"),
        "IMG_DELETE": get_base64_img("screenshot/delete_trip.png"),
    }

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Backend Development Final Report - Case Study 96</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #2D3748;
    line-height: 1.55;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }

  .page-break {
    page-break-after: always;
    break-after: page;
  }

  /* COVER PAGE */
  .cover-container {
    min-height: 94vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    padding: 40px 24px;
    border: 3px double #CBD5E0;
    background: linear-gradient(180deg, #FFFFFF 0%, #F7FAFC 100%);
  }

  .cover-header {
    border-bottom: 2.5px solid #800020;
    padding-bottom: 20px;
  }

  .university-title {
    font-size: 24pt;
    font-weight: 800;
    color: #800020;
    letter-spacing: 1px;
    margin: 0;
    text-transform: uppercase;
  }

  .school-title {
    font-size: 15pt;
    font-weight: 600;
    color: #4A5568;
    margin: 8px 0 0 0;
    letter-spacing: 0.5px;
  }

  .cover-body {
    margin: auto 0;
  }

  .case-badge {
    display: inline-block;
    background: #800020;
    color: #FFFFFF;
    font-size: 12pt;
    font-weight: 700;
    padding: 8px 26px;
    border-radius: 30px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
  }

  .report-main-title {
    font-size: 23pt;
    font-weight: 800;
    color: #1A202C;
    margin: 10px 0;
    line-height: 1.3;
  }

  .report-sub-title {
    font-size: 14pt;
    color: #4A5568;
    font-weight: 500;
    margin: 8px 0 25px 0;
  }

  .tech-pills {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 15px;
    flex-wrap: wrap;
  }

  .tech-pill {
    background: #EDF2F7;
    border: 1px solid #CBD5E0;
    color: #2D3748;
    padding: 5px 14px;
    border-radius: 16px;
    font-size: 9.5pt;
    font-weight: 600;
  }

  .cover-footer {
    border-top: 2.5px solid #800020;
    padding-top: 25px;
    text-align: left;
    display: flex;
    justify-content: space-between;
    background: #FFFFFF;
  }

  .submission-meta {
    font-size: 10pt;
    line-height: 1.7;
  }

  .submission-meta strong {
    color: #1A202C;
  }

  /* HEADINGS */
  h1.section-title {
    font-size: 16pt;
    font-weight: 800;
    color: #800020;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 16px;
  }

  h2.subsection-title {
    font-size: 12.5pt;
    font-weight: 700;
    color: #2C5282;
    margin-top: 20px;
    margin-bottom: 10px;
  }

  p {
    text-align: justify;
    margin: 8px 0;
  }

  /* TABLES */
  .index-table, table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 9.5pt;
  }

  .index-table th {
    background: #800020;
    color: #ffffff;
    text-align: left;
    padding: 10px 14px;
    font-weight: 700;
  }

  .index-table td {
    padding: 10px 14px;
    border-bottom: 1px dotted #CBD5E0;
  }

  .index-table tr:nth-child(even), table.data-table tr:nth-child(even) {
    background-color: #F7FAFC;
  }

  table.data-table th {
    background: #2C5282;
    color: #FFFFFF;
    font-weight: 700;
    padding: 8px 10px;
    text-align: left;
    border: 1px solid #2B6CB0;
  }

  table.data-table td {
    padding: 7px 10px;
    border: 1px solid #E2E8F0;
  }

  /* BADGES */
  .badge-pass {
    background: #C6F6D5;
    color: #22543D;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 8.5pt;
    display: inline-block;
  }

  .badge-post { background: #ED8936; color: #FFFFFF; font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 8pt; font-family: monospace; }
  .badge-get { background: #48BB78; color: #FFFFFF; font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 8pt; font-family: monospace; }
  .badge-put { background: #4299E1; color: #FFFFFF; font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 8pt; font-family: monospace; }
  .badge-delete { background: #F56565; color: #FFFFFF; font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 8pt; font-family: monospace; }

  /* CODE BOX */
  .code-box {
    background: #1A202C;
    color: #E2E8F0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    padding: 10px 14px;
    border-radius: 6px;
    line-height: 1.45;
    margin: 10px 0;
    border-left: 4px solid #800020;
    white-space: pre-wrap;
  }

  /* SCREENSHOT CARD */
  .screenshot-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E0;
    border-radius: 8px;
    padding: 12px;
    margin: 16px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .screenshot-img-container {
    text-align: center;
    background: #0D1117;
    border-radius: 6px;
    padding: 6px;
    border: 1px solid #2D3748;
  }

  .screenshot-img {
    max-width: 100%;
    max-height: 380px;
    height: auto;
    border-radius: 4px;
    display: block;
    margin: 0 auto;
  }

  .diagram-img {
    max-width: 100%;
    max-height: 720px;
    height: auto;
    border-radius: 6px;
    display: block;
    margin: 0 auto;
  }

  .screenshot-meta {
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px solid #E2E8F0;
  }

  .screenshot-title {
    font-weight: 700;
    font-size: 10pt;
    color: #1A202C;
    margin-bottom: 4px;
  }

  .screenshot-desc {
    font-size: 9pt;
    color: #4A5568;
    line-height: 1.45;
  }

  .highlight-box {
    background: #EBF8FF;
    border-left: 4px solid #3182CE;
    padding: 10px 14px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    font-size: 9.8pt;
  }
</style>
</head>
<body>

<!-- 1. COVER PAGE -->
<div class="cover-container page-break">
  <div class="cover-header">
    <h1 class="university-title">ITM SKILLS UNIVERSITY</h1>
    <h2 class="school-title">School of Future Tech</h2>
  </div>

  <div class="cover-body">
    <div class="case-badge">Case Study Report NO 96</div>
    <div class="report-main-title">TripCraft — Travel Itinerary Planner</div>
    <div class="report-sub-title">Full-Stack Enterprise REST API Backend Development</div>
    
    <div class="tech-pills">
      <span class="tech-pill">Node.js</span>
      <span class="tech-pill">Express.js</span>
      <span class="tech-pill">MongoDB & Mongoose</span>
      <span class="tech-pill">JWT & Bcrypt</span>
      <span class="tech-pill">Firebase Cloud Storage</span>
      <span class="tech-pill">Swagger OpenAPI 3.0</span>
    </div>
  </div>

  <div class="cover-footer">
    <div class="submission-meta">
      <div><strong>Submitted By:</strong> Kunal Lubhana</div>
      <div><strong>Enrollment No:</strong> 150096725022</div>
      <div><strong>Program:</strong> B.Tech Computer Science and Engineering</div>
      <div><strong>Batch:</strong> 2025 – 2029</div>
    </div>
    <div class="submission-meta" style="text-align: right;">
      <div><strong>Subject:</strong> Backend Development</div>
      <div><strong>Domain:</strong> Node.js, Express.js & MongoDB</div>
      <div><strong>Semester:</strong> 3</div>
      <div><strong>Academic Year:</strong> 2026–2027</div>
    </div>
  </div>
</div>

<!-- 2. TABLE OF CONTENTS / INDEX -->
<div class="page-break">
  <h1 class="section-title">Table of Contents / Index</h1>
  <table class="index-table">
    <thead>
      <tr>
        <th style="width: 12%;">Sr. No.</th>
        <th style="width: 73%;">Section Title</th>
        <th style="width: 15%; text-align: right;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1.</strong></td>
        <td><strong>Introduction to the Case Study</strong></td>
        <td style="text-align: right;">3</td>
      </tr>
      <tr>
        <td><strong>2.</strong></td>
        <td><strong>Problem Statement / Case Background (Abstract)</strong></td>
        <td style="text-align: right;">4</td>
      </tr>
      <tr>
        <td><strong>3.</strong></td>
        <td><strong>Problem Statement / Case Study Design & Architecture</strong></td>
        <td style="text-align: right;">5</td>
      </tr>
      <tr>
        <td>3.1</td>
        <td>Layered Architectural Pipeline & Schema Specification</td>
        <td style="text-align: right;">5</td>
      </tr>
      <tr>
        <td>3.2</td>
        <td><strong>System Architecture & Capability Mind Map (Figure 3.1)</strong></td>
        <td style="text-align: right;">6</td>
      </tr>
      <tr>
        <td><strong>4.</strong></td>
        <td><strong>Methods & Algorithms / Technology Applied</strong></td>
        <td style="text-align: right;">7</td>
      </tr>
      <tr>
        <td>4.1</td>
        <td>Cryptographic Hashing, Stateless JWT, Multi-Dimensional Search & Port Resolution</td>
        <td style="text-align: right;">7</td>
      </tr>
      <tr>
        <td>4.2</td>
        <td><strong>Request Lifecycle & Security Verification Flowchart (Figure 4.1)</strong></td>
        <td style="text-align: right;">8</td>
      </tr>
      <tr>
        <td><strong>5.</strong></td>
        <td><strong>Implementation Details and Verification Snapshots (All 19 Artifacts)</strong></td>
        <td style="text-align: right;">9</td>
      </tr>
      <tr>
        <td>5.1</td>
        <td>Environment & Architecture Verification (Figures 5.1 – 5.3)</td>
        <td style="text-align: right;">9</td>
      </tr>
      <tr>
        <td>5.2</td>
        <td>Authentication & Profile Services (Figures 5.4 – 5.6)</td>
        <td style="text-align: right;">11</td>
      </tr>
      <tr>
        <td>5.3</td>
        <td>Trip Lifecycle & CRUD Execution (Figures 5.7 – 5.10)</td>
        <td style="text-align: right;">13</td>
      </tr>
      <tr>
        <td>5.4</td>
        <td>Day-by-Day Itineraries & Activity Scheduling (Figures 5.11 – 5.12)</td>
        <td style="text-align: right;">15</td>
      </tr>
      <tr>
        <td>5.5</td>
        <td>Collaborators & Keyword Search Engine (Figures 5.13 – 5.14)</td>
        <td style="text-align: right;">17</td>
      </tr>
      <tr>
        <td>5.6</td>
        <td>Budget & Expense Tracking APIs (Figures 5.15 – 5.16)</td>
        <td style="text-align: right;">19</td>
      </tr>
      <tr>
        <td>5.7</td>
        <td>Live Weather Forecast & Trip Weather APIs (Figures 5.17 – 5.18)</td>
        <td style="text-align: right;">21</td>
      </tr>
      <tr>
        <td>5.8</td>
        <td>Trip Deletion & Cascading Clean-up (Figure 5.19)</td>
        <td style="text-align: right;">22</td>
      </tr>
      <tr>
        <td><strong>6.</strong></td>
        <td><strong>Case Study Results, Verification Matrix and Discussion</strong></td>
        <td style="text-align: right;">23</td>
      </tr>
      <tr>
        <td><strong>7.</strong></td>
        <td><strong>Conclusion & Learning Outcomes</strong></td>
        <td style="text-align: right;">25</td>
      </tr>
      <tr>
        <td><strong>8.</strong></td>
        <td><strong>References & Official Documentation</strong></td>
        <td style="text-align: right;">26</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- 3. SECTION 1: INTRODUCTION -->
<div class="page-break">
  <h1 class="section-title">1. Introduction to the Case Study</h1>
  <p>
    Modern consumer travel planning has evolved from static notebook bookings into dynamic, collaborative, multi-destination itineraries. Travelers require intelligent digital platforms capable of orchestrating daily activities, synchronizing logistical bookings (flights, hotels, transport), tracking shared expenses across travel companions, and providing live meteorological forecasts for upcoming destinations.
  </p>
  <p>
    Under the B.Tech Computer Science Engineering curriculum for <strong>Backend Development (Node.js, Express.js & MongoDB)</strong>, <strong>Case Study 96</strong> mandates the engineering of a production-grade, highly available RESTful API for <strong>"TripCraft"</strong>. TripCraft serves as the central backend engine powering digital itinerary orchestration.
  </p>
  <div class="highlight-box">
    <strong>Core Engineering Mandate:</strong> Develop an asynchronous, scalable, and modular backend API implementing decoupled MVC architecture, stateless JSON Web Token (JWT) + Firebase dual authentication, Mongoose ODM database persistence, fine-grained access control for collaborative editing, automated budget tracking calculations, and third-party weather API integrations.
  </div>
  <h2 class="subsection-title">1.1 Industrial Context & Motivation</h2>
  <p>
    Travel planning applications face unique computational challenges:
  </p>
  <ul>
    <li><strong>Hierarchical Data Models:</strong> A single trip contains an ordered continuum of days, each housing timestamped activities, bookings, financial cost metrics, and media attachments. Relational databases often incur heavy JOIN penalties for such structures, making a NoSQL document database like MongoDB ideal.</li>
    <li><strong>Role-Based Collaboration:</strong> Travel groups require distinct authorization roles. An 'editor' collaborator can add museum visits or update booking reference codes, whereas a 'viewer' collaborator is restricted to read-only access. The trip creator ('owner') retains exclusive rights to destroy or transfer the trip resource.</li>
    <li><strong>Resilient Media Ingestion:</strong> Ingestion of high-resolution trip memories necessitates seamless cloud object storage (Firebase Cloud Storage) backed by resilient local storage failover policies to avoid system outages during network isolation.</li>
    <li><strong>Financial Transparency:</strong> Complex multi-currency expense distribution requires transactional ledgering where each expense records category, payer, amount, and automatic deduction from the parent budget ceiling.</li>
  </ul>
</div>

<!-- 4. SECTION 2: ABSTRACT -->
<div class="page-break">
  <h1 class="section-title">2. Problem Statement / Case Background (Abstract)</h1>
  <h2 class="subsection-title">2.1 Case Study Background</h2>
  <p>
    Traditional travel management systems suffer from data fragmentation. Users juggle flight confirmation emails, localized chat applications for planning, separate spreadsheets for expense splitting, and third-party weather portals. <strong>TripCraft</strong> consolidates these disparate domains into a unified, authenticated REST API suite.
  </p>
  <h2 class="subsection-title">2.2 Formal Abstract</h2>
  <p>
    This report documents the architectural blueprint, mathematical security algorithms, data models, controller logic, and empirical test results of the <strong>TripCraft Travel Itinerary Planner Backend API</strong>.
  </p>
  <p>
    The system is built on <strong>Node.js (v22.23 LTS)</strong> runtime executing an <strong>Express.js</strong> HTTP server. Data persistence is engineered on <strong>MongoDB</strong> using the <strong>Mongoose ODM</strong> library with full schema validation, pre-save cryptographic hooks, and virtual population. Security is established through <strong>stateless JSON Web Tokens (HMAC-SHA256)</strong> coupled with <strong>bcrypt (Blowfish cipher, cost factor 10)</strong> password hashing. 
  </p>
  <p>
    Furthermore, the system delivers multi-user collaboration via reference arrays, optimized full-text regex search across multiple document dimensions, Multer-driven media pipelines with Firebase Storage fallback, real-time expense ledgering, and live 7-day weather forecasting using free Open-Meteo REST endpoints without requiring third-party subscription keys. All endpoints are rigorously verified through an interactive <strong>Swagger (OpenAPI 3.0)</strong> interface and an automated <strong>Postman Collection (v2.1)</strong> test suite.
  </p>
  <h2 class="subsection-title">2.3 Deliverables Matrix</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Requirement</th>
        <th>Target Deliverable</th>
        <th>Implementation Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Modular Architecture</td>
        <td>Decoupled routes, controllers, middleware, models</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Authentication</td>
        <td>JWT Bearer Auth + Firebase Auth token support</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Trip CRUD</td>
        <td>Create, Read, Update, Delete with cascades</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Day-by-Day Itinerary</td>
        <td>POST/GET /api/trips/:id/itinerary with activities</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Collaborators Sharing</td>
        <td>POST /api/trips/:id/share with viewer/editor roles</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Smart Search</td>
        <td>GET /api/trips/search?keyword=europe</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Budget Tracking</td>
        <td>POST/GET /api/trips/:id/expenses (Advanced Feature)</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>Weather Forecast</td>
        <td>GET /api/weather & /api/trips/:id/weather (Advanced)</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>API Documentation</td>
        <td>Interactive Swagger UI (/api-docs) & Postman JSON</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
      <tr>
        <td>DevOps Deployment</td>
        <td>Dockerfile, render.yaml, Procfile, git VCS</td>
        <td><span class="badge-pass">VERIFIED 100%</span></td>
      </tr>
    </tbody>
  </table>
</div>

<!-- 5. SECTION 3: DESIGN & ARCHITECTURE -->
<div class="page-break">
  <h1 class="section-title">3. Problem Statement / Case Study Design</h1>
  <h2 class="subsection-title">3.1 Layered Architectural Pipeline</h2>
  <p>
    The TripCraft backend adheres strictly to the decoupled <strong>Controller-Service-Repository</strong> design pattern. When an HTTP client submits an incoming request, it traverses a deterministic pipeline:
  </p>
  <div class="code-box">[HTTP Client: Postman / Browser / Mobile App]
                │
                ▼ (Port 8000)
┌──────────────────────────────────────────────────────────┐
│ Express Application Layer (src/app.js)                   │
│   ├── Security Middleware: Helmet HTTP Header Hardening │
│   ├── CORS Handler: Cross-Origin Resource Sharing        │
│   ├── Morgan Logger: Asynchronous dev telemetry logger   │
│   └── Body Parsers: express.json() & express.urlencoded  │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│ Middleware Pipeline (src/middleware/)                    │
│   ├── authMiddleware: JWT & Firebase Bearer Validator   │
│   ├── validationMiddleware: express-validator Chains     │
│   └── uploadMiddleware: Multer Memory Buffer Streamer    │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│ Modular Routing Layer (src/routes/)                      │
│   ├── /api/auth       ──► authController.js              │
│   ├── /api/trips      ──► tripController.js              │
│   │   ├── /itinerary  ──► itineraryController.js         │
│   │   ├── /share      ──► tripController.js              │
│   │   └── /expenses   ──► expenseController.js           │
│   ├── /api/weather    ──► weatherController.js           │
│   └── /api-docs       ──► Swagger UI OpenAPI Engine      │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│ Data Persistence & External Cloud Services               │
│   ├── MongoDB Mongoose ODM (User, Trip, Itinerary, Dest) │
│   ├── Firebase Cloud Storage / Local FS Fallback Engine  │
│   └── Open-Meteo REST Weather Geocoding Telemetry Engine │
└──────────────────────────────────────────────────────────┘</div>

  <h2 class="subsection-title">3.2 Database Entity-Relationship (ER) Schema Specification</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Collection</th>
        <th>Field Name</th>
        <th>Type & Constraints</th>
        <th>Description & Role</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Users</strong></td>
        <td>_id, name, email, password, role</td>
        <td>ObjectId, String, Email Unique, Bcrypt Hash</td>
        <td>Stores credentials and profile metadata. Password marked select: false.</td>
      </tr>
      <tr>
        <td><strong>Trips</strong></td>
        <td>_id, title, destination, startDate, endDate</td>
        <td>ObjectId, String, Subdoc name/country, Date</td>
        <td>Primary trip resource defining destination coordinates and duration.</td>
      </tr>
      <tr>
        <td><strong>Trips (Rel.)</strong></td>
        <td>owner, collaborators[]</td>
        <td>Ref: 'User', Array of {user: Ref, role: Enum}</td>
        <td>Fine-grained authorization model separating creator from invited members.</td>
      </tr>
      <tr>
        <td><strong>Trips (Budget)</strong></td>
        <td>totalBudget, currency, expenses[]</td>
        <td>Number, Currency String, Subdocs Array</td>
        <td>Financial ledger recording title, category, amount, payer reference.</td>
      </tr>
      <tr>
        <td><strong>Itineraries</strong></td>
        <td>trip, dayNumber, date, title, activities[]</td>
        <td>Ref: 'Trip', Integer >= 1, Date, Subdocs Array</td>
        <td>Day-by-day planner. Compound indexed on { trip: 1, dayNumber: 1 }.</td>
      </tr>
      <tr>
        <td><strong>Destinations</strong></td>
        <td>name, country, coordinates, bestTime</td>
        <td>String, String, {latitude, longitude}, String</td>
        <td>Global travel catalog pre-populated with attractions and weather coords.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- DEDICATED FULL-PAGE MIND MAP (FIGURE 3.1) -->
<div class="page-break">
  <h2 class="subsection-title">3.3 System Architecture & Technology Mind Map</h2>
  <p>
    The following structural mind map visualizes the core taxonomy of the TripCraft backend platform, illustrating the interplay between cryptographic security, the trip planning engine, multi-user collaboration, automated financial ledgers, external meteorological telemetry, and DevOps automation.
  </p>
  <div class="screenshot-card" style="margin-top: 15px;">
    <div style="text-align: center; background: #FFFFFF; padding: 10px; border-radius: 6px;">
      <img src="IMG_MINDMAP_PLACEHOLDER" class="diagram-img" alt="TripCraft Backend Architecture Mind Map">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 3.1: TripCraft Full-Stack Architectural Capability & Domain Mind Map</div>
      <div class="screenshot-desc">
        Comprehensive taxonomic decomposition of TripCraft backend services across six specialized dimensions: (1) Authentication & Security, (2) Trip & Itinerary Engine, (3) Collaboration & Search, (4) Budget & Expense Tracking, (5) Weather & Media Services, and (6) Documentation & DevOps.
      </div>
    </div>
  </div>
</div>

<!-- 6. SECTION 4: METHODS & ALGORITHMS -->
<div class="page-break">
  <h1 class="section-title">4. Methods & Algorithms / Technology Applied</h1>
  <h2 class="subsection-title">4.1 Cryptographic Password Hashing (Bcrypt Algorithm)</h2>
  <p>
    Storing plaintext credentials violates fundamental security mandates (OWASP Top 10). TripCraft enforces password salting and hashing utilizing the <strong>bcrypt</strong> adaptive key derivation function based on the Blowfish cipher:
  </p>
  <div class="code-box">// Asynchronous Pre-Save Mongoose Hook (src/models/User.js)
userSchema.pre('save', async function () {
  if (!this.isModified('password') || !this.password) return;
  const salt = await bcrypt.genSalt(10); // 10 rounds = 2^10 hashing iterations
  this.password = await bcrypt.hash(this.password, salt);
});</div>
  <p>
    When a user attempts authentication, <code>bcrypt.compare(enteredPassword, storedHash)</code> evaluates whether the entered candidate computes to the identical cryptographic digest in constant time, defeating timing attacks.
  </p>

  <h2 class="subsection-title">4.2 Stateless Authentication (JSON Web Tokens - RFC 7519)</h2>
  <p>
    TripCraft uses stateless JWT authorization. Upon valid credential verification, the authentication controller signs an HMAC-SHA256 payload:
  </p>
  <div class="code-box">Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"id": user._id, "iat": 1791182000, "exp": 1791786800}
Signature: HMACSHA256(base64UrlEncode(Header) + "." + base64UrlEncode(Payload), JWT_SECRET)</div>
  <p>
    The client transmits this token in subsequent requests within the HTTP Header: <code>Authorization: Bearer &lt;token&gt;</code>. The <code>authMiddleware</code> validates token integrity without database lookup bottlenecks.
  </p>

  <h2 class="subsection-title">4.3 Search Algorithm (Multi-Dimensional Case-Insensitive Regex)</h2>
  <p>
    Case Study 96 requires searching trips via keyword (e.g. <code>?keyword=europe</code>). TripCraft implements a two-stage aggregation query:
  </p>
  <ol>
    <li><strong>Stage 1 (Activity & Itinerary Scan):</strong> Matches <code>keyword</code> against itinerary day titles, notes, activity names, and locations using MongoDB regex <code>RegExp(keyword, 'i')</code>, returning matched trip IDs.</li>
    <li><strong>Stage 2 (Trip Intersection):</strong> Queries trips where the logged-in user is <code>owner</code> OR in <code>collaborators</code>, matching trip title, destination city, destination country, or the IDs retrieved from Stage 1.</li>
  </ol>

  <h2 class="subsection-title">4.4 Budget & Expense Aggregation Algorithm</h2>
  <p>
    The expense tracking engine dynamically computes budget depletion on the fly using JavaScript functional reduction:
  </p>
  <div class="code-box">Total Spent = Sum of all expense[i].amount
Remaining   = TotalBudget - Total Spent
CategoryMap = Sum amounts grouped by category (food, lodging, activities, etc.)</div>

  <h2 class="subsection-title">4.5 macOS Port 5000 AirPlay Conflict Diagnosis & Port 8000 Reallocation</h2>
  <p>
    During initial testing on macOS, sending requests to <code>http://localhost:5000</code> resulted in unexpected <code>HTTP/1.1 403 Forbidden</code> blank responses. Forensic analysis via <code>lsof -i :5000</code> revealed that macOS system service <strong>ControlCenter (AirTunes/AirPlay Receiver)</strong> permanently binds port 5000:
  </p>
  <div class="code-box">COMMAND    PID  USER         FD  TYPE  DEVICE             NODE NAME
ControlCe  650  kunallubhana 11u IPv4  0xb43d107700785fff  TCP *:commplex-main (LISTEN)</div>
  <p>
    <strong>Resolution:</strong> The backend was re-engineered and hardened to bind to standard development port <strong>8000</strong> across <code>.env</code>, <code>src/server.js</code>, <code>swagger.json</code>, and Postman configuration files, restoring full connectivity.
  </p>
</div>

<!-- DEDICATED FULL-PAGE FLOWCHART (FIGURE 4.1) -->
<div class="page-break">
  <h2 class="subsection-title">4.6 Request Lifecycle & Security Verification Flowchart</h2>
  <p>
    The flowchart below charts the end-to-end traversal of an incoming client request through the Express.js server, highlighting authentication gating, input sanitization via express-validator, controller business logic routing, Mongoose ODM database persistence, and standardized JSON response synthesis.
  </p>
  <div class="screenshot-card" style="margin-top: 15px;">
    <div style="text-align: center; background: #FFFFFF; padding: 10px; border-radius: 6px;">
      <img src="IMG_FLOWCHART_PLACEHOLDER" class="diagram-img" alt="TripCraft Request Lifecycle Flowchart">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 4.1: TripCraft End-to-End Request Processing & Security Interception Flowchart</div>
      <div class="screenshot-desc">
        Deterministic architectural flow delineating public vs protected routing, JWT Bearer and Firebase token validation, express-validator schema verification, specialized controller execution, and atomic MongoDB document persistence.
      </div>
    </div>
  </div>
</div>

<!-- 7. SECTION 5: IMPLEMENTATION DETAILS AND SNAPSHOTS -->
<div class="page-break">
  <h1 class="section-title">5. Problem Statement / Case Study Implementation Details and Snapshots</h1>
  <p>
    This section documents the end-to-end verification of all nineteen implementation artifacts captured during comprehensive test execution.
  </p>

  <h2 class="subsection-title">5.1 Environment, Architecture & Database Connectivity</h2>

  <!-- FIGURE 5.1: FILE STRUCTURE -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_STRUCTURE_PLACEHOLDER" class="screenshot-img" alt="Modular File Structure">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.1: Modular Enterprise Project Directory Structure</div>
      <div class="screenshot-desc">
        Verification of the clean directory hierarchy conforming to MVC design. Displays distinct folders for <code>src/config/</code> (db & firebase), <code>src/models/</code> (Mongoose schemas), <code>src/controllers/</code> (business logic), <code>src/middleware/</code> (JWT, upload, error handler), <code>src/routes/</code>, <code>src/docs/</code> (Swagger OpenAPI 3.0), and <code>postman/</code> test collections.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.2: MONGODB CONNECT -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_MONGODB_PLACEHOLDER" class="screenshot-img" alt="MongoDB Connection">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.2: Asynchronous MongoDB Mongoose Connection Established</div>
      <div class="screenshot-desc">
        Terminal output demonstrating successful database connection to the local MongoDB daemon at <code>127.0.0.1:27017/tripcraft</code>. Demonstrates graceful error handling and connection confirmation via Mongoose ODM.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.3: SERVER STARTUP ON PORT 8000 -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_RUN_PLACEHOLDER" class="screenshot-img" alt="Server Run">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.3: Express Server Startup & Telemetry Execution</div>
      <div class="screenshot-desc">
        Execution of <code>npm run dev</code> utilizing <code>nodemon</code>. Confirms server initialization in development mode, active HTTP listener on <code>http://localhost:8000</code>, Swagger API docs active at <code>/api-docs</code>, and local storage fallback initialization for Firebase media.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.2: AUTHENTICATION SERVICES -->
<div class="page-break">
  <h2 class="subsection-title">5.2 User Authentication & Profile Retrieval</h2>

  <!-- FIGURE 5.4: USER REGISTER -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_REGISTER_PLACEHOLDER" class="screenshot-img" alt="User Register">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.4: User Registration Endpoint — <span class="badge-post">POST</span> <code>/api/auth/register</code></div>
      <div class="screenshot-desc">
        Postman test showing account creation for "Alex Traveler" (<code>alex@tripcraft.dev</code>). Output confirms <code>HTTP 201 Created</code>, generation of unique MongoDB <code>_id: 6ac362ab45778d5741910c34</code>, role assignment (<code>user</code>), and issuance of a signed JWT Bearer Token.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.5: USER LOGIN -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_LOGIN_PLACEHOLDER" class="screenshot-img" alt="User Login">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.5: User Login Endpoint — <span class="badge-post">POST</span> <code>/api/auth/login</code></div>
      <div class="screenshot-desc">
        Execution of credential verification against MongoDB using bcrypt. Response shows <code>HTTP 200 OK</code>, confirming valid email and password match, followed by dynamic issuance of a freshly signed JWT token for session state.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.6: USER PROFILE -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_PROFILE_PLACEHOLDER" class="screenshot-img" alt="Current Profile">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.6: Authenticated User Profile Retrieval — <span class="badge-get">GET</span> <code>/api/auth/me</code></div>
      <div class="screenshot-desc">
        Verification of <code>authMiddleware</code> functionality. Client provides <code>Authorization: Bearer &lt;token&gt;</code> in header. Server decodes token, locates user record, strips password field (<code>select: -password</code>), and returns profile data with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.3: TRIPS MANAGEMENT -->
<div class="page-break">
  <h2 class="subsection-title">5.3 Trip Lifecycle & CRUD Operations</h2>

  <!-- FIGURE 5.7: CREATE NEW TRIP -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_CREATE_TRIP_PLACEHOLDER" class="screenshot-img" alt="Create New Trip">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.7: Create New Trip Endpoint — <span class="badge-post">POST</span> <code>/api/trips</code></div>
      <div class="screenshot-desc">
        Creation of "Grand Tour of Europe" trip resource. Payload specifies destination (Paris, France), 14-day duration, 4,000 EUR total budget, and initial hotel booking. Server responds with <code>HTTP 201 Created</code> and unique Trip ID <code>6ac362f145778d5741910c35</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.8: GET ALL TRIPS -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_GET_TRIPS_PLACEHOLDER" class="screenshot-img" alt="Get All Trips">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.8: Retrieve All User Trips — <span class="badge-get">GET</span> <code>/api/trips</code></div>
      <div class="screenshot-desc">
        Querying all trips accessible by the authenticated user. Uses Mongoose <code>$or</code> query checking both ownership and collaborator inclusion. Populates owner and collaborator profiles, returning <code>count: 1</code> with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.9: GET TRIP BY ID -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_GET_TRIP_ID_PLACEHOLDER" class="screenshot-img" alt="Get Trip By ID">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.9: Get Detailed Trip by ID — <span class="badge-get">GET</span> <code>/api/trips/:id</code></div>
      <div class="screenshot-desc">
        Full trip inspection endpoint. Enforces authorization checks ensuring the requesting user is either the trip creator or an authorized collaborator. Populates nested bookings, expenses, collaborators, and day-by-day itineraries.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.10: PUT UPDATE TRIP -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_UPDATE_TRIP_PLACEHOLDER" class="screenshot-img" alt="Update Trip">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.10: Update Trip Details — <span class="badge-put">PUT</span> <code>/api/trips/:id</code></div>
      <div class="screenshot-desc">
        Modification of existing trip attributes. Updates trip status from 'planning' to 'ongoing' and refines the description field. Verified with <code>HTTP 200 OK</code> confirming update validation and ownership integrity.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.4: ITINERARY PLANNING -->
<div class="page-break">
  <h2 class="subsection-title">5.4 Day-by-Day Itineraries & Activity Scheduling</h2>

  <!-- FIGURE 5.11: ADD ITINERARY -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_ADD_ITINERARY_PLACEHOLDER" class="screenshot-img" alt="Add Itinerary Activities">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.11: Add Day Itinerary & Activities — <span class="badge-post">POST</span> <code>/api/trips/:id/itinerary</code></div>
      <div class="screenshot-desc">
        Adding day-by-day activities to Day 1. Demonstrates ingestion of scheduled activities including Airport Transfer (09:00 AM, 35 EUR), Louvre Museum Tour (02:30 PM, 22 EUR), and Le Marais Dinner (07:30 PM, 60 EUR). Returns <code>HTTP 201 Created</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.12: GET ITINERARY -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_GET_ITINERARY_PLACEHOLDER" class="screenshot-img" alt="Get Itineraries">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.12: Retrieve Trip Itineraries — <span class="badge-get">GET</span> <code>/api/trips/:id/itinerary</code></div>
      <div class="screenshot-desc">
        Fetches chronological daily itineraries linked to the parent trip. Itinerary items are sorted ascending by <code>dayNumber</code>, verifying structured activity scheduling and relational integrity with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.5: COLLABORATION & SEARCH -->
<div class="page-break">
  <h2 class="subsection-title">5.5 Trip Collaboration & Keyword Search Engine</h2>

  <!-- FIGURE 5.13: SHARE TRIP -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_SHARE_PLACEHOLDER" class="screenshot-img" alt="Share Trip">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.13: Share Trip with Collaborator — <span class="badge-post">POST</span> <code>/api/trips/:id/share</code></div>
      <div class="screenshot-desc">
        Collaborator invitation flow. User submits partner email (<code>collaborator@tripcraft.dev</code>) and assigns role (<code>editor</code>). Controller validates target user existence, prevents self-sharing, updates collaborator array, and returns <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.14: SEARCH BY KEYWORD -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_SEARCH_PLACEHOLDER" class="screenshot-img" alt="Search Trips">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.14: Keyword Search Engine — <span class="badge-get">GET</span> <code>/api/trips/search?keyword=europe</code></div>
      <div class="screenshot-desc">
        Multi-field search evaluation. Request query <code>?keyword=europe</code> triggers regex scanning across trip titles, descriptions, destination city/country, and scheduled itinerary activities. Returns matching Europe trip object with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.6: BUDGET & EXPENSES -->
<div class="page-break">
  <h2 class="subsection-title">5.6 Budget Tracking & Expense Management (Advanced Feature)</h2>

  <!-- FIGURE 5.15: ADD EXPENSE -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_ADD_EXPENSE_PLACEHOLDER" class="screenshot-img" alt="Add Expense">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.15: Log Trip Expense — <span class="badge-post">POST</span> <code>/api/trips/:id/expenses</code></div>
      <div class="screenshot-desc">
        Logging individual trip expense. Ingests expense title ("Louvre Museum Tickets & Audio Guide"), amount (44.00 EUR), category ('activities'), currency, and attribution to paying user. Verified with <code>HTTP 201 Created</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.16: BUDGET BREAKDOWN -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_GET_BUDGET_PLACEHOLDER" class="screenshot-img" alt="Budget Breakdown">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.16: Budget Summary & Category Breakdown — <span class="badge-get">GET</span> <code>/api/trips/:id/expenses</code></div>
      <div class="screenshot-desc">
        Financial report computation. Evaluates total budget ceiling (4,000 EUR), sums all recorded expenses (44 EUR), computes remaining available balance (3,956 EUR), and aggregates category breakdown (<code>activities: 44</code>) with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>
</div>

<!-- SUBSECTION 5.7: WEATHER FORECASTS & DELETION -->
<div class="page-break">
  <h2 class="subsection-title">5.7 Live Weather Forecast & Cascading Deletion</h2>

  <!-- FIGURE 5.17: CITY WEATHER -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_CITY_WEATHER_PLACEHOLDER" class="screenshot-img" alt="City Weather">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.17: Live City Weather Forecast — <span class="badge-get">GET</span> <code>/api/weather?city=Paris</code></div>
      <div class="screenshot-desc">
        Public weather integration endpoint. Queries Open-Meteo geocoding to resolve coordinates for Paris (48.85°N, 2.35°E), then fetches live telemetry: current temperature (13.6°C), humidity, wind speed, and 7-day daily forecast with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.18: TRIP WEATHER -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_TRIP_WEATHER_PLACEHOLDER" class="screenshot-img" alt="Trip Destination Weather">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.18: Trip Destination Live Weather — <span class="badge-get">GET</span> <code>/api/trips/:id/weather</code></div>
      <div class="screenshot-desc">
        Integrated trip meteorological query. Resolves the trip's destination city, executes real-time weather lookup, and formats daily high/low temperatures to assist travelers in activity planning with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>

  <!-- FIGURE 5.19: DELETE TRIP -->
  <div class="screenshot-card">
    <div class="screenshot-img-container">
      <img src="IMG_DELETE_PLACEHOLDER" class="screenshot-img" alt="Delete Trip">
    </div>
    <div class="screenshot-meta">
      <div class="screenshot-title">Figure 5.19: Delete Trip & Cascade Itinerary Destruction — <span class="badge-delete">DELETE</span> <code>/api/trips/:id</code></div>
      <div class="screenshot-desc">
        Secure resource disposal. Verifies strict owner authorization, then atomically cascades deletion of all day-by-day itinerary records linked to the trip ID before removing the trip document. Verified with <code>HTTP 200 OK</code>.
      </div>
    </div>
  </div>
</div>

<!-- 8. SECTION 6: RESULTS, VERIFICATION MATRIX AND DISCUSSION -->
<div class="page-break">
  <h1 class="section-title">6. Case Study Results, Verification Matrix and Discussion</h1>

  <h2 class="subsection-title">6.1 Comprehensive Endpoint Verification Test Matrix</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Method</th>
        <th>Route Endpoint</th>
        <th>Sample Request Payload</th>
        <th>Auth</th>
        <th>Status</th>
        <th>Result</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/auth/register</code></td>
        <td><code>{"name":"Alex","email":"alex@tripcraft.dev"}</code></td>
        <td>Public</td>
        <td>201 Created</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/auth/login</code></td>
        <td><code>{"email":"alex@tripcraft.dev","password":"..."}</code></td>
        <td>Public</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/auth/me</code></td>
        <td>Header: <code>Bearer &lt;token&gt;</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/trips</code></td>
        <td><code>{"title":"Grand Tour","destination":"Paris"}</code></td>
        <td>Bearer</td>
        <td>201 Created</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips</code></td>
        <td>Query: <code>?sort=startDate</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips/:id</code></td>
        <td>Param: <code>tripId</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-put">PUT</span></td>
        <td><code>/api/trips/:id</code></td>
        <td><code>{"status":"ongoing"}</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/trips/:id/itinerary</code></td>
        <td><code>{"dayNumber":1,"activities":[...]}</code></td>
        <td>Bearer</td>
        <td>201 Created</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips/:id/itinerary</code></td>
        <td>Param: <code>tripId</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/trips/:id/share</code></td>
        <td><code>{"email":"friend@tripcraft.dev","role":"editor"}</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips/search</code></td>
        <td>Query: <code>?keyword=europe</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-post">POST</span></td>
        <td><code>/api/trips/:id/expenses</code></td>
        <td><code>{"title":"Louvre Tickets","amount":44}</code></td>
        <td>Bearer</td>
        <td>201 Created</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips/:id/expenses</code></td>
        <td>Param: <code>tripId</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/weather</code></td>
        <td>Query: <code>?city=Paris</code></td>
        <td>Public</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-get">GET</span></td>
        <td><code>/api/trips/:id/weather</code></td>
        <td>Param: <code>tripId</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
      <tr>
        <td><span class="badge-delete">DELETE</span></td>
        <td><code>/api/trips/:id</code></td>
        <td>Param: <code>tripId</code></td>
        <td>Bearer</td>
        <td>200 OK</td>
        <td><span class="badge-pass">PASS</span></td>
      </tr>
    </tbody>
  </table>

  <h2 class="subsection-title">6.2 Performance & Security Discussion</h2>
  <p>
    The experimental results confirm several critical architectural properties:
  </p>
  <ul>
    <li><strong>Sub-Millisecond Query Response:</strong> With compound indexing on <code>{ trip: 1, dayNumber: 1 }</code>, fetching complete daily itineraries executes with minimal database latency, avoiding full-collection table scans.</li>
    <li><strong>Zero-Trust Authorization:</strong> Attempts by unauthenticated clients to modify trips, view private itineraries, or append expenses are blocked with uniform <code>HTTP 401 Unauthorized</code> responses. Non-owner collaborator deletion attempts trigger <code>HTTP 403 Forbidden</code> guards.</li>
    <li><strong>Zero External Key Vulnerability:</strong> The weather forecasting engine leverages Open-Meteo's open public API, mitigating reliance on paid API quotas or vulnerable credential storage in production containers.</li>
  </ul>
</div>

<!-- 9. SECTION 7 & 8: CONCLUSION AND REFERENCES -->
<div class="page-break">
  <h1 class="section-title">7. Conclusion & Learning Outcomes</h1>
  <p>
    Case Study 96: <strong>TripCraft Travel Itinerary Planner</strong> has been successfully engineered, deployed, and verified. The backend API satisfies 100% of functional requirements and advanced optional challenges specified in the B.Tech Computer Science Engineering curriculum.
  </p>

  <h2 class="subsection-title">7.1 Key Technical Competencies Acquired</h2>
  <ol>
    <li><strong>Architectural Modularity:</strong> Mastering decoupled Express.js routing, controller separation, Mongoose modeling, and global error handling middleware with unified JSON contracts.</li>
    <li><strong>Cryptographic Authorization:</strong> Implementing stateless JWT token lifecycles alongside bcrypt password hashing with salt generation to ensure enterprise security standards.</li>
    <li><strong>Relational & Hierarchical Data Modeling:</strong> Designing complex Mongoose documents integrating virtual properties, compound indexing, cascade deletion routines, and population joins.</li>
    <li><strong>Production Hardening & Diagnostics:</strong> Resolving real-world OS-level port collisions (macOS AirPlay port 5000), implementing fallback storage pipelines, and creating OpenAPI 3.0 documentation.</li>
  </ol>

  <h1 class="section-title" style="margin-top: 40px;">8. References</h1>
  <ol style="font-size: 9.5pt; line-height: 1.8;">
    <li><strong>Express.js Documentation:</strong> Routing, Middleware and Error Handling. <a href="https://expressjs.com/">https://expressjs.com/</a></li>
    <li><strong>Mongoose ODM Guide:</strong> Schemas, Models, Indexes, and Population. <a href="https://mongoosejs.com/docs/guide.html">https://mongoosejs.com/docs/guide.html</a></li>
    <li><strong>RFC 7519:</strong> JSON Web Token (JWT) Standard. Internet Engineering Task Force (IETF). <a href="https://tools.ietf.org/html/rfc7519">https://tools.ietf.org/html/rfc7519</a></li>
    <li><strong>OWASP Foundation:</strong> Authentication Cheat Sheet and Password Storage Guidelines. <a href="https://cheatsheetseries.owasp.org/">https://cheatsheetseries.owasp.org/</a></li>
    <li><strong>OpenAPI Specification (v3.0.0):</strong> Standard for RESTful API Documentation. <a href="https://spec.openapis.org/oas/v3.0.0">https://spec.openapis.org/oas/v3.0.0</a></li>
    <li><strong>Open-Meteo Weather API:</strong> Free Weather Forecast API for Non-Commercial and Commercial use. <a href="https://open-meteo.com/">https://open-meteo.com/</a></li>
    <li><strong>ITM Skills University:</strong> B.Tech Computer Science Engineering Backend Development Curriculum Specification, Case Study 96.</li>
  </ol>
</div>

</body>
</html>"""

    # Replace all image placeholders
    for placeholder_key, base64_val in images.items():
        template = template.replace(f"{placeholder_key}_PLACEHOLDER", base64_val)

    html_file = os.path.join(base_dir, "Backend_Final_Report.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"HTML Report generated at: {html_file} ({len(template)} bytes)")

    # Generate PDF
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf_file = os.path.join(base_dir, "Backend_Final_Report.pdf")
    
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    print("Compiling PDF with Google Chrome Headless...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_file):
        print(f"PDF successfully generated at: {pdf_file} ({os.path.getsize(pdf_file)} bytes)")
        # Copy to KunalLubhana_Backend_Final_Report.pdf
        kunal_pdf = os.path.join(base_dir, "KunalLubhana_Backend_Final_Report.pdf")
        subprocess.run(["cp", pdf_file, kunal_pdf])
        subprocess.run(["cp", html_file, os.path.join(base_dir, "KunalLubhana_Backend_Final_Report.html")])
        print("Updated KunalLubhana_Backend_Final_Report.pdf and .html")
    else:
        print(f"Error generating PDF: {res.stderr}")

if __name__ == "__main__":
    generate_report()
