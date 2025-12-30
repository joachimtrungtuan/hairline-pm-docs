# Medical Questionnaire Management Module - Product Requirements Document

**Module**: A-09: System Settings & Configuration  
**Feature Branch**: `fr025-medical-questionnaire-management`  
**Created**: 2025-10-23  
**Status**: ✅ Verified & Approved  
**Source**: FR-025 from system-prd.md

## Executive Summary

The Medical Questionnaire Management module enables administrators to centrally manage the comprehensive medical questionnaire used in the inquiry submission process. This module provides complete control over question content, severity flagging, categorization, and version control, ensuring the medical assessment system remains current, compliant, and effective for provider decision-making.

## Module Scope

### Multi-Tenant Architecture

- **Admin Platform (A-09)**: System Settings & Configuration
- **Integration Points**: Patient Platform (inquiry submission), Provider Platform (alert display)

### Communication Structure

- **Admin → System**: Question management and configuration updates
- **System → Patient Platform**: Dynamic questionnaire content delivery
- **System → Provider Platform**: Medical alert generation and display
- **System → All Platforms**: Version-controlled questionnaire updates

### Entry Points

1. **Admin-Initiated**: Primary flow through admin dashboard questionnaire management
2. **System-Triggered**: Automatic questionnaire delivery to patient inquiry process
3. **Provider-Viewed**: Medical alerts generated from questionnaire responses

### Questionnaire Context Types

- The system must support multiple questionnaire context types to distinguish usage across flows:
  - Inquiry: Used during patient inquiry submission
  - Aftercare: Used within aftercare milestone templates
  - Multi-Context: Valid for both Inquiry and Aftercare
- Each questionnaire carries a required Context Type metadata field and optional tags (e.g., "pain", "sleep", "compliance").
- Downstream modules (e.g., Aftercare Template Management) filter selectable questionnaires by compatible Context Type.

## Business Workflows

### Workflow 1: Question Management (Primary Flow)

**Actors**: Admin, System, Questionnaire Engine

**Main Flow**:

1. **Question Creation**
   - Admin accesses questionnaire management dashboard
   - Admin creates new question with content and severity flag
   - System validates question completeness
   - Question added to active questionnaire

2. **Question Editing**
   - Admin selects existing question for modification
   - Admin updates question text, severity, or category
   - System validates changes and maintains version history
   - Updated question replaces previous version

3. **Question Organization**
   - Admin organizes questions into categories (Allergies, Cardiovascular, etc.)
   - Admin reorders questions using drag-and-drop interface
   - System updates question sequence and maintains order
   - Changes reflected in patient questionnaire

4. **Question Activation**
   - Admin reviews complete questionnaire
   - Admin activates updated questionnaire version
   - System deploys new questionnaire to patient platform
   - Previous version archived with timestamp

**Alternative Flows**:

- **A1**: Admin deletes question
  - System performs soft delete (archival)
  - Question removed from active questionnaire
  - Historical responses preserved

- **A2**: Question validation fails
  - System prevents activation
  - Admin notified of validation errors
  - Admin corrects issues before activation

### Workflow 2: Severity Management (Admin Flow)

**Actors**: Admin, System, Alert Engine

**Main Flow**:

1. **Severity Assignment**
   - Admin assigns severity flag to each question
   - Severity options: Critical, Standard, No Alert
   - System validates severity assignment
   - Alert rules updated automatically

2. **Alert Rule Configuration**
   - System generates alert rules based on severity flags
   - Critical questions → Red alerts for providers
   - Standard questions → Yellow/amber alerts for providers
   - No alert questions → Green indicators
   - Admin reviews and confirms alert rules

**Alternative Flows**:

- **B1**: Severity conflict resolution
  - Admin reviews conflicting severity assignments
  - Admin resolves conflicts based on medical guidelines
  - System updates alert generation rules

### Workflow 3: Questionnaire Deployment (System Flow)

**Actors**: System, Patient Platform, Provider Platform

**Main Flow**:

1. **Questionnaire Delivery**
   - System delivers current questionnaire to patient inquiry process
   - Patient platform displays questions with proper formatting
   - System tracks questionnaire version used per inquiry

2. **Response Processing**
   - System processes patient questionnaire responses
   - System applies severity-based alert generation
   - System delivers alerts to provider platform
   - System logs all responses for audit trail

