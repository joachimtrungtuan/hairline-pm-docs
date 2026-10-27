# FR-003 - Inquiry Submission & Distribution

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr003-inquiry-submission`  
**Created**: 2025-10-23  
**Status**: 🟡 Revised — Pending Consolidated Verification  
**Source**: FR-003 from system-prd.md  
**Change Request**: [CR-FR003-20261014-01 — Provider status cancellation cascade](change-request-2026-10-14-provider-status-cancellation-cascade.md)
**Change Request**: [CR-FR003-20261015-01 — Distribution requires a set password](change-request-2026-10-15-distribution-requires-password-set.md)
**Change Request**: [CR-FR003-20261016-01 — Quote model alignment: provider fault after acceptance keeps the inquiry open](change-request-2026-10-16-mtg002-quote-model-alignment.md)
**Change Request**: [CR-FR003-20261027-01 — Legacy status value migration](change-request-2026-10-27-legacy-status-value-migration.md)
**Change Request**: [CR-FR003-20261027-02 — Automatic redistribution when a provider-status cascade removes the last live offer](change-request-2026-10-27-pre-acceptance-redistribution.md)

## Executive Summary

The Inquiry Submission & Distribution module enables patients to submit comprehensive treatment requests through the mobile app, which are then automatically distributed to relevant providers based on location and availability. The module supports multi-country selection, detailed medical questionnaires, head scan capture *(V1 photo set; true 3D in V2)*, and comprehensive inquiry management across all platform tenants.
In V1, "3D head scan" capture is implemented as a standardized head scan photo set (multiple 2D views). True 3D capture is deferred to V2.

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Quote Request & Management
- **Provider Platform (PR-02)**: Inquiry & Quote Management  
- **Admin Platform (A-01)**: Patient Management & Oversight

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- Create and manage inquiries on mobile (service selection, destinations, medical questionnaire, media upload, date ranges)
- Resume drafts; view inquiry dashboard and status timeline
- Review anonymized provider responses (quotes handled by FR-004)

**Provider Platform (PR-02)**:

- View distributed inquiries with anonymized patient info and medical alerts
- Review inquiry details including head scan capture assets *(V1 photo set; true 3D in V2)* and questionnaire
- Manage inquiry status prior to quote creation (quote creation in FR-004)

**Admin Platform (A-01)**:

- Global oversight of all inquiries across lifecycle stages
- Edit/override inquiry details; reassign providers; soft-delete with audit
- Configure distribution rules and expirations aligned with system PRD

**Shared Services (S-XX)**:

- Notification service for distribution and status changes
- Media service for secure storage and retrieval of head scan capture assets *(V1 photo sets; V2 true 3D)*
- Audit logging, anonymization and soft delete utilities

### Communication Structure

**In Scope**:

- Patient → System: Inquiry submission with comprehensive data
- System → Provider: Automatic inquiry distribution and notifications
- Provider → System: Inquiry management prior to quote (quotes in FR-004)
- Admin → All Parties: Oversight, edit, and management actions
- Structured Updates: System-generated notifications and status updates

**Out of Scope**:

- Direct patient-provider chat (handled by FR-012)

### Entry Points

1. **Patient-Initiated**: Primary flow through mobile app inquiry creation
2. **Admin-Managed**: Direct inquiry creation and management by admin team
3. **Provider-Viewed**: Provider access to distributed inquiries

## Business Workflows

### Workflow 1: Patient Inquiry Creation (Primary Flow)

**Actors**: Patient, System, Medical Questionnaire Engine, Head Scan Media Service  
**Trigger**: Patient starts a new inquiry in the mobile app and proceeds through the creation steps  
**Outcome**: A complete inquiry is created with destinations, media, head scan reference, date ranges, and medical questionnaire; inquiry ID generated

**Flow Diagram**:

```mermaid
flowchart TD
    Start["Service Selection"] --> Service["Patient opens mobile app and selects &quot;Get a Hair Transplant&quot;<br/>System retrieves the active treatment-area catalog<br/>Patient selects one active treatment-area option<br/>System validates patient eligibility"]
    Service --> Eligible{"Eligibility valid?"}
    Eligible -->|No| EligibleErr["Show eligibility error + block progression"]
    Eligible -->|Yes| Dest["Destination Selection<br/>Patient selects preferred countries/locations (max 10 countries)<br/>System displays starting prices for each location<br/>Patient can select multiple destinations<br/>System suggests nearest countries to patient's location first"]

    Dest --> DestOk{"Destination selection valid?"}
    DestOk -->|No| DestErr["Show validation error + stay on destination selection"] --> Dest
    DestOk -->|Yes| Details["Detailed Information Collection<br/>Patient provides detailed hair concerns:<br/>- Nature of concern (text)<br/>- Duration of concern (dropdown enum)<br/>- Previous treatments (text)<br/>- Symptom severity (1-10 slider)<br/>- Lifestyle factors (optional text)<br/>- Additional notes (optional text)"]

    Details --> Upload["Visual Evidence Upload<br/>Patient uploads visual evidence (max 5 photos/videos)<br/>Photos: JPG/PNG &lt;= 2MB each<br/>Videos: MP4 &lt;= 30s, &lt;= 20MB each"]
    Upload --> MediaOk{"Uploads meet policy?"}
    MediaOk -->|No| MediaErr["Show upload policy error + require changes"] --> Upload
    MediaOk -->|Yes| Scan["Head Scan Photo Set Capture (V1)<br/>Patient receives capture instructions<br/>Patient captures standardized head scan photo set (multiple 2D views)<br/>System validates capture quality<br/>Media stored for provider review"]

    Scan --> ScanOk{"Scan quality valid?"}
    ScanOk -->|No| Retake["Prompt retake + guidance"] --> Scan
    ScanOk -->|Yes| Dates["Treatment Date Selection<br/>Patient selects preferred treatment dates (max 10 date ranges)<br/>Date ranges can be up to 2 years in the future<br/>Patient can select multiple non-overlapping ranges<br/>System validates date availability"]

    Dates --> DatesOk{"Date selection valid?"}
    DatesOk -->|No| DatesErr["Show validation error + stay on date selection"] --> Dates
    DatesOk -->|Yes| Med["Medical Questionnaire Completion<br/>Patient completes comprehensive medical questionnaire (allergies, medications, chronic diseases, previous surgeries, etc.)<br/>Each question requires Yes/No answer<br/>Detailed explanation required for &quot;Yes&quot; answers<br/>System applies 3-tier medical alert system:<br/>- Critical (red)<br/>- Standard (yellow/amber)<br/>- None (green)"]

    Med --> MedOk{"Questionnaire complete + valid?"}
    MedOk -->|No| MedErr["Show validation error + stay on medical questionnaire"] --> Med
    MedOk -->|Yes| ProviderSel["Provider Selection<br/>Patient selects preferred providers (max 5 providers) on Screen 7a<br/>System suggests providers based on positive reviews and admin curation<br/>Patient can search/filter providers by country, rating, and specialty"]

    ProviderSel --> ProvOk{"Provider selection valid?"}
    ProvOk -->|No| ProvErr["Show validation error + stay on provider selection"] --> ProviderSel
    ProvOk -->|Yes| Review["Inquiry Review &amp; Submission<br/>Patient reviews complete inquiry summary (including selected providers)<br/>Patient confirms all information accuracy<br/>Patient submits inquiry to system<br/>System generates unique inquiry ID (HPID format)"]

    Review --> SubmitOk{"Submission succeeds?"}
    SubmitOk -->|No| SubmitErr["Show submission error + allow retry"] --> Review
    SubmitOk -->|Yes| Created["Inquiry created (HPID generated)"]
```

### Alternative Flows

**A1: Patient abandons inquiry mid-process**:

- **Trigger**: Patient leaves the inquiry creation flow before submission
- **Outcome**: Draft saved; patient can resume within 7 days
- **Flow Diagram**:

```mermaid
flowchart TD
    Exit["Patient abandons inquiry mid-process (before submission)"] --> Save["System saves draft automatically"]
    Save --> Resume{"Patient returns within 7 days?"}
    Resume -->|Yes| Continue["Patient can resume from last completed step"]
    Resume -->|No| Expire["Draft expires after 7 days of inactivity"]
```

**A2: Patient has existing incomplete inquiry**:

- **Trigger**: Patient returns to the app with an existing incomplete inquiry
- **Outcome**: Patient resumes or modifies existing inquiry
- **Flow Diagram**:

```mermaid
flowchart TD
    Start["Patient returns to app with an existing incomplete inquiry"] --> Prompt["System shows &quot;continue with your request&quot; option"]
    Prompt --> Resume["Patient can resume from last completed step"]
    Resume --> CanEdit{"Inquiry still in &quot;Inquiry&quot; stage?"}
    CanEdit -->|Yes| Modify["Patient can modify existing inquiry"]
    CanEdit -->|No| Block["Show blocked message (stage changed)"]
    Modify --> Status["System displays inquiry status as &quot;incomplete&quot; or &quot;pending&quot;"]
```

**A3: Medical questionnaire reveals critical conditions**:

- **Trigger**: Patient answers indicate high-risk medical conditions
- **Outcome**: Inquiry flagged with critical alerts for provider awareness (not patient rejection)
- **Flow Diagram**:

```mermaid
flowchart TD
    Detect["Medical questionnaire reveals critical conditions"] --> Flag["System flags inquiry with critical medical alerts (red indicators)"]
    Flag --> Providers["Providers are alerted to high-risk conditions"]
    Providers --> Admin["Admin can review and provide guidance to providers"]
    Admin --> Note["Note: Medical alerts are for provider awareness, not patient rejection"]
```

**A4: Patient cancels inquiry (see Workflow 5)**:

- **Trigger**: Patient initiates cancellation from Inquiry Dashboard (Screen 8) in stages: Inquiry or Quoted. From acceptance onward the patient sees "Contact support" instead, and only an admin can cancel the booking (FR-006).
- **Outcome**: Inquiry cancelled; quotes auto-cancelled; providers notified; inquiry becomes read-only
- **Flow Diagram**:

```mermaid
flowchart TD
    Start["Patient initiates cancellation from Inquiry Dashboard (Screen 8)<br/>in stages: Inquiry or Quoted"] --> Eligible{"Stage eligible?"}
    Eligible -->|No| Block["Block cancellation + message: Contact support"]
    Eligible -->|Yes| Process["System validates eligibility, captures cancellation reason, and processes cancellation"]
    Process --> Cascade["All associated quotes auto-cancelled; providers notified;<br/>inquiry becomes read-only"]
    Cascade --> New["Patient can immediately create a new inquiry (no cooldown;<br/>one-active-inquiry rule still applies)"]
    New --> Ref["See Workflow 5 for full cancellation behavior"]
