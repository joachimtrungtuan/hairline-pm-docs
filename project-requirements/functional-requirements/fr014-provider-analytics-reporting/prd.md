# Product Requirements Document: Provider Analytics & Reporting

**Module**: PR-05: Financial Management & Reporting | A-08: Analytics & Reporting
**Feature Branch**: `fr014-provider-analytics-reporting`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-014 from system-prd.md

---

## Executive Summary

The Provider Analytics & Reporting module empowers clinic operators with comprehensive data insights to optimize their business operations, track financial performance, and make data-driven decisions. Providers access real-time dashboards displaying key metrics including inquiry-to-booking conversion rates, revenue trends, patient demographics, and comparative benchmarks against anonymized industry averages.

This module addresses a critical business need: providers currently operate with limited visibility into their platform performance, making it difficult to optimize pricing strategies, improve response times, or understand competitive positioning. By delivering actionable analytics through intuitive visualizations and exportable reports, the platform transforms raw operational data into strategic business intelligence.

**Value Proposition**:

- **For Providers**: Gain competitive advantage through data-driven insights, optimize pricing and conversion rates, track financial performance in real-time
- **For Hairline**: Demonstrate platform value, increase provider engagement and retention, enable proactive support for underperforming providers
- **For Patients**: Indirectly benefit from improved provider responsiveness and competitive pricing driven by analytics insights

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing features (analytics are provider-internal)
- **Provider Platform (PR-05)**: Performance dashboards, financial reports, conversion analytics, export capabilities
- **Admin Platform (A-08)**: Platform-wide analytics aggregation, provider performance monitoring, benchmark calculations
- **Shared Services (S-XX)**: Analytics data pipeline service for metrics calculation, report generation service

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- No direct functionality (patients do not see provider analytics)
- Patient behavior data (inquiry timing, booking patterns) feeds analytics pipeline

**Provider Platform (PR-05)**:

- Access comprehensive performance dashboard with key metrics
- View inquiry and quote statistics (count, conversion rates, response times)
- Monitor financial data (revenue trends, earnings breakdown, payment schedules)
- Analyze conversion funnels (inquiry → quote → acceptance → booking)
- Compare performance against anonymized industry benchmarks
- Export reports in PDF and CSV formats
- Filter and segment data by date ranges, treatment types, patient locations

**Admin Platform (A-08)**:

- Monitor all provider analytics across platform
- Calculate and publish anonymized industry benchmarks
- Identify underperforming providers for proactive support
- Generate platform-wide analytics reports
- Configure benchmark calculation methodologies
- Audit analytics data accuracy and integrity

**Shared Services (S-XX)**:

- **Analytics Data Pipeline Service**: Aggregates raw operational data from inquiries, quotes, bookings, payments
- **Report Generation Service**: Produces formatted PDF/CSV exports
- **Benchmark Calculation Service**: Computes anonymized industry averages by region, treatment type, clinic size

### Communication Structure

**In Scope**:

- Email notifications for scheduled report delivery (if provider enables automated reporting)
- In-app alerts when provider metrics fall below defined thresholds (e.g., quote response time exceeding 72 hours)

**Out of Scope**:

- Direct messaging between providers about analytics insights (handled by separate provider community features, future enhancement)
- SMS notifications for analytics updates (email and in-app only)
- Real-time collaborative dashboard viewing (multi-user simultaneous viewing - future enhancement)

### Entry Points

- **Provider Dashboard Access**: Providers navigate to "Analytics" or "Performance" section from main navigation menu
- **Financial Reports Access**: Accessed via "Financial Management" → "Reports & Analytics" submenu
- **Export Triggers**: Providers click "Export Report" button on any analytics screen, triggering report generation
- **Scheduled Reports**: Providers configure automated weekly/monthly report delivery via email (optional)
- **Admin Monitoring**: Admin platform continuously aggregates provider analytics for oversight dashboard

---

## Business Workflows

### Main Flow: Provider Views Performance Dashboard

**Actors**: Provider (Clinic Admin, Owner), Analytics Data Pipeline Service, Provider Platform  
**Trigger**: Provider clicks "Analytics" or "Performance" menu item in provider platform  
**Outcome**: Provider views comprehensive dashboard with key performance metrics for selected time period

**Steps**:

1. Provider navigates to Analytics section from main menu
2. System retrieves provider's historical data (inquiries, quotes, bookings, payments) for default time period (last 30 days)
3. System calculates key metrics:
   - Total inquiries received
   - Total quotes submitted
   - Quote acceptance rate (accepted quotes / total quotes)
   - Booking conversion rate (confirmed bookings / accepted quotes)
   - Total revenue (completed treatments)
   - Average quote amount
   - Average price per graft
   - Average response time (inquiry receipt to quote submission)
4. System generates visualizations (line charts for trends, bar charts for comparisons, pie charts for breakdowns)
5. System displays dashboard with metrics, charts, and comparison indicators (up/down arrows vs previous period)
6. Provider reviews dashboard and identifies trends or areas for improvement
7. Provider optionally adjusts date range filter (last 7 days, last 30 days, last 90 days, last 12 months, custom range)
8. System recalculates and updates dashboard for selected period

### Alternative Flows

**A1: Provider Filters by Treatment Type**:

- **Trigger**: Provider wants to analyze performance for specific treatment (e.g., FUE vs DHI)
- **Steps**:
  1. Provider selects treatment type filter dropdown
  2. Provider chooses treatment (FUE, FUT, DHI, etc.)
  3. System filters all metrics to show only data for selected treatment
  4. Dashboard updates with treatment-specific metrics
- **Outcome**: Provider sees performance data isolated to single treatment type

**A2: Provider Compares Performance Against Benchmarks**:

