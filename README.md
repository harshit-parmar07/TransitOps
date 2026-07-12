# TransitOps: Smart Transport Operations Platform

## Overview
TransitOps is an end-to-end transport operations platform designed to digitize vehicle, driver, dispatch, maintenance, and expense management[cite: 4]. Built as an Odoo custom module, this system eliminates manual logbooks by enforcing strict business rules, automating state transitions, and providing real-time operational insights[cite: 4].

## Core Architecture & Tech Stack
* **Framework:** Odoo 17 (Python / XML)
* **Database:** PostgreSQL
* **Security:** Odoo Native Role-Based Access Control (RBAC)

## Key Features & Mandatory Deliverables

### 1. Fleet & Driver Management
* **Vehicle Registry:** Maintains a master list of vehicles with strictly enforced unique Registration Numbers, load capacities, and acquisition costs[cite: 4].
* **Driver Profiles:** Tracks driver licenses, expiry dates, and safety scores[cite: 4].

### 2. Automated Trip Dispatching
* **Strict Validations:** Trips cannot be dispatched if the cargo weight exceeds the vehicle's maximum capacity[cite: 4]. The system blocks the assignment of 'In Shop' or 'Retired' vehicles, as well as 'Suspended' drivers or drivers with expired licenses[cite: 4].
* **State Machine:** Dispatching a trip automatically transitions the linked driver and vehicle statuses to 'On Trip'[cite: 4]. Completing or cancelling the trip automatically restores them to 'Available'[cite: 4].

### 3. Maintenance & Financial Analytics
* **Maintenance Workflow:** Logging an active maintenance record automatically flags the vehicle as 'In Shop', removing it from the available dispatch pool[cite: 4].
* **Automated Computations:** The system automatically aggregates fuel and maintenance logs to calculate the Total Operational Cost per vehicle[cite: 4]. 
* **Vehicle ROI Tracking:** Implements the core financial formula to calculate return on investment: `(Revenue - (Maintenance + Fuel)) / Acquisition Cost`[cite: 4].

### 4. Role-Based Access Control (RBAC)
The platform enforces strict data access layers for four target user personas[cite: 4]:
1. **Fleet Manager:** Full administrative CRUD access over fleet assets and maintenance lifecycles.
2. **Driver:** Operational access to view assigned trips and update active delivery statuses.
3. **Safety Officer:** Compliance access to monitor safety scores and license validities.
4. **Financial Analyst:** Read-only access to operational expenses, fuel consumption, and ROI metrics.

## Installation & Deployment

1. Clone this repository into your Odoo `custom_addons` directory.
2. Update your `odoo.conf` to include the `custom_addons` path.
3. Restart the Odoo server.
4. Navigate to the Apps menu in Odoo, click "Update Apps List", search for `TransitOps`, and click Install.