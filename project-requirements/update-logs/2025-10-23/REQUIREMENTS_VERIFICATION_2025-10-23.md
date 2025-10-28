# Requirements Verification Report - October 23, 2025

## Executive Summary

Comprehensive review of system documentation against original transcriptions to verify accuracy and identify gaps or unclear requirements.

**Status**: ⚠️ 5 Critical Issues Identified

---

## Issues Identified

### 1. ⚠️ UNCLEAR: Patient-Provider Chat/Negotiation

**Current Documentation**:

- FR-012 includes patient-provider messaging for "quote negotiation"
- Listed as a core communication channel

**Transcription Evidence**:

```sh
Source: HairlineApp-Part1.txt (Lines 138-140)
"I did want them to have the option of speaking directly to the provider 
for questions, but I'm not sure at the end if that's what we decided or not."
```

**Issue**:

- Transcription shows **UNCERTAINTY** about whether patient-provider direct chat was included in final scope
- Documentation treats it as confirmed feature

**Recommendation**:

- ⚠️ **CLARIFY WITH STAKEHOLDERS** whether patient-provider direct messaging is in scope
- If NOT in scope: Remove from FR-012, update communication channels to only include:
  - Patient ↔ Hairline Support (confirmed)
  - Patient ↔ Aftercare Team (confirmed)
  - Provider ↔ Hairline Admin (confirmed)

---

### 2. ❌ OUT OF SCOPE: Provider Onboarding Flow

**Current Documentation**:

- FR-015 states "Admins MUST be able to onboard new providers"
- Implies admin-initiated onboarding process

**Transcription Evidence**:

```sh
Source: Hairline-AdminPlatform-Part1.txt (Lines 75-86)
"you'll be able to add a new provider... you'll be able to edit them, 
you'll be able to see all the details... insurance, license, different 
things that we will be able to add to keep on record"
```

**Issue**:

- Documentation correctly reflects that **ADMIN adds providers** (not provider self-registration)
- However, FR-015 title "Provider Onboarding & Verification" suggests provider-initiated flow
- **NO self-service provider registration** is mentioned in transcriptions

**Recommendation**:

- ✅ **CORRECT**: FR-015 should be retitled to **"Provider Management (Admin-Initiated)"**
- Clarify that providers do NOT self-register - admin creates provider accounts
- Remove any implication of "onboarding flow" (implies multi-step provider-initiated process)
- Update to: Admin creates provider account → Admin adds credentials/licenses → Admin activates provider

---

### 3. ❌ NOT MENTIONED: Escrow Account Management

**Current Documentation**:

- No explicit mention of escrow accounts
- Payment flow shows: Patient pays → Platform holds → Provider payout after completion

**Transcription Evidence**:

- **ZERO mentions** of "escrow" or "escrow account" in any transcription file
- Payment split mentioned (platform commission vs provider payout)
- No explicit mention of funds being held in escrow

**Issue**:

- Documentation doesn't explicitly state how funds are held between payment and payout
- Unclear if this is Stripe Connect escrow, platform bank account, or other mechanism

**Recommendation**:

- ⚠️ **CLARIFY WITH STAKEHOLDERS** on payment holding mechanism:
  - Option A: Stripe Connect with escrow (automatic escrow via Stripe)
  - Option B: Platform bank account (manual transfers)
  - Option C: Instant payout (no holding period)
- Add explicit section to FR-007 "Payment Processing & Escrow Management" with:
  - How funds are held
  - When provider payout is triggered
  - Refund handling from held funds

---

### 4. ⚠️ INCOMPLETE: FR-011 Aftercare Management

**Current Documentation**:

- FR-011 lists basic aftercare features
- Missing several critical requirements from transcriptions

**Transcription Evidence**:

#### A) Provider Aftercare Template Selection

```sh
Source: Hairline-ProviderPlatformPart1.txt (Lines 348-354)
"Providers are going to be able to add their own aftercare setup. 
But really, we're going to do it from templates. So we're going to 
do a few templates... the idea is just to select from a template 
and it'll fill out all the details."
```

**Missing**: Provider MUST select aftercare template during treatment completion setup

---

#### B) Aftercare Setup Process (Instructions & Medications)

```sh
Source: Hairline-ProviderPlatformPart1.txt (Lines 354, 376-378)
"They can add instructions or medication."
"We can have the instructions from the operating physician, for example, 
and all that stuff. And then we will then provide the aftercares ourselves separately."
```

