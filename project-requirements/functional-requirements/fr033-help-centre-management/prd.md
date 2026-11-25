# FR-033 - Help Centre Content Management

**Module**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management | P-08: Help Center & Support Access
**Feature Branch**: `fr033-help-centre-management`
**Created**: 2025-11-17
**Status**: ✅ Verified & Approved
**Source**: FR-033 from system-prd.md

---

## Executive Summary

The Help Centre Content Management module provides a centralized knowledge base and support system for both provider and patient platforms. This feature enables Hairline admins to create, organize, and maintain comprehensive help documentation that providers and patients can access for self-service support, reducing support ticket volume and improving user efficiency across all platform tenants.

**Key Objectives**:

- Provide providers and patients with 24/7 access to self-service help resources
- Reduce support ticket volume by enabling users to find answers independently
- Enable admins to centrally manage and update help content for TWO distinct audiences: Providers and Patients
- Maintain separate content repositories for provider-facing and patient-facing content to prevent cross-contamination (REQ-033-001)
- Maintain a canonical Help Centre taxonomy (categories, ordering, visibility) aligned with `system-prd.md` and tenant UX (FR-032 / FR-035)
- Support scalable content organization with multi-category structure for each audience
- Maintain content consistency and quality through admin-controlled publishing workflow

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-08)**: Read-only access to Patient Help Centre content via FR-035 (Patient Help Center & Support Submission module) - patients view FAQs, guides, tutorials, and resources tailored for patient audience (REQ-033-008)
- **Provider Platform (PR-06)**: Read-only access to Provider Help Centre content via FR-032 (Provider Dashboard Settings module) - providers view FAQs, guides, tutorials, and resources tailored for provider audience (REQ-033-007)
- **Admin Platform (A-09)**: Full Help Centre content management capabilities for BOTH provider and patient audiences including content creation, editing, categorization, versioning, and publishing with clear audience separation
- **Shared Services (S-XX)**: No dedicated shared services required (uses standard S-05 for media storage)

### Multi-Tenant Breakdown

**Patient Platform (P-08)**:

- Patients access Help Centre content via FR-035 (Patient Help Center & Support Submission module)
- Content managed by admins in FR-033 is displayed to patients in FR-035 as read-only resources
- Patient Help Centre includes: FAQs, Tutorial Guides, Troubleshooting Tips, Resource Library, Video Tutorials (REQ-033-003)
- No Service Status page for patients (provider-only feature)
- Content updates from FR-033 propagate to FR-035 patient views within 1 minute, including edits, reordering, unpublishing and deleting (REQ-033-034, REQ-035-028)

**Provider Platform (PR-06)**:

- Providers access Help Centre content via FR-032 (Provider Dashboard Settings module)
- Content managed by admins in FR-033 is displayed to providers in FR-032 as read-only resources
- Provider Help Centre includes 10 categories aligned with `system-prd.md`/FR-032: FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials (REQ-033-002)
- Content updates from FR-033 propagate to FR-032 provider views within 1 minute (REQ-033-034, REQ-032-092)
- Search functionality across all provider Help Centre content (REQ-033-035)

**Admin Platform (A-09)**:

- Admins manage Help Centre content for TWO distinct audiences: Providers and Patients
- Content repositories completely separated by audience type to prevent cross-contamination (REQ-033-001)
- Admin selects "Provider" or "Patient" audience when creating/editing content
- **Provider Content Management**:
  - Manage FAQ content (for FR-032 Screen 5.1)
  - Manage article content: Tutorial Guides, Troubleshooting Tips, Policies (for FR-032 Screen 5.2)
  - Upload and manage Resource Library files (for FR-032 Screen 5.3)
  - Upload and manage Video Tutorials (for FR-032 Screen 5.4)
  - Manage Service Status components, incidents, and maintenance windows (for FR-032 Screen 5.7) (REQ-033-030)
  - Configure category metadata for all 10 provider categories (visibility, ordering, labels, descriptions, routing)
- **Patient Content Management**:
  - Manage FAQ content (for FR-035 patient FAQs)
  - Manage article content: Tutorial Guides, Troubleshooting Tips (for FR-035 patient articles)
  - Upload and manage Resource Library files (for FR-035 patient resources)
  - Upload and manage Video Tutorials (for FR-035 patient videos)
  - No Service Status management for patients (provider-only feature) (REQ-033-030)
- **Shared Admin Capabilities** (applies to both provider and patient content):
  - Publish/unpublish content to control visibility (REQ-033-037)
  - Version control for content updates with change tracking (REQ-033-012)
  - Preview content in audience-facing layout before publishing (REQ-033-011)
  - Audit trail for all content changes (who, when, what changed) (REQ-033-015)
  - Bulk operations for content management (REQ-033-062)
  - Content analytics (view counts, search queries, popular topics by audience) (REQ-033-018)
  - Multi-language content management (future enhancement)

**Shared Services (S-XX)**:

- Standard media storage service (S-05) for uploaded documents, videos, images
- Standard notification service (S-03) for content update notifications (future enhancement)

### Communication Structure

**In Scope**:

- Admin-to-provider communication via published Help Centre content
- Content update notifications (future enhancement)

**Out of Scope**:

- Provider Contact Support form submissions (handled by FR-034: Support Center & Ticketing; forms in provider UX create support cases in FR-034) (REQ-033-032)
- Provider Feedback & Suggestions form submissions (handled by FR-034: Support Center & Ticketing; forms in provider UX create support cases in FR-034) (REQ-033-032)
- Real-time chat between providers and admin (handled by separate communication module A-10) (REQ-033-032)
- Provider-to-provider communication in community forum (future enhancement; FR-033 can only configure category presentation/routing) (REQ-033-032)
- Automated chatbot responses (future V2 enhancement) (REQ-033-032)
- Email digest subscriptions for content updates (future enhancement) (REQ-033-032)

### Entry Points

**Provider Entry**:

- Providers access Help Centre via "Help Centre" menu item in provider platform navigation (REQ-033-031)
- Direct link from provider dashboard settings page (FR-032 integration point) (REQ-033-031)
- Context-sensitive help links from various provider platform screens (future enhancement)

**Admin Entry**:

- Admins access Help Centre management via Settings > Help Centre Management (REQ-033-031)
- Quick access from admin dashboard for content updates (REQ-033-031)

---

## Business Workflows

### Provider Consumption (via FR-032)

**Actors**: Provider (clinic staff), System (FR-032 provider dashboard), FR-033 Help Centre content service  
**Trigger**: Provider clicks "Help Centre" menu item in provider platform (see FR-032 Business Workflows)  
**Outcome**: Provider views provider-facing Help Centre screens backed by content managed in FR-033

**Behaviour (high level)**:

1. Provider navigates to "Help Centre" from provider platform navigation (per FR-032).
2. FR-032 calls FR-033 provider Help Centre APIs to load the provider category registry (10 categories) and published provider-audience content (FAQs, Articles, Resources, Videos, Service Status).
3. System displays category navigation and content in provider-facing layouts defined in FR-032 (Screens 5.x), routing Contact Support/Feedback categories to their form flows (FR-034 integration).
4. Providers interact with content in read-only mode; any feedback or support submissions are handled by FR-032 + FR-034. (REQ-033-007)

---

### Main Flow: Admin Creates Help Centre Content

**Actors**: Admin (Help Centre content manager), System
**Trigger**: Admin needs to create new help content or update existing content
**Outcome**: New or updated content published to Help Centre for provider access

**Steps**:

1. Admin navigates to Settings > Help Centre Management
2. System displays Help Centre management dashboard with category navigation aligned to the provider Help Centre taxonomy (10 categories)
3. Admin selects Help Centre category to manage (e.g., FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials)
4. Admin clicks the primary action for the selected category (Create Content / Manage / Configure)
5. System displays the appropriate editor optimized for the selected category:
   - **FAQs**: FAQ editor with question/answer fields, topic assignment, accordion preview
   - **Articles**: Article editor with rich text, table of contents generation, article layout preview
   - **Resources**: File upload interface with metadata (name, description, category, file type), file viewer preview
   - **Videos**: Video upload interface with title, description, thumbnail, video player preview
   - **Service Status**: Status component/incident management interface
   - **Contact Support / Feedback & Suggestions / Community Forum**: Category configuration (copy, routing, and availability; submissions and/or forum interactions handled outside FR-033)
6. Admin enters details using the category-specific editor
7. Admin uploads attachments if needed (images, PDFs, videos) - optimized for the content type
8. Admin assigns tags for content organization and searchability
9. Admin clicks "Preview" to see how content will appear to providers in the specific subscreen layout (REQ-033-011)
10. System renders preview matching provider-facing layout (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, status page for service status) (REQ-033-011)
11. Admin reviews preview and clicks "Save as Draft" or "Publish"
12. System checks the required fields (the same check for Save as Draft and for Publish, REQ-033-056) and saves content with status (Draft/Published) and timestamps (REQ-033-053)
13. System logs content creation in audit trail (admin name, timestamp, action) (REQ-033-015)
14. If published, system makes content available in the Help Centre category of its audience (provider or patient) within 1 minute (REQ-033-034)
15. System displays success confirmation with link to view published content (REQ-033-053)

### Alternative Flows

**A2: Admin Edits Existing Help Centre Content**:

- **Trigger**: Admin needs to update outdated or incorrect help content
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management
  2. Admin searches/filters content by category, title, or tags
  3. Admin clicks "Edit" on target content item
  4. System loads content editor pre-filled with existing content (REQ-033-054)
  5. Admin makes changes to title, body, attachments, or content kind (a change of kind also moves the content to the matching section) (REQ-033-036)
  6. Admin previews changes to verify formatting and accuracy
  7. Admin saves changes with optional "Version note" describing what changed (REQ-033-054)
  8. System creates a new version on save (opening the editor or cancelling creates none), updates the content version and logs change in audit trail; if two admins edit the same item, the last save wins and both saves are versions (REQ-033-054)
  9. If content is published, system updates the Help Centre content of its audience within 1 minute (REQ-033-034)
  10. System sends notification to admins who subscribed to content change alerts (future enhancement)
- **Outcome**: Content updated with new version and change tracked in audit trail

**A3: Admin Organizes FAQ Content into Topics**:

- **Trigger**: Admin needs to organize multiple FAQ items under topic sections for better navigation
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management > FAQ Management (Screen 2)
  2. System displays all FAQ items with current organization structure
  3. Admin clicks "Manage Topics" to create/edit FAQ topic sections
  4. System displays topic management interface with drag-and-drop organization
  5. Admin creates new topic section (e.g., "Quote Submission", "Payment Processing")
  6. Admin assigns FAQ items to topics by dragging items into topic groups
  7. Admin reorders topics and FAQ items within topics for logical flow
  8. Admin previews FAQ accordion layout to verify organization
  9. Admin saves organization structure
  10. System updates FAQ navigation structure for provider Help Centre (FR-032 Screen 5.1)
  11. Provider Help Centre reflects new organization in accordion layout within 1 minute (REQ-033-034)
- **Outcome**: FAQ content organized into logical topic sections displayed in accordion layout for easier provider navigation

**A4: Admin Uploads Video Tutorial**:

- **Trigger**: Admin needs to add video tutorial to Help Centre
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management > Video Tutorial Management (Screen 5)
  2. Admin clicks "Create New Video Tutorial"
  3. System displays video upload form with fields: title, description, video file upload, thumbnail image, transcript (optional), tags
  4. Admin enters title and description for video tutorial
  5. Admin uploads video file (supports MP4, MOV formats, max 500MB) (REQ-033-077)
  6. System validates file size, format, and begins upload to media storage (S-05)
  7. System displays upload progress bar (REQ-033-077)
  8. System auto-extracts video duration and generates thumbnail from video frame (10% mark) (REQ-033-077)
  9. Admin uploads custom thumbnail image or uses auto-generated thumbnail
  10. Admin optionally enters video transcript for accessibility
  11. Admin previews video in video player interface (matches FR-032 Screen 5.4)
  12. System processes video for streaming optimization (if applicable); if processing fails, the processing status becomes Failed, the admin is told and can re-upload, and a new item stays Draft; when the file of a Published video is replaced or its source is switched, the previous video stays live for viewers until the new one is Ready, and if the new file fails the old one stays in place and the admin is told (REQ-033-077)
  13. Admin publishes video tutorial; an uploaded video cannot be published until its processing status is Ready (embedded videos are exempt) (REQ-033-077)
  14. System makes video available in provider Help Centre Video Tutorials subscreen (FR-032 Screen 5.4)
- **Outcome**: Video tutorial uploaded, processed, and published to Help Centre with video player interface

**A5: Admin Unpublishes Outdated Content**:

- **Trigger**: Admin needs to remove outdated or incorrect content from provider view
- **Steps**:
  1. Admin identifies outdated content item in content list
  2. Admin clicks "Unpublish" action on content item
  3. System prompts admin to confirm unpublish action with reason (REQ-033-055)
  4. Admin enters reason (e.g., "Content outdated, new version coming soon")
  5. Admin confirms unpublish
  6. System changes content status from "Published" to "Unpublished" (REQ-033-055)
  7. System removes content from the Help Centre view of its audience within 1 minute (REQ-033-055, REQ-033-034)
  8. System logs unpublish action in audit trail with reason (REQ-033-055)
  9. Content remains in admin view as "Unpublished" for future editing or re-publishing (REQ-033-055)
- **Outcome**: Content removed from provider view but preserved in admin system for future use

**B1: Content Validation Fails**:

- **Trigger**: Admin attempts to save or publish content with missing required fields or invalid format
- **Steps**:
  1. Admin completes content creation form and clicks "Save as Draft" or "Publish"
  2. System checks the required fields of the content kind, the same list for both actions (FAQ: question, answer, topic; article: title, content, article type; resource: name, file; video: title, source type) (REQ-033-056)
  3. System detects validation error (e.g., missing title, empty content body, unsupported file format)
  4. System displays error message highlighting missing/invalid fields (REQ-033-056)
  5. Admin corrects validation errors
  6. Admin re-submits content (save or publish)
  7. System re-validates and proceeds with the save or publish if all validations pass
- **Outcome**: Validation errors corrected and content saved or published successfully

**B2: File Upload Exceeds Size Limit**:

- **Trigger**: Admin attempts to upload file larger than maximum allowed size
- **Steps**:
  1. Admin selects file for upload (video, PDF, image) in appropriate management screen
  2. System checks file size against the limit of the upload kind (resource file 50MB whatever its type, uploaded video 500MB, resource thumbnail 1MB, video thumbnail 2MB, image placed inside article or FAQ text 10MB) (REQ-033-057, REQ-033-010)
  3. File exceeds size limit
  4. System displays error message with file size limit and suggested alternatives (compress file, use external video hosting) (REQ-033-057)
  5. Admin reduces file size or uses alternative hosting (YouTube/Vimeo embed link) (REQ-033-057)
  6. Admin re-uploads compressed file or adds external video embed link
  7. System validates new file/link and proceeds with upload
  8. System scans the file for viruses; a file that fails is rejected and not stored, the admin sees "File failed security scan. Upload a clean file.", and the event is written to the audit trail (REQ-033-098)
- **Outcome**: File size issue resolved and content uploaded successfully

**A6: Admin Updates Service Status**:

- **Trigger**: Admin needs to update platform service status or create incident report
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management > Service Status Management (Screen 6)
  2. System displays current overall status, service components list, incident history, maintenance schedule
  3. Admin updates service component status (e.g., "API Service" → Degraded) (REQ-033-081)
  4. System automatically recalculates overall status based on component statuses only, not on open incidents or maintenance (unless an admin has set the overall status by hand) (REQ-033-080)
  5. Admin creates new incident: enters title, description, selects affected services, sets status (Investigating) (REQ-033-082)
  6. System creates incident record and adds to incident history timeline (REQ-033-083)
  7. Admin updates incident status as investigation progresses (Investigating → Identified → Monitoring → Resolved) (REQ-033-082)
  8. System updates incident timeline with each status change (REQ-033-083)
  9. Status updates propagate to provider Service Status subscreen (FR-032 Screen 5.7) within 1 minute (REQ-033-033)
  10. Providers see the updated status in the status page interface within 1 minute (REQ-033-033)
- **Outcome**: Service status updated and displayed to providers in status page interface

**A7: Admin Restores Archived Content**:

- **Trigger**: Admin needs to bring back content that was deleted (archived)
- **Steps**:
  1. Admin opens a content list (FAQs, articles, resources or videos) and selects the "Archived" filter (admin only) (REQ-033-100)
  2. Admin clicks "Restore" on the archived item
  3. System returns the item as Draft; Related Content links removed at deletion (REQ-033-092) are not put back (REQ-033-100)
- **Outcome**: Archived item is back in the content list as Draft and can be edited and published again

---

## Screen Specifications

### Admin Platform Screens

#### Provider Help Centre Content Management

### Screen 1: Provider Help Centre Management Dashboard

**Purpose**: Landing page for provider-facing Help Centre management with category navigation aligned to the 10-category provider taxonomy. Provides overview and quick access to manage content-backed categories (FAQs, Articles, Resources, Videos, Service Status) and configure non-content categories (Contact Support, Feedback & Suggestions, Community Forum).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Category Navigation | navigation menu | Yes | Links to category management for the 10 provider Help Centre categories: FAQ's (Screen 2), Tutorial Guides (Screen 3, filtered), Contact Support (Screen 1.1), Troubleshooting Tips (Screen 3, filtered), Resource Library (Screen 4), Community Forum (Screen 1.1), Feedback & Suggestions (Screen 1.1), Service Status (Screen 6), Policy Information (Screen 3, filtered), Video Tutorials (Screen 5) | N/A | ENT-help-centre-category.label |
| Quick Stats | display cards | No | Summary statistics: total content, published content, draft content, total views | Read-only, calculated | ENT-help-centre-stats.total_content_count, ENT-help-centre-stats.published_content_count, ENT-help-centre-stats.draft_content_count, ENT-help-centre-stats.total_views |
| Recent Activity | timeline | No | Recent content changes and updates | Read-only, sorted by date | ENT-help-centre-audit-entry.action_type, ENT-help-centre-audit-entry.occurred_at, ENT-help-centre-audit-entry.target_id |

**Business Rules**:

- Dashboard provides category navigation matching the provider Help Centre taxonomy in `system-prd.md`/FR-032 (10 categories) (REQ-033-049)
- Clicking "FAQs" category navigates to Screen 2 (FAQ Management) where FAQ list is displayed (REQ-033-049)
- Clicking "Tutorial Guides" navigates to Screen 3 (Article Management) filtered to Article Type = Tutorial Guide (REQ-033-049)
- Clicking "Troubleshooting Tips" navigates to Screen 3 (Article Management) filtered to Article Type = Troubleshooting Tip (REQ-033-049)
- Clicking "Policy Information" navigates to Screen 3 (Article Management) filtered to Article Type = Policy Information (REQ-033-049)
- Clicking "Resources" category navigates to Screen 4 (Resource Management) where resource list is displayed (REQ-033-049)
- Clicking "Videos" category navigates to Screen 5 (Video Management) where video list is displayed (REQ-033-049)
- Clicking "Service Status" category navigates to Screen 6 (Service Status Management) where service status overview is displayed (REQ-033-049)
- Clicking "Contact Support", "Feedback & Suggestions", or "Community Forum" navigates to Screen 1.1 (Category Configuration) for those categories (REQ-033-049)
- Quick stats update in real-time showing aggregate metrics across all content types (REQ-033-050)
- Recent activity shows: content created/edited/published, category configuration changes, service status updates (REQ-033-050)

**Notes**:

- Dashboard serves as landing page and navigation hub for Help Centre management
- Category navigation matches the provider Help Centre taxonomy in `system-prd.md`/FR-032 (10 categories)
- Each category tile/card links to the corresponding management screen or configuration screen
- Visual indicators on category cards can show content count or status summary
- Breadcrumb navigation: Settings > Help Centre Management

---

### Screen 1.1: Provider Help Centre Category Configuration

**Purpose**: Configure the provider Help Centre category registry (labels, ordering, visibility, and routing) for categories that are not pure content lists (Contact Support, Feedback & Suggestions, Community Forum), and manage any category-level copy shown above downstream experiences.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Category List | table/list | Yes | Provider categories with ordering and visibility controls | Categories are predefined; cannot be deleted (REQ-033-043) | ENT-help-centre-category.category_key |
| Display Order | number / drag-drop | Yes | Order categories appear in provider Help Centre navigation | Integer; drag-and-drop supported | ENT-help-centre-category.display_order |
| Visibility Toggle | toggle | Yes | Show/Hide category in provider Help Centre navigation | Every hide (any of the 10 categories) asks the admin for confirmation (REQ-033-044) | ENT-help-centre-category.visible |
| Category Label | text | Yes | Display label per category | Max 50 chars (REQ-033-048) | ENT-help-centre-category.label |
| Category Description | textarea | No | Short description shown on category tile/landing | Max 200 chars (REQ-033-048) | ENT-help-centre-category.description |
| Routing Type | dropdown | Yes | How the category behaves in provider UX | Content List, Ticket Form, External Link, Coming Soon (REQ-033-045) | ENT-help-centre-category.routing_type |
| External URL | url | No | Used when Routing Type = External Link (e.g., Community Forum link-out) | Must be valid HTTPS URL (REQ-033-046) | ENT-help-centre-category.external_url |
| Contact Support Intro Copy | rich text | No | Admin-managed copy shown above the Contact Support submission CTA/form | Sanitized HTML (REQ-033-048) | ENT-help-centre-category.intro_copy |
| Feedback & Suggestions Intro Copy | rich text | No | Admin-managed copy shown above the Feedback submission CTA/form | Sanitized HTML (REQ-033-048) | ENT-help-centre-category.intro_copy |

**Business Rules**:

- Provider Help Centre categories are fixed to the 10-category taxonomy in `system-prd.md`; admins can reorder and toggle visibility but cannot add/remove categories. (REQ-033-043)
- For Contact Support and Feedback & Suggestions, Routing Type MUST be Ticket Form and MUST route to the FR-034-backed submission flows exposed in provider UX (FR-032 integration). (REQ-033-045)
- For Community Forum, Routing Type defaults to Coming Soon in MVP; if set to External Link, the External URL is required. (REQ-033-046)
- Changes to category registry propagate to provider Help Centre navigation within 1 minute. (REQ-033-033)
- All category configuration changes are versioned and recorded in audit trail (who/when/old value/new value). (REQ-033-047)

---

### Screen 2: Provider FAQ Management (for FR-032 Screen 5.1)

**Purpose**: Manage all FAQ content that displays in accordion layout on provider platform (matches FR-032 Screen 5.1). Admin can view FAQ list, add new FAQs, edit existing FAQs, delete FAQs, and organize by topics.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| FAQ List | table/list | Yes | List of all FAQ items organized by topics | Each row: question, topic, display order, status, helpfulness rating, actions (Edit, Delete, Preview) | ENT-help-centre-content.title, ENT-help-centre-content.topic, ENT-help-centre-content.display_order, ENT-help-centre-content.publish_status, ENT-help-centre-content.helpfulness_rating |
| FAQ Question | text | Yes | FAQ question text | Max 200 chars (REQ-033-065) | ENT-help-centre-content.title |
| FAQ Answer | rich text | Yes | FAQ answer content | Max 5000 chars, supports HTML formatting (REQ-033-065) | ENT-help-centre-content.body |
| FAQ Topic | dropdown | Yes | Topic category for organization | Pre-defined topics or create new (REQ-033-065) | ENT-help-centre-content.topic |
| Display Order | number | No | Order within topic | Integer, auto-incremented (REQ-033-065) | ENT-help-centre-content.display_order |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (REQ-033-065, REQ-033-099) | ENT-help-centre-content.publish_status |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback (REQ-033-087, REQ-033-096) | ENT-help-centre-content.helpfulness_rating |
| Action Buttons | buttons | Yes | Add New FAQ, Edit, Delete, Preview, Manage Topics | N/A | no graph field (control) |

**Business Rules**:

- FAQ list displays all FAQs organized by topics with expandable topic sections (REQ-033-064)
- FAQ list filterable by topic, status, and searchable by question text (REQ-022-118)
- "Add New FAQ" button opens FAQ creation form (inline or modal)
- "Edit" button on each FAQ opens FAQ editor pre-filled with existing content (REQ-033-060)
- "Delete" button on each FAQ prompts confirmation before deletion (soft-delete) (REQ-033-059)
- "Preview" button shows exact accordion layout as providers will see (FR-032 Screen 5.1) (REQ-033-064)
- "Manage Topics" button opens topic management interface (create, edit, delete, reorder topics)
- FAQs organized by topics with drag-and-drop reordering within topics (REQ-033-064)
- Multiple FAQs can be edited in batch (REQ-033-062)
- Helpfulness feedback tracked per FAQ for analytics (REQ-033-087)
- List has an admin-only "Archived" filter; "Restore" on an archived FAQ returns it as Draft (REQ-033-100)
- FAQ editor optimized for accordion display format (question as header, answer as expandable content) (REQ-033-064)

**Notes**:

- FAQ management interface: list view with action buttons for each FAQ item
- FAQ creation/editing: form with question field at top, answer field below with rich text editor
- Topic selector with "Create New Topic" option
- Drag-and-drop interface for reordering FAQs within topics
- Preview shows accordion layout with expand/collapse functionality matching FR-032 Screen 5.1
- Bulk operations: assign multiple FAQs to topic, change status (Publish or Unpublish only) for multiple FAQs, delete multiple FAQs (REQ-033-062)
- Breadcrumb navigation: Settings > Help Centre Management > FAQs

---

### Screen 2.1: Provider FAQ Add/Edit Form

**Purpose**: Create new FAQ or edit existing FAQ content. Accessed from Screen 2 (FAQ Management) via "Add New FAQ" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| FAQ Question | text | Yes | FAQ question text | Max 200 chars, required | ENT-help-centre-content.title |
| FAQ Answer | rich text | Yes | FAQ answer content | Max 5000 chars, supports HTML formatting, required | ENT-help-centre-content.body |
| FAQ Topic | dropdown | Yes | Topic category for organization | Pre-defined topics or create new, required | ENT-help-centre-content.topic |
| Display Order | number | No | Order within topic | Integer, auto-incremented if not specified | ENT-help-centre-content.display_order |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (Unpublish action is the only way out); defaults to Draft (REQ-033-099) | ENT-help-centre-content.publish_status |
| Preview Button | button | No | Preview FAQ in accordion layout | N/A | no graph field (control) |
| Save Button | button | Yes | Save FAQ (as Draft or Publish) | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to FAQ list | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Add New FAQ" or "Edit" is clicked from Screen 2
- If editing existing FAQ, form is pre-filled with current FAQ data (REQ-033-060)
- If creating new FAQ, form starts empty with default values (Draft status, auto-incremented display order) (REQ-033-060)
- Topic dropdown includes "Create New Topic" option which opens topic creation dialog
- Rich text editor for FAQ Answer supports: bold, italic, lists, links, images (REQ-033-061)
- "Preview" button shows FAQ in accordion layout exactly as providers will see (FR-032 Screen 5.1) (REQ-033-064)
- Form validation: question, answer and topic are required before saving, for Save as Draft and for Publish alike (REQ-033-065, REQ-033-056)
- On save, FAQ is created/updated and admin returns to Screen 2 (FAQ Management) with updated list (REQ-033-060)
- On cancel, changes are discarded and admin returns to Screen 2 (REQ-033-060)

**Notes**:

- Form layout: question field at top, answer field below with rich text editor
- Character counters for question (200 max) and answer (5000 max)
- Topic selector with search/autocomplete for existing topics
- Save options: "Save as Draft" or "Publish" buttons (REQ-033-053)
- Success message displayed after save: "FAQ saved successfully" or "FAQ published successfully" (REQ-033-053)
- Breadcrumb navigation: Settings > Help Centre Management > FAQs > [Add New FAQ / Edit FAQ]

---

### Screen 2.2: FAQ Topic Management

**Purpose**: Manage FAQ topics used to group FAQ items for the provider Help Centre (FR-032 Screen 5.1) and the patient Help Centre (FR-035). One screen serves both audiences; an audience switch selects whether Provider or Patient topics are shown and edited. Admin can create, edit, delete, and reorder topics, and see which FAQs belong to each topic.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Audience Switch | toggle | Yes | Selects whether Provider or Patient topics are shown and edited | Provider or Patient; starts on the audience of the FAQ screen it was opened from | ENT-faq-topic.audience |
| Topic List | table/list | Yes | List of all FAQ topics of the selected audience | Each row: topic name, description (optional), number of FAQs, display order, actions (Edit, Delete) | ENT-faq-topic.name, ENT-faq-topic.description, ENT-faq-topic.faq_count, ENT-faq-topic.display_order |
| Topic Name | text | Yes | Name of topic section (e.g., "Quote Submission", "Payment Processing") | Max 100 chars, unique per audience (Provider/Patient) (REQ-033-066) | ENT-faq-topic.name |
| Topic Description | textarea | No | Optional description for internal/admin context | Max 250 chars (REQ-033-066) | ENT-faq-topic.description |
| Display Order | number | Yes | Order in which topic appears in FAQ accordion | Integer, required; supports drag-and-drop reordering (REQ-033-066) | ENT-faq-topic.display_order |
| Number of FAQs | display | No | Count of FAQs currently assigned to topic | Read-only, calculated (REQ-033-068) | ENT-faq-topic.faq_count |
| Action Buttons | buttons | Yes | Add New Topic, Edit, Delete, Save Order, Cancel | N/A | no graph field (control) |

**Business Rules**:

- Screen opened from Screen 2 (Provider FAQ Management) or Screen 9 (Patient FAQ Management) when admin clicks "Manage Topics".
- Topic list shows all topics for the selected audience (Provider or Patient, chosen with the audience switch) with current display order.
- "Add New Topic" opens inline row or modal with fields: Topic Name, Topic Description, Display Order (auto-suggested as last).
- "Edit" opens topic edit form (inline or modal) allowing admin to change name, description, and display order.
- "Delete" prompts confirmation; topics with assigned FAQs cannot be hard-deleted (REQ-033-067):
  - If topic has FAQs, system blocks deletion and prompts admin to reassign or remove FAQs first. (REQ-033-067)
  - Implementation may soft-delete topic only when no FAQs are assigned. (REQ-033-067)
- Topics support drag-and-drop reordering; moving rows updates Display Order values. (REQ-033-066)
- "Save Order" persists new topic ordering; the FAQ accordion of the selected audience (FR-032 Screen 5.1 for providers, FR-035 for patients) reflects updated topic order. (REQ-033-066)
- "Cancel" discards unsaved changes to ordering or edits and returns admin to the FAQ management screen it was opened from. (REQ-033-066)
- Validation ensures Topic Name is required and unique within the audience; Display Order must be a positive integer. (REQ-033-066)

**Notes**:

- Visual layout: list of topics with drag handle on each row for reordering.
- Badge or column for "Number of FAQs" to help admins understand impact before deleting topics.
- Optional search/filter for topic name when list is long.
- Breadcrumb navigation: Settings > Help Centre Management > FAQs > Manage Topics.

---

### Screen 3: Provider Article Management (for FR-032 Screen 5.2)

**Purpose**: Manage all article content (Tutorial Guides, Troubleshooting Tips, Policy Information) that displays in article layout on provider platform (matches FR-032 Screen 5.2). Admin can view article list, add new articles, edit existing articles, delete articles, and organize by type.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Article List | table/list | Yes | List of all articles organized by type | Each row: title, article type, category/tags, status, last updated, view count, actions (Edit, Delete, Preview) | ENT-help-centre-content.title, ENT-help-centre-content.content_type, ENT-help-centre-content.tags, ENT-help-centre-content.publish_status, ENT-help-centre-content.updated_at, ENT-help-centre-content.view_count |
| Article Title | text | Yes | Article title | Max 200 chars (REQ-033-070) | ENT-help-centre-content.title |
| Article Content | rich text | Yes | Full article content with formatting | Max 10,000 chars, supports HTML, headings, lists, images, tables (REQ-033-070) | ENT-help-centre-content.body |
| Article Type | dropdown | Yes | Tutorial Guide, Troubleshooting Tip, Policy Information | Pre-defined types (REQ-033-070) | ENT-help-centre-content.content_type |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new (REQ-033-070) | ENT-help-centre-content.tags |
| Table of Contents | auto-generated | No | Auto-generated from headings (for articles >1000 words) | Read-only, generated on save (REQ-033-071) | ENT-help-centre-content.table_of_contents |
| Related Articles | multi-select | No | Links to related articles | References to other articles (REQ-033-063) | ENT-help-centre-content.related_content_ids |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (REQ-033-099) | ENT-help-centre-content.publish_status |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback (REQ-033-087, REQ-033-096) | ENT-help-centre-content.helpfulness_rating |
| Action Buttons | buttons | Yes | Add New Article, Edit, Delete, Preview | N/A | no graph field (control) |

**Business Rules**:

- Article list displays all articles organized by type (Tutorial Guide, Troubleshooting Tip, Policy Information) (REQ-033-069)
- Article list filterable by type, category/tags, status, and searchable by title (REQ-022-119)
- "Add New Article" button opens article creation form (inline or modal)
- "Edit" button on each article opens article editor pre-filled with existing content
- "Delete" button on each article prompts confirmation before deletion (soft-delete) (REQ-033-059)
- "Preview" button shows exact article layout as providers will see (FR-032 Screen 5.2) (REQ-033-069)
- Article editor optimized for article layout format (full-width content with formatted text, images, code blocks) (REQ-033-069)
- Rich text editor supports: headings (H1-H6), bold, italic, lists, links, images, tables, code blocks (REQ-033-061)
- Table of contents auto-generated for articles with multiple headings (articles >1000 words) (REQ-033-071)
- Related articles can be manually assigned or auto-suggested based on tags/category (REQ-033-063)
- Print-friendly view available in preview (REQ-033-069)
- List has an admin-only "Archived" filter; "Restore" on an archived article returns it as Draft (REQ-033-100)

**Notes**:

- Article management interface: list view with action buttons for each article item
- Article creation/editing: full-featured rich text editor with formatting toolbar
- Image upload inline within editor
- Screenshot/image insertion with captions
- Step-by-step tutorial format: numbered lists with visual separators
- Preview shows: formatted article with table of contents (if applicable), related articles section matching FR-032 Screen 5.2
- Character counter for content body
- Bulk operations: change status (Publish or Unpublish only) for multiple articles, delete multiple articles (REQ-033-062)
- Breadcrumb navigation: Settings > Help Centre Management > Articles

---

### Screen 3.1: Provider Article Add/Edit Form

**Purpose**: Create new article or edit existing article content. Accessed from Screen 3 (Article Management) via "Add New Article" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Article Title | text | Yes | Article title | Max 200 chars, required (REQ-033-070) | ENT-help-centre-content.title |
| Article Content | rich text | Yes | Full article content with formatting | Max 10,000 chars, supports HTML, headings, lists, images, tables, required (REQ-033-070) | ENT-help-centre-content.body |
| Article Type | dropdown | Yes | Tutorial Guide, Troubleshooting Tip, Policy Information | Pre-defined types, required (REQ-033-070) | ENT-help-centre-content.content_type |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new | ENT-help-centre-content.tags |
| Related Articles | multi-select | No | Links to related articles | References to other articles (REQ-033-063) | ENT-help-centre-content.related_content_ids |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (Unpublish action is the only way out); defaults to Draft (REQ-033-099) | ENT-help-centre-content.publish_status |
| Table of Contents | auto-generated | No | Auto-generated from headings (for articles >1000 words) | Read-only, generated on save (REQ-033-071) | ENT-help-centre-content.table_of_contents |
| Preview Button | button | No | Preview article in article layout | N/A | no graph field (control) |
| Save Button | button | Yes | Save article (as Draft or Publish) | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to article list | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Article" or "Edit" is clicked from Screen 3
- If editing existing article, form is pre-filled with current article data (REQ-033-060)
- If creating new article, form starts empty with default values (Draft status) (REQ-033-060)
- See REQ-033-061.
- Table of contents auto-generated for articles with multiple headings (articles >1000 words) on save (REQ-033-071)
- "Preview" button shows article in article layout exactly as providers will see (FR-032 Screen 5.2) (REQ-033-069)
- Form validation: title, content and article type are required before saving, for Save as Draft and for Publish alike (REQ-033-070, REQ-033-056)
- Image upload available inline within editor (REQ-033-061)
- Related articles can be manually selected or auto-suggested based on tags/category (REQ-033-063)
- On save, article is created/updated and admin returns to Screen 3 (Article Management) with updated list (REQ-033-060)
- On cancel, changes are discarded and admin returns to Screen 3 (REQ-033-060)