```

---

### Workflow 2: Inquiry Distribution (System Flow)

**Actors**: System, Providers, Admin  
**Trigger**: System detects a newly submitted inquiry meeting completeness requirements  
**Outcome**: Inquiry is distributed to matching providers; provider dashboards updated and notifications sent

**Flow Diagram**:

```mermaid
flowchart TD
    Start["System receives submitted inquiry"] --> Validate{"Inquiry complete + valid?"}

    Validate -->|No| Invalid["Do not distribute; return errors / flag for fix"]
    Validate -->|Yes| Identify["Generate inquiry ID (HPID) + timestamps"]

    Identify --> Exclusive{"FR-037 monitoring conversion with exclusive<br/>assigned provider?"}
    Exclusive -->|Yes| ExclusiveRoute["Route only to the assigned provider;<br/>skip country/selection matching and the 10-provider cap"]
    Exclusive -->|No| Match["Match eligible providers (Active, password set) by selected countries + explicit selections"]
    Match --> Cap{"Matched providers &gt; 10?"}
    Cap -->|Yes| Select10["Select up to 10 providers (ensure explicitly selected providers included; remaining per matching rules)"]
    Cap -->|No| Matched["Use matched provider list"]

    Select10 --> Views["Create provider-specific inquiry views (anonymized)"]
    Matched --> Views
    ExclusiveRoute --> Views

    Views --> Found{"Any providers to distribute to?"}
    Found -->|No| Manual["Notify admin: unmatched inquiry + manual assignment"]
    Manual --> Delay["Optionally notify patient of delay"]

    Found -->|Yes| Distribute["Distribute inquiry to providers + record timestamps"]
    Distribute --> Notify["Send provider notifications (within 5 minutes)"]
    Notify --> NotifyOk{"Notification dispatch OK?"}
    NotifyOk -->|No| Retry["Queue/retry + alert on SLA risk; log attempts"] --> Access
    NotifyOk -->|Yes| Access["Provider views enforce anonymization until payment<br/>+ medical alerts shown prominently"]
```

### Alternative Flows

**B1: No providers available in selected countries**:

- **Trigger**: No active providers found in patient's selected countries
- **Outcome**: Admin manually assigns providers; patient notified of potential delay
- **Flow Diagram**:

```mermaid
flowchart TD
    Start["System attempts provider matching"] --> Found{"Any providers matched?"}
    Found -->|No| NotifyAdmin["System notifies admin of unmatched inquiry"]
    NotifyAdmin --> Manual["Admin manually assigns providers"]
    Manual --> NotifyPatient["Patient notified of potential delay (optional)"]
    Found -->|Yes| Continue["Proceed with normal distribution"]
```

**B2: Provider capacity exceeded**:

- **Trigger**: Provider's inquiry capacity is reached
- **Outcome**: Deferred to separate FR for provider capacity management
- **Flow Diagram**:

```mermaid
flowchart TD
    Start["System considers provider capacity signals (if available)"] --> Gate{"Provider capacity exceeded?"}
    Gate -->|Yes| Advisory["Capacity checks are advisory in MVP;<br/>do NOT block inquiry distribution"]
    Gate -->|No| Continue["Proceed with normal distribution"]
    Advisory --> Continue
```

**B3: Inquiry originates from a monitoring-case conversion with an exclusive assigned provider**:

- **Trigger**: Inquiry is created via FR-037 (Monitor Your Hair Loss) conversion, and the source monitoring case has an active provider assignment at the time of conversion (REQ-037-029, Business Rule 7)
- **Outcome**: Normal country/selection matching and the 10-provider distribution cap are bypassed; the inquiry is distributed exclusively to the assigned provider. Standard anonymization, notification timing, and dashboard behavior are unchanged
- **Flow Diagram**:

```mermaid
flowchart TD
    Start["Inquiry created via FR-037 conversion"] --> Check{"Source monitoring case has<br/>an active provider assignment?"}
    Check -->|No| Normal["Proceed with normal distribution (Workflow 2 main flow)"]
    Check -->|Yes| Exclusive["Distribute exclusively to the assigned provider;<br/>skip matching + 10-provider cap"]
    Exclusive --> Views["Create provider-specific inquiry view (anonymized)"]
    Views --> Notify["Send provider notification (within 5 minutes)"]
```

**B4: Provider becomes Suspended or Deactivated**:

- **Trigger**: A provider's `Suspended` or `Deactivated` status becomes effective under FR-015 (Alternative Flow A5 and Screen 4).
- **Steps**:
  1. From the effective time, the provider is ineligible for new inquiry allocation. Workflow 2 matching, exclusive routing, and Workflow 4 reassignment revalidate provider status immediately before creating a ProviderInquiry; in-flight distribution jobs, retries, or callbacks MUST NOT create or reopen that provider's participation.
  2. If the inquiry's accepted treatment belongs to the affected provider (stage Accepted, Confirmed, In Progress, or Aftercare), the inquiry is not cancelled; it keeps its current stage and is flagged `supportRequired = true`. FR-006 Alternative Flow B4 records cause `ProviderSuspended` or `ProviderDeactivated` on the booking. Before treatment starts (Accepted or Confirmed), B4 closes the booking and an admin rehomes the patient to a replacement provider in the same inquiry through FR-006 Alternative Flow B5. An `In Progress` booking is not closed or transferred; it stays `In Progress` and an admin decides under FR-006 Alternative Flow B7 whether to move it to Aftercare with aftercare reassignment or cancel it with a reason. An `Aftercare` booking stays `Aftercare` and follows the aftercare reassignment in FR-006 Alternative Flow B6. FR-004 cancels the provider's unaccepted quotes; FR-005 and FR-006 own hold release, payment blocking, and the linked replacement acceptance record.
  3. If the inquiry is still comparing providers (stage Inquiry or Quoted), only the affected provider's ProviderInquiry participation and quotes are cancelled. The inquiry keeps its current stage and is flagged `supportRequired = true`; other providers' participation and offers remain available. Automatic redistribution then applies as follows:
     - If the cascade cancels a live offer of the affected provider (a sent quote that has not expired) and the patient has no other live offer on the inquiry, the system automatically redistributes the inquiry to eligible providers that have not yet received it. It uses the normal Workflow 2 matching, eligibility, and cap rules, so a `Suspended`, `Deactivated`, or password-not-set provider is never chosen. For an FR-037 exclusive inquiry, redistribution removes the exclusive restriction in the same way as the explicit-decline fallback (REQ-003-016). The `supportRequired` marker stays on the inquiry.
     - If the patient had explicitly selected the affected provider (Screen 7a), the system asks the patient to confirm before it redistributes, and it redistributes only after the patient confirms. Until then, the inquiry is not redistributed and the patient keeps the Contact Admin/Support action.
     - If the patient still has another live offer on the inquiry, the inquiry is not redistributed.
     - If redistribution finds no eligible provider, Alternative Flow B1 applies.
     - Redistribution runs at most once per provider-status event and inquiry; a replayed cascade does not distribute again.
  4. Before acceptance (stage Inquiry or Quoted), the patient receives the offer-unavailability message (`provider.status_cancellation_patient`) with a Contact Admin/Support action (FR-020). When the inquiry is redistributed, the message also tells the patient: "We are finding new offers for you." When the patient must confirm first (step 3), the message asks the patient to confirm the redistribution. After acceptance and before treatment starts (stage Accepted or Confirmed), the patient receives the `booking.provider_fault_replacement` notice (FR-020) saying that the provider can no longer perform the treatment and that an admin will arrange a replacement provider within the same inquiry; no cancellation copy is shown. For stage In Progress or Aftercare, patient notices follow FR-006 Alternative Flows B7 and B6 and FR-015 Screen 4. In neither case does the patient see the Workflow 5 patient-cancellation confirmation, and no patient cancellation reason is requested.
  5. Completed and already-cancelled inquiries are not reclassified. Later reactivation does not restore cancelled participation or quotes and does not clear `supportRequired`; only an audited admin resolution clears it.
- **Outcome**: Affected inquiries stay open and are flagged for special admin support under a provider-caused cause; a still-comparing inquiry left with no live offer is redistributed automatically to other eligible providers (after patient confirmation when the patient had selected the affected provider); accepted cases before treatment are rehomed through FR-006 Alternative Flow B5, `In Progress` cases follow the admin decision in FR-006 Alternative Flow B7, `Aftercare` cases follow FR-006 Alternative Flow B6, and unrelated providers' offers are unaffected.
- **Boundary**: Distinct from Workflow 5 patient cancellation, E3 account-deletion cancellation, and Payment Window Expired. Cascade processing is deduplicated per provider-status event and inquiry. FR-015 A5/Screen 4 owns the triggering event and cross-module cascade.

---

### Workflow 3: Provider Inquiry Management (Provider Flow)

**Actors**: Provider, System, Admin  
**Trigger**: Provider receives a distributed inquiry or opens an assigned inquiry from the dashboard  
**Outcome**: Provider reviews anonymized details and manages status prior to quote creation

**Flow Diagram**:

```mermaid
flowchart TD
    Start["Provider opens Inquiry List (Screen 9)"] --> Open["Provider opens Inquiry Detail (Screen 10)"]
    Open --> Review["Provider reviews scan/media + questionnaire + alerts"]
    Review --> Action{"Provider action"}

    Action -->|Proceed to quote| Quote["Continue to FR-004 (Quote creation flow)"]
    Action -->|Decline exclusive inquiry| DeclineGate{"Monitoring conversion routed<br/>exclusively to this provider?"}
    DeclineGate -->|No| DeclineBlocked["Use the ordinary inquiry-management rules"]
    DeclineGate -->|Yes| Decline["Provider confirms decline with a reason"]
    Decline --> Release["System audits the decline, removes the exclusive-provider restriction,<br/>and runs Workflow 2 normal matching and distribution"]
    Action -->|Need clarification| RequestInfo["Provider requests clarification via admin"]
    RequestInfo --> AdminHelp["Admin facilitates communication"]
    AdminHelp --> Stay["Inquiry remains in &quot;Inquiry&quot; stage until resolved"]
```

### Alternative Flows

**C1: Provider needs additional information**:

- **Trigger**: Provider cannot make assessment based on submitted inquiry data
- **Outcome**: Clarification requested through admin; inquiry stays in current stage
- **Flow Diagram**:

```mermaid
flowchart TD
    Review["Provider cannot assess from submitted data"] --> Need{"Need clarification?"}
    Need -->|Yes| Request["Provider requests clarification via admin"]
    Request --> Admin["Admin facilitates communication"]
    Admin --> Stay["Inquiry remains in &quot;Inquiry&quot; stage until resolved"]
    Need -->|No| Continue["Proceed toward quote creation (FR-004)"]
