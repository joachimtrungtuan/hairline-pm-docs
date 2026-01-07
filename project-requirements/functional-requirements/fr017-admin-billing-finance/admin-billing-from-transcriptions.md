# FR-017 Admin Billing & Finance - Client Requirements Report

## Overview

The client requires comprehensive billing and finance management capabilities across three main areas: provider payments, patient billing, and affiliate payments.

## Provider Billing

- **Payment Scheduling**: Support weekly or monthly payment cycles with clear visibility of who needs payment on scheduled dates
- **Payment Confirmation**: Ability to confirm payment amounts and methods, with automatic notifications to providers
- **Internal Notes**: Add administrative notes (e.g., payment routing changes, bank account switches) separate from provider-facing information

## Patient Billing

- **Invoice Management**: View invoice numbers, amounts due, payment status (pending/paid), with ability to download invoices and send payment reminders
- **Split Payment Plans**: Interest-free installment system where patients can split costs over multiple months (2-9 months) based on time until treatment. Maximum installments calculated from quote date until 30 days before procedure. System must track partial payments and outstanding balances across multiple invoices per patient
- **Payment Tracking**: Display amount paid vs. outstanding balance clearly

## Affiliate Billing

- **Monthly Payments**: Affiliates paid monthly (typically on 7th of following month for previous month's activity)
- **Status Management**: Separate "pending" and "paid" sections to avoid confusion
- **Discount Code Tracking**: Track applied vs. completed discounts (applied at checkout vs. completed purchase)

## Billing Settings

- **Stripe Account Management**: Support multiple Stripe accounts for different countries/companies/currencies, with country/region assignment per account
- **Currency Conversion**: Automatic conversion rate API integration (e.g., xe.com) with ability to add percentage buffer (e.g., 5-10%) to cover bank conversion fees and currency fluctuations
- **Split Pay Configuration**: Configure installment options (2-9 months) with 30-day cutoff requirement (full payment must be completed 30 days before treatment)

## Key Requirements

- Clear separation between pending and paid transactions
- Proper discount breakdown display (Hairline fees only vs. both fees)
- Support for multiple invoices per patient due to split payments
- Manual override capabilities for currency conversion during rapid fluctuations
