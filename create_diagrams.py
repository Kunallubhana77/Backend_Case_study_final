import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(base_dir, "screenshot")
os.makedirs(screenshot_dir, exist_ok=True)

flowchart_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #FFFFFF;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1E293B;
    padding: 30px 20px;
    width: 950px;
    margin: 0 auto;
  }
  .header {
    text-align: center;
    margin-bottom: 25px;
  }
  .univ {
    font-size: 13px;
    font-weight: 700;
    color: #800020;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }
  .title {
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
    margin: 5px 0;
  }
  .subtitle {
    font-size: 13.5px;
    color: #64748B;
  }
  svg {
    display: block;
    margin: 0 auto;
  }
  text {
    font-family: 'Inter', -apple-system, sans-serif;
  }
  .mono {
    font-family: 'JetBrains Mono', monospace;
  }
</style>
</head>
<body>

<div class="header">
  <div class="univ">ITM Skills University • School of Future Tech</div>
  <div class="title">TripCraft Backend API — Request & Security Flowchart</div>
  <div class="subtitle">Complete Execution Lifecycle from Client Ingestion to Persistence</div>
</div>

<svg width="900" height="1580" viewBox="0 0 900 1580" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Arrow marker -->
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#64748B"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16A34A"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563EB"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#DC2626"/>
    </marker>
    
    <!-- Drop Shadow Filter -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- 1. START NODE (Y: 20 to 66) -->
  <rect x="330" y="20" width="240" height="46" rx="23" fill="#0F172A" filter="url(#shadow)"/>
  <text x="450" y="48" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="1">START: CLIENT REQUEST</text>

  <!-- Arrow to Express Server -->
  <line x1="450" y1="66" x2="450" y2="105" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 2. EXPRESS PIPELINE NODE (Y: 105 to 167) -->
  <rect x="250" y="105" width="400" height="62" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="450" y="131" fill="#0F172A" font-size="13.5" font-weight="700" text-anchor="middle">Express Server &amp; Security Pipeline</text>
  <text x="450" y="152" fill="#64748B" font-size="11.5" text-anchor="middle">Port 8000 • Helmet Hardening • CORS • express.json()</text>

  <!-- Arrow to Router -->
  <line x1="450" y1="167" x2="450" y2="205" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 3. EXPRESS ROUTER (Y: 205 to 267) -->
  <rect x="250" y="205" width="400" height="62" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="450" y="231" fill="#0F172A" font-size="13.5" font-weight="700" text-anchor="middle">Express Router Dispatcher</text>
  <text x="450" y="252" fill="#64748B" font-size="11.5" text-anchor="middle">Inspects URL: /api/auth, /api/trips, /api/weather</text>

  <!-- Arrow to Diamond 1 (Plenty of clearance: 48px gap) -->
  <line x1="450" y1="267" x2="450" y2="315" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 4. DECISION DIAMOND 1: Protected Route? (Center: 450, 365 | Height: 100, Width: 220) (Y: 315 to 415) -->
  <polygon points="450,315 560,365 450,415 340,365" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2.5" filter="url(#shadow)"/>
  <text x="450" y="360" fill="#92400E" font-size="13" font-weight="700" text-anchor="middle">Protected</text>
  <text x="450" y="377" fill="#92400E" font-size="13" font-weight="700" text-anchor="middle">Route?</text>

  <!-- Branch YES (Left): to authMiddleware (Clearance: 70px vertical gap) -->
  <line x1="340" y1="365" x2="250" y2="365" stroke="#16A34A" stroke-width="2"/>
  <line x1="250" y1="365" x2="250" y2="480" stroke="#16A34A" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="290" y="355" fill="#16A34A" font-size="11.5" font-weight="700">[ YES ]</text>

  <!-- Branch NO (Right): to Public Route (Clearance: 70px vertical gap) -->
  <line x1="560" y1="365" x2="675" y2="365" stroke="#2563EB" stroke-width="2"/>
  <line x1="675" y1="365" x2="675" y2="480" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <text x="615" y="355" fill="#2563EB" font-size="11.5" font-weight="700">[ NO ]</text>

  <!-- 5. BRANCH TARGETS (Y: 480 to 548) -->
  <!-- Left Target: authMiddleware -->
  <rect x="70" y="480" width="360" height="68" rx="10" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2" filter="url(#shadow)"/>
  <text x="250" y="508" fill="#1E3A8A" font-size="13" font-weight="700" text-anchor="middle">authMiddleware Verification</text>
  <text x="250" y="528" fill="#3B82F6" font-size="11" text-anchor="middle">Validates JWT Bearer Token / Firebase Token</text>

  <!-- Right Target: Public Allowed -->
  <rect x="520" y="480" width="310" height="68" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="675" y="508" fill="#1E293B" font-size="13" font-weight="700" text-anchor="middle">Public Route Allowed</text>
  <text x="675" y="528" fill="#64748B" font-size="11" text-anchor="middle">Register, Login, Swagger Docs, Weather</text>

  <!-- Line from authMiddleware to Diamond 2 (Clearance: 70px gap) -->
  <line x1="250" y1="548" x2="250" y2="620" stroke="#64748B" stroke-width="2"/>
  <line x1="250" y1="620" x2="340" y2="670" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Public Route line down directly on the right edge to avoid crossing any boxes -->
  <line x1="840" y1="514" x2="870" y2="514" stroke="#2563EB" stroke-width="2"/>
  <line x1="870" y1="514" x2="870" y2="925" stroke="#2563EB" stroke-dasharray="5,5" stroke-width="2"/>
  <line x1="870" y1="925" x2="710" y2="925" stroke="#2563EB" stroke-dasharray="5,5" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <text x="760" y="730" fill="#2563EB" font-size="10.5" font-weight="600">Public Access Route</text>

  <!-- 6. DECISION DIAMOND 2: Validation & Token Valid? (Center: 450, 670 | Height: 100, Width: 220) (Y: 620 to 720) -->
  <polygon points="450,620 560,670 450,720 340,670" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2.5" filter="url(#shadow)"/>
  <text x="450" y="663" fill="#92400E" font-size="12.5" font-weight="700" text-anchor="middle">Token &amp;</text>
  <text x="450" y="680" fill="#92400E" font-size="12.5" font-weight="700" text-anchor="middle">Validation Valid?</text>

  <!-- Branch NO (Right): Error Intercepted (Clear horizontal layout, Y: 670) -->
  <line x1="560" y1="670" x2="625" y2="670" stroke="#DC2626" stroke-width="2" marker-end="url(#arrow-red)"/>
  <text x="585" y="660" fill="#DC2626" font-size="11.5" font-weight="700">[ NO ]</text>
  <rect x="630" y="640" width="210" height="60" rx="8" fill="#FEF2F2" stroke="#EF4444" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="735" y="665" fill="#991B1B" font-size="11.5" font-weight="700" text-anchor="middle">✗ Error Intercepted</text>
  <text x="735" y="683" fill="#B91C1C" font-size="10" text-anchor="middle">400 Bad Request / 401 Unauthorized</text>

  <!-- Branch YES (Down): to Passed Box (Clearance: 65px gap) -->
  <line x1="450" y1="720" x2="450" y2="785" stroke="#16A34A" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="460" y="755" fill="#16A34A" font-size="11.5" font-weight="700">[ YES ]</text>

  <!-- 7. VALIDATION PASSED BOX (Y: 785 to 850) -->
  <rect x="220" y="785" width="460" height="65" rx="10" fill="#ECFDF5" stroke="#10B981" stroke-width="2" filter="url(#shadow)"/>
  <text x="450" y="812" fill="#065F46" font-size="13" font-weight="700" text-anchor="middle">✓ Validation Passed: User Injected into req.user</text>
  <text x="450" y="833" fill="#047857" font-size="11" text-anchor="middle">express-validator rules sanitize body, query &amp; route parameters</text>

  <!-- Arrow to Controller Layer -->
  <line x1="450" y1="850" x2="450" y2="905" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 8. CONTROLLERS HEADER (Y: 925) -->
  <text x="450" y="930" fill="#0F172A" font-size="13.5" font-weight="800" text-anchor="middle" letter-spacing="1">CONTROLLER BUSINESS LOGIC EXECUTION LAYER</text>

  <!-- 9. CONTROLLER SERVICE CARDS GRID (Y: 955 to 1220) -->
  <!-- Row 1: Auth, Trips, Itinerary -->
  <!-- Auth Controller -->
  <rect x="40" y="955" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="55" y="978" fill="#0F172A" font-size="12.5" font-weight="700">Auth Controller</text>
  <text x="55" y="998" fill="#475569" font-size="10.5">Bcrypt hash (cost 10) &amp;</text>
  <text x="55" y="1014" fill="#475569" font-size="10.5">JWT token generation.</text>
  <rect x="55" y="1030" width="85" height="22" rx="4" fill="#DBEAFE"/>
  <text x="97" y="1045" fill="#1E40AF" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">POST /register</text>
  <rect x="148" y="1030" width="75" height="22" rx="4" fill="#DBEAFE"/>
  <text x="185" y="1045" fill="#1E40AF" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">POST /login</text>

  <!-- Trip Controller -->
  <rect x="320" y="955" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="335" y="978" fill="#0F172A" font-size="12.5" font-weight="700">Trip Controller</text>
  <text x="335" y="998" fill="#475569" font-size="10.5">Ownership check, sharing &amp;</text>
  <text x="335" y="1014" fill="#475569" font-size="10.5">multi-field regex search.</text>
  <rect x="335" y="1030" width="72" height="22" rx="4" fill="#D1FAE5"/>
  <text x="371" y="1045" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">CRUD /trips</text>
  <rect x="415" y="1030" width="55" height="22" rx="4" fill="#D1FAE5"/>
  <text x="442" y="1045" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">/share</text>
  <rect x="478" y="1030" width="60" height="22" rx="4" fill="#D1FAE5"/>
  <text x="508" y="1045" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">/search</text>

  <!-- Itinerary Controller -->
  <rect x="600" y="955" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="615" y="978" fill="#0F172A" font-size="12.5" font-weight="700">Itinerary Controller</text>
  <text x="615" y="998" fill="#475569" font-size="10.5">Day-by-day timetable &amp;</text>
  <text x="615" y="1014" fill="#475569" font-size="10.5">scheduled activity updates.</text>
  <rect x="615" y="1030" width="90" height="22" rx="4" fill="#D1FAE5"/>
  <text x="660" y="1045" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">POST /itinerary</text>
  <rect x="715" y="1030" width="85" height="22" rx="4" fill="#D1FAE5"/>
  <text x="757" y="1045" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">GET /itinerary</text>

  <!-- Row 2: Expense, Weather, Media (Y: 1085 to 1200) -->
  <!-- Expense & Budget -->
  <rect x="40" y="1085" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="55" y="1108" fill="#0F172A" font-size="12.5" font-weight="700">Expense &amp; Budget</text>
  <text x="55" y="1128" fill="#475569" font-size="10.5">Total spent aggregation &amp;</text>
  <text x="55" y="1144" fill="#475569" font-size="10.5">category breakdown map.</text>
  <rect x="55" y="1160" width="88" height="22" rx="4" fill="#DBEAFE"/>
  <text x="99" y="1175" fill="#1E40AF" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">POST /expenses</text>
  <rect x="150" y="1160" width="82" height="22" rx="4" fill="#DBEAFE"/>
  <text x="191" y="1175" fill="#1E40AF" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">GET /expenses</text>

  <!-- Weather Telemetry -->
  <rect x="320" y="1085" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="335" y="1108" fill="#0F172A" font-size="12.5" font-weight="700">Weather Telemetry</text>
  <text x="335" y="1128" fill="#475569" font-size="10.5">Open-Meteo geocoding &amp;</text>
  <text x="335" y="1144" fill="#475569" font-size="10.5">7-day weather forecast.</text>
  <rect x="335" y="1160" width="80" height="22" rx="4" fill="#FEF3C7"/>
  <text x="375" y="1175" fill="#92400E" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">GET /weather</text>
  <rect x="422" y="1160" width="75" height="22" rx="4" fill="#FEF3C7"/>
  <text x="459" y="1175" fill="#92400E" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">/:id/weather</text>

  <!-- Media Pipeline -->
  <rect x="600" y="1085" width="260" height="115" rx="10" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="615" y="1108" fill="#0F172A" font-size="12.5" font-weight="700">Media Pipeline</text>
  <text x="615" y="1128" fill="#475569" font-size="10.5">Multer memory buffer streaming</text>
  <text x="615" y="1144" fill="#475569" font-size="10.5">to Firebase or local disk.</text>
  <rect x="615" y="1160" width="115" height="22" rx="4" fill="#D1FAE5"/>
  <text x="672" y="1175" fill="#065F46" font-size="9.5" font-weight="700" class="mono" text-anchor="middle">POST /trips/:id/photos</text>

  <!-- Arrow from Controllers to MongoDB (Clearance: 60px gap) -->
  <line x1="450" y1="1200" x2="450" y2="1275" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 10. MONGODB PERSISTENCE LAYER (Y: 1280 to 1355) -->
  <rect x="200" y="1280" width="500" height="75" rx="12" fill="#F1F5F9" stroke="#0F172A" stroke-width="2" filter="url(#shadow)"/>
  <text x="450" y="1312" fill="#0F172A" font-size="14" font-weight="800" text-anchor="middle">MongoDB Document Persistence (Mongoose ODM)</text>
  <text x="450" y="1335" fill="#475569" font-size="11.5" text-anchor="middle">Atomic Operations • Cascade Itinerary Clean-up • Schema Virtuals</text>

  <!-- Arrow from MongoDB to Final Output -->
  <line x1="450" y1="1355" x2="450" y2="1425" stroke="#16A34A" stroke-width="2" marker-end="url(#arrow-green)"/>

  <!-- 11. END NODE (Y: 1430 to 1488) -->
  <rect x="275" y="1430" width="350" height="56" rx="28" fill="#16A34A" filter="url(#shadow)"/>
  <text x="450" y="1465" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle" letter-spacing="1">END: HTTP JSON RESPONSE (200 / 201)</text>
</svg>

</body>
</html>
"""

flowchart_html_path = os.path.join(base_dir, "temp_flowchart.html")
with open(flowchart_html_path, "w", encoding="utf-8") as f:
    f.write(flowchart_html)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
flowchart_png = os.path.join(screenshot_dir, "tripcraft_flowchart.png")

print("Re-rendering TripCraft Flowchart with 100% SVG spacing (no overlapping boxes)...")
subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--screenshot={flowchart_png}",
    "--window-size=1000,1720",
    flowchart_html_path
], check=True)

print(f"Flowchart re-saved at: {flowchart_png} ({os.path.getsize(flowchart_png)} bytes)")
if os.path.exists(flowchart_html_path): os.remove(flowchart_html_path)
