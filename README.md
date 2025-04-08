## ⚠️ Archived Version of FastBidder

This project is no longer under active development.  
It has been replaced by a new, rethought version available here:  
➡️ [FastBidder v2 (Active Development)] (soon on github)

---

### 🧠 Why?

After working on this version, I took a step back to carefully evaluate the structure, architecture, and overall direction of the project.  
Based on that, I decided to start fresh — with a clearer design, improved modularity, and better scalability in mind.

This repository remains public for reference purposes, as part of my learning journey and development process.

---

*Thank you for checking out my work — feel free to explore the new version!*

---
---


# FastBidderApplication
(early stage of application - developing mostly for learning purpose)

In the construction industry, preparing a bid is a simple, yet time-consuming task, where it mainly involves comparing descriptions of works to be done in different excel files.

Fast Bidder's task is to semantically compare offer descriptions with the company's catalog prices. Based on the match between descriptions, a unit price is entered. By comparing hundreds or even thousands of cells, the automation of this process saves a lot of time and money.


## Functionality

-**Uploading excel files**

-**Data validation**

-**Excel files processing**

-**Matching excel descriptions:** For now, RapidFuzz library is used, more advances tools will be added in the future (Scikit-learn / SpaCy / AI API)

--- More comming soon ---

## TODO in close future

- changing descriptions from polish to english, improving doc-strings

- adding boundary condition validation, error protection, edge-case scenario testing (for now, happy path is implemented )


## Technologies

-**Backend**: Django, Django REST Framework


-**Database**: SQLite(default)

-**Authentication**: Token Authentication

-**Other**: Pagination, filtering, sorting