- **Trigger**: Provider wants to understand competitive positioning
- **Steps**:
  1. Provider clicks "Show Benchmarks" toggle
  2. System retrieves anonymized industry averages for provider's region and clinic size segment
  3. System overlays benchmark data on charts (dotted lines or shaded comparison bars)
  4. System displays variance indicators (+10% above average, -5% below average, etc.)
- **Outcome**: Provider understands performance relative to industry standards

**A3: Provider Drills Down into Conversion Funnel**:

- **Trigger**: Provider notices low conversion rate and wants details
- **Steps**:
  1. Provider clicks on "Conversion Funnel" widget
  2. System displays detailed funnel visualization:
     - Stage 1: Inquiries received (100%)
     - Stage 2: Quotes submitted (80% of inquiries)
     - Stage 3: Quotes accepted (40% of quotes = 32% of inquiries)
     - Stage 4: Bookings confirmed (90% of accepted = 28.8% of inquiries)
  3. System highlights bottleneck stage (lowest conversion percentage)
  4. Provider reviews drop-off points and considers process improvements
- **Outcome**: Provider identifies specific stage causing conversion losses

**A4: Provider Views Revenue by Treatment Type**:

- **Trigger**: Provider wants to understand which treatments generate most revenue
- **Steps**:
  1. Provider navigates to "Revenue Breakdown" section
  2. System displays pie chart showing revenue distribution by treatment type
  3. System shows table with:
     - Treatment type
     - Number of procedures performed
     - Total revenue generated
     - Average revenue per procedure
     - Percentage of total revenue
  4. Provider identifies most profitable treatment offerings
- **Outcome**: Provider optimizes treatment portfolio based on revenue data

**B1: Insufficient Data for Meaningful Analytics**:

- **Trigger**: Provider is new to platform (< 5 inquiries, < 3 quotes)
- **Steps**:
  1. System detects insufficient data volume
  2. System displays friendly message: "You're just getting started! Analytics insights will appear once you've received at least 5 inquiries and submitted 3 quotes."
  3. System shows simplified metrics (inquiry count, quotes submitted) without complex charts
  4. System provides educational tips: "Respond to inquiries within 24 hours to improve conversion rates"
- **Outcome**: Provider understands why full analytics are unavailable and how to unlock them

**B2: Data Processing Delay**:

- **Trigger**: Provider views analytics immediately after completing a booking
- **Steps**:
  1. System attempts to retrieve latest data
  2. Analytics pipeline is still processing recent transaction
  3. System displays notice: "Analytics data updates every 15 minutes. Latest data processed at 10:45 AM."
  4. System shows most recent available data (may be 10-15 minutes delayed)
  5. Provider can refresh page after delay period to see updated metrics
- **Outcome**: Provider understands analytics are near-real-time, not instantaneous

**B3: Export Generation Failure**:

- **Trigger**: Provider requests PDF export but system encounters error
- **Steps**:
  1. Provider clicks "Export to PDF"
  2. Report generation service attempts to create PDF
  3. Service encounters error (data timeout, formatting issue, etc.)
  4. System displays error message: "Report generation failed. Please try again or contact support if issue persists."
  5. System logs error for admin investigation
  6. Provider can retry export or switch to CSV format as alternative
- **Outcome**: Provider receives clear error feedback and alternative options

---

## Screen Specifications

### Screen 1: Performance Dashboard (Overview)

**Purpose**: Provide at-a-glance summary of key provider performance metrics with visual trend indicators

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Selector | dropdown | Yes | Filter for time period (Last 7 days, Last 30 days, Last 90 days, Last 12 months, Custom) | Must select valid range |
| Treatment Type Filter | multi-select dropdown | No | Filter by treatment types (All, FUE, FUT, DHI, etc.) | Optional, defaults to "All" |
| Show Benchmarks Toggle | checkbox | No | Enable/disable benchmark comparison overlay | Optional, defaults to OFF |
| Total Inquiries | numeric display | Yes | Count of inquiries received in period | Read-only, auto-calculated |
| Total Quotes Submitted | numeric display | Yes | Count of quotes submitted in period | Read-only, auto-calculated |
| Quote Acceptance Rate | percentage display | Yes | (Accepted quotes / Total quotes) × 100 | Read-only, displays with trend arrow |
| Booking Conversion Rate | percentage display | Yes | (Confirmed bookings / Accepted quotes) × 100 | Read-only, displays with trend arrow |
| Total Revenue | currency display | Yes | Sum of completed treatment revenue in period | Read-only, formatted in provider's currency |
| Average Quote Amount | currency display | Yes | Average total quote value submitted | Read-only |
| Average Price Per Graft | currency display | Yes | Total revenue / Total grafts performed | Read-only |
| Average Response Time | duration display | Yes | Average time from inquiry receipt to quote submission (hours) | Read-only, displays "24h" format |

**Business Rules**:

- Date range selector defaults to "Last 30 days" on first visit
- Trend arrows compare selected period to previous equivalent period (e.g., last 30 days vs prior 30 days)
- Green up arrow indicates improvement, red down arrow indicates decline
- Benchmark comparison only available if provider has at least 10 completed treatments
- Currency displays always use provider's configured currency (set in profile settings)
- Metrics update every 15 minutes from analytics pipeline
- Zero-state message displayed if no data exists for selected filters

**Notes**:

- Use card-based layout for metric tiles (responsive grid)
- Charts should use consistent color scheme (primary blue for provider data, gray for benchmarks)
- Tooltips on hover provide metric definitions and calculation methods
- "Learn More" links beside each metric open contextual help explaining how to improve that metric

---

### Screen 2: Conversion Funnel Analysis

**Purpose**: Visualize patient journey from inquiry to completed treatment, identifying drop-off points

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Selector | dropdown | Yes | Filter for time period | Same as Dashboard screen |
| Treatment Type Filter | dropdown | No | Filter by treatment type | Optional |
| Funnel Visualization | interactive chart | Yes | Horizontal funnel showing stages with percentages | Read-only, clickable stages |
| Stage 1: Inquiries Received | numeric + percentage | Yes | Count and 100% baseline | Auto-calculated |
| Stage 2: Quotes Submitted | numeric + percentage | Yes | Count and % of inquiries | Shows conversion rate |
| Stage 3: Quotes Accepted | numeric + percentage | Yes | Count and % of quotes | Shows acceptance rate |
| Stage 4: Bookings Confirmed | numeric + percentage | Yes | Count and % of accepted | Shows booking rate |
| Stage 5: Treatments Completed | numeric + percentage | Yes | Count and % of bookings | Shows completion rate |
| Stage Details Table | data table | Yes | Breakdown by treatment type | Expandable rows |

**Business Rules**:

- Each funnel stage clickable to drill down into detailed list (e.g., click "Quotes Accepted" to see list of accepted quotes)
- Color coding: Green for high conversion (>industry benchmark), Yellow for average, Red for low
- Benchmark comparison overlay shows industry average conversion rates as dotted lines
- Bottleneck stage highlighted with warning icon if conversion < 50% of benchmark
- Minimum 10 inquiries required to display funnel (otherwise shows "Insufficient Data" message)

**Notes**:

- Use animated transitions when updating funnel based on filter changes
- Provide actionable recommendations beside low-performing stages (e.g., "Consider responding faster to inquiries")
- Include "Download Funnel Report" button to export as PDF with insights

---

### Screen 3: Financial Reports

**Purpose**: Detailed financial analytics including revenue trends, earnings breakdown, payment schedules

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Selector | dropdown | Yes | Filter for time period | Same as Dashboard |
| Revenue Trend Chart | line chart | Yes | Revenue over time (daily, weekly, monthly granularity) | Auto-calculated based on date range |
| Total Revenue | currency display | Yes | Sum of completed treatment revenue | Read-only |
| Total Platform Commission | currency display | Yes | Sum of Hairline commission deducted | Read-only, may be hidden per provider agreement |
| Net Earnings | currency display | Yes | Total revenue minus commission | Read-only, highlighted/bold |
| Revenue by Treatment Table | data table | Yes | Treatment type, count, total revenue, avg per procedure | Sortable columns |
| Revenue by Patient Location | pie chart | Yes | Geographic breakdown of patient origins | Interactive, click to filter |
| Upcoming Payments | data table | Yes | Scheduled payout date, amount, status | Linked to billing module |
| Previous Payments | data table | Yes | Payment date, amount, invoice link | Paginated, searchable |

**Business Rules**:

- Revenue only includes completed treatments (status = "Completed")
- Pending/in-progress treatments shown separately as "Projected Revenue"
- Commission visibility depends on provider agreement (some contracts hide platform commission from provider view)
- Upcoming payments calculated based on provider's configured payout frequency (weekly, bi-weekly, monthly)
- Payment schedule determined by treatment completion date + payout cycle
- All currency amounts displayed in provider's configured currency
- Historical exchange rates locked at time of treatment booking (no retrospective currency fluctuations)

**Notes**:

- Revenue trend chart allows granularity toggle (daily/weekly/monthly) based on date range length
- Export options: PDF (formatted report), CSV (raw data for further analysis)
- Include comparison to previous period (e.g., "Revenue up 15% vs last month")

---

### Screen 4: Comparative Benchmarks

**Purpose**: Display provider performance against anonymized industry averages for competitive positioning insights

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Benchmark Category Selector | tabs | Yes | Choose benchmark view (Regional, Clinic Size, Treatment Type) | At least one selected |
| Provider Metric | numeric/percentage | Yes | Provider's actual value for metric | Auto-calculated |
| Industry Average | numeric/percentage | Yes | Anonymized average across similar providers | Calculated by admin analytics |
| Variance | percentage display | Yes | Difference from average (+15%, -10%, etc.) | Color-coded: green positive, red negative |
| Percentile Ranking | visual indicator | Yes | Provider's position (e.g., "Top 25%") | Shown as progress bar |
| Benchmark Metrics | multi-metric table | Yes | Quote response time, acceptance rate, average quote value, patient satisfaction | Multiple rows |

**Business Rules**:

- Benchmarks only available if provider has minimum 10 completed treatments
- Industry averages calculated from providers in same:
  - Geographic region (country or city cluster)
  - Clinic size segment (small <50 procedures/year, medium 50-200, large >200)
  - Treatment specialization (e.g., only FUE-focused clinics)
- Benchmark data refreshed monthly (not real-time)
- Provider identity fully anonymized in benchmark calculations
- Admin configures minimum provider count for benchmark calculation (e.g., ≥5 providers required)
- If insufficient providers for segment, system shows broader benchmark (e.g., expand from city to country)

**Notes**:

- Include disclaimer: "Benchmarks based on anonymized data from similar providers. Individual results may vary."
- Provide contextual explanations for each metric (e.g., "Quote response time: Average hours from inquiry receipt to quote submission")
- Use visual indicators (progress bars, gauges) for easy comprehension
- Link to "Improvement Tips" for metrics below average

---

### Screen 5: Export Report Configuration

**Purpose**: Allow providers to customize and generate exportable reports (PDF, CSV)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Report Type | radio buttons | Yes | Choose export format (PDF Summary, CSV Detailed Data) | Must select one |
| Date Range | date picker | Yes | Start and end dates for report data | End date ≥ start date, max 12 months range |
| Include Sections | checkboxes | Yes | Select report sections (Overview, Funnel, Financial, Benchmarks) | At least one selected |
| Treatment Type Filter | dropdown | No | Filter by treatment type | Optional |
| Email Delivery | checkbox | No | Send report to provider's email | Optional, requires valid email |
| Schedule Recurring | checkbox | No | Enable automated report delivery | Optional |
| Recurrence Frequency | dropdown | No (conditional) | Weekly, Monthly, Quarterly | Required if recurring enabled |

**Business Rules**:

- PDF reports formatted with provider branding (logo, colors from profile)
- CSV exports include raw data for custom analysis in external tools
- Report generation may take 30-60 seconds for large data sets (show progress indicator)
- Generated reports stored temporarily (7 days) for re-download from "Report History" section
- Email delivery includes PDF attachment + secure link to download (link expires in 48 hours)
- Recurring reports automatically generated at end of period (e.g., monthly report sent on 1st of next month)
- Maximum 5 active recurring report configurations per provider (prevent system overload)

**Notes**:

- Display estimated file size before generation
- Include preview thumbnail for PDF reports
- Allow report configuration saving as templates for reuse
- Notify provider via email when report generation completes

---

## Business Rules

### General Module Rules

- **Rule 1**: Analytics data updates every 15 minutes from operational database (not real-time)
- **Rule 2**: Providers must have at least 5 inquiries and 3 quotes before comprehensive analytics features unlock
- **Rule 3**: All financial data displays in provider's configured currency (set in provider profile settings)
- **Rule 4**: Benchmark comparisons only available to providers with minimum 10 completed treatments
- **Rule 5**: Historical data available up to 24 months prior (older data archived and available upon request to admin)
- **Rule 6**: Date range filters limited to maximum 12-month spans (prevents performance issues with large data sets)
- **Rule 7**: Export file size limited to 50MB (CSV) and 10MB (PDF) to ensure deliverability

### Data & Privacy Rules

- **Privacy Rule 1**: Patient personal identifiers (names, contact details) never displayed in analytics views (only anonymized patient IDs or aggregated counts)
- **Privacy Rule 2**: Benchmark calculations fully anonymize provider data (no individual provider identifiable in industry averages)
- **Privacy Rule 3**: Provider performance data only visible to that provider's account users (not shared with other providers)
- **Privacy Rule 4**: Admin platform can view individual provider analytics for support and quality assurance purposes (logged for audit)
- **Audit Rule**: All analytics data access logged with timestamp, user ID, and data accessed (retained 12 months)
- **Compliance**: Analytics data handling complies with GDPR (data minimization, purpose limitation, access controls)

### Admin Editability Rules

**Editable by Admin**:

- Benchmark calculation methodology (regional groupings, clinic size thresholds, minimum provider counts)
- Metric definitions and calculation formulas (with version control to maintain consistency)
- Industry average refresh frequency (monthly, quarterly - default monthly)
- Alert thresholds for underperformance notifications (e.g., response time >72 hours)
- Report template designs (PDF layouts, branding elements)
- Maximum export file sizes and recurring report limits

**Fixed in Codebase (Not Editable)**:

- Core metrics definitions (inquiry count, quote acceptance rate, revenue) - standardized for consistency
- Data retention policy (24 months for active analytics, archival beyond)
- Analytics update frequency (15-minute pipeline runs)
- Currency conversion API integration (locked to prevent financial discrepancies)

**Configurable with Restrictions**:

- Admin can add new metrics to dashboard but cannot remove core metrics (inquiry, quotes, revenue)
- Admin can adjust benchmark segments but must maintain minimum 5 providers per segment
- Admin can customize report templates but must include required legal disclaimers

### Performance & Scalability Rules

- **Performance Rule 1**: Dashboard loads in <3 seconds for 95th percentile (pre-aggregated data caching)
- **Performance Rule 2**: Chart rendering completes in <1 second for date ranges up to 12 months
- **Performance Rule 3**: Export generation for PDF reports <60 seconds, CSV <30 seconds
- **Scalability Rule 1**: Analytics pipeline designed to support 1,000+ active providers without degradation
- **Scalability Rule 2**: Benchmark calculations run as overnight batch jobs (not on-demand) to prevent system load

---

## Success Criteria

### Provider Experience Metrics

- **SC-001**: Providers can view their complete performance dashboard in under 5 seconds from navigation click
- **SC-002**: 80% of providers access analytics dashboard at least weekly
- **SC-003**: Providers can identify their top-performing treatment type in under 30 seconds
- **SC-004**: Providers successfully generate and download PDF reports on first attempt 95% of the time
- **SC-005**: Providers understand benchmark comparisons without requiring support documentation (measured by <5% support ticket rate on benchmarks)

### Provider Efficiency Metrics

- **SC-006**: Providers using analytics demonstrate 20% higher quote acceptance rates within 3 months (compared to control group not using analytics)
- **SC-007**: Providers reduce average quote response time by 25% after viewing response time analytics
- **SC-008**: Providers adjust pricing strategies based on average price per graft comparisons, leading to 15% revenue increase
- **SC-009**: Providers identify and address conversion bottlenecks, improving booking conversion rate by 10%

### Admin Management Metrics

- **SC-010**: Admin team can identify underperforming providers (quote acceptance rate <25th percentile) in real-time dashboard view
- **SC-011**: Admin can generate platform-wide analytics reports summarizing all provider performance in under 2 minutes
- **SC-012**: Admin successfully onboards new providers with analytics access within 24 hours of first inquiry
- **SC-013**: 100% of provider analytics access logged for audit compliance

### System Performance Metrics

- **SC-014**: Analytics data pipeline processes updates every 15 minutes with 99.5% reliability
- **SC-015**: Dashboard loads with full data visualization in <3 seconds for 95% of requests
- **SC-016**: Export generation (PDF/CSV) completes within 60 seconds for 90% of requests
- **SC-017**: System supports 1,000 concurrent providers viewing analytics without performance degradation
- **SC-018**: Zero data loss in analytics aggregation pipeline (100% data integrity)