**Missing**:

- Provider adds post-op instructions to aftercare template
- Provider specifies medications for patient
- System must capture these as part of aftercare setup

---

#### C) Patient 3D Scans During Aftercare

```sh
Source: Hairline-AdminPlatformPart2.txt (Lines 297-304)
"So this is the head scan part. So for each milestone, we ask them to do a 3D scan. 
So, you know, once every five days, you know, repeat three times, you know, 
every five days, for example, and that would finish the milestone once every week, 
month, or whatever it is, for example."
```

**Missing**:

- Patients MUST be prompted to upload 3D head scans at milestone intervals
- Milestones define scan frequency (every 5 days, weekly, monthly, etc.)
- System tracks scan completion as part of milestone progress

---

#### D) Questionnaires During Aftercare

```sh
Source: Hairline-AdminPlatformPart2.txt (Lines 315-329)
"So the questionnaire is, you know, so some milestones will... does it require 
a questionnaire, for example, and then you add which questionnaire is for each 
milestone... pain questionnaire, sleep questionnaire... and it will ask it daily, 
it'll ask it, you know, every week, whatever it is"
```

**Missing**:

- Patients MUST complete questionnaires at milestone intervals
- Questionnaire types: pain, sleep, compliance, etc.
- Frequency: daily, weekly, monthly (defined per milestone)
- System tracks questionnaire completion

---

#### E) Standalone Aftercare Package

```sh
Source: Hairline-AdminPlatformPart2.txt (Lines 258-261)
"Aftercare, we provide as a separate service, as I mentioned. 
So it will be an add-on to the treatment."
```

**Missing**:

- Aftercare is offered as **standalone service** by Hairline (separate from treatment)
- Patients can request aftercare separately (not just bundled with treatment)
- Aftercare pricing: fixed amount OR monthly subscription
- Aftercare is Hairline's service (not provider's)

---

#### F) Admin Assigns Provider for Standalone Aftercare

```sh
Source: Hairline-ProviderPlatformPart1.txt (Lines 369-379)
"Most of the time, our company will be doing the hairline, the aftercare service. 
So we will have agreements with each provider. So some of them will be… we will 
definitely want to be part of that service. And we might pay them extra for that, 
for example. Some of them will not."
```

**Issue**:

- When patient requests standalone aftercare (no prior treatment through Hairline), **who provides the service?**
- Transcription mentions agreements with providers to participate in aftercare service
- Unclear if admin assigns provider OR if Hairline aftercare team handles standalone cases

**Missing**:

- If standalone aftercare is requested, does admin assign a provider?
- OR does Hairline aftercare team handle it without provider involvement?
- Pricing model for standalone aftercare (separate from treatment quote)

**Recommendation**:

- ⚠️ **CLARIFY WITH STAKEHOLDERS** on standalone aftercare workflow:
  - Can patients request aftercare if they had treatment elsewhere?
  - If yes, who provides it? (Hairline team vs assigned provider)
  - How is it priced? (fixed fee vs monthly subscription)

---

## Updated Requirements for FR-011

Based on transcription review, FR-011 should include:

### FR-011: Aftercare Management (Revised)

**Priority**: P1 (MVP)

#### Part A: Treatment-Linked Aftercare

**Requirements**:

- System MUST automatically create aftercare timeline upon treatment completion
- Providers MUST select aftercare template during treatment completion
- Providers MUST be able to add custom instructions to template
- Providers MUST specify post-op medications for patient
- System MUST generate aftercare plan with milestones based on selected template

**Aftercare Templates**:

- Admin creates milestone templates (post-op phase, recovery phase, growth phase, etc.)
- Each milestone defines:
  - Duration (7 days, 30 days, 90 days, etc.)
  - Required 3D scan frequency (daily, every 5 days, weekly, monthly)
  - Required questionnaires (pain, sleep, compliance, etc.)
  - Questionnaire frequency (daily, weekly, monthly)
  - Resources (videos, instructions, best practices)
- Providers select template → system generates complete aftercare plan

---

#### Part B: Patient Aftercare Activities

**3D Scan Requirements**:

- Patients MUST upload 3D head scans at milestone-defined intervals
- System MUST notify patients when scan is due
- System MUST track scan completion progress
- Scans used to monitor hair growth progress

**Questionnaire Requirements**:

- Patients MUST complete questionnaires at milestone-defined intervals
- Questionnaire types:
  - Pain assessment (visual scale)
  - Sleep quality assessment
  - Compliance assessment (following instructions)
  - Activity restrictions check
- System MUST notify patients when questionnaire is due
- System MUST track questionnaire completion

**Medication & Instructions**:

- Patients receive medication schedule from provider
- System sends medication reminders
- Patients can view activity restrictions timeline
- Patients can access milestone-specific resources (videos, guides)

---

#### Part C: Standalone Aftercare Service

**Business Model**:

- Hairline offers aftercare as **standalone service** (separate from treatment)
- Patients can purchase aftercare even if treatment was elsewhere
- Pricing options:
  - Fixed amount (e.g., £500 for 6-month aftercare)
  - Monthly subscription (e.g., £80/month for 6 months)
- Aftercare is Hairline's service (Hairline team provides support)

**Requirements** (⚠️ **NEEDS CLARIFICATION**):

- [ ] Can patients request standalone aftercare if they had treatment at external clinic?
- [ ] If yes, does admin assign a provider to oversee? OR does Hairline aftercare team handle independently?
- [ ] How is standalone aftercare priced? (same as treatment-linked or different pricing?)
- [ ] What information is required from patient? (treatment details, surgeon notes, photos?)

---

#### Part D: Communication & Support

**Requirements**:

- Patients MUST be able to chat with aftercare team (Hairline staff)
- Aftercare specialists can view:
  - Patient's milestone progress
  - Scan history
  - Questionnaire responses
  - Compliance data
- Aftercare specialists can request live video consultation if needed
- System MUST flag urgent cases (high pain, complications) for immediate attention

---

## Summary of Required Changes

### High Priority (Blocking MVP)

| Issue | Action | Files to Update |
|-------|--------|-----------------|
| 1. Patient-Provider Chat | **CLARIFY** if in scope, remove if not | FR-012, system-prd.md |
| 2. Provider Onboarding | **RENAME** to "Admin-Initiated Provider Management" | FR-015, system-prd.md |
| 3. Escrow Management | **ADD** explicit escrow/fund holding section | FR-007, system-prd.md, system-technical-spec.md |
| 4. Aftercare Template Selection | **ADD** to FR-011 | system-prd.md |
| 5. Aftercare 3D Scans | **ADD** to FR-011 | system-prd.md, system-data-schema.md |
| 6. Aftercare Questionnaires | **ADD** to FR-011 | system-prd.md, system-data-schema.md |
| 7. Standalone Aftercare | **ADD** to FR-011 + **CLARIFY** workflow | system-prd.md, system-technical-spec.md |

---

### Medium Priority (Clarification Needed)

| Issue | Question | Stakeholder |
|-------|----------|-------------|
| Standalone Aftercare Assignment | Who provides standalone aftercare? Admin assigns provider OR Hairline team handles? | Product Owner |
| Patient-Provider Chat Scope | Is direct patient-provider messaging in scope or removed? | Product Owner |
| Escrow Mechanism | Stripe Connect escrow, platform bank, or instant payout? | Technical Lead + Finance |

---

## Next Steps

1. **Stakeholder Meeting Required** to clarify:
   - Patient-provider direct messaging (in/out of scope)
   - Standalone aftercare workflow (who provides service)
   - Escrow/payment holding mechanism

2. **Update Documentation** after clarifications:
   - Expand FR-011 with missing aftercare requirements
   - Update FR-015 (provider management, not onboarding)
   - Add escrow section to FR-007
   - Remove/update patient-provider chat in FR-012 if out of scope

3. **Database Schema Updates** for:
   - Aftercare milestone tracking
   - 3D scan uploads during aftercare
   - Questionnaire responses during aftercare
   - Standalone aftercare packages (separate from treatment quotes)

4. **API Specification** for:
   - Aftercare template selection
   - Milestone progress tracking
   - Scan upload during aftercare
   - Questionnaire submission during aftercare

---

## Verification Checklist

- [x] Reviewed all 7 transcription files
- [x] Cross-referenced against system-prd.md
- [x] Identified unclear requirements
- [x] Identified missing requirements
- [x] Identified out-of-scope features
- [ ] **Pending**: Stakeholder clarification meeting
- [ ] **Pending**: Documentation updates after clarification

---

**Report Generated**: October 23, 2025  
**Reviewed By**: System Documentation Team  
**Status**: ⚠️ Pending Stakeholder Clarification
