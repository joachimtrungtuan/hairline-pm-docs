# Product Requirements Document: Help Centre Content Management

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
- Maintain separate content repositories for provider-facing and patient-facing content to prevent cross-contamination
- Support scalable content organization with multi-category structure for each audience
- Maintain content consistency and quality through admin-controlled publishing workflow

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-08)**: Read-only access to Patient Help Centre content via FR-035 (Patient Help Center & Support Submission module) - patients view FAQs, guides, tutorials, and resources tailored for patient audience
- **Provider Platform (PR-06)**: Read-only access to Provider Help Centre content via FR-032 (Provider Dashboard Settings module) - providers view FAQs, guides, tutorials, and resources tailored for provider audience
- **Admin Platform (A-09)**: Full Help Centre content management capabilities for BOTH provider and patient audiences including content creation, editing, categorization, versioning, and publishing with clear audience separation
- **Shared Services (S-XX)**: No dedicated shared services required (uses standard S-05 for media storage)

### Multi-Tenant Breakdown

**Patient Platform (P-08)**:

- Patients access Help Centre content via FR-035 (Patient Help Center & Support Submission module)
- Content managed by admins in FR-033 is displayed to patients in FR-035 as read-only resources
- Patient Help Centre includes: FAQs, Tutorial Guides, Troubleshooting Tips, Resource Library, Video Tutorials
- No Service Status page for patients (provider-only feature)
- Content updates from FR-033 propagate to FR-035 patient views within 1 minute

**Provider Platform (PR-06)**:

- Providers access Help Centre content via FR-032 (Provider Dashboard Settings module)
- Content managed by admins in FR-033 is displayed to providers in FR-032 as read-only resources
- Provider Help Centre includes: FAQs (FR-032 Screen 5.1), Tutorial Guides/Tips/Policies (FR-032 Screen 5.2), Resource Library (FR-032 Screen 5.3), Video Tutorials (FR-032 Screen 5.4), Service Status (FR-032 Screen 5.7)
- Content updates from FR-033 propagate to FR-032 provider views within 1 minute
- Search functionality across all provider Help Centre content

**Admin Platform (A-09)**:

- Admins manage Help Centre content for TWO distinct audiences: Providers and Patients
- Content repositories completely separated by audience type to prevent cross-contamination
- Admin selects "Provider" or "Patient" audience when creating/editing content
- **Provider Content Management**:
  - Manage FAQ content (for FR-032 Screen 5.1)
  - Manage article content: Tutorial Guides, Troubleshooting Tips, Policies (for FR-032 Screen 5.2)
  - Upload and manage Resource Library files (for FR-032 Screen 5.3)
  - Upload and manage Video Tutorials (for FR-032 Screen 5.4)
  - Manage Service Status components, incidents, and maintenance windows (for FR-032 Screen 5.7)
- **Patient Content Management**:
  - Manage FAQ content (for FR-035 patient FAQs)
  - Manage article content: Tutorial Guides, Troubleshooting Tips (for FR-035 patient articles)
  - Upload and manage Resource Library files (for FR-035 patient resources)
  - Upload and manage Video Tutorials (for FR-035 patient videos)
  - No Service Status management for patients (provider-only feature)
- **Shared Admin Capabilities** (applies to both provider and patient content):
  - Publish/unpublish content to control visibility
  - Version control for content updates with change tracking
  - Preview content in audience-facing layout before publishing
  - Audit trail for all content changes (who, when, what changed)
  - Bulk operations for content management
  - Content analytics (view counts, search queries, popular topics by audience)
  - Multi-language content management (future enhancement)

**Shared Services (S-XX)**:

- Standard media storage service (S-05) for uploaded documents, videos, images
- Standard notification service (S-03) for content update notifications (future enhancement)

### Communication Structure

**In Scope**:

- Admin-to-provider communication via published Help Centre content
- Content update notifications (future enhancement)

**Out of Scope**:

- Provider Contact Support form submissions (handled by FR-034: Support Center & Ticketing - provider submissions via FR-032 Screen 5.5 automatically create support cases in FR-034)
- Provider Feedback & Suggestions form submissions (handled by FR-034: Support Center & Ticketing - provider submissions via FR-032 Screen 5.6 automatically create support cases in FR-034)
- Real-time chat between providers and admin (handled by separate communication module A-10)
- Provider-to-provider communication in community forum (future enhancement)
- Automated chatbot responses (future V2 enhancement)
- Email digest subscriptions for content updates (future enhancement)

### Entry Points

**Provider Entry**:

- Providers access Help Centre via "Help Centre" menu item in provider platform navigation
- Direct link from provider dashboard settings page (FR-032 integration point)
- Context-sensitive help links from various provider platform screens (future enhancement)

**Admin Entry**:

- Admins access Help Centre management via Settings > Help Centre Management
- Quick access from admin dashboard for content updates

---

## Business Workflows

### Provider Consumption (via FR-032)

**Actors**: Provider (clinic staff), System (FR-032 provider dashboard), FR-033 Help Centre content service  
**Trigger**: Provider clicks "Help Centre" menu item in provider platform (see FR-032 Business Workflows)  
**Outcome**: Provider views provider-facing Help Centre screens backed by content managed in FR-033

**Behaviour (high level)**:

1. Provider navigates to "Help Centre" from provider platform navigation (per FR-032).
2. FR-032 calls FR-033 provider Help Centre APIs to load published provider-audience content (FAQs, Articles, Resources, Videos, Service Status).
3. System displays content in provider-facing layouts defined in FR-032 (Screens 5.x).
4. Providers interact with content in read-only mode; any feedback or support submissions are handled by FR-032 + FR-034.

---

### Main Flow: Admin Creates Help Centre Content

**Actors**: Admin (Help Centre content manager), System
**Trigger**: Admin needs to create new help content or update existing content
**Outcome**: New or updated content published to Help Centre for provider access

**Steps**:

1. Admin navigates to Settings > Help Centre Management
2. System displays Help Centre content management dashboard with content list organized by subscreen type
3. Admin selects subscreen type to manage (FAQs, Articles, Resources, Videos, Service Status)
4. Admin clicks "Create New Content" button for selected subscreen type
5. System displays content creation form optimized for selected subscreen layout:
   - **FAQs**: FAQ editor with question/answer fields, topic assignment, accordion preview
   - **Articles**: Article editor with rich text, table of contents generation, article layout preview
   - **Resources**: File upload interface with metadata (name, description, category, file type), file viewer preview
   - **Videos**: Video upload interface with title, description, thumbnail, video player preview
   - **Service Status**: Status component/incident management interface
6. Admin enters content details using subscreen-specific editor
7. Admin uploads attachments if needed (images, PDFs, videos) - optimized for subscreen type
8. Admin assigns tags for content organization and searchability
9. Admin clicks "Preview" to see how content will appear to providers in the specific subscreen layout
10. System renders preview matching provider-facing layout (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, status page for service status)
11. Admin reviews preview and clicks "Save as Draft" or "Publish"
12. System saves content with status (Draft/Published) and timestamps
13. System logs content creation in audit trail (admin name, timestamp, action)
14. If published, system makes content immediately available in provider Help Centre subscreen
15. System displays success confirmation with link to view published content

### Alternative Flows

**A2: Admin Edits Existing Help Centre Content**:

- **Trigger**: Admin needs to update outdated or incorrect help content
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management
  2. Admin searches/filters content by category, title, or tags
  3. Admin clicks "Edit" on target content item
  4. System loads content editor pre-filled with existing content
  5. System creates new version of content in version control
  6. Admin makes changes to title, body, attachments, or category
  7. Admin previews changes to verify formatting and accuracy
  8. Admin saves changes with optional "Version note" describing what changed
  9. System updates content version and logs change in audit trail
  10. If content is published, system immediately updates provider-facing content
  11. System sends notification to admins who subscribed to content change alerts (future enhancement)
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
  11. Provider Help Centre immediately reflects new organization in accordion layout
- **Outcome**: FAQ content organized into logical topic sections displayed in accordion layout for easier provider navigation

**A4: Admin Uploads Video Tutorial**:

- **Trigger**: Admin needs to add video tutorial to Help Centre
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management > Video Tutorial Management (Screen 5)
  2. Admin clicks "Create New Video Tutorial"
  3. System displays video upload form with fields: title, description, video file upload, thumbnail image, transcript (optional), tags
  4. Admin enters title and description for video tutorial
  5. Admin uploads video file (supports MP4, MOV formats, max 500MB)
  6. System validates file size, format, and begins upload to media storage (S-05)
  7. System displays upload progress bar
  8. System auto-extracts video duration and generates thumbnail from video frame (10% mark)
  9. Admin uploads custom thumbnail image or uses auto-generated thumbnail
  10. Admin optionally enters video transcript for accessibility
  11. Admin previews video in video player interface (matches FR-032 Screen 5.4)
  12. Admin publishes video tutorial
  13. System processes video for streaming optimization (if applicable)
  14. System makes video available in provider Help Centre Video Tutorials subscreen (FR-032 Screen 5.4)
- **Outcome**: Video tutorial uploaded, processed, and published to Help Centre with video player interface

**A5: Admin Unpublishes Outdated Content**:

- **Trigger**: Admin needs to remove outdated or incorrect content from provider view
- **Steps**:
  1. Admin identifies outdated content item in content list
  2. Admin clicks "Unpublish" action on content item
  3. System prompts admin to confirm unpublish action with reason
  4. Admin enters reason (e.g., "Content outdated, new version coming soon")
  5. Admin confirms unpublish
  6. System changes content status from "Published" to "Unpublished"
  7. System immediately removes content from provider Help Centre view
  8. System logs unpublish action in audit trail with reason
  9. Content remains in admin view as "Unpublished" for future editing or re-publishing
- **Outcome**: Content removed from provider view but preserved in admin system for future use

**B1: Content Validation Fails**:

- **Trigger**: Admin attempts to publish content with missing required fields or invalid format
- **Steps**:
  1. Admin completes content creation form and clicks "Publish"
  2. System validates required fields (category, title, content body)
  3. System detects validation error (e.g., missing title, empty content body, unsupported file format)
  4. System displays error message highlighting missing/invalid fields
  5. Admin corrects validation errors
  6. Admin re-submits content for publishing
  7. System re-validates and proceeds with publish if all validations pass
- **Outcome**: Validation errors corrected and content published successfully

**B2: File Upload Exceeds Size Limit**:

- **Trigger**: Admin attempts to upload file larger than maximum allowed size
- **Steps**:
  1. Admin selects file for upload (video, PDF, image) in appropriate management screen
  2. System checks file size against limits (videos: 500MB, PDFs: 50MB, images: 10MB)
  3. File exceeds size limit
  4. System displays error message with file size limit and suggested alternatives (compress file, use external video hosting)
  5. Admin reduces file size or uses alternative hosting (YouTube/Vimeo embed link)
  6. Admin re-uploads compressed file or adds external video embed link
  7. System validates new file/link and proceeds with upload
- **Outcome**: File size issue resolved and content uploaded successfully

**A6: Admin Updates Service Status**:

- **Trigger**: Admin needs to update platform service status or create incident report
- **Steps**:
  1. Admin navigates to Settings > Help Centre Management > Service Status Management (Screen 8)
  2. System displays current overall status, service components list, incident history, maintenance schedule
  3. Admin updates service component status (e.g., "API Service" → Degraded)
  4. System automatically recalculates overall status based on component statuses
  5. Admin creates new incident: enters title, description, selects affected services, sets status (Investigating)
  6. System creates incident record and adds to incident history timeline
  7. Admin updates incident status as investigation progresses (Investigating → Identified → Monitoring → Resolved)
  8. System updates incident timeline with each status change
  9. Status updates propagate to provider Service Status subscreen (FR-032 Screen 5.7) within 1 minute
  10. Providers see updated status in real-time status page interface
- **Outcome**: Service status updated and displayed to providers in status page interface

---

## Screen Specifications

### Admin Platform Screens

#### Provider Help Centre Content Management

### Screen 1: Provider Help Centre Management Dashboard

**Purpose**: Landing page for provider-facing Help Centre content management with category navigation to access provider content management screens. Provides overview and quick access to manage provider FAQs, Articles, Resources, Videos, and Service Status (content displayed in FR-032 provider Help Centre).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Category Navigation | navigation menu | Yes | Links to content management screens: FAQs (Screen 2), Articles (Screen 3), Resources (Screen 4), Videos (Screen 5), Service Status (Screen 6) | N/A |
| Quick Stats | display cards | No | Summary statistics: total content, published content, draft content, total views | Read-only, calculated |
| Recent Activity | timeline | No | Recent content changes and updates | Read-only, sorted by date |

**Business Rules**:

- Dashboard provides category navigation matching FR-032 Screen 5 structure (FAQs, Articles, Resources, Videos, Service Status)
- Clicking "FAQs" category navigates to Screen 2 (FAQ Management) where FAQ list is displayed
- Clicking "Articles" category navigates to Screen 3 (Article Management) where article list is displayed
- Clicking "Resources" category navigates to Screen 4 (Resource Management) where resource list is displayed
- Clicking "Videos" category navigates to Screen 5 (Video Management) where video list is displayed
- Clicking "Service Status" category navigates to Screen 6 (Service Status Management) where service status overview is displayed
- Quick stats update in real-time showing aggregate metrics across all content types
- Recent activity shows: content created/edited/published, service status updates

**Notes**:

- Dashboard serves as landing page and navigation hub for Help Centre management
- Category navigation matches FR-032 Screen 5 category navigation structure
- Each category tile/card links to corresponding management screen where content list is displayed
- Visual indicators on category cards can show content count or status summary
- Breadcrumb navigation: Settings > Help Centre Management

---

### Screen 2: Provider FAQ Management (for FR-032 Screen 5.1)

**Purpose**: Manage all FAQ content that displays in accordion layout on provider platform (matches FR-032 Screen 5.1). Admin can view FAQ list, add new FAQs, edit existing FAQs, delete FAQs, and organize by topics.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| FAQ List | table/list | Yes | List of all FAQ items organized by topics | Each row: question, topic, display order, status, helpfulness rating, actions (Edit, Delete, Preview) |
| FAQ Question | text | Yes | FAQ question text | Max 200 chars |
| FAQ Answer | rich text | Yes | FAQ answer content | Max 5000 chars, supports HTML formatting |
| FAQ Topic | dropdown | Yes | Topic category for organization | Pre-defined topics or create new |
| Display Order | number | No | Order within topic | Integer, auto-incremented |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |
| Action Buttons | buttons | Yes | Add New FAQ, Edit, Delete, Preview, Manage Topics | N/A |

**Business Rules**:

- FAQ list displays all FAQs organized by topics with expandable topic sections
- FAQ list filterable by topic, status, and searchable by question text
- "Add New FAQ" button opens FAQ creation form (inline or modal)
- "Edit" button on each FAQ opens FAQ editor pre-filled with existing content
- "Delete" button on each FAQ prompts confirmation before deletion (soft-delete)
- "Preview" button shows exact accordion layout as providers will see (FR-032 Screen 5.1)
- "Manage Topics" button opens topic management interface (create, edit, delete, reorder topics)
- FAQs organized by topics with drag-and-drop reordering within topics
- Multiple FAQs can be edited in batch
- Helpfulness feedback tracked per FAQ for analytics
- FAQ editor optimized for accordion display format (question as header, answer as expandable content)

**Notes**:

- FAQ management interface: list view with action buttons for each FAQ item
- FAQ creation/editing: form with question field at top, answer field below with rich text editor
- Topic selector with "Create New Topic" option
- Drag-and-drop interface for reordering FAQs within topics
- Preview shows accordion layout with expand/collapse functionality matching FR-032 Screen 5.1
- Bulk operations: assign multiple FAQs to topic, change status for multiple FAQs, delete multiple FAQs
- Breadcrumb navigation: Settings > Help Centre Management > FAQs

---

### Screen 2.1: Provider FAQ Add/Edit Form

**Purpose**: Create new FAQ or edit existing FAQ content. Accessed from Screen 2 (FAQ Management) via "Add New FAQ" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| FAQ Question | text | Yes | FAQ question text | Max 200 chars, required |
| FAQ Answer | rich text | Yes | FAQ answer content | Max 5000 chars, supports HTML formatting, required |
| FAQ Topic | dropdown | Yes | Topic category for organization | Pre-defined topics or create new, required |
| Display Order | number | No | Order within topic | Integer, auto-incremented if not specified |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses, defaults to Draft |
| Preview Button | button | No | Preview FAQ in accordion layout | N/A |
| Save Button | button | Yes | Save FAQ (as Draft or Publish) | N/A |
| Cancel Button | button | No | Cancel and return to FAQ list | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Add New FAQ" or "Edit" is clicked from Screen 2
- If editing existing FAQ, form is pre-filled with current FAQ data
- If creating new FAQ, form starts empty with default values (Draft status, auto-incremented display order)
- Topic dropdown includes "Create New Topic" option which opens topic creation dialog
- Rich text editor for FAQ Answer supports: bold, italic, lists, links, images
- "Preview" button shows FAQ in accordion layout exactly as providers will see (FR-032 Screen 5.1)
- Form validation: question and answer are required before saving
- On save, FAQ is created/updated and admin returns to Screen 2 (FAQ Management) with updated list
- On cancel, changes are discarded and admin returns to Screen 2

**Notes**:

- Form layout: question field at top, answer field below with rich text editor
- Character counters for question (200 max) and answer (5000 max)
- Topic selector with search/autocomplete for existing topics
- Save options: "Save as Draft" or "Publish" buttons
- Success message displayed after save: "FAQ saved successfully" or "FAQ published successfully"
- Breadcrumb navigation: Settings > Help Centre Management > FAQs > [Add New FAQ / Edit FAQ]

---

### Screen 2.2: Provider FAQ Topic Management

**Purpose**: Manage FAQ topics used to group FAQ items for provider Help Centre (FR-032 Screen 5.1). Admin can create, edit, delete, and reorder topics, and see which FAQs belong to each topic.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Topic List | table/list | Yes | List of all FAQ topics | Each row: topic name, description (optional), number of FAQs, display order, actions (Edit, Delete) |
| Topic Name | text | Yes | Name of topic section (e.g., "Quote Submission", "Payment Processing") | Max 100 chars, unique per audience (Provider/Patient) |
| Topic Description | textarea | No | Optional description for internal/admin context | Max 250 chars |
| Display Order | number | Yes | Order in which topic appears in FAQ accordion | Integer, required; supports drag-and-drop reordering |
| Number of FAQs | display | No | Count of FAQs currently assigned to topic | Read-only, calculated |
| Action Buttons | buttons | Yes | Add New Topic, Edit, Delete, Save Order, Cancel | N/A |

