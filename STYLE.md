# AI Collaboration Rules

## Development Workflow

Before generating code:

1. Ask for the relevant file when modifications are required.
2. Read the existing implementation first.
3. Explain where the logic belongs:

   * Router
   * Service
   * Repository
   * Schema
   * Dependency
   * Utility
4. Explain why the change belongs there.
5. Reuse existing code whenever possible.
6. Extend existing implementations before creating new files.
7. Do not generate duplicate business logic.

---

## Teaching Style

The goal is not only to complete the project but also to improve the developer's skills.

When introducing new concepts:

1. Briefly explain the reasoning.
2. Explain why a design decision was chosen.
3. Explain tradeoffs when relevant.
4. Keep explanations concise unless more detail is requested.
5. Prefer practical examples over theory.

---

## Code Review Behavior

When reviewing code:

1. Identify architectural issues.
2. Identify responsibility violations.
3. Identify duplicated logic.
4. Identify naming inconsistencies.
5. Suggest improvements that align with the project's architecture.
6. Do not rewrite large sections unless necessary.

---

## Response Format

For implementation requests:

### Step 1: Analysis

* Determine the architectural layer involved.
* Check if existing code can be reused.
* Identify required files.

### Step 2: Plan

* Explain the proposed implementation.
* Explain what files will be modified.

### Step 3: Code

* Generate only the required changes.

### Step 4: Explanation

* Explain what was added.
* Explain why it was added.
* Mention any future considerations.

---

## Project Awareness

Always remember that ShareBridge is:

* A location-based donation platform.
* A volunteer delivery coordination platform.
* A social media platform.
* A direct messaging platform.
* A reputation and rating platform.

When implementing features, consider how they interact with:

* Users
* Donations
* Deliveries
* Messaging
* Notifications
* Ratings
* Location tracking
* Social feed features

Avoid building features in isolation when they logically affect other areas of the system.

---

## Existing Developer Preferences

The developer prefers:

* Enterprise-style architecture.
* FastAPI.
* SQLAlchemy Async.
* PostgreSQL.
* Docker-based development.
* Readable code over short code.
* Explicit names over abbreviations.
* Step-by-step guidance.
* Understanding the code rather than blindly copying it.

The objective is to build production-quality software while helping the developer learn professional backend engineering practices.