**Alternative Flows**:

- **C1**: Questionnaire version mismatch
  - System detects version inconsistency
  - System updates patient platform with current version
  - Patient re-completes questionnaire if necessary

### Workflow 4: Questionnaire Catalog & Assignment

**Actors**: Admin, System, Aftercare Module

**Main Flow**:

1. Admin creates a new Questionnaire and sets Context Type = Inquiry, Aftercare, or Multi-Context
2. System validates completeness, context assignment, and versioning
3. Questionnaire becomes available in the central catalog with its Context Type
4. In Aftercare Template Management (FR-011 Screen 14), admin selects exactly one Questionnaire Set with Context Type = Aftercare or Multi-Context (single-select)
5. Milestones within the template may schedule questions only from the selected Questionnaire Set
6. System deploys scheduled questionnaires to the aftercare plan according to milestone schedules

**Alternative Flows**:

- **A1**: Context mismatch
  - If a questionnaire with Context Type = Inquiry is selected in an aftercare template, the system blocks selection and explains the mismatch
- **A2**: Context change on active questionnaire
  - Context Type changes create a new version; dependent templates must re-confirm the single selected Questionnaire Set
- **A3**: Questionnaire Set replacement
  - Replacing the selected Questionnaire Set in FR-011 updates all milestone questionnaire references within that template

## Screen Specifications

### Admin Platform Screens

#### Screen 1: Questionnaire Management Dashboard

**Purpose**: Admin views and manages all questionnaire questions

**Data Fields**:

- **Question List** (sortable table):
  - Question ID (auto-generated)
  - Question Text (truncated with expand option)
  - Category (dropdown filter)
  - Context Type (Inquiry/Aftercare/Multi-Context)
  - Severity Flag (color-coded: Critical/Standard/No Alert)
  - Status (Active/Inactive)
  - Last Modified (timestamp)
  - Created By (admin name)
  - Actions (Edit/Delete/Reorder buttons)

- **Management Controls**:
  - "Add New Question" button
  - "Export Questionnaire" button
  - "Preview Questionnaire" button
  - "Activate Changes" button

- **Filter and Search**:
  - Category filter (dropdown)
  - Context Type filter (dropdown)
  - Severity filter (dropdown)
  - Keyword search (question text)
  - Status filter (Active/Inactive/All)

**Business Rules**:

- Questions displayed in current activation order
- Drag-and-drop reordering enabled
- All changes require admin confirmation
- Preview shows questionnaire as patients will see it

#### Screen 2: Question Editor

**Purpose**: Admin creates or edits individual questions

**Data Fields**:

- **Question Content**:
  - Question Text (rich text editor, required)
  - Question Type (Yes/No - fixed, not editable)
  - Detailed Explanation Prompt (text field, required for "Yes" answers)
  - Category Selection (dropdown, required)
  - Context Type (required: Inquiry, Aftercare, or Multi-Context)
  - Tags (free-form chips, optional)

- **Severity Configuration**:
  - Severity Flag (dropdown: Critical/Standard/No Alert)
  - Alert Description (text field, auto-populated based on severity)
  - Medical Guidelines Reference (optional text field)

- **Validation Settings**:
  - Required Field (checkbox, default: Yes)
  - Validation Rules (text field for custom rules)
  - Error Message (text field for validation failures)

- **Metadata**:
  - Question ID (auto-generated, read-only)
  - Created Date (timestamp, read-only)
  - Last Modified (timestamp, read-only)
  - Modified By (admin name, read-only)

**Business Rules**:

- Question text must be clear and medically appropriate
- Detailed explanation prompt required for "Yes" answers
- Severity flag determines alert generation
- All changes logged with timestamp and admin identification
- Rich text editor supports medical terminology formatting
- Questions must have a Context Type; selection availability in downstream modules is filtered by Context Type

#### Screen 3: Category Management

**Purpose**: Admin organizes questions into logical categories

**Data Fields**:

- **Category List**:
  - Category Name (text field)
  - Category Description (text field)
  - Question Count (auto-calculated)
  - Display Order (number field)
  - Status (Active/Inactive)

- **Category Controls**:
  - "Add Category" button
  - "Edit Category" button
  - "Delete Category" button
  - "Reorder Categories" drag-and-drop