**Business Rules**:

- Screen opened from Screen 2 (FAQ Management) when admin clicks "Manage Topics".
- Topic list shows all topics for the selected audience (Provider or Patient, depending on context) with current display order.
- "Add New Topic" opens inline row or modal with fields: Topic Name, Topic Description, Display Order (auto-suggested as last).
- "Edit" opens topic edit form (inline or modal) allowing admin to change name, description, and display order.
- "Delete" prompts confirmation; topics with assigned FAQs cannot be hard-deleted:
  - If topic has FAQs, system blocks deletion and prompts admin to reassign or remove FAQs first.
  - Implementation may soft-delete topic only when no FAQs are assigned.
- Topics support drag-and-drop reordering; moving rows updates Display Order values.
- "Save Order" persists new topic ordering; provider Help Centre FAQ accordion (FR-032 Screen 5.1) reflects updated topic order.
- "Cancel" discards unsaved changes to ordering or edits and returns admin to Screen 2 (FAQ Management).
- Validation ensures Topic Name is required and unique within the audience; Display Order must be a positive integer.

**Notes**:

- Visual layout: list of topics with drag handle on each row for reordering.
- Badge or column for "Number of FAQs" to help admins understand impact before deleting topics.
- Optional search/filter for topic name when list is long.
- Breadcrumb navigation: Settings > Help Centre Management > FAQs > Manage Topics.

---

### Screen 3: Provider Article Management (for FR-032 Screen 5.2)

**Purpose**: Manage all article content (Tutorial Guides, Troubleshooting Tips, Policy Information) that displays in article layout on provider platform (matches FR-032 Screen 5.2). Admin can view article list, add new articles, edit existing articles, delete articles, and organize by type.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Article List | table/list | Yes | List of all articles organized by type | Each row: title, article type, category/tags, status, last updated, view count, actions (Edit, Delete, Preview) |
| Article Title | text | Yes | Article title | Max 200 chars |
| Article Content | rich text | Yes | Full article content with formatting | Max 10,000 chars, supports HTML, headings, lists, images, tables |
| Article Type | dropdown | Yes | Tutorial Guide, Troubleshooting Tip, Policy Information | Pre-defined types |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Table of Contents | auto-generated | No | Auto-generated from headings (for articles >1000 words) | Read-only, generated on save |
| Related Articles | multi-select | No | Links to related articles | References to other articles |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |
| Action Buttons | buttons | Yes | Add New Article, Edit, Delete, Preview | N/A |

**Business Rules**:

- Article list displays all articles organized by type (Tutorial Guide, Troubleshooting Tip, Policy Information)
- Article list filterable by type, category/tags, status, and searchable by title
- "Add New Article" button opens article creation form (inline or modal)
- "Edit" button on each article opens article editor pre-filled with existing content
- "Delete" button on each article prompts confirmation before deletion (soft-delete)
- "Preview" button shows exact article layout as providers will see (FR-032 Screen 5.2)
- Article editor optimized for article layout format (full-width content with formatted text, images, code blocks)
- Rich text editor supports: headings (H1-H6), bold, italic, lists, links, images, tables, code blocks
- Table of contents auto-generated for articles with multiple headings (articles >1000 words)
- Related articles can be manually assigned or auto-suggested based on tags/category
- Print-friendly view available in preview

**Notes**:

- Article management interface: list view with action buttons for each article item
- Article creation/editing: full-featured rich text editor with formatting toolbar
- Image upload inline within editor
- Screenshot/image insertion with captions
- Step-by-step tutorial format: numbered lists with visual separators
- Preview shows: formatted article with table of contents (if applicable), related articles section matching FR-032 Screen 5.2
- Character counter for content body
- Bulk operations: change status for multiple articles, delete multiple articles
- Breadcrumb navigation: Settings > Help Centre Management > Articles

---

### Screen 3.1: Provider Article Add/Edit Form

**Purpose**: Create new article or edit existing article content. Accessed from Screen 3 (Article Management) via "Add New Article" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Article Title | text | Yes | Article title | Max 200 chars, required |
| Article Content | rich text | Yes | Full article content with formatting | Max 10,000 chars, supports HTML, headings, lists, images, tables, required |
| Article Type | dropdown | Yes | Tutorial Guide, Troubleshooting Tip, Policy Information | Pre-defined types, required |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Related Articles | multi-select | No | Links to related articles | References to other articles |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses, defaults to Draft |
| Table of Contents | auto-generated | No | Auto-generated from headings (for articles >1000 words) | Read-only, generated on save |
| Preview Button | button | No | Preview article in article layout | N/A |
| Save Button | button | Yes | Save article (as Draft or Publish) | N/A |
| Cancel Button | button | No | Cancel and return to article list | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Article" or "Edit" is clicked from Screen 3
- If editing existing article, form is pre-filled with current article data
- If creating new article, form starts empty with default values (Draft status)
- Rich text editor supports: headings (H1-H6), bold, italic, lists, links, images, tables, code blocks
- Table of contents auto-generated for articles with multiple headings (articles >1000 words) on save
- "Preview" button shows article in article layout exactly as providers will see (FR-032 Screen 5.2)
- Form validation: title and content are required before saving
- Image upload available inline within editor
- Related articles can be manually selected or auto-suggested based on tags/category
- On save, article is created/updated and admin returns to Screen 3 (Article Management) with updated list
- On cancel, changes are discarded and admin returns to Screen 3

**Notes**:

- Full-featured rich text editor with formatting toolbar
- Character counter for content body (10,000 max)
- Image upload inline within editor with caption support
- Step-by-step tutorial format support: numbered lists with visual separators
- Print-friendly view available in preview
- Save options: "Save as Draft" or "Publish" buttons
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Articles > [Add New Article / Edit Article]

---

### Screen 4: Provider Resource Library Management (for FR-032 Screen 5.3)

**Purpose**: Manage all downloadable resources (templates, documents, PDFs) that display in file viewer interface on provider platform (matches FR-032 Screen 5.3). Admin can view resource list, add new resources, edit existing resources, delete resources, and organize by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resource List | table/list | Yes | List of all resources organized by category | Each row: name, category, file type, file size, download count, status, last updated, actions (Edit, Delete, Preview, Download) |
| Resource Name | text | Yes | Display name for resource | Max 200 chars |
| Resource Description | textarea | No | Brief description of resource | Max 500 chars |
| Resource File | file upload | Yes | File to upload (PDF, DOCX, XLSX, etc.) | Max 50MB, whitelist: PDF, DOCX, XLSX, PNG, JPG |
| Resource Category | dropdown | No | Category (Templates, Documents, Forms, etc.) | Pre-defined categories |
| File Type | auto-detected | No | File format detected from upload | Read-only, auto-detected |
| File Size | auto-calculated | No | File size in MB | Read-only, auto-calculated |
| Thumbnail/Icon | image upload | No | Custom thumbnail or file type icon | Max 1MB, PNG/JPG, 128x128px recommended |
| Download Count | display | No | Number of times resource downloaded | Read-only, incremented on download |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Action Buttons | buttons | Yes | Add New Resource, Edit, Delete, Preview, Download | N/A |

**Business Rules**:

- Resource list displays all resources organized by category
- Resource list filterable by category, file type, status, and searchable by name
- "Add New Resource" button opens resource upload form (inline or modal)
- "Edit" button on each resource opens resource editor pre-filled with existing metadata
- "Delete" button on each resource prompts confirmation before deletion (soft-delete)
- "Preview" button shows exact file viewer interface as providers will see (FR-032 Screen 5.3)
- "Download" button allows admin to download resource file
- File upload interface optimized for resource management (drag-and-drop or file picker with progress indicator)
- File type icons auto-assigned if no custom thumbnail uploaded
- Download count tracked per resource
- Preview available for PDF and image files (opens in modal)

**Notes**:

- Resource management interface: list view with action buttons for each resource item
- Resource creation/editing: form with file upload, metadata fields, thumbnail upload
- File validation: size check, format check, virus scan
- Thumbnail generation: auto-generate from PDF first page or use custom upload
- Preview modal: shows resource card with thumbnail, name, description, file type badge, download button matching FR-032 Screen 5.3
- Bulk upload: upload multiple files at once
- File replacement: replace existing file while keeping same resource record
- Bulk operations: change status for multiple resources, delete multiple resources
- Breadcrumb navigation: Settings > Help Centre Management > Resources

---

### Screen 4.1: Provider Resource Add/Edit Form

