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
