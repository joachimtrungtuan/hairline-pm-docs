# RBAC Requirements from Client Transcriptions

**Extracted from**: Transcription files in `local-docs/project-requirements/transcriptions/`  
**Date**: 2025-12-27  
**Purpose**: Systematic extraction of client's specific statements about RBAC (Role-Based Access Control)

---

## 1. Admin Platform RBAC Requirements

### Source: Hairline-AdminPlatformPart2.txt (Lines 441-458)

**Key Statement:**
> "And then this is what I was saying to you before about user permissions. We need to be able to have user permission for us, but also the provider needs to have that as well."

### Specific Requirements for Admin Platform

1. **User Permissions System**
   - Admin platform needs user permission management
   - Provider platform also needs user permission management (separate but similar system)

2. **Role-Based Access**
   - Admin users will have "different functions" based on their role
   - Not all admin users should have access to all features

3. **Aftercare Specialist Role (Example)**
   - Specific role for users who "don't do anything except aftercare"
   - These users are "nurses or whatever"
   - **Access Permissions for Aftercare Specialists:**
     - Overview of aftercare
     - Support functionality
     - Their own settings to change their profile
     - Ability to add pictures
   - This should be a "separate category"

4. **Role Management System**
   - Need ability to "Add roles and be able to manage the different permissions and so on"
   - System "needs to be a little bit more complicated than this" (referring to basic implementation)

### Client's Direct Quote
>
> "So the idea is, you know, admin to, you know, like all of this stuff, they will have different functions. There'll also be users, for example, for aftercare. So there'll be people that don't do anything except aftercare, there'll be nurses or whatever. So all they have is they'll have the, you know, the overview of aftercare, they'll have the support, they'll have their own settings to change their profile and add pictures and all that stuff. So that will be a separate category, for example. Add roles and be able to manage the different permissions and so on. Again, it needs to be a little bit more complicated than this, but anyway."

---

## 2. Provider Platform RBAC Requirements

### Source: Hairline-ProviderPlatformPart2.txt (Lines 46-59)

**Key Statement:**
> "This is the team, so they need to be able to invite staff. And currently we have, you know, two, there really should be three different ones, which is front of staff."

### Specific Requirements for Provider Platform

1. **Staff Invitation System**
   - Providers need ability to invite staff members
   - Originally described in transcription as \"two, there really should be three\" staff types
   - Normalized here to the **four canonical roles defined in FR-009**: Owner, Manager, Clinical Staff, Billing Staff

2. **Provider Role Model (aligned with FR-009):**
   - **Owner (Main Account Holder)**  
     - Single primary account per provider organization  
     - Responsible for bank details and payouts, contract acceptance, and high-risk configuration  
   - **Manager (Clinic Manager / Operations / Front-of-staff)**  
     - Operational lead and \"front-of-staff\" representative mentioned in the transcription  
     - Can see and manage the full patient journey in the provider portal (inquiries, quotes, schedules, day-to-day operations)  
   - **Clinical Staff**  
     - \"Just perform procedures\" and aftercare (surgeons, clinicians, nurses)  
     - Focused on in-progress and aftercare sections, treatment documentation, scans, and medical notes  
     - Limited or no access to billing or sensitive configuration  
     - Need to: take pictures, perform 3D scans, update treatment stage, provide aftercare  
   - **Billing Staff**  
     - Finance-oriented staff who \"go through the quotes and see how much they're making\"  
     - Can view and reconcile financial information but cannot alter clinical records or manage team structure/ownership

3. **Permission-Based Access Control**
   - System should control "which staff member can see which part"
   - "Permissions, who can do what page"
   - When inviting a staff member, should be able to "select which pages they can see"

### Client's Direct Quote
>
> "But the idea is, it's permissions, really, so which staff member can see which part. So for example, there should be a clinical staff. So those, for example, will probably not be looking at quotes or confirmations or anything. But they might be just looking at the in progress and aftercare section, for example. And that's because they just perform procedures, for example. So they need to take pictures, 3D scans of the procedure. They need to input that they've gone from here to here or provide aftercare and so on. And then there'll be billing staff, you know, that will be able to go through the quotes and see how much they're making and all of this stuff. So we just need to figure out, you know, permissions, who can do what page. But in reality, it's, you know, like once you invite a staff member, you should be able to select which pages they can see and so on."

---

## 3. Key Principles Extracted

### 3.1 Role-Based Access

- Different users should have different functions/access based on their role
- Not everyone should see everything
- Access should be granular (page-level control mentioned)

### 3.2 Role Categories

**Admin Platform:**

- Full admin (all functions)
- Aftercare specialist (limited to aftercare, support, profile settings)

**Provider Platform:**

- Owner (main account holder; payouts, contracts, high-risk configuration)
- Manager (clinic manager / operations / front-of-staff; full journey operations)
- Clinical Staff (in-progress and aftercare only; procedures, scans, medical notes)
- Billing Staff (quotes and financial information)

### 3.3 Permission Management

- System should allow adding roles
- System should allow managing different permissions
- When inviting users/staff, should be able to select which pages/sections they can access
- System needs to be "more complicated" than basic - implying granular control needed

### 3.4 Separation of Concerns

- Admin platform RBAC is separate from Provider platform RBAC
- Each platform needs its own permission system
- Provider platform team management is separate (mentioned in context)

---

## 4. Implementation Notes from Client

1. **Complexity Requirement:**
   - Client explicitly states: "Again, it needs to be a little bit more complicated than this, but anyway."
   - This suggests the system needs more sophistication than a simple role-based system

2. **Page-Level Control:**
   - Client mentions "who can do what page" and "select which pages they can see"
   - This suggests granular, page-level or feature-level permissions, not just role-based

3. **Work in Progress:**
   - Client mentions "this is something that we need to work on" for provider staff permissions
   - Indicates this is an area requiring further definition

---

## 5. Missing/Unclear Areas

The transcriptions do not explicitly mention:

- Super admin role (though implied by "admin to, you know, like all of this stuff")
- Permission inheritance or hierarchies
- Time-based or conditional permissions
- Audit logging requirements for permission changes (though this may be implied by security needs)
- Specific permission names or detailed permission matrix
- How roles relate to specific features/modules beyond the examples given

---

## 6. Summary

The client has provided clear direction on RBAC requirements:

1. **Both platforms need RBAC** (Admin and Provider)
2. **Role-based with granular permissions** (page/feature level)
3. **Specific role examples provided:**
   - Admin: Aftercare specialists
   - Provider: Owner, Manager, Clinical Staff, Billing Staff (per FR-009, mapping \"front of staff\" concept to Manager/operations)
4. **System should allow:**
   - Adding roles
   - Managing permissions
   - Selecting page access when inviting users
5. **System needs to be sophisticated** - more than basic role assignment

The client's statements are consistent and provide a clear foundation for implementing RBAC, though some details (like specific permission names, full permission matrix) would need to be defined during implementation.