**Purpose**: Upload new resource or edit existing resource metadata. Accessed from Screen 4 (Resource Management) via "Add New Resource" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resource Name | text | Yes | Display name for resource | Max 200 chars, required |
| Resource Description | textarea | No | Brief description of resource | Max 500 chars |
| Resource File | file upload | Yes (for new) | File to upload (PDF, DOCX, XLSX, etc.) | Max 50MB, whitelist: PDF, DOCX, XLSX, PNG, JPG, required for new resources |
| Resource Category | dropdown | No | Category (Templates, Documents, Forms, etc.) | Pre-defined categories |
| Thumbnail/Icon | image upload | No | Custom thumbnail or file type icon | Max 1MB, PNG/JPG, 128x128px recommended |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses, defaults to Draft |
| File Type | auto-detected | No | File format detected from upload | Read-only, auto-detected |
| File Size | auto-calculated | No | File size in MB | Read-only, auto-calculated |
| Preview Button | button | No | Preview resource in file viewer interface | N/A |
| Save Button | button | Yes | Save resource (as Draft or Publish) | N/A |
| Cancel Button | button | No | Cancel and return to resource list | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Resource" or "Edit" is clicked from Screen 4
- If editing existing resource, form is pre-filled with current resource metadata (file cannot be changed, only replaced)
- If creating new resource, form starts empty with file upload required
- File upload: drag-and-drop or file picker with progress indicator
- File validation: size check (max 50MB), format check (whitelist), virus scan
- Thumbnail generation: auto-generate from PDF first page or use custom upload
- File type icons auto-assigned if no custom thumbnail uploaded
- "Replace File" option available when editing (replaces file while keeping same resource record)
- "Preview" button shows resource in file viewer interface exactly as providers will see (FR-032 Screen 5.3)
- Form validation: name and file are required before saving
- On save, resource is created/updated and admin returns to Screen 4 (Resource Management) with updated list
- On cancel, changes are discarded and admin returns to Screen 4

**Notes**:

- File upload interface with drag-and-drop support
- Upload progress bar showing percentage and estimated time
- File validation feedback (size, format, virus scan status)
- Thumbnail preview/editor
- Preview modal: shows resource card with thumbnail, name, description, file type badge, download button matching FR-032 Screen 5.3
- Save options: "Save as Draft" or "Publish" buttons
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Resources > [Add New Resource / Edit Resource]

---

### Screen 5: Provider Video Tutorial Management (for FR-032 Screen 5.4)

**Purpose**: Manage all video tutorials that display in video viewer interface on provider platform (matches FR-032 Screen 5.4). Admin can view video list, add new videos, edit existing videos, delete videos, and organize by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Video List | table/list | Yes | List of all videos organized by category | Each row: title, source type (File/Embed), category/tags, duration, view count, status, last updated, actions (Edit, Delete, Preview) |
| Video Title | text | Yes | Video tutorial title | Max 200 chars |
| Video Description | textarea | No | Brief description of video content | Max 500 chars |
| Video Source Type | dropdown | Yes | How video is provided | Options: Upload File, Embed from Third-Party |
| Video File | file upload | Conditional | Video file to upload when using "Upload File" source type | Max 500MB, formats: MP4, MOV; required when Video Source Type = Upload File |
| Video Embed URL | text | Conditional | URL to embedded video when using "Embed from Third-Party" source type | Required when Video Source Type = Embed from Third-Party; must be valid YouTube/Vimeo (or approved provider) URL |
| Video Thumbnail | image upload | No | Custom thumbnail image | Max 2MB, PNG/JPG, 16:9 aspect ratio recommended |
| Video Duration | auto-calculated | No | Video length in minutes:seconds | Read-only, extracted from video file |
| Video Transcript | textarea | No | Text transcript of video (optional) | Max 10,000 chars |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Related Videos | multi-select | No | Links to related video tutorials | References to other videos |
| View Count | display | No | Number of times video viewed (>30 seconds) | Read-only, incremented on view |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses |
| Helpfulness Rating | display | No | Aggregated feedback (Yes/No counts) | Read-only, calculated from provider feedback |
| Action Buttons | buttons | Yes | Add New Video, Edit, Delete, Preview | N/A |

**Business Rules**:

- Video list displays all videos organized by category/tags with clear indication of source type (Upload File vs Embed from Third-Party)
- Video list filterable by category/tags, status, source type, and searchable by title
- "Add New Video" button opens video creation form (inline or modal)
- "Edit" button on each video opens video editor pre-filled with existing metadata and source configuration
- "Delete" button on each video prompts confirmation before deletion (soft-delete)
- "Preview" button shows exact video player interface as providers will see (FR-032 Screen 5.4), using either uploaded file or embedded player depending on source type
- For "Upload File" videos, video upload interface is optimized for video management (file picker with progress indicator, supports large files 500MB max)
- For "Upload File" videos, system processes uploaded video for streaming optimization (if applicable)
- For "Embed from Third-Party" videos, system validates embed URL against allowed providers (e.g., YouTube, Vimeo) and stores only the URL/ID, not the video file
- Thumbnail generation: for uploaded videos, auto-generate from video frame at 10% mark or use custom upload; for embedded videos, allow either custom thumbnail upload or retrieval of provider thumbnail (if supported)
- Video transcript optional but recommended for accessibility
- View count incremented when video plays for >30 seconds, regardless of source type
- Related videos can be manually assigned or auto-suggested based on tags/category

**Notes**:

- Video management interface: list view with action buttons for each video item and a visible badge/chip for source type (File / Embed)
- Video creation/editing: form starts with source type selector; when "Upload File" is selected, show file upload controls; when "Embed from Third-Party" is selected, show embed URL input and provider hints/examples
- Upload progress and processing indicators only appear when source type is "Upload File"
- Video processing: background job processes uploaded videos after file upload (transcoding, thumbnail generation)
- Thumbnail editor: crop/select frame from uploaded video for thumbnail; embedded videos can optionally use provider thumbnail or custom upload
- Preview: embedded video player with play controls (play, pause, volume, fullscreen, playback speed) matching FR-032 Screen 5.4, supporting both uploaded and embedded videos
- Transcript editor: textarea with character counter, searchable text
- Video analytics: view count, average watch time, completion rate
- Bulk operations: change status for multiple videos, delete multiple videos
- Breadcrumb navigation: Settings > Help Centre Management > Videos

---

### Screen 5.1: Provider Video Add/Edit Form

**Purpose**: Create a new video tutorial (via file upload or embedded third-party video) or edit existing video metadata. Accessed from Screen 5 (Video Management) via "Add New Video" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Video Title | text | Yes | Video tutorial title | Max 200 chars, required |
| Video Description | textarea | No | Brief description of video content | Max 500 chars |
| Video Source Type | dropdown | Yes | How video is provided | Options: Upload File, Embed from Third-Party; required |
| Video File | file upload | Conditional | Video file to upload when using "Upload File" source type | Max 500MB, formats: MP4, MOV; required for new videos when Video Source Type = Upload File |
| Video Embed URL | text | Conditional | URL to embedded video when using "Embed from Third-Party" source type | Required when Video Source Type = Embed from Third-Party; must be valid URL for supported providers (e.g., YouTube, Vimeo) |
| Video Thumbnail | image upload | No | Custom thumbnail image | Max 2MB, PNG/JPG, 16:9 aspect ratio recommended |
| Video Duration | auto-calculated | No | Video length in minutes:seconds | Read-only, extracted from video file |
| Video Transcript | textarea | No | Text transcript of video (optional) | Max 10,000 chars |
| Category/Tags | multi-select | No | Content tags for organization | Pre-defined tags or create new |
| Related Videos | multi-select | No | Links to related video tutorials | References to other videos |
| Publish Status | dropdown | Yes | Draft, Published, Unpublished | Pre-defined statuses, defaults to Draft |
| Preview Button | button | No | Preview video in video player interface | N/A |
| Save Button | button | Yes | Save video (as Draft or Publish) | N/A |
| Cancel Button | button | No | Cancel and return to video list | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Add New Video" or "Edit" is clicked from Screen 5
- If editing existing video, form is pre-filled with current video metadata including current source type and either file reference or embed URL
- Admin must choose a Video Source Type:
  - When "Upload File" is selected:
    - Video File becomes required for new videos.
    - File upload uses file picker with progress indicator (500MB max, MP4/MOV).
    - Video processing background job is triggered after successful upload (transcoding, thumbnail generation).
    - Video Duration is auto-extracted from uploaded file.
  - When "Embed from Third-Party" is selected:
    - Video Embed URL becomes required.
    - System validates URL format and that domain is in the allowed provider list (e.g., YouTube, Vimeo).
    - No video file is uploaded; Video Duration may be fetched from provider API or left manual/optional (implementation detail).
- For existing videos, a "Change Source Type" flow may be implemented as either:
  - Simple change with required new file/URL and confirmation that old file/URL is replaced; or
  - Restricted to avoid data loss (implementation decision to be finalized at design time).
- Thumbnail generation:
  - For uploaded videos, system auto-generates from frame at 10% mark, with option to override via custom thumbnail upload.
  - For embedded videos, system may pull provider thumbnail (if supported) or allow only custom thumbnail upload.
- Video transcript optional but recommended for accessibility, regardless of source type.
- "Replace Video" option is available when editing "Upload File" videos (replaces file while keeping same video record).
- "Preview" button shows video in video player interface exactly as providers will see (FR-032 Screen 5.4), using either uploaded file or embedded player.
- Form validation:
  - Title and Video Source Type always required.
  - When source type is "Upload File": Video File required for new records.
  - When source type is "Embed from Third-Party": Video Embed URL required and must pass validation.
