
# Evaluation Report

This document outlines the evaluation of the Multi-Source AI Copilot, focusing on its accuracy and performance.

## 1. Overview

The goal of this evaluation is to assess the copilot's ability to correctly route queries, generate accurate responses, and meet the performance requirement of end-to-end latency under 5 seconds for typical queries.

## 2. Test Suite

A suite of 20 sample questions was used for testing, categorized by the expected data source:

### SQL Queries (10)

1.  What were the total sales for Q1 2024?
2.  Show me the top 5 selling products.
3.  Who are the top 3 customers by total spending?
4.  What is the average order value?
5.  How many orders were placed in the last month?
6.  List all products in the 'Bikes' category.
7.  What is the total revenue per year?
8.  Show the sales trend over the last 12 months.
9.  Which territory had the highest sales?
10. What is the total number of customers?

### RAG Queries (5)

*(Assuming a policy document about remote work is uploaded)*

1.  What is the company's policy on remote work?
2.  Can employees work from a different country?
3.  What are the requirements for a home office setup?
4.  Summarize the section on communication expectations.
5.  Who is eligible for the remote work program?

### CSV Queries (5)

*(Assuming a pricing CSV file is uploaded)*

1.  What is the price of product 'X'?
2.  List all products with a price greater than $100.
3.  What is the cheapest product in the 'Accessories' category?
4.  Show me the details of product with SKU 'ABC-123'.
5.  What is the average price of all products?

## 3. Methodology

-   The application was run locally in a development environment.
-   Each query from the test suite was sent to the `/api/ask` endpoint.
-   The accuracy of the response was manually verified.
-   The end-to-end latency was measured from the time the request was sent to the time the response was received.

## 4. Results

### Accuracy

| Query ID | Query | Expected Source | Actual Source | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- |
| SQL-1 | What were the total sales for Q1 2024? | SQL | | |
| ... | ... | ... | ... | ... |
| RAG-1 | What is the company's policy on remote work? | RAG | | |
| ... | ... | ... | ... | ... |
| CSV-1 | What is the price of product 'X'? | CSV | | |
| ... | ... | ... | ... | ... |

**Overall Accuracy:** XX / 20 (XX%)

### Latency

| Query ID | Latency (seconds) |
| :--- | :--- |
| SQL-1 | |
| ... | ... |
| RAG-1 | |
| ... | ... |
| CSV-1 | |
| ... | ... |

**Average Latency:** X.XX seconds

## 5. Analysis

*(Provide a discussion of the results here.)*

-   Which queries failed and why?
-   Were there any routing errors?
-   How was the performance? Were there any queries that exceeded the 5-second latency target?
-   What are the potential areas for improvement?

