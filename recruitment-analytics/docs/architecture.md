<mxfile host="app.diagrams.net" agent="Antigravity Architecture Engine">
  <diagram id="ocs-placement-analytics-architecture" name="Placement Operations Analytics Platform">
    <mxGraphModel dx="906" dy="470" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1700" pageHeight="960" background="#F8FAFC" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="header_banner" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;fontColor=#0F172A;fontSize=16;align=left;spacingLeft=25;shadow=1;strokeWidth=1.5;" value="&lt;b&gt;RECRUITMENT FUNNEL &amp;amp; CAPACITY OPTIMIZATION PLATFORM (OCS LOGISTICS ENGINE)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size: 12px; font-weight: normal; color: #475569;&quot;&gt;Enterprise Product Analytics &amp;amp; Operations Intelligence Architecture • Production Star/Snowflake Dimensional Model&lt;/span&gt;" vertex="1">
          <mxGeometry height="60" width="1620" x="40" y="30" as="geometry" />
        </mxCell>
        <mxCell id="layer1_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#FFFFFF;strokeColor=#94A3B8;strokeWidth=1.5;fontSize=13;fontColor=#0F172A;spacingTop=12;shadow=1;" value="&lt;b&gt;LAYER 1 — DATA SOURCES&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;color:#64748B;&quot;&gt;Raw Recruitment Data (7 CSVs)&lt;/span&gt;" vertex="1">
          <mxGeometry height="780" width="240" x="40" y="110" as="geometry" />
        </mxCell>
        <mxCell id="csv_candidates" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;candidates.csv&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;1,250 rows • 11 cols&lt;br/&gt;Demographics, CGPA, Majors&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="180" as="geometry" />
        </mxCell>
        <mxCell id="csv_companies" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;companies.csv&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;180 rows • 6 cols&lt;br&gt;Industry, Priority Tier&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="260" as="geometry" />
        </mxCell>
        <mxCell id="csv_applications" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;applications.csv&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;6,000 rows • 7 cols&lt;br/&gt;Applicant Role Lifecycle&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="340" as="geometry" />
        </mxCell>
        <mxCell id="csv_stages" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;recruitment_stage_records.csv&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;21,462 rows • 11 cols&lt;br/&gt;Stage Event Telemetry &amp;amp; SLA&lt;/span&gt;" vertex="1">
          <mxGeometry height="75" width="210" x="55" y="420" as="geometry" />
        </mxCell>
        <mxCell id="csv_slots" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;interview_slots.csv&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;2,500 rows • 9 cols&lt;br/&gt;Slot Windows &amp;amp; Bookings&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="510" as="geometry" />
        </mxCell>
        <mxCell id="csv_panels" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;panels.csv&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;50 rows • 4 cols&lt;br/&gt;Interview Panel Quotas&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="590" as="geometry" />
        </mxCell>
        <mxCell id="csv_rooms" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontColor=#1E293B;fontSize=11;align=left;spacingLeft=12;strokeWidth=1;" value="&lt;b&gt;rooms.csv&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;30 rows • 5 cols&lt;br&gt;Interview Rooms &amp;amp; Capacity&lt;/span&gt;" vertex="1">
          <mxGeometry height="65" width="210" x="55" y="670" as="geometry" />
        </mxCell>
        <mxCell id="l1_badge" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#BFDBFE;fontSize=10;align=center;" value="&lt;b style=&quot;color:#2563EB;&quot;&gt;100% Referential Integrity&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;Zero Orphans • Zero PK Duplicates&lt;/span&gt;" vertex="1">
          <mxGeometry height="40" width="210" x="55" y="750" as="geometry" />
        </mxCell>
        <mxCell id="layer2_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#FFFFFF;strokeColor=#3B82F6;strokeWidth=2;fontSize=13;fontColor=#0F172A;spacingTop=12;shadow=1;" value="&lt;b&gt;LAYER 2 — DATA WAREHOUSE&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;color:#2563EB;font-weight:bold;&quot;&gt;DuckDB Analytics Warehouse&lt;/span&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;placement_analytics.duckdb (7.88 MB)&lt;/span&gt;" vertex="1">
          <mxGeometry height="780" width="310" x="340" y="110" as="geometry" />
        </mxCell>
        <mxCell id="dim_group" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1;fontSize=11;spacingTop=8;" value="&lt;b style=&quot;color:#1E3A8A;&quot;&gt;DIMENSION TABLES (4)&lt;/b&gt;" vertex="1">
          <mxGeometry height="260" width="280" x="355" y="180" as="geometry" />
        </mxCell>
        <mxCell id="dim_candidates" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#93C5FD;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;candidates&lt;/b&gt; (PK: candidate_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;1,250 records • Demographics, GPA, Cohort&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="260" x="365" y="215" as="geometry" />
        </mxCell>
        <mxCell id="dim_companies" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#93C5FD;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;companies&lt;/b&gt; (PK: company_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;180 records • Sectors, Priority Tier&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="260" x="365" y="270" as="geometry" />
        </mxCell>
        <mxCell id="dim_panels" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#93C5FD;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;panels&lt;/b&gt; (PK: panel_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;50 records • Department, Daily Slot Cap&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="260" x="365" y="325" as="geometry" />
        </mxCell>
        <mxCell id="dim_rooms" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#93C5FD;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;rooms&lt;/b&gt; (PK: room_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;30 records • Hall, Mode, Seating Capacity&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="260" x="365" y="380" as="geometry" />
        </mxCell>
        <mxCell id="fct_group" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1;fontSize=11;spacingTop=8;" value="&lt;b style=&quot;color:#1E40AF;&quot;&gt;FACT &amp;amp; BRIDGE TABLES (3)&lt;/b&gt;" vertex="1">
          <mxGeometry height="260" width="280" x="355" y="455" as="geometry" />
        </mxCell>
        <mxCell id="fct_applications" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#60A5FA;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;applications&lt;/b&gt; (PK: application_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;6,000 records • FK: candidate_id, company_id&lt;/span&gt;" vertex="1">
          <mxGeometry height="50" width="260" x="365" y="490" as="geometry" />
        </mxCell>
        <mxCell id="fct_stages" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#60A5FA;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;recruitment_stage_records&lt;/b&gt; (PK: stage_record_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;21,462 records • Funnel Progression &amp;amp; SLA&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="260" x="365" y="555" as="geometry" />
        </mxCell>
        <mxCell id="fct_slots" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#60A5FA;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;interview_slots&lt;/b&gt; (PK: slot_id)&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;2,500 records • Capacity Allocation &amp;amp; Status&lt;/span&gt;" vertex="1">
          <mxGeometry height="50" width="260" x="365" y="625" as="geometry" />
        </mxCell>
        <mxCell id="l2_badge" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#93C5FD;fontSize=10;align=center;" value="&lt;b style=&quot;color:#0F172A;&quot;&gt;31,472 Records Loaded&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#2563EB;&quot;&gt;Star / Snowflake Relational Model&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="280" x="355" y="730" as="geometry" />
        </mxCell>
        <mxCell id="layer3_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#FFFFFF;strokeColor=#2563EB;strokeWidth=1.5;fontSize=13;fontColor=#0F172A;spacingTop=12;shadow=1;" value="&lt;b&gt;LAYER 3 — ANALYTICS ENGINE&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;color:#1D4ED8;font-weight:bold;&quot;&gt;SQL Analytics Layer&lt;/span&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;Vectorized In-Process OLAP Queries&lt;/span&gt;" vertex="1">
          <mxGeometry height="780" width="270" x="700" y="110" as="geometry" />
        </mxCell>
        <mxCell id="sql_funnel" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Funnel Analytics&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;Stage volume, progression rates&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="180" as="geometry" />
        </mxCell>
        <mxCell id="sql_conversion" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Conversion Analysis&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Funnel Conversion Analysis&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="245" as="geometry" />
        </mxCell>
        <mxCell id="sql_dropoff" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Drop-off Analysis&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;Screening &amp;amp; tech evaluation churn&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="310" as="geometry" />
        </mxCell>
        <mxCell id="sql_company" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Company Hiring Analytics&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Hiring Outcomes by Company &amp;amp; Sector&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="375" as="geometry" />
        </mxCell>
        <mxCell id="sql_capacity" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Capacity Analytics&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Room utilization &amp;amp; panel workload analysis&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="440" as="geometry" />
        </mxCell>
        <mxCell id="sql_sla" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#E2E8F0;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;SLA Compliance Analytics&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;TAT hours vs SLA window breaches&lt;/span&gt;" vertex="1">
          <mxGeometry height="55" width="240" x="715" y="505" as="geometry" />
        </mxCell>
        <mxCell id="sql_recom" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#93C5FD;fontColor=#1D4ED8;fontSize=11;align=left;spacingLeft=12;" value="&lt;b&gt;Capacity Recommendation Layer&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Rule-Based Capacity Allocation Recommendations&lt;/span&gt;" vertex="1">
          <mxGeometry height="60" width="240" x="715" y="570" as="geometry" />
        </mxCell>
        <mxCell id="metrics_pill_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#CBD5E1;fontSize=10;align=center;" value="&lt;b style=&quot;color: rgb(30, 64, 175);&quot;&gt;BUSINESS METRICS LAYER&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;• Applications • Offers • Hires&lt;br&gt;• Conversion Rate • Drop-off Rate&lt;br&gt;• Panel &amp;amp; Room Utilization&lt;br&gt;• SLA Compliance • Avg Score&lt;/span&gt;&lt;div&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;• Time-to-Hire&lt;/span&gt;&lt;/div&gt;" vertex="1">
          <mxGeometry height="120" width="240" x="715" y="650" as="geometry" />
        </mxCell>
        <mxCell id="layer4_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#FFFFFF;strokeColor=#F59E0B;strokeWidth=1.5;fontSize=13;fontColor=#0F172A;spacingTop=12;shadow=1;" value="&lt;b&gt;LAYER 4 —&amp;nbsp;Business Intelligence Layer&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: rgb(180, 83, 9); font-weight: bold;&quot;&gt;Power BI Dashboard&lt;/span&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;Placement Operations Analytics.pbix&lt;/span&gt;" vertex="1">
          <mxGeometry height="780" width="290" x="1020" y="110" as="geometry" />
        </mxCell>
        <mxCell id="pbi_p1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FDE68A;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b style=&quot;color: rgb(180, 83, 9);&quot;&gt;PAGE 1&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:12px;&quot;&gt;Executive Overview&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;• Executive KPIs &amp;amp; Placement Outcomes&lt;br&gt;• Application, Candidate &amp;amp; Company Overview&lt;br&gt;• Placement Outcome Distribution&lt;/span&gt;" vertex="1">
          <mxGeometry height="110" width="260" x="1035" y="180" as="geometry" />
        </mxCell>
        <mxCell id="pbi_p2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FDE68A;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b style=&quot;color: rgb(180, 83, 9);&quot;&gt;PAGE 2&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:12px;&quot;&gt;Candidate Funnel Monitoring&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;• Stage-by-Stage Conversion Funnel&lt;br&gt;• Funnel Conversion Monitoring&lt;br&gt;• SLA Performance Monitoring&lt;/span&gt;" vertex="1">
          <mxGeometry height="110" width="260" x="1035" y="310" as="geometry" />
        </mxCell>
        <mxCell id="pbi_p3" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FDE68A;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b style=&quot;color:#B45309;&quot;&gt;PAGE 3&lt;/b&gt;&lt;br/&gt;&lt;b style=&quot;font-size:12px;&quot;&gt;Company Analytics&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;• Partner Tier Load Distribution&lt;br/&gt;• Top Hiring Sectors &amp;amp; Role Yields&lt;br/&gt;• Company SLA Adherence Ranking&lt;/span&gt;" vertex="1">
          <mxGeometry height="110" width="260" x="1035" y="440" as="geometry" />
        </mxCell>
        <mxCell id="pbi_p4" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#FDE68A;fontColor=#0F172A;fontSize=11;align=left;spacingLeft=12;" value="&lt;b style=&quot;color:#B45309;&quot;&gt;PAGE 4&lt;/b&gt;&lt;br/&gt;&lt;b style=&quot;font-size:12px;&quot;&gt;Operations &amp;amp; Capacity Analytics&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:10px;color:#64748B;&quot;&gt;• Panel Workload Utilization Gauges&lt;br/&gt;• Room Seating Occupancy Analysis&lt;br/&gt;• Daily Slot Deficit &amp;amp; Overflow Alerts&lt;/span&gt;" vertex="1">
          <mxGeometry height="110" width="260" x="1035" y="570" as="geometry" />
        </mxCell>
        <mxCell id="l4_badge" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#FDE68A;fontSize=10;align=center;" value="&lt;b style=&quot;color:#B45309;&quot;&gt;Interactive DAX Semantic Layer&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#78350F;&quot;&gt;DirectQuery / Native ODBC Driver&lt;/span&gt;" vertex="1">
          <mxGeometry height="50" width="260" x="1035" y="710" as="geometry" />
        </mxCell>
        <mxCell id="layer5_box" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#FFFFFF;strokeColor=#10B981;strokeWidth=1.5;fontSize=13;fontColor=#0F172A;spacingTop=12;shadow=1;" value="&lt;b&gt;LAYER 5 —&amp;nbsp;Decision Intelligence&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 11px; color: rgb(21, 128, 61); font-weight: bold;&quot;&gt;Operational Intelligence&lt;/span&gt;&lt;br&gt;&lt;span style=&quot;font-size: 10px; color: rgb(100, 116, 139);&quot;&gt;Stakeholder Decision Optimization&lt;/span&gt;" vertex="1">
          <mxGeometry height="780" width="300" x="1360" y="110" as="geometry" />
        </mxCell>
        <mxCell id="personas_group" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1;fontSize=11;spacingTop=8;" value="&lt;b style=&quot;color:#15803D;&quot;&gt;KEY STAKEHOLDER PERSONAS&lt;/b&gt;" vertex="1">
          <mxGeometry height="230" width="270" x="1375" y="180" as="geometry" />
        </mxCell>
        <mxCell id="user_placement" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E2E8F0;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;🎓 Placement Team&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;Drive cohort throughput &amp;amp; employer yields&lt;/span&gt;" vertex="1">
          <mxGeometry height="40" width="250" x="1385" y="215" as="geometry" />
        </mxCell>
        <mxCell id="user_ops" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E2E8F0;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;⚙️ Operations Team&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#64748B;&quot;&gt;Schedule rooms &amp;amp; prevent panel bottlenecks&lt;/span&gt;" vertex="1">
          <mxGeometry height="40" width="250" x="1385" y="265" as="geometry" />
        </mxCell>
        <mxCell id="user_exec" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E2E8F0;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;👔 Placement Leadership&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Real-time placement rate visibility&lt;/span&gt;" vertex="1">
          <mxGeometry height="40" width="250" x="1385" y="315" as="geometry" />
        </mxCell>
        <mxCell id="user_recruiter" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E2E8F0;fontColor=#1E293B;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;🎯 Placement Coordinators&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 9px; color: rgb(100, 116, 139);&quot;&gt;Monitor company progress &amp;amp; coordinate hiring operations&lt;/span&gt;" vertex="1">
          <mxGeometry height="40" width="250" x="1385" y="365" as="geometry" />
        </mxCell>
        <mxCell id="decisions_group" parent="1" style="rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;align=center;fillColor=#ECFDF5;strokeColor=#A7F3D0;strokeWidth=1;fontSize=11;spacingTop=8;" value="&lt;b style=&quot;color:#047857;&quot;&gt;ACTIONABLE BUSINESS DECISIONS&lt;/b&gt;" vertex="1">
          <mxGeometry height="340" width="270" x="1375" y="430" as="geometry" />
        </mxCell>
        <mxCell id="act_bottlenecks" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6EE7B7;fontColor=#065F46;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;🔍 Identify Funnel Bottlenecks&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#065F46;&quot;&gt;Pinpoint stages with excessive drop-offs&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="250" x="1385" y="465" as="geometry" />
        </mxCell>
        <mxCell id="act_capacity" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6EE7B7;fontColor=#065F46;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;⚖️ Optimize Interview Capacity&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#065F46;&quot;&gt;Rebalance overloaded evaluator panels&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="250" x="1385" y="520" as="geometry" />
        </mxCell>
        <mxCell id="act_performance" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6EE7B7;fontColor=#065F46;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;📈 Track Recruiter Performance&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#065F46;&quot;&gt;Evaluate turnaround speed &amp;amp; evaluation quality&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="250" x="1385" y="575" as="geometry" />
        </mxCell>
        <mxCell id="act_sla" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6EE7B7;fontColor=#065F46;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;🛡️ Improve SLA Compliance&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#065F46;&quot;&gt;Mitigate 48-hr evaluation breach spikes&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="250" x="1385" y="630" as="geometry" />
        </mxCell>
        <mxCell id="act_throughput" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6EE7B7;fontColor=#065F46;fontSize=10;align=left;spacingLeft=10;" value="&lt;b&gt;🚀 Increase Placement Throughput&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:9px;color:#065F46;&quot;&gt;Maximize campus offer conversion yield&lt;/span&gt;" vertex="1">
          <mxGeometry height="45" width="250" x="1385" y="685" as="geometry" />
        </mxCell>
        <mxCell id="edge_l1_l2" edge="1" parent="1" source="layer1_box" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeColor=#2563EB;strokeWidth=2.5;fillColor=#DBEAFE;" target="layer2_box" value="&lt;b style=&quot;font-size:10px;color:#2563EB;&quot;&gt;Native Ingestion&lt;br/&gt;(7 CSV Entities)&lt;/b&gt;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_l2_l3" edge="1" parent="1" source="layer2_box" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeColor=#2563EB;strokeWidth=2.5;fillColor=#DBEAFE;" target="layer3_box" value="&lt;b style=&quot;font-size:10px;color:#2563EB;&quot;&gt;Vectorized SQL&lt;br/&gt;Execution&lt;/b&gt;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_l3_l4" edge="1" parent="1" source="layer3_box" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeColor=#F59E0B;strokeWidth=2.5;fillColor=#FEF3C7;" target="layer4_box" value="&lt;b style=&quot;font-size:10px;color:#F59E0B;&quot;&gt;Semantic Model&lt;br/&gt;&amp;amp; DAX Measures&lt;/b&gt;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="edge_l4_l5" edge="1" parent="1" source="layer4_box" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeColor=#10B981;strokeWidth=2.5;fillColor=#ECFDF5;" target="layer5_box" value="&lt;b style=&quot;font-size:10px;color:#10B981;&quot;&gt;Operational&lt;br/&gt;Intelligence&lt;/b&gt;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