- On save, video is created/updated and admin returns to Screen 5 (Video Management) with updated list.
- On cancel, changes are discarded and admin returns to Screen 5.

**Notes**:

- Video upload interface with progress tracking
- Video processing status indicator (uploading, processing, ready)
- Thumbnail editor with frame selection from video
- Transcript editor: textarea with character counter (10,000 max), searchable text
- Preview: embedded video player with play controls (play, pause, volume, fullscreen, playback speed) matching FR-032 Screen 5.4
- Related videos can be manually selected or auto-suggested based on tags/category
- Save options: "Save as Draft" or "Publish" buttons
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Videos > [Add New Video / Edit Video]

---

### Screen 6: Provider Service Status Management (for FR-032 Screen 5.7)

**Purpose**: Manage service status components, incidents, and maintenance windows that display in status page interface on provider platform (matches FR-032 Screen 5.7). Admin can view service status overview, manage components, create/edit/delete incidents, and schedule maintenance windows.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Overall Status | dropdown | Yes | All Systems Operational, Partial Outage, Major Outage | Pre-defined statuses |
| Service Components List | table | No | List of service components | Each row: component name, status (Operational/Degraded/Down), last updated |
| Component Name | text | Yes | Service component name | Max 100 chars |
| Component Status | dropdown | Yes | Operational, Degraded, Down | Pre-defined statuses |
| Incident History | timeline | No | List of recent incidents | Each incident: title, description, status, start time, end time, affected services |
| Incident Title | text | Yes | Brief incident title | Max 200 chars |
| Incident Description | textarea | Yes | Detailed incident description | Max 2000 chars |
| Incident Status | dropdown | Yes | Investigating, Identified, Monitoring, Resolved | Pre-defined statuses |
| Affected Services | multi-select | Yes | Service components affected by incident | References to service components |
| Maintenance Schedule | table | No | List of scheduled maintenance windows | Each maintenance: title, description, scheduled start/end time, affected services |
| Maintenance Title | text | Yes | Brief maintenance title | Max 200 chars |
| Maintenance Description | textarea | Yes | Detailed maintenance description | Max 2000 chars |
| Scheduled Start Time | datetime | Yes | Planned maintenance start time | Valid datetime, future date |
| Scheduled End Time | datetime | Yes | Planned maintenance end time | Valid datetime, after start time |

**Business Rules**:

- Service Status overview displays: overall status, service components list, incident history, maintenance schedule
- "Add Component" button allows admin to create new service components
- "Edit" button on each component allows admin to edit component name and status
- "Delete" button on each component prompts confirmation before deletion
- "Create Incident" button opens incident creation form
- "Edit" button on each incident allows admin to update incident details and status
- "Delete" button on each incident prompts confirmation before deletion
- "Schedule Maintenance" button opens maintenance scheduling form
- "Edit" button on each maintenance allows admin to update maintenance details
- "Cancel" button on each maintenance allows admin to cancel scheduled maintenance
- Overall status automatically calculated from service component statuses (if any component is Down → Partial/Major Outage)
- Service components: create, edit, delete components; update status in real-time
- Incident management: create new incidents, update status, add timeline updates, mark as resolved
- Maintenance schedule: create scheduled maintenance, edit, cancel, mark as completed
- Status updates propagate to provider platform within 1 minute
- Incident timeline: system auto-logs status changes with timestamps
- Preview shows exact status page interface as providers will see (FR-032 Screen 5.7)

**Notes**:

- Service Status management interface: overview with action buttons for components, incidents, and maintenance
- Service component management: grid/list interface with status badges and action buttons (Edit, Delete)
- Status badges: color-coded (Operational: green, Degraded: yellow, Down: red)
- Incident editor: form with timeline view showing status progression, action buttons (Edit, Delete, Resolve)
- Maintenance scheduler: calendar interface for scheduling maintenance windows, action buttons (Edit, Cancel, Complete)
- Real-time updates: status changes reflect immediately in provider view
- Notification settings: admins can configure email notifications for status changes (if implemented)
- Historical data: past incidents and completed maintenance retained for historical reference
- Breadcrumb navigation: Settings > Help Centre Management > Service Status

---

### Screen 6.1: Provider Service Component Add/Edit Form

**Purpose**: Create new service component or edit existing service component. Accessed from Screen 6 (Service Status Management) via "Add Component" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Component Name | text | Yes | Service component name | Max 100 chars, required |
| Component Status | dropdown | Yes | Operational, Degraded, Down | Pre-defined statuses, defaults to Operational |
| Save Button | button | Yes | Save component | N/A |
| Cancel Button | button | No | Cancel and return to service status overview | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Add Component" or "Edit" is clicked from Screen 6
- If editing existing component, form is pre-filled with current component data
- If creating new component, form starts empty with default status "Operational"
- Component status affects overall platform status calculation
- On save, component is created/updated and admin returns to Screen 6 with updated component list
- On cancel, changes are discarded and admin returns to Screen 6

**Notes**:

- Simple form with component name and status
- Status dropdown with color-coded options (Operational: green, Degraded: yellow, Down: red)
- Success message displayed after save
- Breadcrumb navigation: Settings > Help Centre Management > Service Status > [Add Component / Edit Component]

---

### Screen 6.2: Provider Incident Add/Edit Form

**Purpose**: Create new incident or edit existing incident. Accessed from Screen 6 (Service Status Management) via "Create Incident" or "Edit" buttons.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Incident Title | text | Yes | Brief incident title | Max 200 chars, required |
| Incident Description | textarea | Yes | Detailed incident description | Max 2000 chars, required |
| Incident Status | dropdown | Yes | Investigating, Identified, Monitoring, Resolved | Pre-defined statuses, defaults to Investigating |
| Affected Services | multi-select | Yes | Service components affected by incident | References to service components, at least one required |
| Start Time | datetime | Yes | Incident start time | Valid datetime, defaults to current time |
| End Time | datetime | No | Incident end time (when resolved) | Valid datetime, after start time |
| Save Button | button | Yes | Save incident | N/A |
| Cancel Button | button | No | Cancel and return to service status overview | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Create Incident" or "Edit" is clicked from Screen 6
- If editing existing incident, form is pre-filled with current incident data
- If creating new incident, form starts empty with default status "Investigating" and current time as start time
- Affected services multi-select shows all available service components
- Incident status changes are logged in incident timeline automatically
- Overall status automatically recalculated based on affected service components
- On save, incident is created/updated and admin returns to Screen 6 with updated incident history
- On cancel, changes are discarded and admin returns to Screen 6

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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Maintenance Title | text | Yes | Brief maintenance title | Max 200 chars, required |
| Maintenance Description | textarea | Yes | Detailed maintenance description | Max 2000 chars, required |
| Scheduled Start Time | datetime | Yes | Planned maintenance start time | Valid datetime, future date, required |
| Scheduled End Time | datetime | Yes | Planned maintenance end time | Valid datetime, after start time, required |
| Affected Services | multi-select | Yes | Service components affected by maintenance | References to service components, at least one required |
| Status | dropdown | Yes | Scheduled, In Progress, Completed, Cancelled | Pre-defined statuses, defaults to Scheduled |
| Save Button | button | Yes | Save maintenance | N/A |
| Cancel Button | button | No | Cancel and return to service status overview | N/A |

**Business Rules**:

- Form opens in modal or separate screen when "Schedule Maintenance" or "Edit" is clicked from Screen 6
- If editing existing maintenance, form is pre-filled with current maintenance data
- If creating new maintenance, form starts empty with default status "Scheduled"
- Scheduled times must be in the future for new maintenance windows
- Affected services multi-select shows all available service components
- Calendar interface available for selecting scheduled times
- On save, maintenance is created/updated and admin returns to Screen 6 with updated maintenance schedule
- On cancel, changes are discarded and admin returns to Screen 6

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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Preview Mode | dropdown | Yes | Select subscreen layout to preview (FAQs, Articles, Resources, Videos, Service Status) | Pre-defined layouts matching FR-032 |
| Content Preview | rendered view | No | Rendered content in provider-facing layout | Read-only, matches FR-032 subscreen layouts |

**Business Rules**:

- Preview renders content in exact provider-facing layout for selected subscreen type
- FAQ preview shows accordion layout with expand/collapse (matches FR-032 Screen 5.1)
- Article preview shows article layout with table of contents (matches FR-032 Screen 5.2)
- Resource preview shows file viewer interface (matches FR-032 Screen 5.3)
- Video preview shows video player interface (matches FR-032 Screen 5.4)
- Service Status preview shows status page interface (matches FR-032 Screen 5.7)
- Preview updates in real-time as admin edits content
- Preview includes all formatting, images, and interactive elements

**Notes**:

- Preview pane: side-by-side or modal view showing provider-facing layout
- Responsive preview: toggle between desktop/tablet/mobile views
- Print preview: available for article content
- Preview navigation: test all interactive elements (expand/collapse, video playback, file download)

---

#### Patient Help Centre Content Management (Admin Platform)

**Note**: The following Patient Help Centre content management screens (Screen 8 through Screen 13) are **admin-only screens on the Admin Platform**. They mirror the provider content management screens (Screen 1 through Screen 7) in structure and functionality, with the following key differences:

- **Audience**: Content managed here is displayed to patients via FR-035 (Patient Help Center & Support Submission module) instead of providers
- **Screen 8**: Patient Help Centre Management Dashboard (mirrors Screen 1)
- **Screen 9**: Patient FAQ Management (mirrors Screen 2)
- **Screen 9.1**: Patient FAQ Add/Edit Form (mirrors Screen 2.1)
- **Screen 10**: Patient Article Management (mirrors Screen 3)
- **Screen 10.1**: Patient Article Add/Edit Form (mirrors Screen 3.1)
- **Screen 11**: Patient Resource Library Management (mirrors Screen 4)
- **Screen 11.1**: Patient Resource Add/Edit Form (mirrors Screen 4.1)
- **Screen 12**: Patient Video Tutorial Management (mirrors Screen 5)
- **Screen 12.1**: Patient Video Add/Edit Form (mirrors Screen 5.1)
- **Screen 13**: Patient Content Preview (mirrors Screen 7)

**Excluded for Patients**:

- **No Service Status Management** (Screen 6, Screen 6.1, Screen 6.2, Screen 6.3): Service Status is provider-only feature not applicable to patient Help Centre

**Content Separation**:

- Patient content and provider content are stored in completely separate database tables/repositories
- Admin UI clearly labels content as "Patient Content" or "Provider Content" throughout the interface
- Content cannot be copied or shared between provider and patient repositories (manual re-creation required)
- Search and filtering functions are scoped to selected audience (provider or patient)
- Analytics and view counts tracked separately per audience

---

## Business Rules

### General Module Rules

- **Rule 1**: Help Centre content managed for TWO distinct audiences: Providers and Patients; content repositories completely separated by audience type
- **Rule 2**: Only admins can create, edit, or delete Help Centre content; providers and patients have read-only access to their respective content
- **Rule 3**: Content must be tagged with audience type (Provider or Patient) and assigned to exactly one of the predefined categories
- **Rule 4**: Content can exist in three states: Draft (admin-only), Published (audience-visible), Unpublished (admin-only, previously published)
- **Rule 5**: All content changes logged in audit trail with admin identity, timestamp, audience type, and action type
- **Rule 6**: Content deletion is soft-delete (archived) not permanent deletion to support recovery and audit compliance
- **Rule 7**: Admin must explicitly select audience (Provider or Patient) when creating content; content cannot be shared across audiences without manual re-creation

### Data & Privacy Rules

- **Privacy Rule 1**: Help Centre content is non-sensitive and accessible to all users within their respective audience (all provider staff see provider content; all patients see patient content; no role-based content restrictions)
- **Privacy Rule 2**: Content view analytics tracked at organization level for providers (clinic), and aggregated for patients (not individual user level)
- **Privacy Rule 3**: Provider-specific content and patient-specific content stored in separate databases/repositories to prevent cross-audience data exposure
- **Audit Rule**: All content creation, editing, publishing, unpublishing, and deletion actions logged with admin identity and timestamp for compliance audit trail
- **Data Retention**: Archived content retained indefinitely for historical reference and audit compliance

### Admin Editability Rules

**Editable by Admin**:

- All Help Centre content for both Provider and Patient audiences (title, body, attachments, category assignment, publish status, audience type)
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
  - No Service Status management for patients (provider-only feature)
- **Shared Admin Capabilities**:
  - Category organization and ordering
  - FAQ topic organization and FAQ item assignment to topics
  - Content tags and related content links

**Fixed in Codebase (Not Editable)**:

- Number of Help Centre content types: 5 types for providers (FAQs, Articles, Resources, Videos, Service Status); 4 types for patients (FAQs, Articles, Resources, Videos - no Service Status)
- Audience types: Provider and Patient (fixed; cannot add new audience types)
- Content type options (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document)
- File upload size limits (PDF: 50MB, Video: 500MB, Image: 10MB)
- Content body character limits (max 5000 characters for FAQ answers, max 10,000 characters for tutorial guides)
- Audit log retention period (indefinite retention for compliance)

**Configurable with Restrictions**:

- Category visibility (admin can show/hide categories but cannot delete predefined categories; applies separately to provider and patient content)
- Content versioning (enabled by default, admin cannot disable version control; applies to both provider and patient content)
- Audience targeting (admin must select Provider or Patient when creating content; content cannot be shared across audiences without manual re-creation)

### Payment & Billing Rules

*Not applicable - Help Centre is a content management feature with no payment or billing components.*

---

## Success Criteria

### Provider Experience Metrics

- **SC-001**: Providers can access Help Centre and find relevant content within 2 clicks from any provider platform screen
- **SC-002**: 70% of provider support questions can be answered via Help Centre self-service content
- **SC-003**: Providers can navigate Help Centre and find answers to common questions in under 3 minutes
- **SC-004**: 80% of providers rate Help Centre content as "Helpful" or "Very Helpful" via feedback buttons

### Patient Experience Metrics

- **SC-013**: Patients can access Help Centre and find relevant content within 2 clicks from any patient app screen
- **SC-014**: 60% of patient support questions can be answered via Help Centre self-service content
- **SC-015**: Patients can navigate Help Centre and find answers to common questions in under 3 minutes
- **SC-016**: 75% of patients rate Help Centre content as "Helpful" or "Very Helpful" via feedback buttons

### Admin Management Metrics

- **SC-005**: Admins can create and publish new Help Centre content (provider or patient) in under 10 minutes per content item
- **SC-006**: Admins can update existing content and publish changes in under 5 minutes
- **SC-007**: Admins can organize FAQ topics and reorder content in under 5 minutes using drag-and-drop interface
- **SC-008**: 100% of Help Centre content changes tracked in audit trail for compliance verification (both provider and patient content)

### System Performance Metrics

- **SC-009**: Help Centre landing page loads in under 2 seconds for 95% of requests (both provider and patient platforms)
- **SC-010**: Content search returns results in under 1 second for 90% of queries (future enhancement, both audiences)
- **SC-011**: File downloads (PDFs, videos) begin within 3 seconds of user click (both provider and patient)
- **SC-012**: System supports 1000 concurrent provider accesses and 5000 concurrent patient accesses to Help Centre without performance degradation

### Business Impact Metrics

- **SC-017**: Average time to resolve provider support issues decreases by 25% due to self-service content availability
- **SC-018**: Average time to resolve patient support issues decreases by 20% due to self-service content availability
- **SC-019**: 60% of providers access Help Centre at least once per month for self-service support
- **SC-020**: 40% of patients access Help Centre at least once per month for self-service support
- **SC-021**: Help Centre content view count increases by 20% month-over-month indicating growing adoption across both audiences

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-032 / Module PR-06**: Provider Help Centre accessed from provider settings page
  - **Why needed**: Help Centre menu item appears in provider platform navigation, linked from FR-032 profile & settings module
  - **Integration point**: Help Centre navigation menu item added to provider platform sidebar, accessible from settings page; displays provider-specific Help Centre content

- **FR-035 / Module P-08**: Patient Help Centre accessed from patient app
  - **Why needed**: Patient Help Centre provides read-only access to patient-specific Help Centre content managed in FR-033
  - **Integration point**: Patient app fetches patient-specific Help Centre content via REST API; displays patient-facing FAQs, articles, resources, and videos (no Service Status)

- **FR-031 / Module A-09**: Admin access control for Help Centre management
  - **Why needed**: Help Centre management requires admin role permissions to create, edit, publish content for both provider and patient audiences
  - **Integration point**: Admin platform role-based permissions control access to Help Centre management features across both content repositories

- **FR-009 / Module PR-01**: Provider team member access to Help Centre
  - **Why needed**: All provider staff (regardless of role) should be able to access provider Help Centre for support
  - **Integration point**: Help Centre accessible to all provider roles defined in FR-009 (Owner, Manager, Clinical Staff, Billing Staff)

- **FR-034 / Module A-10**: Support Center & Ticketing for all submissions
  - **Why needed**: Provider submissions via Help Centre Contact Support form (FR-032 Screen 5.5) and Feedback & Suggestions form (FR-032 Screen 5.6), and patient submissions via FR-035, are managed through FR-034 Support Center & Ticketing system, not within FR-033
  - **Integration point**: All submissions from Help Centre forms automatically create support cases in FR-034; FR-033 provides read-only Help Centre content only, while FR-034 handles all support ticket and feedback case management for both providers and patients

### External Dependencies (APIs, Services)

- **External Service 1**: Media Storage Service (S-05)
  - **Purpose**: Store uploaded tutorial guides, videos, images, PDF documents
  - **Integration**: RESTful API calls for file upload, retrieval, deletion
  - **Failure handling**: If media storage unavailable, queue uploads for retry; display cached content to providers; notify admin of storage issues

- **External Service 2**: Rich Text Editor Library (e.g., Quill, TinyMCE, CKEditor)
  - **Purpose**: Provide WYSIWYG editing for Help Centre content creation
  - **Integration**: JavaScript library integrated into admin content creation form
  - **Failure handling**: If editor library fails to load, fall back to plain textarea with markdown support

- **External Service 3**: Virus Scanning Service (e.g., ClamAV, cloud-based scanner)
  - **Purpose**: Scan uploaded files for viruses and malware before storage
  - **Integration**: API call during file upload process
  - **Failure handling**: If virus scanner unavailable, quarantine uploads and notify admin; do not make files available to providers until scan completes

### Data Dependencies

- **Entity 1**: Admin user accounts with Help Centre management permissions
  - **Why needed**: Cannot create or manage Help Centre content without authenticated admin user with appropriate permissions
  - **Source**: Admin platform authentication module (A-09 / FR-031)

- **Entity 2**: Provider clinic accounts
  - **Why needed**: Cannot display Help Centre content to providers without active provider accounts
  - **Source**: Provider authentication and account management module (PR-01 / FR-009)

- **Entity 3**: Media storage infrastructure
  - **Why needed**: Cannot store or serve uploaded files (videos, PDFs, images) without media storage service
  - **Source**: Shared media storage service (S-05)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Providers and patients will proactively check Help Centre for answers before contacting support (requires cultural shift toward self-service)
- **Assumption 2**: Admins will maintain Help Centre content currency by reviewing and updating content quarterly or as platform features change for both provider and patient content
- **Assumption 3**: Providers and patients have basic computer literacy to navigate Help Centre categories, expand/collapse sections, and download files
- **Assumption 4**: Providers and patients prefer self-service content (FAQ, tutorials) over contacting support for common questions
- **Assumption 5**: Patient content will have higher view volume than provider content due to larger patient user base

### Technology Assumptions

- **Assumption 1**: Providers access Help Centre via modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions) on desktop or tablet devices
- **Assumption 2**: Patients access Help Centre via mobile app (iOS/Android) with occasional web browser access
- **Assumption 3**: Providers and patients have stable internet connection to download tutorial videos and PDF guides (minimum 5 Mbps recommended)
- **Assumption 4**: Admins use desktop/laptop computers for Help Centre content management (not optimized for mobile editing)
- **Assumption 5**: Media storage service (S-05) has sufficient capacity to store tutorial videos for both audiences (assume average 50MB per video, 200 videos total = 10GB storage)

### Business Process Assumptions

- **Assumption 1**: Hairline admin team has dedicated content manager(s) responsible for creating and maintaining Help Centre content for both provider and patient audiences
- **Assumption 2**: Help Centre content reviewed and updated quarterly to ensure accuracy and relevance across both audiences
- **Assumption 3**: Support team monitors feedback submissions and content gaps to prioritize new content creation for both providers and patients
- **Assumption 4**: Service status updates managed by Hairline technical operations team with real-time incident updates during outages (provider-only feature)
- **Assumption 5**: Patient content will be curated to avoid medical advice and focus on platform usage, appointment management, and general information

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Help Centre content stored in relational database with separate tables/repositories for provider and patient content; shared media storage for files; content served via web API with caching layer for frequently accessed content
- **Content Management**: Use headless CMS architecture to separate content management (admin) from content presentation (provider platform and patient app); admin UI clearly distinguishes between provider and patient content repositories
- **Multi-Tenant Separation**: Provider content and patient content completely separated at database level to prevent cross-audience data exposure; separate API endpoints for provider content (/api/provider/help-centre) and patient content (/api/patient/help-centre)
- **File Storage**: Large files (videos, PDFs) stored in cloud object storage (S3, Azure Blob) with CDN for fast global delivery; files tagged with audience type (provider/patient) for access control
- **Performance**: Implement aggressive caching for published Help Centre content (cache invalidation on content updates); pre-generate content indexes for fast category/tag filtering per audience; patient content cached more aggressively due to higher expected traffic
- **Search**: Full-text search across all content (title, body, tags) using database full-text indexing or dedicated search engine (Elasticsearch, Algolia) for advanced search features (future enhancement); search scoped to selected audience (provider or patient)

### Integration Points

- **Integration 1**: Provider platform fetches provider-specific Help Centre content via REST API
  - **Data format**: JSON payload with content metadata (title, category, type, publish date, audience: "provider") and content body (HTML)
  - **Authentication**: Provider platform uses authenticated API calls with provider session token
  - **Error handling**: If API unavailable, display cached content or "Help Centre temporarily unavailable" message; retry API call on next page load
  - **Endpoint**: GET /api/provider/help-centre (returns provider content only)

- **Integration 2**: Patient app fetches patient-specific Help Centre content via REST API
  - **Data format**: JSON payload with content metadata (title, category, type, publish date, audience: "patient") and content body (HTML)
  - **Authentication**: Patient app uses authenticated API calls with patient session token
  - **Error handling**: If API unavailable, display cached content or "Help Centre temporarily unavailable" message; retry API call on next page load
  - **Endpoint**: GET /api/patient/help-centre (returns patient content only, excludes Service Status)

- **Integration 3**: Admin platform manages Help Centre content for both audiences via REST API with rich text editor
  - **Data format**: JSON payload with content metadata (including audience: "provider" or "patient") and HTML content body; file uploads via multipart form data
  - **Authentication**: Admin platform uses authenticated API calls with admin session token and permission verification
  - **Error handling**: If API unavailable, queue content changes locally and sync when API available; notify admin of sync failures
  - **Endpoints**: POST /api/admin/help-centre (create content), PUT /api/admin/help-centre/:id (update), DELETE /api/admin/help-centre/:id (archive)

- **Integration 4**: Media storage service (S-05) stores uploaded files for both audiences
  - **Data format**: Binary file upload with metadata (file name, size, content type, associated content ID, audience type)
  - **Authentication**: Signed upload URLs or API key authentication
  - **Error handling**: If upload fails, retry with exponential backoff (3 attempts); if all retries fail, notify admin and save content as draft

### Scalability Considerations

- **Current scale**: Expect 200 Help Centre content items at launch (100 provider content items + 100 patient content items; 50 FAQs + 30 guides + 20 videos per audience)
- **Growth projection**: Plan for 1000+ content items within 12 months as platform features expand and user base grows (500 provider + 500 patient)
- **Peak load**: Handle 500 concurrent provider accesses and 5000 concurrent patient accesses to Help Centre during major feature launches or platform incidents
- **Data volume**: Expect 20GB media storage for videos and PDFs within first year (200 videos @ 50MB average, 400 PDFs @ 5MB average across both audiences)
- **Scaling strategy**: Horizontal scaling of web servers serving Help Centre API; CDN for media file delivery; database read replicas for content queries; cache layer (Redis/Memcached) for frequently accessed content with separate cache namespaces for provider and patient content

### Security Considerations

- **Authentication**: Help Centre content accessible only to authenticated users (providers and patients access their respective content); admin content management accessible only to authenticated admin users with Help Centre management permissions
- **Authorization**: Role-based access control enforced at API level (providers: read-only provider content, patients: read-only patient content, admins: read-write both content repositories based on permissions)
- **Audience Separation**: Providers cannot access patient content; patients cannot access provider content; API endpoints enforce audience-based access control to prevent cross-audience data exposure
- **File Upload Security**: All uploaded files scanned for viruses before storage; file type validation (whitelist: PDF, MP4, MOV, JPG, PNG); file size limits enforced; uploaded files stored outside web root with access-controlled URLs; files tagged with audience type for access control
- **Content Injection**: Rich text editor sanitizes HTML input to prevent XSS attacks; strip dangerous tags (script, iframe) before saving; use Content Security Policy (CSP) headers
- **Audit trail**: All content changes logged with admin identity, timestamp, IP address, audience type, and action for security audit compliance
- **Data Privacy**: User feedback on content (helpfulness ratings) logged with user identity for analytics but not publicly displayed; support requests encrypted in transit (HTTPS)

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
5. **Given** admin has reviewed preview and verified formatting, **When** admin clicks "Publish", **Then** system saves FAQ with "Published" status, logs creation in audit trail, and makes FAQ immediately available in provider Help Centre

---

### User Story 3 - Admin Updates Service Status During Platform Incident (Priority: P1)

An admin operations staff member needs to update the platform service status when a database outage occurs. They navigate to Service Status Management, create a new incident record, update affected service components, and ensure providers can see the status update in real-time.

**Why this priority**: Critical operational functionality for communicating platform status to providers during outages

**Independent Test**: Can be fully tested by creating service components, simulating incident, updating status, and verifying status propagates to provider view within 1 minute

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to Settings > Help Centre Management > Service Status Management (Screen 6), **Then** Service Status Management screen loads showing overall status, service components list, incident history, and maintenance schedule
2. **Given** admin detects database outage affecting multiple services, **When** admin clicks "Create Incident" button, **Then** incident creation form opens with fields for title, description, affected services, and status
3. **Given** admin has entered incident details "Database Connection Issues" with description and selected affected services, **When** admin sets status to "Investigating" and saves, **Then** system creates incident record, updates overall status to "Partial Outage", and adds incident to timeline
4. **Given** incident is created and status updated, **When** admin updates affected service components to "Degraded" or "Down", **Then** system recalculates overall status and updates provider-facing Service Status page (FR-032 Screen 5.7) within 1 minute
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
5. **Given** FAQs are organized into topics, **When** admin reorders FAQs within topic using drag-and-drop and saves, **Then** system updates display order and provider Help Centre (FR-032 Screen 5.1) immediately reflects new organization in accordion layout

### Edge Cases