**Notes**:

- Full-featured rich text editor with formatting toolbar
- Character counter for content body (10,000 max)
- Image upload inline within editor with caption support
- Step-by-step tutorial format support: numbered lists with visual separators
- See REQ-033-069.
- See REQ-033-053.
- Success message displayed after save (REQ-033-053)
- Breadcrumb navigation: Settings > Help Centre Management > Articles > [Add New Article / Edit Article]

---

### Screen 4: Provider Resource Library Management (for FR-032 Screen 5.3)

**Purpose**: Manage all downloadable resources (templates, documents, PDFs) that display in file viewer interface on provider platform (matches FR-032 Screen 5.3). Admin can view resource list, add new resources, edit existing resources, delete resources, and organize by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Resource List | table/list | Yes | List of all resources organized by category | Each row: name, category, file type, file size, download count, status, last updated, actions (Edit, Delete, Preview, Download) | ENT-help-centre-content.title, ENT-help-centre-content.resource_category, ENT-help-centre-content.file_type, ENT-help-centre-content.file_size, ENT-help-centre-content.download_count, ENT-help-centre-content.publish_status, ENT-help-centre-content.updated_at |
| Resource Name | text | Yes | Display name for resource | Max 200 chars (REQ-033-072) | ENT-help-centre-content.title |
| Resource Description | textarea | No | Brief description of resource | Max 500 chars (REQ-033-072) | ENT-help-centre-content.summary |
| Resource File | file upload | Yes | File to upload (PDF, DOCX, XLSX, etc.) | Max 50MB whatever the file type, whitelist: PDF, DOCX, XLSX, PNG, JPG (REQ-033-072, REQ-033-024) | ENT-help-centre-content.attachments |
| Resource Category | dropdown | No | Category (Templates, Documents, Forms) | Pre-defined categories (REQ-033-072) | ENT-help-centre-content.resource_category |
| File Type | auto-detected | No | File format detected from upload | Read-only, auto-detected (REQ-033-073) | ENT-help-centre-content.file_type |
| File Size | auto-calculated | No | File size in MB | Read-only, auto-calculated (REQ-033-073) | ENT-help-centre-content.file_size |
| Thumbnail/Icon | image upload | No | Custom thumbnail or file type icon | Max 1MB, PNG/JPG, 128x128px recommended (REQ-033-072) | ENT-help-centre-content.thumbnail_url |
| Download Count | display | No | Number of times resource downloaded | Read-only, incremented on each download by either audience (REQ-033-097) | ENT-help-centre-content.download_count |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback (REQ-033-087, REQ-033-096) | ENT-help-centre-content.helpfulness_rating |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (REQ-033-099) | ENT-help-centre-content.publish_status |
| Action Buttons | buttons | Yes | Add New Resource, Edit, Delete, Preview, Download | N/A | no graph field (control) |

**Business Rules**:

- Resource list displays all resources organized by category
- Resource list filterable by category, file type, status, and searchable by name
- "Add New Resource" button opens resource upload form (inline or modal)
- "Edit" button on each resource opens resource editor pre-filled with existing metadata
- "Delete" button on each resource prompts confirmation before deletion (soft-delete) (REQ-033-059)
- "Preview" button shows exact file viewer interface as providers will see (FR-032 Screen 5.3)
- "Download" button allows admin to download resource file (REQ-033-075)
- File upload interface optimized for resource management (drag-and-drop or file picker with progress indicator)
- File type icons auto-assigned if no custom thumbnail uploaded (REQ-033-073)
- Download count tracked per resource (REQ-033-097); helpfulness feedback tracked per resource for analytics (REQ-033-087)
- List has an admin-only "Archived" filter; "Restore" on an archived resource returns it as Draft (REQ-033-100)
- Preview available for PDF and image files (opens in modal) (REQ-033-075)

**Notes**:

- Resource management interface: list view with action buttons for each resource item
- Resource creation/editing: form with file upload, metadata fields, thumbnail upload
- File validation: size check, format check, virus scan (REQ-033-073)
- See REQ-033-073.
- Preview modal: shows resource card with thumbnail, name, description, file type badge, download button matching FR-032 Screen 5.3 (REQ-033-086)
- Bulk upload: upload multiple files at once (REQ-033-062)
- File replacement: replace existing file while keeping same resource record (REQ-033-074)
- Bulk operations: change status (Publish or Unpublish only) for multiple resources, delete multiple resources (REQ-033-062)
- Breadcrumb navigation: Settings > Help Centre Management > Resources

---

### Screen 4.1: Provider Resource Add/Edit Form

**Purpose**: Upload new resource or edit existing resource metadata. Accessed from Screen 4 (Resource Management) via "Add New Resource" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Resource Name | text | Yes | Display name for resource | Max 200 chars, required (REQ-033-072) | ENT-help-centre-content.title |
| Resource Description | textarea | No | Brief description of resource | Max 500 chars (REQ-033-072) | ENT-help-centre-content.summary |
| Resource File | file upload | Yes (for new) | File to upload (PDF, DOCX, XLSX, etc.) | Max 50MB whatever the file type, whitelist: PDF, DOCX, XLSX, PNG, JPG, required for new resources (REQ-033-072, REQ-033-024) | ENT-help-centre-content.attachments |
| Resource Category | dropdown | No | Category (Templates, Documents, Forms) | Pre-defined categories (REQ-033-072) | ENT-help-centre-content.resource_category |
| Thumbnail/Icon | image upload | No | Custom thumbnail or file type icon | Max 1MB, PNG/JPG, 128x128px recommended (REQ-033-072) | ENT-help-centre-content.thumbnail_url |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback (REQ-033-087, REQ-033-096) | ENT-help-centre-content.helpfulness_rating |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (Unpublish action is the only way out); defaults to Draft (REQ-033-099) | ENT-help-centre-content.publish_status |
| File Type | auto-detected | No | File format detected from upload | Read-only, auto-detected (REQ-033-073) | ENT-help-centre-content.file_type |
| File Size | auto-calculated | No | File size in MB | Read-only, auto-calculated (REQ-033-073) | ENT-help-centre-content.file_size |
| Preview Button | button | No | Preview resource in file viewer interface | N/A | no graph field (control) |
| Save Button | button | Yes | Save resource (as Draft or Publish) | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to resource list | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Resource" or "Edit" is clicked from Screen 4
- If editing existing resource, form is pre-filled with current resource metadata (file cannot be changed, only replaced) (REQ-033-074)
- If creating new resource, form starts empty with file upload required (REQ-033-060)
- File upload: drag-and-drop or file picker with progress indicator
- File validation: size check (max 50MB whatever the file type), format check (whitelist), virus scan; a file that fails the scan is rejected and not stored (REQ-033-073, REQ-033-098)
- Thumbnail generation: auto-generate from PDF first page or use custom upload (REQ-033-073)
- See REQ-033-073.
- "Replace File" option available when editing (replaces file while keeping same resource record) (REQ-033-074)
- "Preview" button shows resource in file viewer interface exactly as providers will see (FR-032 Screen 5.3)
- Form validation: name and file are required before saving, for Save as Draft and for Publish alike (REQ-033-072, REQ-033-056)
- On save, resource is created/updated and admin returns to Screen 4 (Resource Management) with updated list (REQ-033-060)
- On cancel, changes are discarded and admin returns to Screen 4 (REQ-033-060)

**Notes**:

- File upload interface with drag-and-drop support
- Upload progress bar showing percentage and estimated time
- File validation feedback (size, format, virus scan status)
- Thumbnail preview/editor
- See REQ-033-086.
- See REQ-033-053.
- See REQ-033-053.
- Breadcrumb navigation: Settings > Help Centre Management > Resources > [Add New Resource / Edit Resource]

---

### Screen 5: Provider Video Tutorial Management (for FR-032 Screen 5.4)

**Purpose**: Manage all video tutorials that display in video viewer interface on provider platform (matches FR-032 Screen 5.4). Admin can view video list, add new videos, edit existing videos, delete videos, and organize by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Video List | table/list | Yes | List of all videos organized by category | Each row: title, source type (File/Embed), category/tags, duration, view count, status, last updated, actions (Edit, Delete, Preview) | ENT-help-centre-content.title, ENT-help-centre-content.video_source_type, ENT-help-centre-content.tags, ENT-help-centre-content.duration, ENT-help-centre-content.view_count, ENT-help-centre-content.publish_status, ENT-help-centre-content.updated_at |
| Video Title | text | Yes | Video tutorial title | Max 200 chars (REQ-033-076) | ENT-help-centre-content.title |
| Video Description | textarea | No | Brief description of video content | Max 500 chars (REQ-033-076) | ENT-help-centre-content.summary |
| Video Source Type | dropdown | Yes | How video is provided | Options: Upload File, Embed from Third-Party (REQ-033-076) | ENT-help-centre-content.video_source_type |
| Video File | file upload | Conditional | Video file to upload when using "Upload File" source type | Max 500MB, formats: MP4, MOV; required when Video Source Type = Upload File (REQ-033-077) | ENT-help-centre-content.attachments |
| Video Embed URL | text | Conditional | URL to embedded video when using "Embed from Third-Party" source type | Required when Video Source Type = Embed from Third-Party; must be valid YouTube/Vimeo (or approved provider) URL (REQ-033-078) | ENT-help-centre-content.video_embed_url |
| Video Thumbnail | image upload | No | Custom thumbnail image | Max 2MB, PNG/JPG, 16:9 aspect ratio recommended (REQ-033-076) | ENT-help-centre-content.thumbnail_url |
| Video Duration | auto-calculated | No | Video length in minutes:seconds | Read-only, extracted from video file (REQ-033-077) | ENT-help-centre-content.duration |
| Video Transcript | textarea | No | Text transcript of video (optional) | Max 10,000 chars (REQ-033-076) | ENT-help-centre-content.transcript |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new | ENT-help-centre-content.tags |
| Related Videos | multi-select | No | Links to related video tutorials | References to other videos (REQ-033-063) | ENT-help-centre-content.related_content_ids |
| View Count | display | No | Number of times video viewed (>30 seconds) | Read-only, incremented on view (REQ-033-079, REQ-033-097) | ENT-help-centre-content.view_count |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (REQ-033-099) | ENT-help-centre-content.publish_status |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback (REQ-033-087, REQ-033-096) | ENT-help-centre-content.helpfulness_rating |
| Action Buttons | buttons | Yes | Add New Video, Edit, Delete, Preview | N/A | no graph field (control) |

**Business Rules**:

- Video list displays all videos organized by category/tags with clear indication of source type (Upload File vs Embed from Third-Party)
- Video list filterable by category/tags, status, source type, and searchable by title
- "Add New Video" button opens video creation form (inline or modal)
- "Edit" button on each video opens video editor pre-filled with existing metadata and source configuration
- "Delete" button on each video prompts confirmation before deletion (soft-delete) (REQ-033-059)
- "Preview" button shows exact video player interface as providers will see (FR-032 Screen 5.4), using either uploaded file or embedded player depending on source type
- For "Upload File" videos, video upload interface is optimized for video management (file picker with progress indicator, supports large files 500MB max) (REQ-033-077)
- For "Upload File" videos, system processes uploaded video for streaming optimization (if applicable) (REQ-033-077)
- For "Embed from Third-Party" videos, system validates embed URL against allowed providers (e.g., YouTube, Vimeo) and stores only the URL/ID, not the video file (REQ-033-078)
- Thumbnail generation: for uploaded videos, auto-generate from video frame at 10% mark or use custom upload; for embedded videos, allow either custom thumbnail upload or retrieval of provider thumbnail (if supported) (REQ-033-077, REQ-033-078)
- Video transcript optional but recommended for accessibility (REQ-033-076)
- View count incremented when video plays for >30 seconds, regardless of source type (REQ-033-079)
- Related videos can be manually assigned or auto-suggested based on tags/category (REQ-033-063)
- List has an admin-only "Archived" filter; "Restore" on an archived video returns it as Draft (REQ-033-100)

**Notes**:

- Video management interface: list view with action buttons for each video item and a visible badge/chip for source type (File / Embed)
- Video creation/editing: form starts with source type selector; when "Upload File" is selected, show file upload controls; when "Embed from Third-Party" is selected, show embed URL input and provider hints/examples
- Upload progress and processing indicators only appear when source type is "Upload File" (REQ-033-077)
- Video processing: background job processes uploaded videos after file upload (transcoding, thumbnail generation) (REQ-033-077)
- Thumbnail editor: crop/select frame from uploaded video for thumbnail; embedded videos can optionally use provider thumbnail or custom upload
- Preview: embedded video player with play controls (play, pause, volume, fullscreen, playback speed) matching FR-032 Screen 5.4, supporting both uploaded and embedded videos
- Transcript editor: textarea with character counter, searchable text
- Video analytics: view count, average watch time, completion rate (REQ-033-079)
- Bulk operations: change status (Publish or Unpublish only) for multiple videos, delete multiple videos (REQ-033-062)
- Breadcrumb navigation: Settings > Help Centre Management > Videos

---

### Screen 5.1: Provider Video Add/Edit Form

**Purpose**: Create a new video tutorial (via file upload or embedded third-party video) or edit existing video metadata. Accessed from Screen 5 (Video Management) via "Add New Video" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Video Title | text | Yes | Video tutorial title | Max 200 chars, required (REQ-033-076) | ENT-help-centre-content.title |
| Video Description | textarea | No | Brief description of video content | Max 500 chars (REQ-033-076) | ENT-help-centre-content.summary |
| Video Source Type | dropdown | Yes | How video is provided | Options: Upload File, Embed from Third-Party; required (REQ-033-076) | ENT-help-centre-content.video_source_type |
| Video File | file upload | Conditional | Video file to upload when using "Upload File" source type | Max 500MB, formats: MP4, MOV; required for new videos when Video Source Type = Upload File (REQ-033-077) | ENT-help-centre-content.attachments |
| Video Embed URL | text | Conditional | URL to embedded video when using "Embed from Third-Party" source type | Required when Video Source Type = Embed from Third-Party; must be valid URL for supported providers (e.g., YouTube, Vimeo) (REQ-033-078) | ENT-help-centre-content.video_embed_url |
| Video Thumbnail | image upload | No | Custom thumbnail image | Max 2MB, PNG/JPG, 16:9 aspect ratio recommended (REQ-033-076) | ENT-help-centre-content.thumbnail_url |
| Video Duration | auto-calculated | No | Video length in minutes:seconds | Read-only, extracted from video file (REQ-033-077) | ENT-help-centre-content.duration |
| Video Transcript | textarea | No | Text transcript of video (optional) | Max 10,000 chars (REQ-033-076) | ENT-help-centre-content.transcript |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new | ENT-help-centre-content.tags |
| Related Videos | multi-select | No | Links to related video tutorials | References to other videos (REQ-033-063) | ENT-help-centre-content.related_content_ids |
| Publish Status | dropdown | Yes | Draft or Published (an Unpublished item can only move to Published) | Dropdown offers Draft and Published only and is read-only while the item is Published (Unpublish action is the only way out); defaults to Draft (REQ-033-099) | ENT-help-centre-content.publish_status |
| Preview Button | button | No | Preview video in video player interface | N/A | no graph field (control) |
| Save Button | button | Yes | Save video (as Draft or Publish) | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to video list | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Video" or "Edit" is clicked from Screen 5
- If editing existing video, form is pre-filled with current video metadata including current source type and either file reference or embed URL (REQ-033-060)
- Admin must choose a Video Source Type:
  - When "Upload File" is selected:
    - Video File becomes required for new videos. (REQ-033-077)
    - File upload uses file picker with progress indicator (500MB max, MP4/MOV). (REQ-033-077)
    - Video processing background job is triggered after successful upload (transcoding, thumbnail generation). (REQ-033-077)
    - Video Duration is auto-extracted from uploaded file. (REQ-033-077)
  - When "Embed from Third-Party" is selected:
    - Video Embed URL becomes required. (REQ-033-078)
    - System validates URL format and that domain is in the allowed provider list (e.g., YouTube, Vimeo). (REQ-033-078)
    - No video file is uploaded; Video Duration may be fetched from provider API or left manual/optional (implementation detail). (REQ-033-078)
- For existing videos, admin can change the source type (Upload File or Embed from Third-Party) by providing the new file or URL and confirming that the old file or URL is replaced; the video keeps its view counts. For a Published video the previous video stays live for viewers until the new one is Ready, and if the new file fails the old one stays in place and the admin is told. (REQ-033-094)
- Thumbnail generation:
  - For uploaded videos, system auto-generates from frame at 10% mark, with option to override via custom thumbnail upload. (REQ-033-077)
  - For embedded videos, system may pull provider thumbnail (if supported) or allow only custom thumbnail upload. (REQ-033-078)
- Video transcript optional but recommended for accessibility, regardless of source type. (REQ-033-076)
- "Replace Video" option is available when editing "Upload File" videos (replaces file while keeping same video record). (REQ-033-074)
- "Preview" button shows video in video player interface exactly as providers will see (FR-032 Screen 5.4), using either uploaded file or embedded player.
- Form validation:
  - Title and Video Source Type always required, for Save as Draft and for Publish alike. (REQ-033-076, REQ-033-056)
  - An uploaded video cannot be published until its processing status is Ready; embedded videos are exempt. (REQ-033-077)
  - When source type is "Upload File": Video File required for new records. (REQ-033-077)
  - When source type is "Embed from Third-Party": Video Embed URL required and must pass validation. (REQ-033-078)
- On save, video is created/updated and admin returns to Screen 5 (Video Management) with updated list. (REQ-033-060)
- On cancel, changes are discarded and admin returns to Screen 5. (REQ-033-060)

**Notes**:

- Video upload interface with progress tracking
- Video processing status indicator (uploading, processing, ready, failed); on failed the admin is told and can re-upload, and a new item stays Draft; a Published video whose file is replaced or whose source is switched stays live with the previous video until the new one is Ready (REQ-033-077)
- Thumbnail editor with frame selection from video
- Transcript editor: textarea with character counter (10,000 max), searchable text
- Preview: embedded video player with play controls (play, pause, volume, fullscreen, playback speed) matching FR-032 Screen 5.4
- Related videos can be manually selected or auto-suggested based on tags/category (REQ-033-063)
- See REQ-033-053.
- See REQ-033-053.
- Breadcrumb navigation: Settings > Help Centre Management > Videos > [Add New Video / Edit Video]

---

### Screen 6: Provider Service Status Management (for FR-032 Screen 5.7)

**Purpose**: Manage service status components, incidents, and maintenance windows that display in status page interface on provider platform (matches FR-032 Screen 5.7). Admin can view service status overview, manage components, create/edit/delete incidents, and schedule maintenance windows.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Overall Status | dropdown | Yes | All Systems Operational, Partial Outage, Major Outage. Calculated by the system from component statuses; admin may pick another value. With no active component the status page shows a fourth value, Status not available, which is never a dropdown option | Pre-defined statuses; a value set by hand stays until an admin switches back to automatic (REQ-033-080, REQ-033-093) | ENT-service-status.overall_status |
| Return to Automatic | button | No | Switches the overall status back to the calculated value; shown only while the overall status was set by hand | N/A (REQ-033-093) | no graph field (control) |
| Service Components List | table | No | List of service components | Each row: component name, status (Operational/Degraded/Down), last updated | ENT-service-status.components |
| Component Name | text | Yes | Service component name | Max 100 chars (REQ-033-081) | ENT-service-component.name |
| Component Status | dropdown | Yes | Operational, Degraded, Down | Pre-defined statuses (REQ-033-081) | ENT-service-component.status |
| Incident History | timeline | No | List of recent incidents | Each incident: title, description, status, start time, end time, affected services | ENT-service-status.incidents |
| Incident Title | text | Yes | Brief incident title | Max 200 chars (REQ-033-082) | ENT-incident-record.title |
| Incident Description | textarea | Yes | Detailed incident description | Max 2000 chars (REQ-033-082) | ENT-incident-record.description |
| Incident Status | dropdown | Yes | Investigating, Identified, Monitoring, Resolved | Pre-defined statuses (REQ-033-082) | ENT-incident-record.status |
| Affected Services | multi-select | Yes | Service components affected by incident | References to service components (REQ-033-082) | ENT-incident-record.affected_services |
| Maintenance Schedule | table | No | List of scheduled maintenance windows | Each maintenance: title, description, scheduled start/end time, affected services | ENT-service-status.maintenance |
| Maintenance Title | text | Yes | Brief maintenance title | Max 200 chars (REQ-033-084) | ENT-maintenance-window.title |
| Maintenance Description | textarea | Yes | Detailed maintenance description | Max 2000 chars (REQ-033-084) | ENT-maintenance-window.description |
| Scheduled Start Time | datetime | Yes | Planned maintenance start time | Valid datetime; future date for new windows (REQ-033-084) | ENT-maintenance-window.scheduled_start |
| Scheduled End Time | datetime | Yes | Planned maintenance end time | Valid datetime, after start time (REQ-033-084) | ENT-maintenance-window.scheduled_end |

**Business Rules**:

- Service Status overview displays: overall status, service components list, incident history, maintenance schedule
- "Add Component" button allows admin to create new service components (REQ-033-081)
- "Edit" button on each component allows admin to edit component name and status (REQ-033-081)
- "Delete" button on each component prompts confirmation before deletion (soft delete: the component is archived, not permanently erased); a component on an open incident or on a Scheduled or In Progress maintenance window cannot be deleted (REQ-033-081)
- "Create Incident" button opens incident creation form (REQ-033-082)
- "Edit" button on each incident allows admin to update incident details and status (REQ-033-082)
- "Delete" button on each incident prompts confirmation before deletion (soft delete: the incident is archived, not permanently erased) (REQ-033-082)
- "Schedule Maintenance" button opens maintenance scheduling form (REQ-033-084)
- "Edit" button on each maintenance allows admin to update maintenance details (REQ-033-084)
- "Cancel" button on each maintenance allows admin to cancel scheduled maintenance (REQ-033-084)
- Overall status is calculated automatically from the statuses of the active service components only; open incidents and maintenance in progress do not change it (they are listed on the status page). Degraded components do not count: if no active component is Down, overall status is All Systems Operational; if some but not all are Down, Partial Outage; if all active components are Down (including a single component), Major Outage; with no active component the page shows "Status not available" unless an admin sets the overall status by hand (REQ-033-080)
- Admin may override the calculated overall status by picking another value in the Overall Status dropdown (REQ-033-080)
- A hand-set overall status stays until an admin switches it back to automatic with the "Return to Automatic" control; it is not reset when component statuses change (REQ-033-093)
- Service components: create, edit, delete components; update status in real-time (REQ-033-081)
- Incident management: create new incidents, update status, add timeline updates, mark as resolved (REQ-033-082)
- Maintenance schedule: create scheduled maintenance, edit, cancel, mark as completed (REQ-033-084); maintenance status changes only by admin action, and a window past its end time stays as the admin left it (REQ-033-084)
- Status updates propagate to provider platform within 1 minute (REQ-033-033)
- Incident timeline: system auto-logs status changes with timestamps (REQ-033-083)
- Preview shows exact status page interface as providers will see (FR-032 Screen 5.7) (REQ-033-086)

**Notes**:

- Service Status management interface: overview with action buttons for components, incidents, and maintenance
- Service component management: grid/list interface with status badges and action buttons (Edit, Delete)
- Status badges: color-coded (Operational: green, Degraded: yellow, Down: red)
- Incident editor: form with timeline view showing status progression, action buttons (Edit, Delete, Resolve)
- Maintenance scheduler: calendar interface for scheduling maintenance windows, action buttons (Edit, Cancel, Complete)
- Status changes reflect in provider view within 1 minute (REQ-033-033)
- Historical data: past incidents and completed maintenance retained for historical reference (REQ-033-085)
- Breadcrumb navigation: Settings > Help Centre Management > Service Status

---

### Screen 6.1: Provider Service Component Add/Edit Form

**Purpose**: Create new service component or edit existing service component. Accessed from Screen 6 (Service Status Management) via "Add Component" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Component Name | text | Yes | Service component name | Max 100 chars, required (REQ-033-081) | ENT-service-component.name |
| Component Status | dropdown | Yes | Operational, Degraded, Down | Pre-defined statuses, defaults to Operational (REQ-033-081) | ENT-service-component.status |
| Save Button | button | Yes | Save component | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to service status overview | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Add Component" or "Edit" is clicked from Screen 6
- If editing existing component, form is pre-filled with current component data
- If creating new component, form starts empty with default status "Operational" (REQ-033-081)
- Component status affects overall platform status calculation (a Down component counts; a Degraded component does not) (REQ-033-080)
- A deleted component is kept on past incidents and maintenance windows and shown there as removed; deleting a component that is on an open incident (not Resolved) or on a Scheduled or In Progress maintenance window is refused with a message naming the incident or window (REQ-033-081)
- On save, component is created/updated and admin returns to Screen 6 with updated component list (REQ-033-060)
- On cancel, changes are discarded and admin returns to Screen 6 (REQ-033-060)

**Notes**:

- Simple form with component name and status
- Status dropdown with color-coded options (Operational: green, Degraded: yellow, Down: red)
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Service Status > [Add Component / Edit Component]

---

### Screen 6.2: Provider Incident Add/Edit Form

**Purpose**: Create new incident or edit existing incident. Accessed from Screen 6 (Service Status Management) via "Create Incident" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Incident Title | text | Yes | Brief incident title | Max 200 chars, required (REQ-033-082) | ENT-incident-record.title |
| Incident Description | textarea | Yes | Detailed incident description | Max 2000 chars, required (REQ-033-082) | ENT-incident-record.description |
| Incident Status | dropdown | Yes | Investigating, Identified, Monitoring, Resolved | Pre-defined statuses, defaults to Investigating (REQ-033-082) | ENT-incident-record.status |
| Affected Services | multi-select | Yes | Service components affected by incident | References to service components, at least one required (REQ-033-082) | ENT-incident-record.affected_services |
| Start Time | datetime | Yes | Incident start time | Valid datetime, defaults to current time (REQ-033-082) | ENT-incident-record.start_time |
| End Time | datetime | No | Incident end time (when resolved) | Valid datetime, after start time (REQ-033-082) | ENT-incident-record.end_time |
| Save Button | button | Yes | Save incident | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to service status overview | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Create Incident" or "Edit" is clicked from Screen 6
- If editing existing incident, form is pre-filled with current incident data
- If creating new incident, form starts empty with default status "Investigating" and current time as start time (REQ-033-082)
- Affected services multi-select shows all available service components
- Incident status changes are logged in incident timeline automatically (REQ-033-083)
- Overall status is recalculated from the component statuses (unless set by hand) (REQ-033-080)
- On save, incident is created/updated and admin returns to Screen 6 with updated incident history (REQ-033-060)
- See REQ-033-060.

**Notes**:

- Form with incident details and affected services selection
- Status dropdown with timeline progression (Investigating → Identified → Monitoring → Resolved)
- Timeline view shows status progression with timestamps
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Service Status > [Create Incident / Edit Incident]

---

### Screen 6.3: Provider Maintenance Add/Edit Form

**Purpose**: Schedule new maintenance window or edit existing maintenance. Accessed from Screen 6 (Service Status Management) via "Schedule Maintenance" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Maintenance Title | text | Yes | Brief maintenance title | Max 200 chars, required (REQ-033-084) | ENT-maintenance-window.title |
| Maintenance Description | textarea | Yes | Detailed maintenance description | Max 2000 chars, required (REQ-033-084) | ENT-maintenance-window.description |
| Scheduled Start Time | datetime | Yes | Planned maintenance start time | Valid datetime; future date for new windows; required (REQ-033-084) | ENT-maintenance-window.scheduled_start |
| Scheduled End Time | datetime | Yes | Planned maintenance end time | Valid datetime, after start time, required (REQ-033-084) | ENT-maintenance-window.scheduled_end |
| Affected Services | multi-select | Yes | Service components affected by maintenance | References to service components, at least one required (REQ-033-084) | ENT-maintenance-window.affected_services |
| Status | dropdown | Yes | Scheduled, In Progress, Completed, Cancelled | Pre-defined statuses, defaults to Scheduled; changed only by admin action, never by time (REQ-033-084) | ENT-maintenance-window.status |
| Save Button | button | Yes | Save maintenance | N/A | no graph field (control) |
| Cancel Button | button | No | Cancel and return to service status overview | N/A | no graph field (control) |

**Business Rules**:

- Form opens in modal or separate screen when "Schedule Maintenance" or "Edit" is clicked from Screen 6
- If editing existing maintenance, form is pre-filled with current maintenance data
- If creating new maintenance, form starts empty with default status "Scheduled" (REQ-033-084)
- Scheduled times must be in the future for new maintenance windows (REQ-033-084)
- Affected services multi-select shows all available service components
- Calendar interface available for selecting scheduled times
- On save, maintenance is created/updated and admin returns to Screen 6 with updated maintenance schedule (REQ-033-060)
- See REQ-033-060.

**Notes**:

- Form with maintenance details, scheduled times, and affected services selection
- Calendar interface for scheduling maintenance windows
- Status dropdown (Scheduled, In Progress, Completed, Cancelled)
- Validation: end time must be after start time
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Service Status > [Schedule Maintenance / Edit Maintenance]

---

### Screen 7: Provider Content Preview

**Purpose**: Preview Help Centre content exactly as it will appear to providers in each subscreen layout before publishing.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Preview Mode | dropdown | Yes | Select subscreen layout to preview (FAQs, Articles, Resources, Videos, Service Status) | Pre-defined layouts matching FR-032 | no graph field (control) |
| Content Preview | rendered view | No | Rendered content in provider-facing layout | Read-only, matches FR-032 subscreen layouts | ENT-help-centre-content.title, ENT-help-centre-content.body, ENT-help-centre-content.attachments, ENT-help-centre-content.thumbnail_url, ENT-service-status.overall_status |

**Business Rules**:

- Preview renders content in exact provider-facing layout for selected subscreen type (REQ-033-086)
- FAQ preview shows accordion layout with expand/collapse (matches FR-032 Screen 5.1) (REQ-033-086)
- Article preview shows article layout with table of contents (matches FR-032 Screen 5.2) (REQ-033-086)
- Resource preview shows file viewer interface (matches FR-032 Screen 5.3) (REQ-033-086)
- Video preview shows video player interface (matches FR-032 Screen 5.4) (REQ-033-086)
- Service Status preview shows status page interface (matches FR-032 Screen 5.7) (REQ-033-086)
- Preview updates in real-time as admin edits content (REQ-033-086)
- Preview includes all formatting, images, and interactive elements (REQ-033-086)

**Notes**:

- Preview pane: side-by-side or modal view showing provider-facing layout
- Responsive preview: toggle between desktop/tablet/mobile views
- Print preview: available for article content
- Preview navigation: test all interactive elements (expand/collapse, video playback, file download)

---

#### Patient Help Centre Content Management (Admin Platform)

**Note**: The following Patient Help Centre content management screens (Screen 8 through Screen 13) are **admin-only screens on the Admin Platform**. They mirror the provider content management screens (Screen 1 through Screen 7) in structure and functionality, with the following key differences (REQ-033-051):

- **Audience**: Content managed here is displayed to patients via FR-035 (Patient Help Center & Support Submission module) instead of providers
- **Screen 8**: Patient Help Centre Management Dashboard (mirrors Screen 1; there is no patient version of Screen 1.1 because the four patient sections are fixed)
- **Screen 9**: Patient FAQ Management (mirrors Screen 2)
- **Screen 9.1**: Patient FAQ Add/Edit Form (mirrors Screen 2.1)
- **Patient FAQ topics**: managed in Screen 2.2 (FAQ Topic Management) through its audience switch; there is no separate patient topic screen
- **Screen 10**: Patient Article Management (mirrors Screen 3)
- **Screen 10.1**: Patient Article Add/Edit Form (mirrors Screen 3.1)
- **Article Type on Screens 10 and 10.1**: the values are Tutorial Guide and Troubleshooting Tip only; Policy Document is not offered and is blocked for the patient audience (REQ-033-036)
- **Screen 11**: Patient Resource Library Management (mirrors Screen 4, including the read-only Helpfulness Rating row and the Resource Category field)
- **Screen 11.1**: Patient Resource Add/Edit Form (mirrors Screen 4.1, including the read-only Helpfulness Rating row and the Resource Category field)
- **Screen 12**: Patient Video Tutorial Management (mirrors Screen 5)
- **Screen 12.1**: Patient Video Add/Edit Form (mirrors Screen 5.1)
- **Screen 13**: Patient Content Preview (mirrors Screen 7)

**Excluded for Patients**:

- **No Service Status Management** (Screen 6, Screen 6.1, Screen 6.2, Screen 6.3): Service Status is provider-only feature not applicable to patient Help Centre (REQ-033-030)

**Content Separation**:

- Patient content and provider content are stored in completely separate database tables/repositories (REQ-033-001)
- Admin UI clearly labels content as "Patient Content" or "Provider Content" throughout the interface (REQ-033-052)
- Content cannot be copied or shared between provider and patient repositories (manual re-creation required) (REQ-033-052)
- Search and filtering functions are scoped to selected audience (provider or patient) (REQ-033-052, REQ-033-035)
- Analytics and view counts tracked separately per audience (REQ-033-018)

---

## Business Rules

### General Module Rules

- **Rule 1**: Help Centre content managed for TWO distinct audiences: Providers and Patients; content repositories completely separated by audience type (REQ-033-001)
- **Rule 2**: Only admins can create, edit, or delete Help Centre content; providers and patients have read-only access to their respective content (REQ-033-020, REQ-033-007, REQ-033-008)
- **Rule 3**: Content must be tagged with audience type (Provider or Patient) and with its kind (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document); the kind decides the Help Centre section the content appears in, and admins do not pick a section separately; Policy Document is for the provider audience only (REQ-033-036)
- **Rule 4**: Content can exist in four states: Draft (admin-only), Published (audience-visible), Unpublished (admin-only, previously published), Archived (admin-only, set when content is deleted) (REQ-033-037). Allowed moves: Draft to Published; Published to Unpublished (only through the Unpublish action with its reason); Unpublished to Published; any state to Archived by Delete, so an admin may delete a Published item directly and it leaves the audience's view within 1 minute (REQ-033-099, REQ-033-034). Draft is not selectable for an Unpublished item. A bulk status change offers Publish and Unpublish only, a bulk Unpublish takes one shared reason for all selected items, and a bulk delete follows the single-item delete rules (REQ-033-062)
- **Rule 5**: All content changes logged in audit trail with admin identity, timestamp, audience type, and action type (REQ-033-015)
- **Rule 6**: Content deletion is soft-delete (archived) not permanent deletion to support recovery and audit compliance (REQ-033-016); an archived item can be restored as Draft (REQ-033-100)
- **Rule 7**: Admin must explicitly select audience (Provider or Patient) when creating content; content cannot be shared across audiences without manual re-creation (REQ-033-004, REQ-033-052)
- **Rule 8**: When content is deleted (archived), Related Content links that point to it are removed from other items and are not put back when the item is restored (REQ-033-092, REQ-033-100)

### Data & Privacy Rules

- **Privacy Rule 1**: Help Centre content is non-sensitive and accessible to all users within their respective audience (all provider staff see provider content; all patients see patient content; no role-based content restrictions) (REQ-033-038)
- **Privacy Rule 2**: Content view analytics tracked at organization level for providers (clinic), and aggregated for patients (not individual user level) (REQ-033-039)
- **View records**: each view of a FAQ, article or resource is stored with its date so views over time can be derived; no user identity is stored with it (REQ-033-097, REQ-033-039)
- **Privacy Rule 3**: Provider-specific content and patient-specific content stored in separate databases/repositories to prevent cross-audience data exposure (REQ-033-001, REQ-033-021)
- **Audit Rule**: All content creation, editing, publishing, unpublishing, and deletion actions logged with admin identity and timestamp for compliance audit trail (REQ-033-015)
- **Data Retention**: Archived content retained indefinitely for historical reference and audit compliance (REQ-033-040)
- **Data Privacy**: User feedback on content (helpfulness ratings) is kept as Yes/No counts only and no user identity is stored (patients are anonymous; providers are counted at clinic level at most); ratings are not publicly displayed; each tap on "Was this helpful?" is one vote, so repeat votes count; support requests encrypted in transit (HTTPS) (REQ-033-095, REQ-033-096)

### Admin Editability Rules

**Editable by Admin**:

- All Help Centre content for both Provider and Patient audiences (title, body, attachments, content kind which decides its section, publish status, audience type) (REQ-033-004)
- **Provider Content**:
  - FAQ content with accordion/topic organization (for FR-032 Screen 5.1)
  - Article content (Tutorial Guides, Troubleshooting Tips, Policies) with article layout formatting (for FR-032 Screen 5.2)
  - Resource Library files with file metadata (for FR-032 Screen 5.3)
  - Video Tutorials with video metadata and transcripts (for FR-032 Screen 5.4)
  - Service Status: overall status, service components, incidents, maintenance windows (for FR-032 Screen 5.7)
- **Patient Content**:
  - FAQ content with accordion/topic organization (for FR-035 patient FAQs)
  - Article content (Tutorial Guides, Troubleshooting Tips) with article layout formatting (for FR-035 patient articles)
  - Resource Library files with file metadata (for FR-035 patient resources)
  - Video Tutorials with video metadata and transcripts (for FR-035 patient videos)
  - See REQ-033-030.
- **Shared Admin Capabilities**:
  - Category organization and ordering
  - FAQ topic organization and FAQ item assignment to topics
  - Content tags and related content links

**Fixed in Codebase (Not Editable)**:

- Provider Help Centre categories: 10 categories (FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials) (REQ-033-041, REQ-033-002)
- Number of Help Centre content types: 5 types for providers (FAQs, Articles, Resources, Videos, Service Status); 4 types for patients (FAQs, Articles, Resources, Videos - no Service Status) (REQ-033-041, REQ-033-003)
- Audience types: Provider and Patient (fixed; cannot add new audience types) (REQ-033-041, REQ-033-001)
- Content type options (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document) (REQ-033-041, REQ-033-005)
- File upload size limits per upload kind (resource file 50MB whatever its type, uploaded video 500MB, resource thumbnail 1MB, video thumbnail 2MB, image placed inside article or FAQ text 10MB) (REQ-033-041, REQ-033-010)
- Content body character limits (max 5000 characters for FAQ answers, max 10,000 characters for tutorial guides) (REQ-033-041)
- Audit log retention period (indefinite retention for compliance) (REQ-033-041, REQ-033-040)

**Configurable with Restrictions**:

- Category visibility (admin can show/hide provider categories but cannot delete predefined categories; every hide asks for confirmation; applies to provider content only, because the four patient sections are fixed and have no category configuration screen) (REQ-033-043, REQ-033-044)
- Content versioning (enabled by default, admin cannot disable version control; applies to both provider and patient content) (REQ-033-042)
- Audience targeting (admin must select Provider or Patient when creating content; content cannot be shared across audiences without manual re-creation) (REQ-033-052)

### Integration Boundaries

- **FR-032 / Module PR-06**: Help Centre navigation menu item added to provider platform sidebar, accessible from settings page; displays provider-specific Help Centre content (REQ-033-031)
- **FR-035 / Module P-08**: Patient app fetches patient-specific Help Centre content via REST API; displays patient-facing FAQs, articles, resources, and videos (no Service Status) (REQ-033-026)
- **FR-031 / Module A-09**: Admin platform role-based permissions control access to Help Centre management features across both content repositories (REQ-033-020)
- **FR-009 / Module PR-01**: Help Centre accessible to all provider roles defined in FR-009 (Owner, Manager, Clinical Staff, Billing Staff) (REQ-033-038)
- **FR-034 / Module A-10**: Provider submissions via Help Centre Contact Support form (FR-032 Screen 5.5) and Feedback & Suggestions form (FR-032 Screen 5.6), and patient submissions via FR-035, are managed through FR-034 Support Center & Ticketing system, not within FR-033 (REQ-033-032)
- **FR-034 / Module A-10**: All submissions from Help Centre forms automatically create support cases in FR-034; FR-033 provides read-only Help Centre content only, while FR-034 handles all support ticket and feedback case management for both providers and patients (REQ-033-032)
- Cannot display Help Centre content to providers without active provider accounts

### Integration Failure Handling

- **Integration 1**: Provider platform fetches provider-specific Help Centre content via REST API (REQ-033-025)
  - **Error handling**: If API unavailable, display cached content or "Help Centre temporarily unavailable" message; retry API call on next page load
- **Integration 2**: Patient app fetches patient-specific Help Centre content via REST API (REQ-033-026)
  - **Error handling**: If API unavailable, display cached content or "Help Centre temporarily unavailable" message; retry API call on next page load
- **Integration 3**: Admin platform manages Help Centre content for both audiences via REST API with rich text editor
  - **Error handling**: If API unavailable, queue content changes locally and sync when API available; notify admin of sync failures
- **Integration 4**: Media storage service (S-05) stores uploaded files for both audiences (REQ-033-027)
  - **Error handling**: If upload fails, retry with exponential backoff (3 attempts); if all retries fail, notify admin and save content as draft (REQ-033-058)

### Security and Upload Controls

- Scan uploaded files for viruses and malware before storage (REQ-033-029, REQ-033-022); a file that fails the scan is rejected and not stored, and the admin sees "File failed security scan. Upload a clean file." (REQ-033-098)
- **Authentication**: Help Centre content accessible only to authenticated users (providers and patients access their respective content); admin content management accessible only to authenticated admin users with Help Centre management permissions (REQ-033-019)
- **Authorization**: Role-based access control enforced at API level (providers: read-only provider content, patients: read-only patient content, admins: read-write both content repositories based on permissions) (REQ-033-020)
- **Audience Separation**: Providers cannot access patient content; patients cannot access provider content; API endpoints enforce audience-based access control to prevent cross-audience data exposure (REQ-033-021)
- **File Upload Security**: All uploaded files scanned for viruses before storage; file type validation (one allowed-file list per upload kind: resources PDF, DOCX, XLSX, PNG, JPG; videos MP4, MOV; images such as thumbnails PNG, JPG); file size limits enforced; uploaded files stored outside web root with access-controlled URLs; files tagged with audience type for access control (REQ-033-022, REQ-033-024)
- **Content Injection**: Rich text editor sanitizes HTML input to prevent XSS attacks; strip dangerous tags (script, iframe) before saving; use Content Security Policy (CSP) headers (REQ-033-023)
- **Audit trail**: All content changes logged with admin identity, timestamp, IP address, audience type, and action for security audit compliance (REQ-033-015)

### Content and Operating Constraints

- **Search**: Full-text search across all content (title, body, tags) is required for P1 and scoped to the selected audience (provider or patient). Database full-text indexing is the minimum implementation baseline; a dedicated search engine remains an optional later enhancement. (REQ-033-035)
- Patient content will be curated to avoid medical advice and focus on platform usage, appointment management, and general information (REQ-033-088)
- Service status updates managed by Hairline technical operations team with real-time incident updates during outages (provider-only feature) (REQ-033-030)
- Admins will maintain Help Centre content currency by reviewing and updating content quarterly or as platform features change for both provider and patient content
- Providers access Help Centre via modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions) on desktop or tablet devices
- Patients access Help Centre via mobile app (iOS/Android) with occasional web browser access
- Providers and patients have stable internet connection to download tutorial videos and PDF guides (minimum 5 Mbps recommended)
- Admins use desktop/laptop computers for Help Centre content management (not optimized for mobile editing)

### Payment & Billing Rules

*Not applicable - Help Centre is a content management feature with no payment or billing components.*

**Carried from dropped sections (original wording)**:

- **Assumption 3**: Support team monitors feedback submissions and content gaps to prioritize new content creation for both providers and patients
- **Content analytics (kept separately per audience)**: view counts, helpfulness counts (Yes and No, counts only, no user identity), average time spent, video watch time and completion rate, and when the item was last viewed.

---

## Dependencies

Related FRs: FR-032 (Provider Help Centre accessed from provider settings page), FR-035 (Patient Help Centre accessed from patient app), FR-031 (Admin access control for Help Centre management), FR-009 (Provider team member access to Help Centre), FR-034 (Support Center & Ticketing for all submissions).

---

## User Scenarios & Testing

### User Story 1 - Provider Finds Answer in FAQ (Priority: P1)

A provider clinic coordinator encounters an issue with submitting a quote and wants to find a quick answer without contacting support. They access the Help Centre, browse the FAQ category, find the relevant question in the "Quote Submission" topic, and resolve their issue within 3 minutes.

**Why this priority**: Core self-service use case that reduces support burden and provides immediate value to providers

**Independent Test**: Can be fully tested by creating sample FAQ content, accessing Help Centre as provider, searching FAQ topics, and verifying answer is clear and resolves common quote submission issue

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider clicks "Help Centre" menu item, **Then** Help Centre landing page loads within 2 seconds showing all 10 categories
2. **Given** provider is on Help Centre landing page, **When** provider clicks "FAQ's" category tile, **Then** FAQ category page loads showing all FAQ topics organized in collapsible sections
3. **Given** provider is viewing FAQ topics, **When** provider clicks "Quote Submission" topic section, **Then** all FAQ items within "Quote Submission" topic expand showing questions and answers
4. **Given** provider has expanded FAQ topic, **When** provider reads answer to their question, **Then** answer provides clear step-by-step resolution with screenshots or examples where applicable
5. **Given** provider has read FAQ answer, **When** provider clicks "Was this helpful? Yes" button, **Then** system records positive feedback and displays "Thank you for your feedback" confirmation

---

### User Story 2 - Admin Creates and Publishes New FAQ Content (Priority: P1)

An admin content manager needs to add a new FAQ item to address a common provider question about payment processing. They navigate to Help Centre Management, access the FAQ Management screen, create a new FAQ with question and answer, organize it into the appropriate topic, preview it, and publish it for provider access.

**Why this priority**: Core content management functionality that enables admins to maintain and expand Help Centre content

**Independent Test**: Can be fully tested by logging in as admin, navigating to FAQ Management, creating new FAQ, assigning to topic, previewing, and verifying it appears in provider Help Centre

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to Settings > Help Centre Management, **Then** Help Centre Content List (Screen 1) loads showing all content organized by type
2. **Given** admin is on Content List screen, **When** admin clicks "FAQs" category or navigates to FAQ Management (Screen 2), **Then** FAQ Management screen loads showing all existing FAQs organized by topics
3. **Given** admin is on FAQ Management screen, **When** admin clicks "Add New FAQ" button, **Then** FAQ creation form opens with fields for question, answer, topic, and publish status
4. **Given** admin has completed FAQ form with question "How do I process patient payments?" and detailed answer, **When** admin selects "Payment Processing" topic and clicks "Preview", **Then** system displays FAQ in accordion layout exactly as providers will see it (matching FR-032 Screen 5.1)
5. **Given** admin has reviewed preview and verified formatting, **When** admin clicks "Publish", **Then** system saves FAQ with "Published" status, logs creation in audit trail, and makes FAQ available in provider Help Centre within 1 minute

---

### User Story 3 - Admin Updates Service Status During Platform Incident (Priority: P1)

An admin operations staff member needs to update the platform service status when a database outage occurs. They navigate to Service Status Management, create a new incident record, update affected service components, and ensure providers can see the status update within 1 minute.

**Why this priority**: Critical operational functionality for communicating platform status to providers during outages

**Independent Test**: Can be fully tested by creating service components, simulating incident, updating status, and verifying status propagates to provider view within 1 minute

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to Settings > Help Centre Management > Service Status Management (Screen 6), **Then** Service Status Management screen loads showing overall status, service components list, incident history, and maintenance schedule
2. **Given** admin detects database outage affecting multiple services, **When** admin clicks "Create Incident" button, **Then** incident creation form opens with fields for title, description, affected services, and status
3. **Given** admin has entered incident details "Database Connection Issues" with description and selected affected services, **When** admin sets status to "Investigating" and saves, **Then** system creates incident record and adds incident to timeline
4. **Given** incident is created and status updated, **When** admin sets one or more affected service components to "Down" (a "Degraded" component does not change the overall status), **Then** system recalculates overall status (Partial Outage if some components are Down, Major Outage if all are Down) and updates provider-facing Service Status page (FR-032 Screen 5.7) within 1 minute
5. **Given** database issue is resolved, **When** admin updates incident status to "Resolved" and updates service components to "Operational", **Then** system updates overall status to "All Systems Operational" and displays resolution in incident timeline

---

### User Story 4 - Provider Downloads Tutorial Resource from Resource Library (Priority: P2)

A provider clinic manager wants to download a template document for patient consent forms. They access Help Centre, navigate to Resource Library, browse available resources, and download the template file for use in their clinic.

**Why this priority**: Enables providers to access downloadable resources that support their clinic operations

**Independent Test**: Can be fully tested by creating resource in admin interface, accessing Resource Library as provider, browsing resources, and verifying download functionality works correctly

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to Help Centre and clicks "Resource Library" category, **Then** Resource Library page loads (FR-032 Screen 5.3) showing all available resources organized by category
2. **Given** provider is viewing Resource Library, **When** provider filters resources by category "Templates" or searches for "consent form", **Then** system displays matching resources with thumbnails, names, descriptions, and file type badges
3. **Given** provider has found "Patient Consent Form Template" resource, **When** provider clicks on resource card, **Then** system displays resource detail view with description, file type, file size, and download button
4. **Given** provider is viewing resource details, **When** provider clicks "Download" button, **Then** system initiates file download and increments download count for analytics
5. **Given** file download completes successfully, **When** provider opens downloaded file, **Then** file is valid PDF/DOCX document matching the resource description

---

### User Story 5 - Admin Organizes FAQ Content into Topics (Priority: P2)

An admin content manager needs to reorganize existing FAQ items into logical topic sections for better provider navigation. They access FAQ Management, use the topic management interface to create new topics, assign FAQs to topics, and reorder items within topics using drag-and-drop.

**Why this priority**: Content organization functionality that improves provider navigation and content discoverability

**Independent Test**: Can be fully tested by accessing FAQ Management, creating topics, assigning FAQs to topics, reordering FAQs, and verifying organization appears correctly in provider Help Centre

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to Settings > Help Centre Management > FAQ Management (Screen 2), **Then** FAQ Management screen loads showing all FAQs with current topic organization
2. **Given** admin wants to create new topic "Account Settings", **When** admin clicks "Manage Topics" button, **Then** topic management interface opens showing all existing topics with options to create, edit, delete, and reorder topics
3. **Given** admin is in topic management interface, **When** admin clicks "Create New Topic" and enters "Account Settings", **Then** system creates new topic and adds it to topic list
4. **Given** admin has created "Account Settings" topic, **When** admin assigns multiple FAQ items to this topic by dragging FAQs into topic group, **Then** system updates FAQ organization and displays FAQs grouped under "Account Settings" topic
5. **Given** FAQs are organized into topics, **When** admin reorders FAQs within topic using drag-and-drop and saves, **Then** system updates display order and provider Help Centre (FR-032 Screen 5.1) reflects new organization in accordion layout within 1 minute

### Edge Cases

- What happens when admin attempts to publish content with missing required fields?
- How does system handle concurrent edits by multiple admins to the same Help Centre content? Platform-wide rule: the second admin is warned that the item changed since they opened it; if they continue, the last save wins.
- How to manage Help Centre content when admin deletes content that is linked as "Related Content" from other items? The links to the deleted (archived) item are removed from the other items. (REQ-033-092)
- What happens when file upload exceeds the size limit of its upload kind (for example an uploaded video over 500MB or a resource file over 50MB)? (REQ-033-057, REQ-033-010)
- How does system handle Help Centre content search when search query returns zero results?

---

## Functional Requirements Summary

### Core Requirements

- **REQ-033-001**: System MUST provide Help Centre content management for TWO distinct audiences: Providers and Patients, with completely separated content repositories
- **REQ-033-002**: System MUST support the 10-category provider Help Centre taxonomy (FAQ's, Tutorial Guides, Contact Support, Troubleshooting Tips, Resource Library, Community Forum, Feedback & Suggestions, Service Status, Policy Information, Video Tutorials) aligned with FR-032, backed by underlying content types and integrations (Contact Support/Feedback routed to FR-034)
- **REQ-033-003**: System MUST support 4 Help Centre content types for patients (FAQs, Articles, Resources, Videos - NO Service Status) displayed via FR-035 patient app
- **REQ-033-004**: Admins MUST be able to create Help Centre content with audience selection (Provider or Patient), content kind (which decides the Help Centre section it appears in), title, rich text body, file attachments, tags, and publish status
- **REQ-033-005**: System MUST support multiple content types (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document) applicable to both audiences, except that Policy Document is for the provider audience only (REQ-033-036)
- **REQ-033-006**: Admins MUST be able to organize FAQ content into collapsible topic sections with drag-and-drop reordering for both provider and patient FAQs separately
- **REQ-033-007**: Providers MUST be able to access provider-specific Help Centre categories in read-only mode via FR-032 with category-appropriate layouts (accordion FAQs, article views, file viewer, video player, status page)
- **REQ-033-008**: Patients MUST be able to access patient-specific Help Centre content in read-only mode via FR-035 (Patient Help Center & Support Submission)
- **REQ-033-009**: System MUST support rich text editing for content creation with formatting (bold, italic, lists, links, images, tables) for both audiences
- **REQ-033-010**: System MUST support file uploads for Help Centre content with a size limit per upload kind (resource file 50MB whatever its type, uploaded video 500MB, resource thumbnail 1MB, video thumbnail 2MB, image placed inside article or FAQ text 10MB) for both audiences
- **REQ-033-011**: System MUST provide content preview functionality allowing admins to view content exactly as target audience will see it before publishing
- **REQ-033-012**: System MUST support content versioning tracking all changes with admin identity, timestamp, audience type, and version notes

### Data Requirements

- **REQ-033-013**: System MUST store Help Centre content with metadata including audience type (Provider/Patient), content type, title, body, tags, publish status, created date, updated date, created by admin, updated by admin
- **REQ-033-014**: System MUST store provider-specific Service Status data with metadata (overall status, service components with statuses, incidents with timeline, maintenance windows with schedules) - NOT applicable to patient content
- **REQ-033-015**: System MUST maintain audit trail logging all content creation, editing, publishing, unpublishing, and deletion actions with admin identity, audience type, and timestamp
- **REQ-033-016**: System MUST support soft-delete for content (move to "Archived" status) not permanent deletion for both audiences; service components and incidents are also soft-deleted
- **REQ-033-017**: System MUST store file attachments in media storage service (S-05) with references in Help Centre content records and audience type tags
- **REQ-033-018**: System MUST track content view analytics (total views per content item, views over time) separately for provider and patient audiences

### Security & Privacy Requirements

- **REQ-033-019**: System MUST enforce authentication for Help Centre access (providers, patients, and admins must be logged in)
- **REQ-033-020**: System MUST enforce authorization for content management (only admins with Help Centre management permissions can create/edit/publish content for both audiences)
- **REQ-033-021**: System MUST enforce audience-based access control preventing providers from accessing patient content and patients from accessing provider content
- **REQ-033-022**: System MUST scan all uploaded files for viruses before making available to users
- **REQ-033-023**: System MUST sanitize rich text HTML input to prevent XSS attacks (strip dangerous tags: script, iframe, object)
- **REQ-033-024**: System MUST enforce one allowed-file list per upload kind, rejecting all other file types: resources (PDF, DOCX, XLSX, PNG, JPG), videos (MP4, MOV), and images such as thumbnails (PNG, JPG)

### Integration Requirements

- **REQ-033-025**: System MUST provide REST API for provider platform (FR-032) to fetch provider-specific Help Centre content with authentication
- **REQ-033-026**: System MUST provide REST API for patient app (FR-035) to fetch patient-specific Help Centre content with authentication
- **REQ-033-027**: System MUST integrate with media storage service (S-05) for file upload, retrieval, and deletion with audience type tagging
- **REQ-033-028**: System MUST integrate with rich text editor library (Quill/TinyMCE/CKEditor) for content creation interface
- **REQ-033-029**: System MUST integrate with virus scanning service for file upload security validation
- **REQ-033-030**: Admins MUST be able to manage Service Status components, incidents, and maintenance windows for provider audience only (not applicable to patient audience)
- **REQ-033-092**: When Help Centre content is deleted (archived), System MUST remove the Related Content links that point to it from other items
- **REQ-033-093**: When an admin sets the overall service status by hand, System MUST keep that value until an admin switches the overall status back to automatic; Service Status Management MUST provide a control to switch back to automatic
- **REQ-033-094**: Admins MUST be able to change the source type of an existing video (uploaded file or third-party link) by providing the new file or URL and confirming that the old one is replaced; the video keeps its view counts; for a Published video the previous video stays live for viewers until the new one is Ready, and if the new file fails the old one stays in place and the admin is told
- **REQ-033-096**: A "Was this helpful?" vote on a FAQ, article, resource or video is one anonymous Yes or No added to the item's helpfulness count, written through the FR-032 and FR-035 content interfaces; no identity is kept, so repeat votes count
- **REQ-033-097**: A view of a FAQ, article or resource is counted each time its detail (or the FAQ answer) is opened, for both audiences; a video view keeps the 30-second rule (REQ-033-079); a resource download is counted for both audiences; each view is stored with its date so views over time and the FR-035 30-day popular list can be derived
- **REQ-033-098**: A file that fails the virus scan MUST be rejected and not stored; the admin sees "File failed security scan. Upload a clean file." and the event is written to the audit trail
- **REQ-033-099**: Content status moves are limited to Draft to Published, Published to Unpublished (only through the Unpublish action with its reason), Unpublished to Published, and any state to Archived by Delete; the Publish Status dropdown offers Draft and Published only, Draft is not selectable for an Unpublished item, and the dropdown is read-only while the item is Published
- **REQ-033-100**: Each content list MUST have an admin-only "Archived" filter, and a Restore action MUST return an archived item as Draft; Related Content links removed at deletion (REQ-033-092) are not put back

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 2.3 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.2) is in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 2.4 | Independent compression review: 2 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-24 | 2.5 | Logic review: size limit stated per upload kind; helpfulness vote and view recording rules (REQ-033-096, REQ-033-097); virus-scan rejection (REQ-033-098); uploaded video published only when processing is Ready, with a Failed state; same required-field check on Save as Draft and Publish; Resource Category field separated from FAQ topic; status-move rule (REQ-033-099); Archived filter and Restore (REQ-033-100); version created on save with last save wins; patient propagation within 1 minute; service status overall-status and maintenance clarifications; patient Article Type values and Policy Document blocked for patients. | Product Owner / Documentation |
| 2026-11-24 | 2.6 | Logic review pass 2: a Published video whose file is replaced or whose source is switched stays live with the previous video until the new one is Ready (REQ-033-077, REQ-033-094); an admin may delete a Published item directly and it leaves the audience's view within 1 minute (REQ-033-034, REQ-033-099); bulk status change offers Publish and Unpublish only with one shared Unpublish reason, bulk delete follows single-item rules (REQ-033-062); Draft is not selectable for an Unpublished item; a deleted service component is kept on past incidents and maintenance windows and cannot be deleted while on an open incident or an upcoming or running maintenance window (REQ-033-081). | Product Owner / Documentation |
| 2026-11-25 | 2.7 | Cross-FR alignment: Overall Status description adds the fourth value Status not available, never a dropdown option; enum value added for ENT-service-status.overall_status (REQ-033-080). | Product Owner / Documentation |

---

## Appendix: Approvals

Approved by the Product Owner as part of the requirements baseline of 2026-11-25. Record: `project-requirements/baseline-sign-off.md`. Changes after that date are listed in the Change Log above.

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD Template
**Last Updated**: 2026-11-25