```

**C2: Exclusive monitoring-conversion provider declines the inquiry**:

- **Trigger**: The sole provider receiving an FR-037 monitoring-conversion inquiry declines before creating a quote
- **Outcome**: The system records the provider and reason, removes the exclusive-provider restriction, and immediately reruns Workflow 2 through normal country, patient-selection, matching, and provider-cap rules. Repeated decline requests MUST NOT distribute the inquiry more than once
- **Expiry boundary**: This automatic fallback is triggered by an explicit provider decline only. Inquiry or quote expiry continues to follow its existing configured rules

---

### Workflow 4: Admin Inquiry Management (Admin Flow)

**Actors**: Admin, System, Providers, Patients  
**Trigger**: Admin opens an inquiry for oversight or intervention, or a policy/action requires admin processing  
**Outcome**: Admin edits/overrides/reassigns/archives with full audit; re-notifications triggered as needed

**Flow Diagram**:

```mermaid
flowchart TD
    Start["Admin opens inquiry (Screen 11/12)"] --> Choose{"Admin action"}

    Choose -->|Edit inquiry| Edit["Edit inquiry fields (with warnings)"]
    Edit --> Reason1{"Reason provided?"}
    Reason1 -->|No| Block1["Block save; require reason"] --> Edit
    Reason1 -->|Yes| Audit1["Save changes + audit log"]
    Audit1 --> Renotify{"Re-notify parties if impactful?"}
    Renotify -->|Yes| Send1["Send notifications per rules/config"]
    Renotify -->|No| Done1["Done"]
    Send1 --> Done1

    Choose -->|Reassign providers| Reassign["Select provider(s) + validate eligibility"]
    Reassign --> Audit2["Apply reassignment + audit log"] --> Done2["Done"]

    Choose -->|Override expiry/distribution| Override["Set override values"]
    Override --> Valid{"Override valid?"}
    Valid -->|No| OverrideErr["Show error; do not apply"] --> Override
    Valid -->|Yes| Audit3["Apply override + audit log"] --> Done3["Done"]

    Choose -->|Soft delete - archive| Archive["Confirm archive + reason"]
    Archive --> Audit4["Archive + audit log"] --> Notify["Notify patient if required"] --> Done4["Done"]

    Choose -->|Escalate urgent case| Esc["Mark urgent + assign owner"]
    Esc --> Audit5["Log escalation"] --> Done5["Done"]

    Choose -->|Contact patient/provider| Contact["Admin contacts patient or provider"]
    Contact --> Resolve["Admin resolves issue + updates inquiry (if needed)"]
    Resolve --> Audit6["System logs intervention in audit trail"] --> Done6["Done"]
```

---

### Workflow 5: Patient-Initiated Inquiry Cancellation

**Actors**: Patient, System, Providers (notified), Admin (observer)  
**Trigger**: Patient opens the Inquiry Dashboard (Screen 8), taps into an inquiry detail view, and selects "Cancel Inquiry" from the action menu, for an inquiry in stage Inquiry or Quoted. From the Accepted stage onward the action is replaced by "Contact support" (see Alternative Flow E2)  
**Outcome**: Inquiry transitions to "Cancelled"; all associated quotes auto-cancelled; providers notified; inquiry becomes read-only in patient dashboard

**Flow Diagram**:

```mermaid
flowchart TD
    Start["Patient opens Inquiry detail (Screen 8)"] --> Cancel["Patient taps &quot;Cancel Inquiry&quot;"]
    Cancel --> CheckStage{"Stage eligible?<br/>Inquiry / Quoted"}

    CheckStage -->|No| Block["Block cancellation + message: Contact support"] --> End1["Exit"]
    CheckStage -->|Yes| Modal["Show cancellation confirmation modal (Screen 8a)"]

    Modal --> ReasonOk{"Reason valid/selected?"}
    ReasonOk -->|No| Modal
    ReasonOk -->|Yes| Preflight["Preflight (no state change):<br/>confirm inquiry still active<br/>load quotes + notification targets"]

    Preflight --> PreflightOk{"Preflight successful?"}
    PreflightOk -->|No| PreflightErr["Show temporary error + Retry/Back<br/>(do NOT cancel yet)"] --> Modal
    PreflightOk -->|Yes| Confirm["Patient confirms cancellation"]

    Confirm --> Commit["Atomic commit:<br/>set inquiry = Cancelled + timestamp + reason<br/>cancel quotes (if any)<br/>write immutable audit event"]
    Commit -.-> Race["If quote submitted concurrently:<br/>quote flow must re-check inquiry status<br/>and reject if not active (FR-004)"]

    Commit --> Notify["Send/enqueue notifications (target &lt;= 5 minutes)<br/>providers: reason NOT shared"]
    Notify --> NotifyOk{"Notification enqueue/send OK?"}
    NotifyOk -->|Yes| Success["Show success screen (Screen 8b)"]
    NotifyOk -->|No| NotifyFallback["Queue/retry notifications + log attempts<br/>(do not roll back cancellation)"] --> Success

    Success --> ReadOnly["Inquiry shows &quot;Cancelled&quot; badge (read-only)"]
    ReadOnly --> End2["Patient returns to My Inquiries or starts new inquiry"]
```

### Alternative Flows

**E1: Patient cancels inquiry with no quotes received (Inquiry stage)**:

- **Trigger**: Patient cancels an inquiry that has not yet received any quotes
- **Outcome**: Only inquiry status updated; no quote cascade needed
- **Flow Diagram**:

```mermaid
flowchart TD
    Preflight["Preflight detects 0 associated quotes"] --> Commit["Commit cancellation (single atomic update)"]
    Commit --> Notify["Send inquiry.cancelled to distributed providers<br/>(no quote.cancelled_inquiry needed)"]
    Notify --> Patient["Send patient confirmation"] --> Done["Show success (Screen 8b)"]
```

**E2: Patient wants to cancel after acceptance (Accepted stage onward)**:

- **Trigger**: Patient wants to cancel an inquiry that has an accepted quote (stage Accepted, Confirmed, In Progress or Aftercare)
- **Outcome**: The patient cannot cancel in the app. The inquiry dashboard shows "Contact support" instead of "Cancel Inquiry". An admin cancels the booking through FR-006 with a mandatory reason and an audit entry. The booking and the inquiry become `Cancelled`, any active appointment hold is released, and the accepted quote keeps the status `accepted`. Any refund or fee follows the payment placeholder, not this FR.
- **Flow Diagram**:

```mermaid
flowchart TD
    Want["Patient opens an inquiry in Accepted stage or later"] --> Support["Cancel Inquiry hidden; patient taps Contact support"]
    Support --> Admin["Admin cancels the booking through FR-006<br/>(mandatory reason + audit)"]
    Admin --> Result["Booking = Cancelled; inquiry = Cancelled<br/>hold released; accepted quote stays accepted"]
    Result --> Notify["Patient and provider notified through FR-006 / FR-020"]