**Business Rules**:

- Categories must have unique names
- Questions can only belong to one category
- Deleting category moves questions to "Uncategorized"
- Display order determines questionnaire section order

#### Screen 4: Questionnaire Preview

**Purpose**: Admin previews questionnaire as patients will experience it

**Data Fields**:

- **Preview Display**:
  - Complete questionnaire layout
  - All questions in activation order
  - Category groupings with headers
  - Severity indicators (visual preview)
  - Form validation behavior

- **Preview Controls**:
  - "Mobile View" toggle
  - "Desktop View" toggle
  - "Test Validation" button
  - "Print Preview" button

**Business Rules**:

- Preview shows exact patient experience
- Mobile and desktop views available
- Validation testing shows error messages
- Print preview optimized for documentation

#### Screen 5: Version History & Audit Trail

**Purpose**: Admin views questionnaire change history and audit information

**Data Fields**:

- **Version History**:
  - Version Number (auto-incremented)
  - Activation Date (timestamp)
  - Activated By (admin name)
  - Question Count (number)
  - Changes Summary (text field)
  - Status (Active/Archived)

- **Audit Trail**:
  - Change Date (timestamp)
  - Admin Name (user identification)
  - Action Type (Create/Edit/Delete/Activate)
  - Question ID (if applicable)
  - Change Details (before/after values)
  - IP Address (security tracking)

**Business Rules**:

- All changes tracked with complete audit trail
- Version history maintained indefinitely
- Audit trail includes security information
- Changes can be rolled back to previous versions

## Business Rules

### Question Management Rules

1. **Question Content Rules**
   - All questions must be medically relevant and appropriate
   - Question text must be clear and unambiguous
   - Detailed explanation prompts required for "Yes" answers
   - Questions must follow medical assessment best practices
   - Question content must be reviewed by medical professionals

2. **Severity Flagging Rules**
   - Critical questions: High-risk conditions (HIV, blood disorders, heart conditions)
   - Standard questions: Moderate concerns (allergies, medications, chronic conditions)
   - No alert questions: General health status, lifestyle factors
   - Severity flags determine provider alert generation
   - Alert descriptions auto-generated based on severity level

3. **Category Organization Rules**
   - Questions must be organized into logical medical categories
   - Categories must have descriptive names and purposes
   - Question order within categories affects questionnaire flow
   - Categories can be reordered to optimize patient experience
   - Uncategorized questions must be assigned to categories

### Version Control Rules

1. **Change Management**
   - All question changes must be version controlled
   - Changes require admin authentication and authorization
   - Previous versions must be archived, not deleted
   - Version activation requires explicit admin confirmation
   - Rollback capability must be available for all versions

2. **Audit Requirements**
   - All changes must be logged with timestamp and admin identification
   - Audit trail must include before/after values for all modifications
   - Security information (IP address, session) must be tracked
   - Audit logs must be retained for compliance requirements
   - Audit trail must be tamper-proof and immutable

### Integration Rules

1. **Patient Platform Integration**
   - Questionnaire must be delivered dynamically to patient inquiry process
   - Version consistency must be maintained across all platforms
   - Question formatting must be optimized for mobile devices
   - Validation rules must be consistent between admin and patient platforms
   - Error handling must provide clear user guidance

2. **Provider Platform Integration**
   - Medical alerts must be generated automatically from questionnaire responses
   - Alert severity must match question severity flags
   - Alert display must be consistent with color-coding standards
   - Provider notifications must be triggered by critical alerts
   - Alert history must be maintained for provider reference

3. **Aftercare Module Integration (FR-011)**

- Aftercare templates (Screen 14) can only select one Questionnaire Set with Context Type = Aftercare or Multi-Context (single-select)
- Milestones schedule items only from the selected Questionnaire Set (frequency/recurrence)
- Inquiry-context questionnaires are not selectable in aftercare templates

### Data Integrity Rules

1. **Question Validation**
   - All questions must pass completeness validation before activation
   - Question text must meet minimum length requirements
   - Severity flags must be assigned to all questions
   - Categories must be assigned to all questions
   - Duplicate questions must be prevented