### Business Impact Metrics

- **SC-019**: Providers with active analytics usage demonstrate 30% higher platform retention rate (12-month retention comparison)
- **SC-020**: Platform quote-to-booking conversion rate increases by 15% across providers using analytics regularly
- **SC-021**: Provider satisfaction with platform increases by 20 points (NPS survey) after analytics launch
- **SC-022**: 60% of providers export reports at least once per month for business planning
- **SC-023**: Admin support tickets related to "How is my performance?" decrease by 50% after analytics rollout (self-service insights)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-003 / Module P-02**: Inquiry Submission & Distribution
  - **Why needed**: Inquiry data (count, timing, patient preferences) feeds analytics calculations
  - **Integration point**: Analytics pipeline queries inquiry database for submission timestamps, patient locations, treatment types requested

- **FR-004 / Module PR-02**: Quote Submission & Management
  - **Why needed**: Quote data (count, amounts, response times, acceptance status) is core to analytics
  - **Integration point**: Pipeline aggregates quote creation timestamps, values, status changes for conversion funnel and financial reports

- **FR-006 / Module P-03**: Booking & Scheduling
  - **Why needed**: Booking confirmation data determines conversion rates and revenue attribution
  - **Integration point**: Booking status changes (accepted → scheduled → confirmed) trigger analytics updates

- **FR-007 / Module P-03**: Payment Processing
  - **Why needed**: Payment transaction data required for revenue calculations and financial reports
  - **Integration point**: Payment completion events update provider revenue totals, commission calculations

- **FR-010 / Module PR-03**: Treatment Execution & Documentation
  - **Why needed**: Treatment completion status determines which revenue is "realized" vs "projected"
  - **Integration point**: Treatment status change to "Completed" triggers revenue recognition in analytics

- **FR-013 / Module P-02**: Reviews & Ratings
  - **Why needed**: Patient satisfaction ratings included in provider performance metrics and benchmarks
  - **Integration point**: Review submissions update provider average rating displayed in analytics

- **FR-015 / Module A-02**: Provider Management (Admin)
  - **Why needed**: Provider profile data (location, clinic size, treatment specializations) determines benchmark segments
  - **Integration point**: Provider classification attributes used to group providers for industry average calculations

### External Dependencies (APIs, Services)

- **External Service 1**: Currency Conversion API (xe.com, fixer.io, or similar)
  - **Purpose**: Convert multi-currency revenue data to provider's preferred currency for consistent reporting
  - **Integration**: Scheduled API calls every 24 hours to fetch exchange rates, stored in currency_rates table
  - **Failure handling**: Use cached rates from previous day if API unavailable; display notice "Exchange rates as of [date]"

- **External Service 2**: PDF Generation Library (e.g., wkhtmltopdf, Puppeteer)
  - **Purpose**: Render HTML report templates into formatted PDF exports
  - **Integration**: Server-side service accepts HTML + CSS template, outputs PDF file
  - **Failure handling**: Fall back to simplified PDF layout if complex rendering fails; notify user of degraded export quality

- **External Service 3**: Data Warehouse / Analytics Database (if separate from operational DB)
  - **Purpose**: Store aggregated analytics data optimized for fast querying (separate from transactional database)
  - **Integration**: Nightly ETL jobs extract, transform, load operational data into analytics schema
  - **Failure handling**: Analytics display most recent successfully processed data with timestamp notice

### Data Dependencies

- **Entity 1**: Inquiry records with complete metadata
  - **Why needed**: Cannot calculate inquiry-related metrics without inquiry data
  - **Source**: Inquiry Submission module (FR-003), must include timestamps, patient location, treatment types

- **Entity 2**: Quote records with pricing and status history
  - **Why needed**: Quote acceptance rates and average values central to analytics
  - **Source**: Quote Management module (FR-004), must include submission timestamp, acceptance/rejection status, final amounts

- **Entity 3**: Booking and payment records
  - **Why needed**: Revenue calculations require confirmed bookings with payment details
  - **Source**: Booking (FR-006) and Payment (FR-007) modules, must include payment completion timestamps and amounts

- **Entity 4**: Provider profile classifications (region, clinic size, specializations)
  - **Why needed**: Benchmark segmentation requires provider categorization
  - **Source**: Provider Management module (FR-015), must be kept current as providers grow/change

- **State 1**: Historical data for trend analysis (minimum 30 days)
  - **Why needed**: Cannot show trends or "vs previous period" comparisons without historical baseline
  - **Source**: Continuous data collection from day 1 of provider onboarding, retained 24 months

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Providers have business acumen to interpret analytics data (quote acceptance rates, conversion funnels) without extensive training
- **Assumption 2**: Providers will check analytics dashboard at least weekly to monitor performance
- **Assumption 3**: Providers are motivated by benchmark comparisons and will take action to improve underperforming metrics
- **Assumption 4**: Providers prefer visual dashboards (charts, graphs) over raw data tables for quick insights
- **Assumption 5**: Providers will export reports monthly for internal business reviews or accounting

### Technology Assumptions

- **Assumption 1**: Providers access platform via desktop/laptop browsers for analytics (not mobile-optimized initially, mobile responsive as future enhancement)
- **Assumption 2**: Providers have reliable internet connectivity for loading data-heavy dashboard visualizations
- **Assumption 3**: Providers' browsers support modern JavaScript charting libraries (Chart.js, D3.js) - Chrome, Firefox, Safari latest 2 versions
- **Assumption 4**: CSV exports can be opened in Excel, Google Sheets, or equivalent spreadsheet software
- **Assumption 5**: Email infrastructure can reliably deliver report attachments up to 10MB without spam filtering

### Business Process Assumptions

- **Assumption 1**: Providers consider platform analytics sufficiently valuable to influence business decisions (pricing, staffing, marketing)
- **Assumption 2**: Providers trust anonymized benchmark data as accurate representation of industry performance
- **Assumption 3**: Admin team reviews platform-wide analytics monthly to identify trends and support needs
- **Assumption 4**: Providers understand commission structures and can interpret net earnings calculations
- **Assumption 5**: Currency conversion rates fetched daily are sufficient accuracy for multi-currency reporting (hourly updates not required)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Analytics pipeline operates as independent service separate from transactional database (prevents analytics queries from impacting operational performance)
- **Data Storage**: Use columnar data warehouse (e.g., PostgreSQL with Citus, Amazon Redshift, Google BigQuery) optimized for analytical queries
- **Caching Strategy**: Pre-aggregate common metrics (daily revenue totals, quote counts) overnight to accelerate dashboard loads
- **Real-Time vs Batch**: Core metrics updated every 15 minutes via scheduled jobs; complex aggregations (benchmarks) calculated nightly
- **Charting**: Use responsive JavaScript libraries (Chart.js for simplicity, D3.js for advanced visualizations) with fallback to static images if JS disabled

### Integration Points

- **Integration 1**: Operational Database → Analytics Pipeline
  - **Data format**: Scheduled queries extract new/updated records (inquiries, quotes, bookings, payments) every 15 minutes
  - **Authentication**: Service-to-service API authentication with read-only database credentials
  - **Error handling**: Log failed extraction runs, retry up to 3 times, alert admin if persistent failures

- **Integration 2**: Analytics Service → Provider Web App
  - **Data format**: RESTful JSON APIs for metrics retrieval (`GET /api/v1/providers/{id}/analytics?period=30d`)
  - **Authentication**: OAuth 2.0 provider bearer tokens validated on each request
  - **Error handling**: Return cached metrics if live calculation fails; display timestamp of cached data

- **Integration 3**: Provider Web App → Report Generation Service
  - **Data format**: HTTP POST with report configuration (date range, sections, format)
  - **Authentication**: Same OAuth 2.0 tokens
  - **Error handling**: Return error message if generation fails, suggest retry or alternative format

- **Integration 4**: Currency Conversion API → Analytics Service
  - **Data format**: JSON response with daily exchange rates for supported currencies
  - **Authentication**: API key in request headers
  - **Error handling**: Use previous day's cached rates if API call fails; display notice to provider

### Scalability Considerations

- **Current scale**: Expected 100 active providers at launch, each receiving 10-50 inquiries/month
- **Growth projection**: Plan for 1,000 providers within 12 months, 50-200 inquiries/month per provider
- **Peak load**: Dashboard access peaks Monday mornings (providers reviewing weekend inquiries) - expect 200+ concurrent requests
- **Data volume**: Estimate 500GB analytics data storage first year (inquiries, quotes, bookings, aggregated metrics)
- **Scaling strategy**:
  - Horizontal scaling of analytics API servers (load balanced)
  - Database read replicas for analytics queries (separate from write master)
  - CDN caching for static chart images and report templates
  - Asynchronous report generation queue (prevents blocking requests)

### Security Considerations

- **Authentication**: Providers must authenticate via platform login to access analytics (no public endpoints)
- **Authorization**: Role-based access: Owner and Admin roles see full analytics; Staff roles see limited views (no financial data)
- **Encryption**: Analytics API responses encrypted in transit (TLS 1.3); sensitive financial data encrypted at rest (AES-256)
- **Audit trail**: All analytics data access logged with user ID, timestamp, IP address, data requested (retained 12 months for compliance audits)
- **Threat mitigation**: Rate limiting on analytics API endpoints (100 requests/hour/provider to prevent data scraping)
- **Data Privacy**: Patient PII never exposed in analytics views (aggregate counts and anonymized IDs only)
- **Compliance**: GDPR compliant data processing (providers are data controllers for their analytics; Hairline is processor)

---

## User Scenarios & Testing

### User Story 1 - New Provider Monitors Initial Performance (Priority: P1)

A newly onboarded provider wants to understand if their quote response strategy is effective after their first 2 weeks on the platform.

**Why this priority**: Core value proposition - providers need immediate feedback on performance to optimize strategy early.

**Independent Test**: Can be fully tested by creating a provider account with 2 weeks of simulated inquiry/quote data and verifying dashboard displays accurate metrics.

**Acceptance Scenarios**:

1. **Given** provider has received 10 inquiries and submitted 7 quotes over 14 days, **When** provider navigates to Analytics dashboard, **Then** system displays accurate counts, 70% quote submission rate, and average response time
2. **Given** provider's average response time is 18 hours, **When** dashboard loads, **Then** system displays green indicator (under 24-hour benchmark) and "Excellent response time!" message
3. **Given** provider has only 7 quotes submitted, **When** provider clicks "Show Benchmarks", **Then** system displays message "Benchmarks available after 10 completed treatments" with progress indicator

---

### User Story 2 - Established Provider Analyzes Conversion Bottleneck (Priority: P1)

An established provider notices declining booking conversion rates and wants to identify where patients are dropping off in the journey.

**Why this priority**: Critical for provider retention - analytics must help providers troubleshoot and improve performance or they'll disengage.

**Independent Test**: Create provider with 3 months of data showing declining conversion, verify funnel identifies specific drop-off stage.

**Acceptance Scenarios**:

1. **Given** provider has 100 inquiries, 80 quotes, 30 accepted quotes, 25 confirmed bookings, **When** provider views Conversion Funnel, **Then** system highlights "Quotes Accepted" stage as bottleneck (37.5% conversion vs 50% benchmark)
2. **Given** bottleneck identified at quote acceptance stage, **When** provider hovers over stage, **Then** system displays actionable tip: "Consider adjusting pricing or highlighting value-adds in quotes"
3. **Given** provider clicks on "Quotes Accepted" stage, **When** drill-down loads, **Then** system displays list of accepted quotes with timestamps, patient locations, and treatment types for detailed analysis

---

### User Story 3 - Provider Optimizes Pricing Strategy Using Benchmarks (Priority: P2)

A provider wants to ensure their pricing is competitive by comparing average quote amounts against industry benchmarks for their region.

**Why this priority**: High value but not critical - providers can operate without benchmarks, but feature significantly enhances strategic decision-making.

**Independent Test**: Configure benchmark data with anonymized averages, verify provider sees accurate comparisons and variance indicators.

**Acceptance Scenarios**:

1. **Given** provider's average quote is £2,200 and regional benchmark is £2,500, **When** provider views Benchmarks screen, **Then** system displays "Your avg: £2,200 | Industry avg: £2,500 | -12% below average" with red indicator
2. **Given** provider is priced below average, **When** provider reviews price-per-graft comparison, **Then** system shows provider at £0.88/graft vs benchmark £1.00/graft, suggesting potential for price increase
3. **Given** provider decides to adjust pricing, **When** provider returns to analytics 30 days later, **Then** system shows updated average quote amount and new variance vs benchmark

---

### User Story 4 - Multi-Location Clinic Reviews Revenue by Location (Priority: P2)

A provider operating clinics in multiple cities wants to understand which location generates the most revenue and patient volume.

**Why this priority**: Useful for multi-location operators but not applicable to single-clinic providers (majority), so P2.

**Independent Test**: Create provider with inquiries/bookings tagged to different clinic locations, verify revenue breakdown by location.

**Acceptance Scenarios**:

1. **Given** provider has clinics in Istanbul and Ankara with 60/40 revenue split, **When** provider views Financial Reports, **Then** system displays pie chart showing Istanbul 60% (£30,000) and Ankara 40% (£20,000)
2. **Given** provider selects "Istanbul" clinic from location filter, **When** dashboard updates, **Then** system shows only Istanbul-specific metrics (inquiries, quotes, revenue)
3. **Given** provider wants detailed location comparison, **When** provider exports CSV report with location breakdown, **Then** CSV includes location column for all transactions

---

### User Story 5 - Provider Schedules Automated Monthly Reports (Priority: P3)

A provider wants to receive automated monthly performance reports via email for internal business review meetings without manual export.

**Why this priority**: Convenience feature that enhances user experience but not essential for core analytics functionality.

**Independent Test**: Configure recurring report, simulate month-end, verify email delivery with correct attachment and data.

**Acceptance Scenarios**:

1. **Given** provider configures monthly recurring report for "Financial Summary" sections, **When** provider saves configuration, **Then** system displays confirmation "Monthly report scheduled for 1st of each month at 9:00 AM"
2. **Given** recurring report configured, **When** month ends and system generates report, **Then** provider receives email with PDF attachment and download link by 9:00 AM on 1st
3. **Given** provider wants to modify recurring report, **When** provider accesses Report History and clicks "Edit Schedule", **Then** system allows changes to frequency, sections, and email recipients

---

### User Story 6 - Admin Identifies Underperforming Provider for Support (Priority: P2)

An admin monitors platform-wide provider analytics and identifies a provider with unusually high inquiry volume but low quote submission rate, indicating potential support need.

**Why this priority**: Important for platform quality but admin-facing (not direct provider value), so P2.

**Independent Test**: Create provider with anomalous metrics (high inquiries, low quotes), verify admin dashboard flags provider.

**Acceptance Scenarios**:

1. **Given** Provider A has 50 inquiries but only 10 quotes (20% submission rate vs 70% average), **When** admin views Platform Analytics dashboard, **Then** system displays Provider A in "Providers Needing Attention" list with red flag
2. **Given** admin clicks on flagged provider, **When** provider detail view loads, **Then** system displays provider's full analytics, contact info, and "Send Support Message" button
3. **Given** admin identifies issue (provider doesn't understand quote creation process), **When** admin sends targeted help resources, **Then** provider's quote submission rate improves over next 2 weeks (measurable in follow-up analytics)

---

### Edge Cases

- **What happens when provider has zero inquiries for selected date range?**
  - System displays zero-state message: "No inquiries received in this period. Try expanding your date range or reviewing your profile visibility settings."
  - Charts show empty state with helpful tips for attracting inquiries

- **How does system handle provider switching currencies mid-period?**
  - Historical revenue data remains in original currency; new data uses new currency
  - Dashboard displays notice: "Currency changed on [date]. Revenue before [date] shown in [old currency], after in [new currency]."
  - Totals calculated using exchange rates at transaction time to ensure accuracy

- **What occurs if benchmark calculation has insufficient providers (<5 in segment)?**
  - System expands benchmark scope (e.g., city → country → global)
  - Displays notice: "Regional benchmark unavailable. Showing country-level average from [N] providers."
  - If still insufficient, hides benchmark comparison with message "Benchmarks available when more providers join your region"

- **How does system handle quote with multiple treatment types?**
  - Analytics attribute full revenue to primary treatment type (first selected in quote)
  - Alternative: Split revenue proportionally if treatment packages have itemized pricing
  - Admin can configure attribution methodology in analytics settings

- **What happens during analytics pipeline outage (failed 15-minute update)?**
  - Dashboard displays cached data with prominent notice: "Data last updated at [timestamp]. Experiencing delays in updates."
  - System automatically retries pipeline run every 15 minutes until recovery
  - Admin receives alert if outage exceeds 1 hour for investigation

- **How does system handle provider with very long quote response times (>7 days)?**
  - Average response time may skew high; display median response time as additional metric
  - Highlight slow quotes in drill-down view for provider review
  - System may flag provider to admin if response time consistently exceeds 72 hours (configurable threshold)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-014-001**: System MUST display provider performance dashboard with key metrics: inquiry count, quote count, quote acceptance rate, booking conversion rate, total revenue, average quote amount, average price per graft, average response time
- **REQ-014-002**: System MUST calculate metrics from operational data (inquiries, quotes, bookings, payments) with maximum 15-minute lag between transaction and analytics reflection
- **REQ-014-003**: Providers MUST be able to filter dashboard by date range (last 7/30/90 days, last 12 months, custom range)
- **REQ-014-004**: Providers MUST be able to filter analytics by treatment type (FUE, FUT, DHI, etc.)
- **REQ-014-005**: System MUST display conversion funnel visualization showing patient journey stages: Inquiries Received → Quotes Submitted → Quotes Accepted → Bookings Confirmed → Treatments Completed
- **REQ-014-006**: System MUST provide comparative benchmarks showing provider performance against anonymized industry averages (regional, clinic size, treatment type segments)
- **REQ-014-007**: Providers MUST be able to export analytics reports in PDF (formatted summary) and CSV (detailed data) formats
- **REQ-014-008**: System MUST generate financial reports including revenue trends, earnings breakdown by treatment type, upcoming payment schedules, previous payment history

### Data Requirements

- **REQ-014-009**: System MUST aggregate data from inquiry, quote, booking, payment, and treatment execution modules to calculate analytics
- **REQ-014-010**: System MUST maintain 24-month historical analytics data for trend analysis and year-over-year comparisons
- **REQ-014-011**: System MUST convert multi-currency financial data to provider's preferred currency using daily exchange rates
- **REQ-014-012**: System MUST store pre-aggregated metrics (daily inquiry counts, revenue totals) for fast dashboard loading

### Visualization Requirements

- **REQ-014-013**: System MUST render interactive charts (line charts for trends, bar charts for comparisons, pie charts for distribution, funnel charts for conversion)
- **REQ-014-014**: Charts MUST support tooltips displaying exact values on hover
- **REQ-014-015**: Charts MUST be responsive and render correctly on desktop and tablet viewports
- **REQ-014-016**: System MUST display trend indicators (up/down arrows) comparing current period to previous equivalent period

### Security & Privacy Requirements

- **REQ-014-017**: System MUST enforce authentication and authorization - only logged-in provider users can access their own analytics
- **REQ-014-018**: System MUST anonymize patient personal identifiers in all analytics views (no names, contact details, only counts and IDs)
- **REQ-014-019**: System MUST fully anonymize provider identities in benchmark calculations (no provider can identify competitors in averages)
- **REQ-014-020**: System MUST log all analytics data access with user ID, timestamp, and data accessed for audit compliance

### Integration Requirements

- **REQ-014-021**: Analytics pipeline MUST extract data from inquiry, quote, booking, payment, treatment modules every 15 minutes
- **REQ-014-022**: System MUST integrate with currency conversion API for multi-currency reporting (daily rate updates)
- **REQ-014-023**: Report generation service MUST accept configuration (date range, sections, format) and produce PDF or CSV output within 60 seconds

### Export & Reporting Requirements

- **REQ-014-024**: System MUST allow providers to schedule recurring reports (weekly, monthly, quarterly) with automated email delivery
- **REQ-014-025**: System MUST store generated reports for 7 days in "Report History" for re-download
- **REQ-014-026**: Exported PDF reports MUST include provider branding (logo, colors) and formatted visualizations
- **REQ-014-027**: Exported CSV files MUST include raw data with column headers and be compatible with Excel/Google Sheets

### Admin Requirements

- **REQ-014-028**: Admin platform MUST aggregate provider analytics across entire platform for oversight dashboard
- **REQ-014-029**: Admin MUST be able to configure benchmark calculation methodology (segments, minimums, refresh frequency)
- **REQ-014-030**: Admin MUST be able to identify underperforming providers via platform analytics dashboard
- **REQ-014-031**: Admin MUST be able to audit individual provider analytics access logs for compliance

---

## Key Entities

- **Entity 1 - Analytics Metrics Aggregate**
  - **Key attributes** (conceptual): provider_id, date, inquiry_count, quote_count, quote_acceptance_rate, booking_conversion_rate, total_revenue, average_quote_amount, average_response_time, currency
  - **Relationships**: One provider has many daily metric aggregates; aggregates roll up to weekly/monthly summaries

- **Entity 2 - Benchmark Segment**
  - **Key attributes**: segment_id, segment_type (regional, clinic_size, treatment_type), segment_value (e.g., "Turkey-Istanbul", "Small Clinic <50/year", "FUE-focused"), provider_count, metric_averages (JSON), calculation_date
  - **Relationships**: One segment contains many providers; each provider belongs to multiple segments (regional AND size AND treatment)

- **Entity 3 - Export Report Configuration**
  - **Key attributes**: config_id, provider_id, report_type (PDF, CSV), date_range_type (last_30d, custom), included_sections (array), recurring (boolean), frequency (weekly, monthly), email_recipients, created_at, last_generated_at
  - **Relationships**: One provider has many report configurations; each configuration generates many report instances (history)

- **Entity 4 - Report History**
  - **Key attributes**: report_id, config_id, provider_id, generated_at, file_url, file_size, expiry_date, download_count
  - **Relationships**: One report configuration has many report instances; reports expire after 7 days

- **Entity 5 - Currency Exchange Rate**
  - **Key attributes**: date, base_currency, target_currency, exchange_rate, source_api, fetched_at
  - **Relationships**: Used by analytics pipeline to convert multi-currency revenue; one date has many currency pairs

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-014 Provider Analytics & Reporting | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-11