- What happens when admin attempts to publish content with missing required fields?
- How does system handle concurrent edits by multiple admins to the same Help Centre content?
- What occurs if provider attempts to download large video tutorial but network connection is unstable?
- How to manage Help Centre content when admin deletes content that is linked as "Related Content" from other items?
- What happens when file upload exceeds maximum size limit (video > 500MB, PDF > 50MB)?
- How does system handle Help Centre content search when search query returns zero results?

---

## Functional Requirements Summary

### Core Requirements

- **REQ-033-001**: System MUST provide Help Centre content management for TWO distinct audiences: Providers and Patients, with completely separated content repositories
- **REQ-033-002**: System MUST support 5 Help Centre content types for providers (FAQs with accordion layout, Articles with article layout, Resources with file viewer, Videos with video player, Service Status with status page interface) matching FR-032 structure
- **REQ-033-003**: System MUST support 4 Help Centre content types for patients (FAQs, Articles, Resources, Videos - NO Service Status) displayed via FR-035 patient app
- **REQ-033-004**: Admins MUST be able to create Help Centre content with audience selection (Provider or Patient), category assignment, content type, title, rich text body, file attachments, tags, and publish status
- **REQ-033-005**: System MUST support multiple content types (FAQ, Tutorial Guide, Troubleshooting Tip, Video Tutorial, Resource Document, Policy Document) applicable to both audiences
- **REQ-033-006**: Admins MUST be able to organize FAQ content into collapsible topic sections with drag-and-drop reordering for both provider and patient FAQs separately
- **REQ-033-007**: Providers MUST be able to access provider-specific Help Centre content in read-only mode via FR-032 with distinct layouts per subscreen type
- **REQ-033-008**: Patients MUST be able to access patient-specific Help Centre content in read-only mode via FR-035 (Patient Help Center & Support Submission)
- **REQ-033-009**: System MUST support rich text editing for content creation with formatting (bold, italic, lists, links, images, tables) for both audiences
- **REQ-033-010**: System MUST support file uploads for Help Centre content (PDFs max 50MB, videos max 500MB, images max 10MB) for both audiences
- **REQ-033-011**: System MUST provide content preview functionality allowing admins to view content exactly as target audience will see it before publishing
- **REQ-033-012**: System MUST support content versioning tracking all changes with admin identity, timestamp, audience type, and version notes

### Data Requirements

- **REQ-033-013**: System MUST store Help Centre content with metadata including audience type (Provider/Patient), content type, title, body, tags, publish status, created date, updated date, created by admin, updated by admin
- **REQ-033-014**: System MUST store provider-specific Service Status data with metadata (overall status, service components with statuses, incidents with timeline, maintenance windows with schedules) - NOT applicable to patient content
- **REQ-033-015**: System MUST maintain audit trail logging all content creation, editing, publishing, unpublishing, and deletion actions with admin identity, audience type, and timestamp
- **REQ-033-016**: System MUST support soft-delete for content (move to "Archived" status) not permanent deletion for both audiences
- **REQ-033-017**: System MUST store file attachments in media storage service (S-05) with references in Help Centre content records and audience type tags
- **REQ-033-018**: System MUST track content view analytics (total views per content item, views over time) separately for provider and patient audiences

### Security & Privacy Requirements

- **REQ-033-019**: System MUST enforce authentication for Help Centre access (providers, patients, and admins must be logged in)
- **REQ-033-020**: System MUST enforce authorization for content management (only admins with Help Centre management permissions can create/edit/publish content for both audiences)
- **REQ-033-021**: System MUST enforce audience-based access control preventing providers from accessing patient content and patients from accessing provider content
- **REQ-033-022**: System MUST scan all uploaded files for viruses before making available to users
- **REQ-033-023**: System MUST sanitize rich text HTML input to prevent XSS attacks (strip dangerous tags: script, iframe, object)
- **REQ-033-024**: System MUST enforce file type whitelist for uploads (PDF, MP4, MOV, JPG, PNG only) rejecting all other file types

### Integration Requirements

- **REQ-033-025**: System MUST provide REST API for provider platform (FR-032) to fetch provider-specific Help Centre content with authentication
- **REQ-033-026**: System MUST provide REST API for patient app (FR-035) to fetch patient-specific Help Centre content with authentication
- **REQ-033-027**: System MUST integrate with media storage service (S-05) for file upload, retrieval, and deletion with audience type tagging
- **REQ-033-028**: System MUST integrate with rich text editor library (Quill/TinyMCE/CKEditor) for content creation interface
- **REQ-033-029**: System MUST integrate with virus scanning service for file upload security validation
- **REQ-033-030**: Admins MUST be able to manage Service Status components, incidents, and maintenance windows for provider audience only (not applicable to patient audience)

---

## Key Entities

[10 detailed entities as specified in complete PRD]

- **Entity 1 - Help Centre Content**
- **Entity 2 - Help Centre Category**
- **Entity 3 - FAQ Topic**
- **Entity 4 - Content File Attachment**
- **Entity 5 - Content Version History**
- **Entity 6 - Service Status Component**: Represents individual service components for status monitoring
  - **Key attributes**: component ID, component name, status (Operational, Degraded, Down), last updated timestamp, last updated by admin ID
  - **Relationships**: Many components contribute to overall platform status; components affected by incidents

- **Entity 7 - Incident Record**: Represents platform incidents and outages
  - **Key attributes**: incident ID, title, description, status (Investigating, Identified, Monitoring, Resolved), start time, end time, affected services (array of component IDs), timeline updates (array of status changes with timestamps), created by admin ID
  - **Relationships**: One incident affects many service components; incidents displayed in FR-032 Screen 5.7

- **Entity 8 - Maintenance Window**: Represents scheduled maintenance periods
  - **Key attributes**: maintenance ID, title, description, scheduled start time, scheduled end time, affected services (array of component IDs), status (Scheduled, In Progress, Completed, Cancelled), created by admin ID
  - **Relationships**: One maintenance window affects many service components; maintenance displayed in FR-032 Screen 5.7

- **Entity 9 - Content Analytics**: Represents content performance metrics
  - **Key attributes**: content ID, view count, helpfulness rating (Yes/No counts), average time spent, last viewed timestamp
  - **Relationships**: One content item has one analytics record; analytics used for content optimization

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-17 | 1.0 | Initial PRD creation for FR-033 Help Centre Content Management | Claude AI Assistant |
| 2025-12-03 | 1.1 | Major updates to align with FR-032 changes: Reorganized screen specifications to match FR-032's 7 subscreen structure (FAQs, Articles, Resources, Videos, Contact Support, Feedback, Service Status); Added submission tracking management screens for Contact Support and Feedback with status workflows; Added Service Status management interface for components, incidents, and maintenance windows; Updated content creation/editing forms to match provider-facing layouts (accordion for FAQs, article layout for guides, file viewer for resources, video player for videos, status page for service status); Updated preview functionality to match each subscreen layout; Updated workflows to reflect new subscreen structure; Added functional requirements for submission tracking and service status management | AI/Claude |
| 2026-01-11 | 1.2 | Moved provider Contact Support and Feedback management to FR-034: Removed Contact Support and Feedback submission management from FR-033 (moved to FR-034 Support Center & Ticketing); Updated to 5 subscreen types (removed Contact Support and Feedback, kept FAQs, Articles, Resources, Videos, Service Status); Removed Screen 6 (Contact Support Management) and Screen 7 (Feedback Management); Removed workflows A1 and A2 for provider submissions; Removed related functional requirements and entities; Provider submissions now managed through FR-034 unified ticketing system | AI Assistant |
| 2026-01-16 | 2.0 | Major scope extension to support both Provider and Patient audiences: Extended module to manage Help Centre content for TWO distinct audiences (Providers and Patients) with completely separated content repositories; Added Patient Help Centre Content Management section (Screens A-8 through A-13 mirroring provider screens A-1 through A-7, excluding Service Status); Updated Executive Summary, Multi-Tenant Architecture, and Module Scope to reflect dual-audience support; Reorganized Screen Specifications with tenant headers and proper screen numbering (A-1 through A-13); Updated Business Rules for multi-tenant support (General Module Rules, Data & Privacy Rules, Admin Editability Rules, Configurable with Restrictions); Added Patient Experience Metrics to Success Criteria; Updated Dependencies to include FR-035 (Patient Help Center & Support Submission); Updated Assumptions for both provider and patient users; Enhanced Implementation Notes with multi-tenant architecture details (separate API endpoints, database separation, audience-based caching); Updated Integration Points to specify provider and patient API endpoints; Updated Scalability, Security Considerations for both audiences; Completely revised Functional Requirements Summary to specify provider AND patient content requirements with audience separation and access control | AI Assistant |
| 2026-01-19 | 2.1 | Verification and finalization: Moved provider-facing Help Centre access flows from FR-033 to FR-032 (provider UX flows belong in FR-032, not content management PRD); Added Screen 2.2 for FAQ Topic Management (create/edit topics, drag-and-drop reordering); Enhanced video management to support both file uploads and third-party embeds (YouTube, Vimeo) with conditional validation; Clarified that Patient Help Centre content management screens are admin-only (not patient app screens); Updated module references to include P-08 (Patient Help Center & Support Access); Updated status to Verified & Approved | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | 2026-01-19 | ✅ Approved |
| Technical Lead | [Name] | 2026-01-19 | ✅ Approved |
| Stakeholder | [Name] | 2026-01-19 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD Template
**Last Updated**: 2026-01-19
