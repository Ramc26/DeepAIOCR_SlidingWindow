"""Synthetic multi-page procurement bundle for manual end-to-end testing.

No real company, person, bank account, or transaction is represented here.
"""

page_texts = [
    """TRANSMITTAL NOTE

From: Procurement Operations
To: Accounts Payable, Northwind Manufacturing Pvt. Ltd.
Date: 14 October 2026
Subject: Supplier documentation for October procurement cycle

Please find attached the documentation received from ACME Industrial Supplies
relating to the September and October procurement cycle. The package includes
a supplier invoice, a purchase order with supporting line-item details, an
executed services agreement, and schedules referenced by that agreement.

Accounts Payable should verify invoice references against the purchase order
and goods receipt before scheduling payment. Legal Operations has completed
an initial review of the agreement. Any discrepancy in the final signed pages
should be reported to the procurement manager.

This message is for internal routing only. It does not authorize payment,
amend any contractual obligation, or replace the original documents.
Reference: PROC-BUNDLE-2026-104""",

    """ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED
TAX INVOICE

Invoice Number: ACME/INV/2026/1042
Invoice Date: 30 September 2026
Purchase Order Reference: PO-NWM-2026-0871
Customer Account: NW-00918

BILL TO:
Northwind Manufacturing Private Limited
Plot 18, Industrial Growth Centre, Hyderabad, Telangana 500081
GSTIN: 36AABCN1234F1Z7

SHIP TO:
Northwind Manufacturing - Component Assembly Unit
Patancheru, Telangana 502319

Supplier GSTIN: 36AACCA5678L1Z2
Payment Terms: Net 30 days from invoice date
Due Date: 30 October 2026

Industrial fastening components were supplied against the purchase order.
Quantities and unit prices appear in the continuation of this invoice.
Delivery Challan: DC-ACME-29814
Delivery Date: 28 September 2026
Goods Receipt Note: GRN-NWM-55216

Authorized Supplier Representative: Accounts and Commercial Department""",

    """ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED
Invoice No.: ACME/INV/2026/1042
Continuation of line-item details

Item Code     Description                    Qty       Unit Price
FAST-M10      Stainless steel fasteners      200          125.00
BOLT-M12      Hexagonal industrial bolts     150          180.00
WASH-M12      Stainless steel washers        500           12.00
NUT-M12       Lock nuts                      300           28.00

FAST-M10 specification: SS304, M10 thread. Batch B-SS304-0926.
Inspection certificate: QC-ACME-1837.
BOLT-M12 specification: Grade 8.8, corrosion-resistant finish.
Inspection certificate: QC-ACME-1841.

Washers and nuts were packed in sealed containers. Lot numbers are recorded
on the delivery challan. Quantities shown represent quantities accepted in
the receiving record available at the time of invoicing.

The invoice number and purchase order reference are unchanged. This page
continues the same billed supply; it is not a separate order.""",

    """ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED
Invoice No.: ACME/INV/2026/1042
Commercial summary and payment instructions

Taxable value for FAST-M10: INR 25,000.00
Taxable value for BOLT-M12: INR 27,000.00
Taxable value for WASH-M12: INR 6,000.00
Taxable value for NUT-M12: INR 8,400.00

Total Taxable Amount: INR 66,400.00
CGST @ 9%: INR 5,976.00
SGST @ 9%: INR 5,976.00
TOTAL INVOICE VALUE: INR 78,352.00
Amount in words: Rupees Seventy-Eight Thousand Three Hundred Fifty-Two Only.

Please remit payment to the supplier using the bank details shown on the
original invoice. The payment reference should include invoice number
ACME/INV/2026/1042. Any short payment, tax deduction, or dispute must be
communicated to the supplier's receivables team with supporting detail.

This page concludes the invoice for the delivery referenced above.
Authorized Signatory, ACME Industrial Supplies Private Limited""",

    """NORTHWIND MANUFACTURING PRIVATE LIMITED
PURCHASE ORDER

Purchase Order Number: PO-NWM-2026-0871
Order Date: 12 September 2026
Revision: 0
Purchasing Department: Direct Materials
Buyer: K. Raghavan

SUPPLIER: ACME Industrial Supplies Private Limited, Hyderabad, Telangana
Supplier Code: SUP-00184
Delivery Location: Northwind Manufacturing - Component Assembly Unit,
Patancheru, Telangana 502319
Requested Delivery Date: 28 September 2026
Currency: INR
Payment Terms: Net 30 days after receipt of a valid invoice

The supplier is instructed to provide industrial fastening components in
accordance with the quantities, technical specifications, and inspection
requirements set out in this order. All shipments must include the purchase
order number on the delivery challan and outer packaging.

The receiving department will compare delivered quantities against the order
before issuing a goods receipt note. No substitutions or specification
changes are permitted without written approval from the authorized buyer.
The detailed item quantities continue on the following page.""",

    """PURCHASE ORDER: PO-NWM-2026-0871
Continuation - material schedule

Line  Item Code  Description                    Quantity   Unit Price
10    FAST-M10   SS304 fasteners                    200        125.00
20    BOLT-M12   Hexagonal industrial bolts         150        180.00
30    WASH-M12   Stainless steel washers            500         12.00
40    NUT-M12    Lock nuts                          300         28.00

Expected goods value: INR 66,400.00 before applicable taxes.

Inspection requirements:
1. Each item must match the approved technical specification.
2. Materials must be free from visible corrosion and transit damage.
3. Supplier batch identification must remain traceable through delivery.
4. Inspection certificates must be available on request.

The receiving team must record shortages or nonconforming materials against
the relevant order line. Accounts Payable will compare this purchase order
with the goods receipt and supplier invoice. Differences must be resolved
with the purchasing department before payment.

The purchase order number, supplier, and conditions match the prior page.
End of purchase order line schedule.""",

    """MASTER SERVICES AGREEMENT
Agreement Reference: MSA-NWM-ACME-2026-014
Effective Date: 1 October 2026

PARTIES
This Master Services Agreement is entered into by Northwind Manufacturing
Private Limited, referred to as the Customer, and ACME Industrial Supplies
Private Limited, referred to as the Supplier.

PURPOSE
The parties establish general commercial and operational terms governing
the supply of industrial materials and related support services ordered by
the Customer from time to time.

1. DEFINITIONS
"Confidential Information" means non-public commercial, operational,
financial, technical, or business information disclosed in connection with
this Agreement.

"Purchase Order" means a written purchasing instruction issued by the
Customer and accepted under the agreed ordering process.

"Deliverables" means materials, documentation, reports, and other outputs
the Supplier must provide under an accepted Purchase Order.

2. CONTRACT DOCUMENTS
This Agreement must be read with valid Purchase Orders and schedules expressly
incorporated into it. The agreed order-of-precedence and amendment rules apply
if the documents conflict. This is an ongoing contract, not an invoice.""",

    """3. DELIVERY AND ACCEPTANCE
The Supplier shall deliver materials at the agreed location and by the date
stated in the applicable Purchase Order. Delivery dates are material to
production planning and shall not change without written agreement.

The Customer may inspect materials on delivery. Acceptance does not waive a
claim for a defect that could not reasonably have been discovered during the
initial receiving inspection.

4. QUALITY AND NONCONFORMITY
Materials must comply with applicable specifications, approved samples, and
quality requirements. The Supplier shall investigate written notices and
provide a corrective-action plan. Subject to the order terms, the Customer
may reject nonconforming materials, request replacement, or agree another
recorded resolution.

5. FEES AND PAYMENT
The Customer shall pay undisputed amounts according to the applicable order.
A valid invoice must identify the Purchase Order and contain enough detail to
reconcile billed materials with accepted deliveries. The Customer shall
notify the Supplier of disputed amounts and the basis for the dispute.

6. CONFIDENTIALITY
Each party shall protect the other's non-public information using reasonable
safeguards and use it only for the business relationship, subject to law.
These obligations survive termination for the period specified in the
Agreement. This page continues the terms begun on the preceding page.""",

    """7. TERM AND TERMINATION
This Agreement begins on the Effective Date and continues for an initial term
of two years unless terminated earlier under this section. Either party may
terminate for a material breach that remains uncured thirty days after written
notice specifying the breach and corrective action reasonably required.

Termination does not automatically cancel an accepted Purchase Order. The
parties shall determine treatment of open orders, completed deliveries,
outstanding payment obligations, and confidential material under the contract.

8. LIABILITY AND INDEMNITY
Each party is responsible for its obligations. Exclusions, limits, and
indemnity obligations are subject to the conditions and exceptions stated in
the executed Agreement.

9. GOVERNING LAW AND DISPUTES
The parties shall first attempt resolution through their designated commercial
representatives. If unresolved, either party may use the agreed dispute process.

10. GENERAL
Any amendment must be in writing and signed by authorized representatives.
Failure to enforce a provision once does not automatically waive future rights.
Notices must be sent to authorized contacts maintained by the parties.

The execution page and incorporated schedules form part of the agreement
package. The provisions on this page continue the same contract.""",

    """EXECUTION PAGE
Master Services Agreement - MSA-NWM-ACME-2026-014

The parties confirm that their authorized representatives have read and
agreed to the Master Services Agreement.

FOR NORTHWIND MANUFACTURING PRIVATE LIMITED
Name: S. Ananya Rao
Title: Head of Procurement
Signature: Ananya Rao
Date: 28 September 2026
Company stamp: NORTHWIND MANUFACTURING PRIVATE LIMITED

FOR ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED
Name: R. Mahesh Kumar
Title: Director - Commercial
Signature: R. Mahesh Kumar
Date: 29 September 2026
Company stamp: ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED

Witness 1: D. Suresh - Signature recorded
Witness 2: P. Lakshmi - Signature recorded

Each signatory represents that they have authority to execute the Agreement.
Schedules marked as appendices are referenced by and incorporated into the
Agreement to the extent specified in its terms.""",

    """APPENDIX A - COMMERCIAL RATE SCHEDULE
Reference Agreement: MSA-NWM-ACME-2026-014
Schedule Version: 1.0; Effective From: 1 October 2026

This schedule records agreed commercial rates for materials and services
covered by the Master Services Agreement. It must be read with the applicable
Purchase Order and does not independently authorize a purchase or guarantee
minimum order quantities.

Item Code   Description                 Unit        Rate (INR)
FAST-M10    SS304 fasteners              Each          125.00
BOLT-M12    Industrial bolts             Each          180.00
WASH-M12    Stainless washers            Each           12.00
NUT-M12     Lock nuts                    Each           28.00
QC-INSPECT  Additional inspection        Hour        1,200.00
PACK-EXPORT Export-grade packing         Lot         4,500.00

Rates exclude applicable taxes unless a Purchase Order says otherwise.
Freight and special handling charges require written approval before shipment.
No charge may be added merely because a shipment is split unless approved.
Price changes require written approval from both parties.

Approved by Customer Procurement Representative and Supplier Commercial
Representative. This schedule supplements the executed agreement.""",

    """APPENDIX B - SERVICE LEVEL AND QUALITY REQUIREMENTS
Reference Agreement: MSA-NWM-ACME-2026-014
Schedule Version: 1.0

1. DELIVERY PERFORMANCE
The Supplier shall target at least 98 percent on-time delivery across accepted
Purchase Orders measured each calendar quarter. An order is on time when its
complete quantity arrives by the confirmed delivery date unless an exception
is agreed in writing.

2. DEFECT MANAGEMENT
Critical defects affecting safety, fit, or production use must be reported
promptly. The Supplier shall acknowledge a critical notice within one business
day and provide an initial containment plan within two business days.

3. DOCUMENTATION
Shipments must include the delivery challan, packing details, batch or lot
identification, and inspection certificates required by the Purchase Order.

4. CORRECTIVE ACTION
For recurring confirmed defects, the Supplier shall provide a root-cause
analysis and corrective-action plan. The parties may review effectiveness.

5. PERFORMANCE REVIEW
Delivery, defect rates, document completeness, and resolution time may be
reviewed quarterly. If this schedule conflicts with the Agreement, its agreed
order-of-precedence provisions govern.""",

    """INTERNAL DOCUMENT ROUTING SHEET
Department: Finance Operations
Routing Reference: FIN-ROUTE-2026-441
Received: 14 October 2026

Package received from Procurement Operations. Initial indexing has been
completed. It appears to contain supplier documentation for several business
purposes.

Required actions:
- Accounts Payable: verify invoice arithmetic and purchase-order matching.
- Procurement: verify quantity and delivery acceptance references.
- Legal Operations: retain the signed agreement and incorporated schedules.
- Records Management: verify legibility and index order before archival.

This routing sheet is an internal administrative record. It is not a purchase
order, tax invoice, contract, or incorporated commercial schedule.

Reviewer note: the invoice reference appears to match the September delivery
record. Confirm the goods receipt before payment approval. Ask Legal Operations
if the signed agreement copy differs from the approved version.

Status: Pending final reconciliation; assigned group: Finance Operations.""",

    """ACME INDUSTRIAL SUPPLIES PRIVATE LIMITED
TAX INVOICE

Invoice Number: ACME/INV/2026/1108
Invoice Date: 15 October 2026
Customer: Northwind Manufacturing Private Limited
Customer Code: NW-00918
Purchase Order Reference: PO-NWM-2026-0912

Description: Emergency replacement components supplied under the referenced
purchase order following the Customer's written request dated 9 October 2026.

Item Code: SEAL-KIT-22
Description: Industrial pump seal replacement kit
Quantity: 12 kits
Unit Price: INR 2,450.00
Taxable Value: INR 29,400.00
CGST @ 9%: INR 2,646.00
SGST @ 9%: INR 2,646.00
TOTAL INVOICE AMOUNT: INR 34,692.00
Amount in Words: Rupees Thirty-Four Thousand Six Hundred Ninety-Two Only.

Delivery Challan: DC-ACME-30119
Goods Receipt: GRN-NWM-55703
Payment Terms: Net 30 days
Due Date: 14 November 2026

Please quote invoice ACME/INV/2026/1108 when making payment or raising a query.
Authorized Signatory, ACME Industrial Supplies Private Limited.""",

    """EMAIL CORRESPONDENCE - PAYMENT QUERY
From: accounts.payable@northwind.example
To: receivables@acme.example
Date: 16 October 2026
Subject: Clarification required - invoice ACME/INV/2026/1042

Dear Accounts Team,
Our preliminary review identifies a possible difference between the invoice
amount and the amount entered in our payment proposal. Please confirm that the
taxable value and tax calculations are correct and provide the delivery record
if available. We have not rejected the invoice; the proposal is on hold until
the usual three-way match is complete.

Forwarded supplier response:
We confirm invoice ACME/INV/2026/1042 was issued against PO-NWM-2026-0871 and
goods receipt GRN-NWM-55216. The invoice summary shows taxable value and tax
separately. Please identify the field that does not match your records so that
we can investigate.

This correspondence records a query and response. It does not revise the
invoice, amend the purchase order, or change the agreement.""",

    """SCANNED ATTACHMENT - RECEIVING DEPARTMENT NOTES
Reference written on the top margin: GRN-NWM-55216 / ACME / September shipment

Receiving inspection summary:
Outer packaging was intact on delivery. Quantities were counted against the
delivery challan. The receiving officer recorded no shortage for FAST-M10 or
BOLT-M12. One carton containing washers was moved to the quality inspection
area because the printed batch label was partly obscured. The batch number was
subsequently verified against the supplier's inspection certificate.

Handwritten note:
"Please retain the original lot label with the goods receipt file. Finance may
proceed after normal document checks are complete."

Received by: Materials Receiving Team
Date stamp: 28 SEP 2026
Initials: S.R.

The bottom portion of the scan contains a partial stamp and photocopy shadow.
No invoice total, ordering instruction, contractual clause, or incorporated
schedule appears on this page. Image quality is low, but the reference numbers
remain readable.""",
]

expected_labels = [
    "Other",
    "Invoice",
    "Invoice",
    "Invoice",
    "Purchase Order",
    "Purchase Order",
    "Contract",
    "Contract",
    "Contract",
    "Contract",
    "Appendix",
    "Appendix",
    "Other",
    "Invoice",
    "Other",
    "Other",
]