```

**E3: System cancels inquiry due to account deletion request (DSR)**:

- **Trigger**: Patient submits an account deletion request (DSR) in FR-001 (Delete Account flow)
- **Outcome**: Inquiry transitions to "Cancelled" without prompting for a patient-entered cancellation reason; system stores a system-generated cancellation reason for audit ("Account Deleted (System)"); all associated quotes auto-cancelled; providers notified; inquiry becomes read-only
- **Notes**:
  - Provider-facing cancellation notifications MUST NOT reveal the cancellation reason (treat as patient-private/system-private data), consistent with Workflow 5 stakeholder notification rules.

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Service Selection

**Purpose**: Patient selects desired hair transplant service

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Service Option | select (single) | Yes | Primary service selection | Must select one |
| Treatment Area | select | Yes | One active, Admin-managed treatment-area option | Must select one active option returned by the Inquiry Configuration API |

**Notes**:

- Service Options:
  - "Get a Hair Transplant" (primary option)
  - "Monitor Hair Loss" (secondary - different workflow)
  - "Aftercare: Monitor Transplant Progress" (secondary - different workflow)
  - "Aftercare for Transplant" (secondary - different workflow)
- Treatment Area Selection:
  - The active, ordered catalog is retrieved from the Inquiry Configuration API.
  - Each option contains a stable identifier, patient-facing label, and image/icon URL.
  - Hair, Beard, and Both remain the default seeded options; they are not a fixed client-side enum.

**Business Rules**:

- Patient must select one active treatment-area option
- The selected option must be active when the inquiry is created; inactive options remain readable on historical inquiries through their saved snapshot.
- Primary focus on "Get a Hair Transplant" option
- Other services are secondary features

#### Screen 2: Destination Selection

**Purpose**: Patient selects preferred treatment locations

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Countries | multiselect | Yes | Up to 10 preferred countries | Max 10; ordered by FR-028 regional configuration when available, otherwise proximity |
| Price Display | derived | No | Starting price per country | Fallback currency support |

**Notes**:

- Country List:
  - Show country name with starting price
  - Order by proximity to patient location
  - Support fallback currency/pricing display
- Price Display:
  - Starting price per country
  - Currency based on patient location
  - Price range indicators

**Business Rules**:

- Maximum 10 countries selectable
- Countries ordered by FR-028 regional configuration when available, otherwise by proximity to patient location
- Starting prices displayed for transparency
- Fallback pricing for unsupported currencies

#### Screen 3: Detailed Information Form

**Purpose**: Patient provides comprehensive hair concern details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Nature of concern | text | Yes | Patient description | Max length; not empty |
| Duration | select | Yes | Duration enum | Must select one |
| Previous treatments | text | Yes | Prior treatments | Max length |
| Symptom severity | slider (1-10) | Yes | Severity index | Integer 1-10 |
| Lifestyle factors | text | No | Optional context | Max length |
| Additional notes | text | No | Optional notes | Max length |
| Photos | file (image) | No | Up to 5 images | JPG/PNG ≤ 2MB each; total ≤ 5 |
| Videos | file (video) | No | Up to 5 videos | MP4 ≤ 30s, ≤ 20MB each |

**Notes**:

- Visual Evidence:
  - Photo upload: max 5 files (JPG/PNG ≤ 2MB each)
  - Video upload: max 5 files (MP4 ≤ 30s, ≤ 20MB each)
  - Enforce file size/format and total file count

**Business Rules**:

- All required fields must be completed
- Visual evidence limited to 5 files total
- Photos: JPG/PNG ≤ 2MB each
- Videos: MP4 ≤ 30s, ≤ 20MB each
- Text fields have character limits

#### Screen 4: Head Scan Photo Set Capture (V1)

**Purpose**: Patient captures standardized head scan photo set for provider assessment *(V1 implementation of “3D scan”; true 3D deferred to V2)*

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Head Scan Photo Set (V1) | capture/upload | Yes | Standardized head scan photo set (multiple 2D views of patient’s head) | Must meet completeness/quality/file constraints from FR-002 |
| Quality Indicators | derived | Yes | Real-time quality feedback | Retake if below threshold |

**Notes**:

- Capture Instructions:
  - Visual guidance for positioning (front, top, left, right angles)
  - Quality indicators and feedback
  - Retake options available
- Media Characteristics (V1):
  - Standardized photo set (multiple 2D views; not a true 3D model)
  - Validated and processed by FR-002 engine and S-01/S-05
  - Future 3D model capture and interactive viewer deferred to V2 (per system PRD)

**Business Rules**:

- Head scan photo set must meet minimum completeness/quality thresholds required by FR-002
- Patient can retake capture if quality poor
- Captured media encrypted and stored securely
- Media accessible to providers for assessment via engine outputs

#### Screen 5: Treatment Date Selection

**Purpose**: Patient selects preferred treatment dates

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Date Ranges | date range (multi) | Yes | Up to 10 ranges | Max 10; non-overlapping; ≤ 2 years out |

**Notes**:

- Date Range Selection:
  - Multiple pickers (max 10)
  - Calendar with availability
  - Non-overlapping validation
- Date Constraints:
  - Max 2 years in future
- Minimum lead time from inquiry date is the active Admin-configured blocked window (default: 3 days)
  - Consider provider availability

**Business Rules**:

- Maximum 10 date ranges selectable
- Date ranges cannot overlap
- Dates limited to 2 years in future
- System validates provider availability
- Calendar eligibility and submission validation must use the same configured minimum lead-time value.

#### Screen 6: Medical Questionnaire

**Purpose**: Patient completes comprehensive medical history assessment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Question | enum | Yes | Medical question item | Must answer Yes/No |
| Answer | boolean | Yes | Yes/No | Required |
| Details | text | Cond. | Required if Answer = Yes | Non-empty when required |
| Alert Level | derived | No | Critical/Standard/None | Derived from rules |

**Notes**:

- Question List:
  - Allergies to medications (Yes/No + details)
  - Other allergies (Yes/No + details)
  - Respiratory conditions (Yes/No + details)
  - Cardiovascular disease (Yes/No + details)
  - Hypertension (Yes/No + details)
  - Diabetes (Yes/No + details)
  - Implanted medical devices (Yes/No + details)
  - Hepatitis B/C (Yes/No + details)
  - HIV/AIDS (Yes/No + details)
  - Arthritis (Yes/No + details)
  - Neurological disorders (Yes/No + details)
  - Other medical conditions (Yes/No + details)
  - Bleeding disorders (Yes/No + details)
  - Kidney disease (Yes/No + details)
  - Cancer history (Yes/No + details)
  - Digestive diseases (Yes/No + details)
  - Mental health disorders (Yes/No + details)
  - Blood clots/DVT (Yes/No + details)
  - Previous surgeries (Yes/No + details)
  - Pregnancy status (Yes/No + details)
  - Regular medications (Yes/No + details)
- Alert System:
  - Critical (red)
  - Standard (amber)
  - None (green)

**Business Rules**:

- All questions require Yes/No answers
- Detailed explanations required for "Yes" answers
- Medical alerts generated automatically
- Questionnaire managed by admin (not hard-coded) via FR-025 (Medical Questionnaire Management)
- **MVP**: Inquiry questionnaires support Yes/No questions only (enforced in FR-025 publishing/activation rules)
- **Future (V2+)**: If Inquiry questionnaires allow non-Yes/No question types, the inquiry response schema and UI must be extended to support typed answers (e.g., numeric scale, multi-select, free text)

#### Screen 7: Inquiry Summary & Submission

**Purpose**: Patient reviews complete inquiry before submission

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Section Summary | group | Yes | Read-only summary of prior steps | Must reflect latest data |
| Terms Acceptance | checkbox | Yes | Accept T&C before submission | Required to submit |

**Notes**:

- Summary includes: treatment type, countries with prices, concern details, media, head scan photo set (V1), date ranges, questionnaire summary
- Submission Controls: per-section Edit, Submit button, T&C acceptance

**Business Rules**:

- Patient must review all sections
- Patient can edit any section before submission
- Terms and conditions must be accepted
- Submission generates unique inquiry ID

#### Screen 7a: Provider Selection

**Purpose**: Patient selects preferred providers to receive the inquiry

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Suggested Providers | list | Yes | System-suggested providers based on reviews and admin curation | Non-empty; ordered by rating/curation score |
| Provider Card | group | Yes | Provider summary: name, country, rating, review count, specialty, starting price | Read-only per card |
| Selected Providers | multiselect | Yes | Patient's chosen providers | Min 1, max 5 |
| Search | control | No | Search by provider name or keyword | Debounced; case-insensitive |
| Filters | control | No | Filter by country (from selected destinations), rating range, specialty | Valid enums/ranges |

**Notes**:

- Provider Suggestions:
  - Ordered by positive reviews and admin curation score
  - Filtered to providers in patient's selected destination countries
  - Each card shows: provider name, country, star rating, review count, specialty tags, starting price in patient's currency
- Selection Controls:
  - Tap to select/deselect provider card
  - Visual indicator (checkmark/highlight) on selected providers
  - Counter shows "X of 5 selected"
  - "Continue" button enabled when at least 1 provider selected

**Business Rules**:

- Maximum 5 providers selectable
- Only providers in patient's selected destination countries are shown
- Provider suggestions based on positive reviews and admin curation (system PRD)
- Patient must select at least 1 provider to proceed
- Selected providers are included in the inquiry for distribution; system may also distribute to additional matching providers per distribution rules

#### Screen 8: Inquiry Dashboard (Post-Submission)

**Purpose**: Patient views submitted inquiry status and details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Current Stage | badge | Yes | Inquiry stage (Inquiry/Quoted/Accepted/Cancelled/...) | Valid lifecycle value; includes "Cancelled" |
| Timeline | timeline | Yes | Chronological status changes | Timestamps present |
| Responses Count | number | Yes | Number of provider responses | Non-negative integer |
| Inquiry Summary | group | Yes | Read-only inquiry info | Complete and consistent |
| Quotes Received | list | No | Provider quotes (from FR-004) | Read-only links |
| Deadlines | datetime | Yes | Response/expiry deadlines | Future or past allowed |
| Next Actions | actions | Yes | Available user actions | Based on stage/permissions |
| Cancel Inquiry | action | Conditional | "Cancel Inquiry" button; visible only in Inquiry or Quoted stages | Hidden when stage is Accepted, Confirmed, In Progress, Aftercare, Completed, or Cancelled; triggers Workflow 5 cancellation flow |
| Contact Support | action | Conditional | "Contact support" action shown in place of "Cancel Inquiry" from the Accepted stage onward | Visible when stage is Accepted, Confirmed, In Progress or Aftercare; opens Help & Support so an admin can act on the request |

**Notes**:

- Dashboard shows: full inquiry summary, provider responses, deadlines, and context-aware next actions
- "Cancel Inquiry" action appears in Next Actions area only for eligible stages (Inquiry, Quoted). From the Accepted stage onward, Next Actions shows "Contact support" instead, and any booking cancellation is performed by an admin through FR-006
- If inquiry is in "Cancelled" stage, dashboard is read-only with "Cancelled" badge; no actions available except viewing details
- A provider-caused status change (`ProviderSuspended` or `ProviderDeactivated`) never shows patient-cancellation copy. For a still-comparing inquiry (Inquiry or Quoted stage), the dashboard shows a provider-unavailable message with a Contact Admin/Support action, and the affected provider's offers show as unavailable while other offers remain actionable. When no live offer remains and the inquiry is redistributed, the message says "We are finding new offers for you." When the patient had explicitly selected the affected provider, the dashboard first asks the patient to confirm the redistribution. After acceptance, the dashboard keeps the current stage and tells the patient that an admin will arrange a replacement provider within the same inquiry (Workflow 2 Alternative Flow B4)

**Business Rules**:

- Patient can only have one active inquiry at a time
- Patient can modify inquiry if still in "Inquiry" stage
- Patient can cancel inquiry if in Inquiry or Quoted stage (see Workflow 5); from the Accepted stage onward the patient contacts support and an admin cancels through FR-006
- Patient receives notifications for status changes
- Inquiry data persists for 7 years minimum
- Cancelled inquiries are not counted as "active" — patient can create a new inquiry immediately after cancellation

#### Screen 8a: Cancel Inquiry Confirmation Modal

**Purpose**: Confirm patient's intent to cancel and capture cancellation reason (Workflow 5 step 2)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Warning Icon | icon | Yes | Red warning triangle or alert icon | Displayed at top of modal |
| Modal Title | text | Yes | "Cancel Inquiry?" | Displayed prominently in red/destructive color |
| Warning Message | text | Yes | Explanation of consequences: "Canceling this inquiry is irreversible. All quotes you've received will be cancelled and providers will be notified." | Read-only informational text |
| Current Stage Badge | badge | Yes | Shows inquiry current stage | Enum: "Inquiry", "Quoted"; read-only |
| Inquiry Reference | text | Yes | Inquiry ID (HPID format) | Read-only; format: HPID + YY + MM + 4-digit sequence |
| Impact Summary | text | Yes | Summary of cancellation impact based on current stage | Conditional: "X active quotes will be cancelled" OR "No quotes received yet"; derived from associated quote count |
| Cancellation Reason Selector | select | Yes | Dropdown or radio list of predefined reasons | Must select one option; default options: "Changed my mind", "Found a better option elsewhere", "Medical concerns", "Financial reasons", "Travel restrictions", "Timeline doesn't work", "Other" (admin-configurable via FR-026 Screen 5a) |
| Additional Notes | text | Conditional | Free text field; shown when "Other" selected | Required if "Other" selected; max 500 characters |
| Optional Feedback | text | No | General feedback text area | Max 1000 characters; placeholder: "Any additional feedback? (Optional)" |
| Provider Notification Note | text | Yes | Informational message: "Affected providers will be notified of this cancellation within 5 minutes" | Read-only |
| Confirm Cancellation Button | button | Yes | Destructive primary CTA | Red/destructive style; label: "Confirm Cancellation"; disabled until reason selected |
| Go Back Button | button | Yes | Secondary CTA to dismiss modal | Default/neutral style; label: "Go Back"; closes modal without action |

**Business Rules**:

- Modal is triggered from the "Cancel Inquiry" action on Screen 8 (Inquiry Dashboard)
- Modal is only reachable when inquiry stage is Inquiry or Quoted (Workflow 5 step 1 validates this)
- Cancellation reason is required before the Confirm button becomes active
- Cancellation reason is patient-private data (not shared with providers; stored for analytics and audit)
- On "Confirm Cancellation", system processes Workflow 5 steps 3–5; modal is dismissed and Screen 8b is shown
- On "Go Back", modal is dismissed with no state change

**Acceptance Scenarios**:

1. **Given** inquiry in eligible stage, **When** patient opens modal, **Then** Current Stage Badge and Impact Summary reflect actual inquiry state and quote count
2. **Given** patient has not selected a reason, **When** patient taps Confirm Cancellation, **Then** button remains disabled
3. **Given** patient selects "Other", **When** Additional Notes is empty, **Then** Confirm Cancellation remains disabled until notes entered
4. **Given** patient taps Go Back, **When** modal dismisses, **Then** no inquiry state is changed

#### Screen 8b: Cancellation Success Confirmation

**Purpose**: Confirm the inquiry has been successfully cancelled and provide next-step navigation (Workflow 5 step 5)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Success Icon | icon | Yes | Checkmark or completion illustration | Green color; displayed at top center |
| Confirmation Title | text | Yes | "Inquiry Cancelled" | Displayed prominently below icon |
| Confirmation Message | text | Yes | "Your inquiry has been successfully cancelled." | Read-only |
| Inquiry Reference | text | Yes | Inquiry ID (HPID format) | Read-only; label: "Reference:" |
| Cancellation Timestamp | datetime | Yes | Server-side cancellation timestamp | Format: "Cancelled on [Month DD, YYYY] at [HH:MM AM/PM]"; reflects server time, not client |
| Impact Summary | text | Yes | Summary of what was cancelled | Conditional based on stage: "Your inquiry was cancelled." or "Your inquiry and X active quote(s) were cancelled." |
| Provider Notification Status | text | Yes | "All affected providers have been notified of this cancellation." | Read-only |
| Back to My Inquiries Button | button | Yes | Primary CTA | Default style; label: "Back to My Inquiries"; navigates to Inquiry Dashboard (Screen 8) |
| Start New Inquiry Button | button | Yes | Secondary CTA | Outlined/secondary style; label: "Start New Inquiry"; navigates to Inquiry Creation flow (Screen 1) |
| Contact Support Link | link | No | Optional support contact link | Text link; label: "Need help? Contact support"; navigates to Help & Support |

**Business Rules**:

- This screen is shown only after Workflow 5 completes successfully (steps 3–4 finished)
- Cancellation Timestamp reflects server-side time (not client clock) for audit consistency
- Impact Summary must match the actual cascade results (number of quotes cancelled)
- Cancelled inquiry is now read-only; "Back to My Inquiries" returns to Screen 8 where it shows "Cancelled" badge
- "Start New Inquiry" navigates to Screen 1; patient can create immediately (one-active-inquiry rule: cancelled inquiry is no longer "active")

**Acceptance Scenarios**:

1. **Given** cancellation completed for Inquiry-stage inquiry with 0 quotes, **When** Screen 8b displays, **Then** Impact Summary shows "Your inquiry was cancelled." with no quote mention
2. **Given** cancellation completed for Quoted-stage inquiry with 3 quotes, **When** Screen 8b displays, **Then** Impact Summary shows "Your inquiry and 3 active quote(s) were cancelled."

### Provider Platform Screens

#### Screen 9: Inquiry List Dashboard

**Purpose**: Provider views all distributed inquiries

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Patient ID | column | Yes | HPID + YY + MM + 4-digit sequence | Sortable; searchable |
| Patient Name | column | Yes | Partially masked name | Mask until payment confirmation |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern enum | Filterable |
| Requested Date Ranges | column | Yes | Primary + tooltip for others | Non-overlap; tooltip expansion |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Color-coded chips | Critical/Standard/None |
| Inquiry Date | column | Yes | Created timestamp | Relative formatting rules |
| Action | column | Yes | View/Create Quote buttons | State-aware actions |
| Search | control | No | Keyword search (ID, Name) | Debounced; case-insensitive |
| Filters | control | No | Age range, Concern, Date range, Alerts, Location | Valid ranges/enums |

**Notes**:

- Requested Date Ranges: primary displayed; all ranges via tooltip
- Patient Name: masked until payment confirmation
- Time Display: relative for recent; formatted for older
- Empty States: Loading, Error, No permission

**Business Rules**:

- Only shows inquiries for provider's countries OR explicitly selected by patient
- Patient names partially masked until payment confirmation
- Medical alerts prominently displayed with color coding
- Inquiry expiration configurable by admin
- Date ranges display primary range with tooltip for additional ranges
- Time display: relative for recent ("X minutes ago"), specific for older ("Sep 22, 2025")
- Empty states: Loading, Error, No permission

#### Screen 10: Inquiry Detailed View

**Purpose**: Provider reviews comprehensive inquiry details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Inquiry ID | text | Yes | Unique ID and current stage | Read-only |
| Timestamps | group | Yes | Created/updated/activity times | ISO 8601 |
| Patient (masked) | group | Yes | Partially masked identity | Reveal post-payment confirmation |
| Countries | list | Yes | Selected treatment countries | Non-empty |
| Problem Details | group | Yes | Concern text, duration, previous treatments | Complete |
| Media | gallery | No | Photos/videos previews | File constraints enforced |
| Head Scan (V1 Photo Set) | viewer/gallery | No | Head scan capture assets (photo set in V1; 3D model in V2) | Available if captured |
| Date Ranges | list | Yes | All selected date ranges | Non-overlapping |
| Medical Questionnaire | group | Yes | Full Q&A responses | Completed |
| Medical Alerts | chips | Yes | Tiered alert indicators | Critical/Standard/None |
| Decline Exclusive Inquiry | action | Conditional | Declines an FR-037 monitoring-conversion inquiry before quote creation | Exclusive assigned provider only; confirmation and reason required |

**Notes**:

- Inquiry Metadata:
  - Inquiry ID (HPID + YY + MM + 4-digit sequence)
  - Current stage (Inquiry/Quoted/Accepted/...)
  - Created at, Updated at, Last activity timestamps (ISO 8601)
- Patient (Masked):
  - Display name: First name + last initial + asterisks (e.g., "John D*****")
  - Age, Gender, Country (contact details masked until payment)
  - Patient ID (HPID-based) visible; name, phone number, and email remain masked/hidden until payment confirmation
- Countries:
  - Full list of selected treatment countries (ISO country + display name)
  - Primary country highlighted; remaining listed in order selected
- Problem Details:
  - Nature of concern (required)
  - Duration (enum)
  - Previous treatments (required)
  - Symptom severity (1–10)
  - Lifestyle factors (optional)
  - Additional notes (optional)
- Media:
  - Photos (JPG/PNG ≤ 2MB each, max 5): show thumbnails with modal preview
  - Videos (MP4 ≤ 30s, ≤ 20MB each, max 5): show poster frame with player
  - Validation messages for any file policy violations
- Head Scan:
  - V1: Photo set gallery viewer (zoom/compare)
  - Quality score and capture metadata if available
  - Retake indicator if replaced after initial capture
  - V2 (future): If a true 3D model exists, viewer may support orbit/zoom
- Date Ranges:
  - Display all selected ranges, non-overlapping
  - Primary range shown first; additional ranges listed below
  - Server-side validation notes for overlaps and max count (10)
- Medical Questionnaire:
  - Full Q&A list (Yes/No + required details for Yes)
  - Derived medical alerts: Critical (red), Standard (amber), None (green)
  - Link to audit trail of questionnaire version used
- Timeline:
  - Creation, distribution to providers, provider views, status changes
  - Sorted descending by time with relative and absolute timestamps

**Business Rules**:

- Full patient details visible only after payment confirmation
- Medical alerts color-coded by severity
- Head scan requires viewer (photo set gallery in V1; interactive 3D in V2)
- All data editable by admin
- Provider can review inquiry details
- When the exclusive provider declines before quote creation, the system must audit the reason, clear the exclusive routing restriction, and invoke normal Workflow 2 distribution exactly once.
- **Note**: Quote creation functionality handled in FR-004

### Admin Platform Screens

#### Screen 11: Hairline Overview Dashboard

**Purpose**: Admin monitors all inquiries across all stages

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Patient ID | column | Yes | HPID + YY + MM + 4-digit sequence | Sortable; searchable |
| Full Patient Name | column | Yes | Unmasked name | Admin only |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern enum | Filterable |
| Requested Date Ranges | column | Yes | Primary + tooltip for others | Non-overlap; tooltip expansion |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Color-coded chips | Critical/Standard/None |
| Inquiry Date | column | Yes | Created timestamp | Relative date logic |
| Current Status | column | Yes | Lifecycle stage | Enum validation |
| Quotes Count | column | No | Number of quotes | Non-negative integer |
| Payment Status | column | No | Payment indicator | Enum validation |
| Last Active | column | No | Last activity timestamp | ISO 8601 |
| Assigned Providers | column | No | Provider(s) assigned | List formatting |
| Action | column | Yes | Action buttons | State-aware actions |
| Advanced Filters | control | No | Patient/Provider locations, Stage, Payment, Date ranges | Valid enums/ranges |

**Business Rules**:

- Shows all inquiries in all lifecycle stages
- Admin has full visibility of all data
- Advanced filtering capabilities
- Bulk actions available
- Real-time status updates

#### Screen 12: Inquiry Detailed Management (Admin)

**Purpose**: Admin manages individual inquiry with full control

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Full Inquiry | group | Yes | All patient and inquiry data | Admin-only visibility |
| Admin Actions | actions | Yes | Edit, reassign, override, soft delete | Reason required; audited |
| Override Controls | form | No | Expiry/distribution overrides | Confirmation + reason required |
| Reassignment | control | No | Assign/reassign providers | Validation on provider eligibility |
| Soft Delete | control | No | Archive inquiry | Requires reason; reversible view-only |
| Audit Trail | log | Yes | Full change history | Immutable; timestamped |

**Notes**:

- Full Inquiry (read-only groups):
  - Patient (unmasked for admin): name, contact, country
  - Inquiry metadata: ID, stage, created/updated/activity times
  - Countries, Problem details, Media, head scan viewer, Date ranges
  - Medical questionnaire Q&A and derived alerts
- Admin Actions:
  - Edit inquiry details with caution banners and field-level audit
  - Reassign providers (single/multi) with eligibility checks
  - Override expiry/distribution windows with required reason
  - Soft delete (archive) with reason; read-only view after deletion
  - Add admin notes (time-stamped; visible to admins only)
  - Trigger re-notifications when impactful fields change
- Override Controls:
  - Expiry: set new deadline (cannot be in the past without justification)
  - Distribution: re-run matching; include/exclude specific providers
  - All overrides require confirmation and reason entry
- Reassignment:
  - Search providers by country/specialty; multi-select
  - Validation: avoid duplicates; respect provider capacity policies (if enabled)
  - Optional note sent to provider(s) upon assignment
- Soft Delete:
  - Requires reason; retains data for audit; prevents further edits
  - Display badge "Archived" across all admin views
- Audit Trail:
  - Records: who, when, what changed (old → new), reason, IP (if available)
  - Filterable by field, user, date range
  - Exportable (CSV/JSON) for compliance

**Business Rules**:

- Admin can edit any inquiry data
- All changes require reason documentation
- Soft delete only (no hard deletes)
- Visual warnings for data modification
- Complete audit trail maintained

**Note**: Medical questionnaire and system configuration management will be handled in a separate FR for centralized settings management.

## Business Rules

### General Inquiry Rules

1. **Submission Rules**
   - Patient must complete medical questionnaire before submission
   - Patient can only have one active inquiry at a time
   - Inquiry automatically expires if unquoted (configurable timeframe)
   - Patient can modify inquiry if still in "Inquiry" stage

2. **Distribution Rules**
   - System distributes inquiry to providers in selected countries OR explicitly selected by patient
   - Providers must respond within 72 hours (configurable)
   - Provider capacity limits affect distribution where capacity data is available; until the dedicated Provider Capacity Management FR is delivered, capacity checks are advisory and MUST NOT block inquiry distribution
   - Admin can manually assign inquiries
   - Only providers in `Active` status are eligible for distribution, exclusive routing, or reassignment; eligibility is revalidated at allocation time (Workflow 2 Alternative Flow B4)
   - Patient can select maximum 5 preferred providers
   - Provider suggestions based on positive reviews and admin curation
   - An FR-037 monitoring-conversion inquiry is initially restricted to its assigned provider. If that provider explicitly declines before quote creation, the system removes the restriction and immediately reruns normal distribution. Expiry does not use this decline fallback

3. **Data Access Rules**
   - Patient direct identifiers (name, phone number, email) anonymized until payment confirmation
   - Provider access limited to assigned inquiries
   - Admin has full access to all inquiry data
   - All data access logged for audit trail

4. **Cancellation Rules**
   - These rules govern patient- and account-deletion-initiated cancellation. Provider-status cancellation follows Rule 6 and does not use the patient cancellation reason, confirmation, or messaging.
   - Patient can cancel their own inquiry in stages: Inquiry or Quoted (before acceptance)
   - Patient cancellation is blocked for inquiries in Accepted, Confirmed, In Progress, Aftercare, or Completed stages — the patient sees "Contact support"
   - From acceptance onward, only an admin can cancel, through the FR-006 booking cancellation, from any booking state, with a mandatory reason and an audit entry. The booking and the inquiry become `Cancelled`, any active appointment hold is released, and the accepted quote keeps the status `accepted`. Refunds and fees follow the payment placeholder
   - Cancellation is immediate and irreversible; no grace period, no admin approval required
   - Cancellation reason is required (predefined options; see Workflow 5)
   - System MAY cancel an eligible inquiry as a consequence of a patient account deletion request (FR-001). In that case, the system MUST set a system-generated cancellation reason for audit (e.g., "Account Deleted (System)") and MUST NOT prompt the patient for a cancellation reason.
   - All associated draft, sent and expired quotes are auto-cancelled with status "Cancelled (Inquiry Cancelled)" (FR-004)
   - All affected providers receive notification of cancellation; cancellation reason is NOT shared with providers (patient-private analytics data)
   - Cancelled inquiry remains visible in patient dashboard with "Cancelled" badge (read-only)
   - No cooldown period after cancellation — patient can immediately create a new inquiry (one-active-inquiry rule: cancelled inquiry is no longer "active")
   - Admin has oversight visibility of patient-initiated cancellations but cannot block or reverse them
   - Cancellation event is logged in immutable audit trail with: patient ID, inquiry ID, timestamp, reason, optional feedback

5. **Inquiry Configuration Rules**
   - Admin-managed treatment-area options control the choices presented at inquiry creation. Each active option has a stable ID, label, display order, and image/icon URL.
   - A treatment-area option used by an existing inquiry cannot be deleted. It may be deactivated for future inquiries while historical inquiry display retains the saved label and asset reference.
   - Admin configures the minimum inquiry lead time as a whole number of blocked days. The default is 3; the permitted value is 0 through 730, consistent with the existing two-year date horizon.
   - The patient platform retrieves the current catalog and lead-time setting from the backend. A client release is not required for ordinary option or lead-time changes only after implementation verifies compatibility with this dynamic response.

6. **Provider Status Cancellation Rules** (FR-015 Alternative Flow A5 and Screen 4)
   - A provider's effective `Suspended` or `Deactivated` status blocks new inquiry allocation to that provider; in-flight requests or callbacks MUST NOT revive cancelled participation.
   - An `Active` provider that has not yet set its password (FR-015 `password_set = false`) is not eligible for allocation, explicit patient selection, or reassignment. It becomes eligible once the password is set; inquiries distributed before then are not re-sent to it.
   - An inquiry whose accepted treatment belongs to the affected provider is not cancelled: its booking carries cause `ProviderSuspended` or `ProviderDeactivated` and the inquiry is flagged `supportRequired = true`. Before treatment starts the booking is closed and an admin rehomes the patient through FR-006 Alternative Flow B5; an `In Progress` booking stays `In Progress` for the admin decision in FR-006 Alternative Flow B7; an `Aftercare` booking follows FR-006 Alternative Flow B6.
   - An inquiry still comparing providers keeps its stage; only the affected provider's ProviderInquiry participation and quotes are cancelled, the inquiry is flagged `supportRequired = true`, and other providers' offers stay available.
   - When that cancellation removes a live offer and the patient has no other live offer on the inquiry, the system automatically redistributes the inquiry to eligible providers that have not yet received it, under the normal distribution rules. If the patient had explicitly selected the affected provider, the patient confirms first. No redistribution happens while another live offer remains (Workflow 2 Alternative Flow B4 step 3).
   - `supportRequired` is an independent marker, not a lifecycle stage. Clearing it requires an audited admin resolution.
   - Provider-caused causes are distinct from patient cancellation, account-deletion cancellation, and Payment Window Expired, and are never overwritten by later provider status changes.

### Medical Data Rules

1. **Medical Alert System**
   - 3-tier color-coded alert system:
     - Critical alerts (red - high risk conditions)
     - Standard alerts (yellow/amber - moderate concerns)
     - No alerts (green - no medical concerns)
   - Alerts generated automatically from questionnaire
   - Alerts prominently displayed to providers

2. **Questionnaire Management**
   - Medical questionnaire managed by admin through FR-025 (not hard-coded)
   - Questions require Yes/No answers
   - Detailed explanations required for "Yes" answers
   - Questionnaire content versioned and auditable
   - **Note**: Centralized questionnaire management handled in FR-025

### Data and Privacy Rules

1. **Data Retention**
   - Inquiry data retained for 7 years minimum
   - Head scan media retained for 2 years after inquiry completion (photo sets in V1; 3D scans in V2)
   - Medical questionnaire responses retained for 7 years
   - All data encrypted at rest and in transit
   - Cancelled inquiries are subject to the same retention policy as completed inquiries; cancellation does not accelerate data deletion timelines

2. **Data Access**
   - Patient direct identifiers (name, phone number, email) anonymized until payment confirmation
   - Provider access limited to assigned inquiries
   - Admin access logged for audit trail
   - Cross-tenant data access through authenticated APIs only

3. **Data Security**
   - All inquiry data encrypted at rest and in transit
   - Head scan media stored securely with access controls
   - Access attempts logged and monitored
   - Soft deletes only (no hard deletes allowed)

### Admin Editability Rules

1. **Full Admin Override**
   - Admin can edit ALL inquiry data in the system
   - Admin can modify any patient's inquiry details
   - Admin can reassign inquiries to different providers
   - Admin can override any system-calculated settings

2. **Edit Capabilities**
   - **Inquiry Data**: Modify all patient-submitted information
   - **Patient Data**: Edit patient information, contact details
   - **Provider Data**: Modify provider assignments and settings
   - **System Data**: Override expiration rules, capacity limits
   - **Medical Data**: Edit questionnaire responses and alerts

3. **Edit Tracking**
   - All admin edits logged with timestamp and admin identification
   - Change reason required for all modifications
   - Edit history maintained for audit trail
   - Patient and provider notified of significant changes
   - Visual warnings displayed for data modification

### UI/UX Display Rules

1. **Date Range Display**
   - Primary date range displayed prominently
   - Additional ranges shown as "[+ X other ranges]" with tooltip expansion
   - Tooltip shows all date ranges with full details

2. **Time Display Logic**
   - Recent inquiries: Relative format ("X minutes ago", "X hours ago")
   - Previous day: Specific format ("Yesterday at 3:45 PM")
   - Older inquiries: Date format ("Sep 22, 2025")

3. **Patient ID Format**
   - Format: HPID + YY + MM + 4-digit sequence
   - Example: HPID2501001 (HPID + 25 + 01 + 0001)

4. **Medical Alert Display**
   - Critical alerts: Red color-coded chips
   - Standard alerts: Yellow/amber color-coded chips
   - No alerts: Green color-coded chips

5. **Patient Name Masking**
   - Format: First name + last initial + asterisks (e.g., "John D*****")
   - Full name revealed only after payment confirmation

### Validation and Constraints

1. **Input Validation**
   - Country selection limited to 10 countries maximum
   - Date ranges limited to 2 years in future
   - Visual evidence limited to 5 files total
   - File size and format validation enforced
   - Text field character limits enforced

2. **Business Logic Validation**
   - Date ranges cannot overlap
   - Provider capacity validation
   - Medical questionnaire completeness validation
   - Head scan media quality validation
   - Inquiry uniqueness validation

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 95% of patients can complete inquiry submission in under 15 minutes
- **SC-002**: 90% of patients successfully upload head scan photo sets (V1) on first attempt
- **SC-003**: 85% of patients complete medical questionnaire without assistance
- **SC-004**: Patient satisfaction score of 4.5+ stars for inquiry process

### Provider Efficiency Metrics

- **SC-005**: Providers can review inquiry details in under 5 minutes
- **SC-006**: 90% of providers respond to inquiries within 24 hours
- **SC-007**: Provider inquiry review completion rate of 95%
- **SC-008**: Provider quote creation time under 10 minutes

### Admin Management Metrics

- **SC-009**: Admin can manage all inquiries from single dashboard
- **SC-010**: 95% of inquiries processed without admin intervention
- **SC-011**: Admin dashboard loads with all data in under 3 seconds
- **SC-012**: Admin can edit inquiry data with full audit trail

### System Performance Metrics

- **SC-013**: Inquiry submission completes in under 30 seconds
- **SC-014**: Inquiry distribution to providers in under 2 minutes
- **SC-015**: System supports 1000+ concurrent inquiry submissions
- **SC-016**: 99.5% uptime for inquiry module during business hours

### Business Impact Metrics

- **SC-017**: 80% of submitted inquiries receive provider quotes
- **SC-018**: 25% conversion rate from inquiry to quote acceptance
- **SC-019**: 50% reduction in inquiry-related support tickets
- **SC-020**: 30% improvement in provider response times

## Functional Requirements Summary

### Core Requirements

- **REQ-003-001**: System MUST allow patients to create and submit inquiries with destinations, media, date ranges, head scan media (V1 photo set; V2 true 3D), and medical questionnaire.
- **REQ-003-002**: System MUST distribute completed inquiries to matching providers in selected countries and those explicitly chosen by the patient.
- **REQ-003-003**: Providers MUST see anonymized patient data and tiered medical alerts until payment/acceptance per system PRD.
- **REQ-003-004**: System MUST support draft autosave and resume with 7-day inactivity expiry for incomplete inquiries.
- **REQ-003-005**: Admin MUST be able to view, edit (with warnings), reassign, soft delete, and override distribution/expiration with full audit trail.

### Data Requirements

- **REQ-003-006**: System MUST retain inquiry data for at least 7 years; scan retention per system policy.
- **REQ-003-007**: System MUST link inquiries to patients, providers, locations, head scan media, and questionnaire responses.

### Security & Privacy Requirements

- **REQ-003-008**: System MUST mask patient names and hide phone numbers and email addresses until payment confirmation; patient ID (HPID-based) may remain visible as a pseudonymous identifier.
- **REQ-003-009**: System MUST encrypt all inquiry-related data at rest and in transit, and maintain immutable audit logs.

### Integration Requirements

- **REQ-003-010**: System MUST integrate with Shared Services for notifications and media/scan handling.
- **REQ-003-011**: System MUST expose internal APIs required by FR-004 (quote) to consume inquiry data without mutation.
- **REQ-003-017**: System MUST expose an active, ordered treatment-area catalog for inquiry creation, including a stable option identifier, label, and image/icon URL; Admin manages the catalog under FR-026.
- **REQ-003-018**: System MUST enforce the Admin-configured minimum inquiry lead time consistently in the patient date picker and at submission. The default blocked window is 3 days and does not change the existing two-year, non-overlap, or availability rules.
- **REQ-003-016**: When the exclusive provider explicitly declines an FR-037 monitoring-conversion inquiry before quote creation, the system MUST audit the decline reason, remove exclusive routing, and execute normal inquiry distribution exactly once.

### Cancellation Requirements

- **REQ-003-012**: System MUST allow patients to cancel their own inquiry in Inquiry or Quoted stages with a required cancellation reason; cancellation is immediate and irreversible. From the Accepted stage onward, System MUST NOT offer patient cancellation; it MUST show "Contact support", and cancellation is performed only by an admin through FR-006.
- **REQ-003-013**: System MUST auto-cancel all associated quotes when an inquiry is cancelled by the patient, with distinct cancellation status "Cancelled (Inquiry Cancelled)" and provider notifications via FR-020.
- **REQ-003-014**: When an admin cancels a booking through FR-006, System MUST set the inquiry to `Cancelled`, release any active appointment slot hold (FR-006 hold of the FR-026 configured duration) immediately, and leave the accepted quote with the status `accepted`.
- **REQ-003-019**: System MUST revalidate provider status at allocation, exclusive routing, and reassignment, and MUST NOT allocate inquiries to a `Suspended` or `Deactivated` provider from the effective time, including through in-flight jobs or retries, or to an `Active` provider whose FR-015 `password_set` is false.
- **REQ-003-020**: When a provider becomes `Suspended` or `Deactivated`, System MUST NOT cancel an inquiry whose accepted treatment belongs to that provider; it MUST keep the inquiry open with `supportRequired = true` while FR-006 Alternative Flow B4 records cause `ProviderSuspended` or `ProviderDeactivated` on the booking; before treatment starts, B4 closes the booking and an admin rehomes the patient through FR-006 Alternative Flow B5, an `In Progress` booking stays `In Progress` for the admin decision in FR-006 Alternative Flow B7, and an `Aftercare` booking follows FR-006 Alternative Flow B6; for inquiries still comparing providers, System MUST cancel only that provider's ProviderInquiry participation and quotes, keep the inquiry stage, flag it `supportRequired = true`, and preserve other providers' offers. Before acceptance, patients MUST receive the offer-unavailability message with Contact Admin/Support; after acceptance and before treatment starts, they MUST receive the `booking.provider_fault_replacement` notice that an admin will arrange a replacement provider within the same inquiry. Patients MUST NOT receive the patient-cancellation message in either case (FR-015 A5/Screen 4).
- **REQ-003-021**: Before acceptance, when the provider-status cascade cancels a live offer (a sent quote that has not expired) and the patient has no other live offer on the inquiry, System MUST automatically redistribute the inquiry, at most once per provider-status event, to eligible providers that have not yet received it under the normal Workflow 2 distribution rules, keep `supportRequired = true`, and tell the patient "We are finding new offers for you." If the patient had explicitly selected the affected provider, System MUST ask the patient to confirm and MUST redistribute only after confirmation. System MUST NOT redistribute while another live offer remains (Workflow 2 Alternative Flow B4).

### Marking Unclear Requirements

- **REQ-003-015**: Provider capacity management is referenced but handled by a separate FR (TBD); integration expectations remain.

## Key Entities

- **Inquiry**: patientId, treatmentAreaId, treatmentAreaSnapshot, destinations[], problem details, media[], scanRef, dateRanges[] (each entry carries a stable ID, persisted as `inquiry_date_ranges`, so FR-004 date-price rows can reference the source range), questionnaireSummary, status, createdAt, cancelledAt, cancellationReason, cancellationFeedback
  - Status enum: Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, **Cancelled**
  - Provider suspension or deactivation never cancels an inquiry; the causes `ProviderSuspended` and `ProviderDeactivated` are stored on the affected ProviderInquiry and on the FR-006 booking. `supportRequired` (boolean) is an independent admin-support marker with audited resolution, not a stage (Workflow 2 Alternative Flow B4)
  - Relationships: belongsTo Patient; hasMany ProviderInquiry; hasOne Scan; hasMany MedicalAlert
- **ProviderInquiry** (persisted as `inquiry_providers`): inquiryId, providerId, distributed_at, viewedAt, status
  - `distributed_at` (timestamp, UTC): set once per provider when the inquiry is distributed to that provider, including when an inquiry is released to normal distribution after an exclusive provider declines (REQ-003-016). Distribution retries or re-sends to the same provider never overwrite it. It is the start point for FR-014 time to first quote (TTFQ) and response rate, and for the FR-020/FR-030 `inquiry.ttfq_sla_breached` alert.
  - `status` includes Cancelled with cause `ProviderSuspended` or `ProviderDeactivated` when only that provider's participation is cancelled; the record is retained and never reopened by reactivation.
  - Relationships: belongsTo Inquiry; belongsTo Provider
- **MedicalQuestionnaireResponse**: inquiryId, questionId, answer, details *(MVP: `answer` is boolean; V2+: extend to typed answers if Inquiry supports additional question types)*
  - Relationships: belongsTo Inquiry
- **MedicalAlert**: inquiryId, level (critical/standard/none), reason
  - Relationships: belongsTo Inquiry
- **Scan**: inquiryId, storageUrl, qualityScore, metadata
  - Relationships: belongsTo Inquiry

### Inquiry Payload (Composition)

- Every Inquiry record MUST, at minimum, include:
  - Destinations (selected treatment countries/locations)
  - Treatment date ranges (up to configured limits)
  - Problem details and questionnaireSummary (including derived medical alerts)
  - Media attachments (photos/videos and head scan photo set / scanRef from FR-002)
  - Linked patient identifier (HPID-based patientId)
  - Distribution metadata via related ProviderInquiry records
- These fields MUST be fully populated before an inquiry is eligible for distribution to providers.

## Dependencies

### Internal Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient registration)
- **FR-002**: Medical History & 3D Scanning (head scan media validation/processing; V1 photo set; V2 true 3D)
- **FR-004**: Quote Submission & Management (provider quote creation)
- **FR-015**: Provider Management (provider status eligibility and the suspension/deactivation cancellation cascade — Alternative Flow A5 and Screen 4)
- **FR-020**: Notifications & Alerts (inquiry notifications)
- **FR-025**: Medical Questionnaire Management (centralized settings)
- **FR-026**: App Settings & Security Policies (owns the treatment-area catalog and minimum inquiry lead-time configuration consumed by FR-003)
- **FR-037**: Monitor Your Hair Loss (advice-mode monitoring conversion may create an inquiry with an exclusive assigned provider, overriding normal distribution matching — see Workflow 2 Alternative Flow B3)
- **Future FR**: Provider Capacity Management (provider availability)

### External Dependencies

- **3D Scanning SDK (V2)**: ARKit (iOS) and ARCore (Android) for true 3D capture (future enhancement)
- **Cloud Storage**: Secure storage for head scan photo sets (V1), 3D scans (V2), and documents
- **Geolocation Services**: Country/location detection and mapping
- **Currency APIs**: Real-time exchange rates for pricing

### Data Dependencies

- **Patient Data**: From patient registration and profile management
- **Provider Data**: From provider onboarding and location management
- **Location Data**: From admin-configured country/location lists
- **Medical Data**: From admin-configured questionnaire templates

## Assumptions

### User Behavior Assumptions

- Patients will actively complete comprehensive inquiries and provide accurate medical information
- Patients can have incomplete inquiries and resume from where they left off
- Patients will provide honest and complete medical information
- Providers will respond to distributed inquiries within specified timeframes

### Technology Assumptions

- Patients have access to smartphones with camera capabilities for head scan capture (V1 photo set; V2 true 3D)
- Patients have reliable internet access for inquiry submission
- Infrastructure can handle concurrent inquiry operations without degradation

### Business Process Assumptions

- Sufficient provider capacity exists to handle inquiry volume (capacity management handled separately)
- Admin team has capacity to manage inquiry operations and system configuration
- Head scan media (V1 photo set) and questionnaire responses will be of sufficient quality for medical assessment
- Medical data handling meets healthcare compliance requirements
- Medical questionnaire alerts are for provider awareness, not patient rejection

## Implementation Notes

### Technical Considerations

- **Real-time Distribution**: Inquiry distribution requires real-time processing
- **File Management**: Head scan media storage and retrieval must be optimized for performance
- **Mobile Optimization**: Patient screens must work seamlessly on mobile devices
- **Offline Capability**: Core inquiry features should work with limited connectivity

### Integration Points

- **Patient Module**: Seamless integration with patient authentication and profile
- **Provider Module**: Integration with provider dashboard and quote management
- **Admin Module**: Integration with admin oversight and system configuration
- **Notification Module**: Automated notifications for inquiry status changes

### Scalability Considerations

- **Database Design**: Efficient querying for large numbers of inquiries
- **File Storage**: Scalable storage solution for head scan media (V1 photo sets; V2 3D scans) and documents
- **Distribution Logic**: Automated distribution algorithms for high-volume inquiries
- **Provider Assignment**: Intelligent provider matching based on capacity and specialization

### Security Considerations

- **Data Encryption**: All inquiry data encrypted at rest and in transit
- **Access Control**: Strict role-based access to inquiry data
- **Audit Logging**: Comprehensive logging of all inquiry activities
- **Compliance**: Healthcare data protection regulations compliance

---

## User Scenarios & Testing

### User Story 1 - Submit Complete Inquiry (Priority: P1)

Why: Core entry point that powers distribution and provider review.

Independent Test: Patient completes all sections (destinations, media, head scan media, date ranges, questionnaire) and submits; verify inquiry creation and distribution readiness.

Acceptance Scenarios:

1. Given patient completes required fields, When submitting inquiry, Then system validates and creates inquiry with unique ID
2. Given a created inquiry, When distribution runs, Then matching providers are identified and prepared for notification
3. Given a created inquiry, When viewing patient dashboard, Then status shows Inquiry with full summary

### User Story 2 - Draft Autosave & Resume (Priority: P2)

Why: Reduces drop-off and improves completion rates.

Independent Test: Patient abandons mid-flow; later resumes and completes submission.

Acceptance Scenarios:

1. Given patient leaves mid-inquiry, When returning within 7 days, Then system restores last step and data
2. Given a restored draft, When continuing, Then previously validated sections remain intact
3. Given 7 days of inactivity, When resuming, Then draft has expired and patient starts a new inquiry

### User Story 3 - Provider Review Read-Only (Priority: P2)

Why: Ensures providers can triage efficiently while protecting patient privacy.

Independent Test: Provider opens distributed inquiry and reviews anonymized details, media, head scan media, date ranges, and medical alerts.

Acceptance Scenarios:

1. Given distributed inquiry, When provider opens it, Then anonymized patient and medical alerts are visible
2. Given head scan media and media, When provider views, Then performance and policy constraints are respected
3. Given pre-quote stage, When provider attempts to modify patient data, Then system blocks and logs read-only access
4. Given an FR-037 inquiry routed exclusively to the provider, When the provider confirms decline with a reason before creating a quote, Then the system removes the restriction and distributes the inquiry through normal Workflow 2 exactly once

### User Story 4 - Patient Cancels Inquiry (Priority: P2)

Why: Gives patients autonomy to cancel inquiries they no longer wish to pursue, reducing provider effort on abandoned inquiries.

Independent Test: Patient cancels inquiry at each eligible stage; verify status update, quote cascade, provider notifications, and dashboard state.

Acceptance Scenarios:

1. Given inquiry in "Inquiry" stage (no quotes), When patient cancels with reason, Then inquiry status becomes Cancelled; no quote cascade; distributed providers notified
2. Given inquiry in "Quoted" stage with 3 active quotes, When patient cancels, Then inquiry and all 3 quotes are cancelled; all 3 providers notified
3. Given inquiry in "Accepted" stage with a slot hold active, When patient opens the inquiry, Then "Cancel Inquiry" is hidden and "Contact support" is shown; When an admin then cancels the booking through FR-006 with a reason, Then booking and inquiry become Cancelled, the hold is released and the accepted quote stays accepted
4. Given inquiry in "Confirmed" stage, When patient looks for Cancel Inquiry, Then it is not shown and the patient is directed to "Contact support"
5. Given patient cancels inquiry, When patient returns to Inquiry Dashboard, Then cancelled inquiry visible with "Cancelled" badge (read-only); patient can create new inquiry immediately

### Edge Cases

- Patient uploads invalid media exceeding limits: validation blocks with actionable guidance
- Overlapping date ranges: server-side validation rejects with correction prompts
- Missing questionnaire details for "Yes" answers: system requires completion before submission
- Patient cancels inquiry while provider is drafting a quote: provider's draft is locked with "Inquiry Cancelled" banner upon next save/refresh
- Patient cancels inquiry during simultaneous provider quote submission: system processes cancellation first (inquiry status is source of truth); incoming quote submission rejected with "Inquiry no longer active" error. **Cross-FR note**: FR-004 must implement corresponding rejection handling for this edge case.
- Exclusive provider submits duplicate decline requests: the first accepted request releases the inquiry to normal distribution; later duplicates return the committed result without creating duplicate provider views or notifications.
- Exclusive inquiry reaches its configured expiry without an explicit provider decline: existing expiry rules apply and the decline-triggered redistribution path does not run.
- Distribution job or retry targets a provider that became `Suspended` or `Deactivated` after matching: allocation is revalidated and skipped; no ProviderInquiry or notification is created.
- Provider-status cascade is replayed for the same event: no duplicate cancellations, support flags, or patient messages are produced.
- Provider-status cascade removes the patient's only live offer and the patient had explicitly selected that provider: the inquiry is redistributed only after the patient confirms; until then the patient keeps the Contact Admin/Support action and the inquiry stays flagged `supportRequired = true`.

---

**Document Status**: ✅ Complete  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes

## Appendix: Change Log

| Date | Version | Changes | Author |
| --- | --- | --- | --- |
| 2025-10-23 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-03 | 1.1 | Template normalization; added tenant breakdown, field tables, FR summary, entities, appendices | Product & Engineering |
| 2025-12-01 | 1.2 | Aligned with client scope by removing unsourced budget requirement from System PRD, defining explicit inquiry payload composition, and clarifying anonymization to keep IDs visible while masking name/phone/email until payment confirmation | Product & Engineering |
| 2025-12-16 | 1.3 | Aligned destination selection ordering with FR-028 (regional configuration when available, proximity fallback) | Product & Engineering |
| 2026-02-05 | 1.4 | Added Workflow 5 (Patient-Initiated Inquiry Cancellation), Alternative Flow A4, Screen 8 Cancel Inquiry action + Cancelled stage, Cancellation Rules in Business Rules, REQ-003-013/014/015, updated Key Entities with Cancelled status and cancellation fields, added User Story 4 and edge cases. Cross-FR impact: FR-004, FR-005, FR-006, FR-020, FR-030, FR-001, FR-016, FR-023. See cancel-inquiry-fr-impact-report.md | Product & Engineering |
| 2026-02-08 | 1.5 | Integrity fixes: Added Screen 11 (Cancel Inquiry Confirmation Modal) and Screen 11a (Cancellation Success Confirmation) with formal 5-column field tables and acceptance scenarios. Enumerated default cancellation reason options (admin-configurable via FR-026 Screen 5a). Added 5-minute notification timing SLA to Workflow 5 step 4. Added cross-FR note for FR-004 concurrent cancellation handling. Aligned design complement P02.2 status and status string. Updated system PRD cancellation scope to "before Confirmed stage". | AI |
| 2026-02-10 | 1.6 | Moved Cancel Inquiry screens from Provider Platform section to Patient Platform section (they are patient-facing). Renumbered Screen 11 → Screen 8a (Cancel Inquiry Confirmation Modal) and Screen 11a → Screen 8b (Cancellation Success Confirmation). Updated all internal cross-references. | AI |
| 2026-02-10 | 1.7 | Verification fixes: Added Screen 7a (Provider Selection) with full field table and business rules — resolves orphaned provider selection from Workflow 1. Updated Workflow 1 to separate provider selection (step 7) from review/submission (step 8). Aligned provider response time from 48h to 72h to match system PRD. | AI |
| 2026-02-11 | 1.8 | Workflow 5 (Patient-Initiated Inquiry Cancellation): Updated trigger and Step 1 to include intermediary inquiry detail view before Cancel Inquiry action, aligning with P02.2 design complement flow. Patient now navigates: Dashboard → Inquiry Detail → Cancel Inquiry (action menu) instead of Dashboard → Cancel Inquiry (direct). | AI |
| 2026-03-03 | 1.9 | Clarified that V1 head scan capture is a standardized photo set (multiple 2D views), with true 3D capture deferred to V2. Updated Workflow 1 terminology and Screen 4 accordingly. | AI |
| 2026-08-20 | 2.0 | Cross-FR sync (FR-037 verification): Added Workflow 2 exclusive-provider override branch and Alternative Flow B3 for monitoring-case conversion inquiries with an active provider assignment (REQ-037-029, Business Rule 7); added FR-037/FR-038 as dependencies. See [Change Request](./change-request-2026-08-20-fr037-monitoring-conversion-alignment.md) | Verification alignment (2026-08-20) |
| 2026-08-20 | 2.1 | Added explicit-provider-decline fallback for FR-037/FR-038 monitoring conversions: provider confirmation and reason, audited removal of exclusive routing, idempotent return to normal Workflow 2 distribution, and an explicit boundary preserving existing expiry behavior. See [Change Request](./change-request-2026-08-20-fr037-monitoring-conversion-alignment.md) | Product Team |
| 2026-09-04 | 2.2 | Replaced the fixed Hair/Beard/Both inquiry choice with an Admin-managed treatment-area catalog that carries image/icon metadata, and replaced the fixed 30-day date lead time with an Admin-configured blocked window (default 30 days). Added dynamic API, historical-snapshot, and validation requirements. See [Change Request](./change-request-2026-09-04-inquiry-configuration.md). | Product Owner |
| 2026-09-04 | 2.3 | Corrected the approved default inquiry lead time from 30 days to 3 days; the configurable range and all other date constraints are unchanged. See [Change Request](./change-request-2026-09-04-inquiry-configuration.md). | Product Owner |
| 2026-09-04 | 2.4 | Verification correction: limited exclusive-provider conversion and decline fallback to FR-037, and declared FR-026 as the owner of the inquiry-configuration dependency. | Product Owner |
| 2026-09-04 | 2.5 | Verification correction: aligned Workflow 1's service-selection step with the Admin-managed treatment-area catalog rather than a fixed Hair/Beard/Both enum. | Product Owner |
| 2026-10-14 | 2.6 | Cross-FR sync (FR-014 verification): ProviderInquiry now names its persisted table `inquiry_providers` and defines the per-provider `distributed_at` timestamp (set on first distribution to that provider, including release after an exclusive-provider decline; never overwritten by retries) consumed by FR-014 TTFQ and response rate and the FR-020/FR-030 TTFQ SLA alert | AI Assistant |
| 2026-10-14 | 2.7 | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9: Workflow 2 Alternative Flow B4, Distribution and Cancellation Rules notes, new Rule 6, Screen 8 provider-caused messaging, REQ-003-019/020, Inquiry and ProviderInquiry cause/marker notes, FR-015 dependency, and edge cases. See [Change Request](./change-request-2026-10-14-provider-status-cancellation-cascade.md). Status reset pending consolidated verification. | Vân Tay Media |
| 2026-10-15 | 2.8 | FR-015 v1.16 alignment: providers with `password_set = false` are excluded from allocation, explicit selection, and reassignment until the password is set (Workflow 2 matching, Rule 6, REQ-003-019). See [Change Request](./change-request-2026-10-15-distribution-requires-password-set.md) | Claude |
| 2026-10-16 | 2.9 | MTG-002 quote model alignment (decision M18, cross-FR check against FR-006 and FR-015): a provider suspended or deactivated after acceptance no longer cancels the inquiry. Workflow 2 Alternative Flow B4 step 2 and Outcome, the related business rule, and REQ-003-020 now keep the inquiry open with `supportRequired = true` while FR-006 Alternative Flow B4 closes the booking and an admin rehomes the patient through FR-006 Alternative Flow B5. Pre-acceptance participation cancellation is unchanged. See CR-FR003-20261016-01; CR-FR003-20261014-01 is superseded in part. | Product Owner / Documentation |
| 2026-10-18 | 2.10 | Consolidated verification corrections (CR-FR003-20261016-01; decisions M18, D6, Q9): Workflow 2 Alternative Flow B4 step 4, Screen 8 Notes and REQ-003-020 now separate the patient message by stage. Before acceptance the patient receives the offer-unavailability message with Contact Admin/Support; after acceptance the patient receives the `booking.provider_fault_replacement` notice that an admin will arrange a replacement provider within the same inquiry, with no cancellation copy. B4 step 5 no longer implies that suspension cancels inquiries. Round-two correction (Q45): B4 steps 2 and 4, the Outcome, the provider-status business rule and REQ-003-020 now limit the B5 transfer and the `booking.provider_fault_replacement` notice to bookings before treatment starts; an `In Progress` booking stays `In Progress` for the FR-006 Alternative Flow B7 admin decision, and an `Aftercare` booking follows FR-006 Alternative Flow B6. | AI |
| 2026-10-18 | 2.11 | Final audit corrections (CR-FR003-20261016-01; decisions Q37 and Q43): patient cancellation is now limited to the Inquiry and Quoted stages. A4, Workflow 5 trigger and diagram, Alternative Flow E2, Screen 8 (new Contact Support action), Screen 8a, Screen 8b, Cancellation Rules, REQ-003-012, REQ-003-014 and User Story 4 now say that from acceptance onward the patient sees "Contact support" and an admin cancels the booking through FR-006 with a mandatory reason and audit, the inquiry becomes Cancelled and the accepted quote stays accepted. The inquiry quote cascade now names draft, sent and expired quotes. Key Entities states that each date range carries a stable ID. Added the Product Owner approval row and a document footer. | Product Owner |
| 2026-10-27 | 2.12 | Product Owner decisions on the FR-015 follow-up questions (F9, F1, F2). Before acceptance, when the provider-status cascade cancels a live offer and the patient has no other live offer, the inquiry is now redistributed automatically to eligible providers that have not yet received it; the patient confirms first when they had explicitly selected that provider, and the patient is told "We are finding new offers for you." Updated Workflow 2 Alternative Flow B4 steps 3 and 4 and Outcome, Rule 6, Screen 8 Notes, new REQ-003-021, and Edge Cases. See [CR-FR003-20261027-02](./change-request-2026-10-27-pre-acceptance-redistribution.md). The legacy inquiry stage and `inquiry_providers` participation value migration is recorded in [CR-FR003-20261027-01](./change-request-2026-10-27-legacy-status-value-migration.md); the requirement values are unchanged. | Product Owner |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
| --- | --- | --- | --- |
| Product Owner | Product Owner | 2026-10-18 | Approved via MTG-002 decision log (documentation only), v2.11 (CR-FR003-20261016-01) |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-003 from system-prd.md
**Last Updated**: 2026-10-27