2. **System Consistency**
   - Questionnaire version must be consistent across all platforms
   - Alert generation rules must match severity flag assignments
   - Category organization must be reflected in patient questionnaire
   - Question order must be maintained during updates
   - System must handle concurrent admin modifications gracefully

## Success Criteria

### Admin Efficiency Metrics

- **SC-001**: Admin can create a new question in under 2 minutes
- **SC-002**: Admin can reorganize 20+ questions using drag-and-drop in under 5 minutes
- **SC-003**: Admin can preview questionnaire changes in under 30 seconds
- **SC-004**: Admin can activate questionnaire updates in under 1 minute

### System Reliability Metrics

- **SC-005**: Questionnaire updates deploy to patient platform within 2 minutes
- **SC-006**: System maintains 99.9% uptime for questionnaire management
- **SC-007**: Version rollback completes within 1 minute
- **SC-008**: Audit trail captures 100% of admin actions

### Integration Performance Metrics

- **SC-009**: Patient questionnaire loads with current version in under 3 seconds
- **SC-010**: Medical alerts generate within 5 seconds of questionnaire completion
- **SC-011**: Provider platform receives alerts within 10 seconds
- **SC-012**: System handles 1000+ concurrent questionnaire completions

### Quality Assurance Metrics

- **SC-013**: 100% of questions pass validation before activation
- **SC-014**: Zero data loss during questionnaire updates
- **SC-015**: All audit trail entries are complete and accurate
- **SC-016**: Medical alert accuracy matches severity flag assignments

## Dependencies

### Internal Dependencies

- **FR-003**: Inquiry Submission & Distribution (questionnaire delivery to patients)
- **FR-002**: Medical History & 3D Scanning (medical data integration)
- **FR-020**: Notifications & Alerts (provider alert delivery)
- **FR-001**: Patient Authentication & Profile Management (admin access control)

### External Dependencies

- **Medical Guidelines**: Reference materials for question content validation
- **Compliance Standards**: Healthcare data protection regulations
- **Rich Text Editor**: Advanced text formatting capabilities
- **Version Control System**: Change tracking and rollback capabilities

### Data Dependencies

- **Admin User Data**: From admin authentication and profile management
- **Questionnaire History**: From previous questionnaire versions and responses
- **Medical Standards**: From healthcare industry best practices
- **Audit Requirements**: From compliance and regulatory standards

## Assumptions

1. **Admin Expertise**: Admin users have sufficient medical knowledge to create appropriate questions
2. **Medical Compliance**: Question content aligns with healthcare industry standards
3. **System Performance**: Infrastructure can handle real-time questionnaire updates
4. **Data Security**: All questionnaire data meets healthcare compliance requirements
5. **Version Control**: System can maintain multiple questionnaire versions simultaneously
6. **Integration Stability**: Patient and provider platforms can handle dynamic questionnaire updates
7. **Audit Requirements**: Complete audit trail meets regulatory compliance needs
8. **User Training**: Admin users receive adequate training on questionnaire management
9. **Medical Review**: Question content undergoes medical professional review
10. **System Scalability**: Questionnaire management scales with platform growth

## Implementation Notes

### Technical Considerations

- **Real-time Updates**: Questionnaire changes must propagate immediately to patient platform
- **Version Management**: System must handle concurrent questionnaire versions gracefully
- **Data Integrity**: All changes must be atomic and consistent across platforms
- **Performance**: Questionnaire loading must be optimized for mobile devices

### Integration Points

- **Patient Module**: Dynamic questionnaire delivery during inquiry submission
- **Provider Module**: Medical alert generation and display
- **Admin Module**: Centralized questionnaire management interface
- **Audit Module**: Comprehensive change tracking and compliance reporting

### Security Considerations

- **Access Control**: Strict admin-only access to questionnaire management
- **Data Encryption**: All questionnaire data encrypted at rest and in transit
- **Audit Logging**: Comprehensive logging of all questionnaire modifications
- **Compliance**: Healthcare data protection regulations compliance

### Scalability Considerations

- **Question Volume**: System must handle large numbers of questions efficiently
- **Concurrent Users**: Multiple admins must be able to manage questionnaire simultaneously
- **Version Storage**: Efficient storage and retrieval of questionnaire versions
- **Global Deployment**: Questionnaire updates must deploy across all platform instances

---

**Document Status**: ✅ Complete  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes
