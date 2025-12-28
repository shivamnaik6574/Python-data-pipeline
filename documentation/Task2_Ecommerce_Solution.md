TASK 2 EXPLANATION: E-COMMERCE SALES ANALYTICS

File Content = Given sales records in "orders.csv". So need to calculate revenue, find best-selling products, and check if the company is growing year over year.

Command to run SCRIPT : python task2_analysis.py

STEP INVOLVED IN CALCULATION

1. Ingestion
- Reads the "orders.csv" file.
- Fixes Data : It converts the dates into Date objects so the computer can understand years and months.
- Fixes Numbers : Ensures "Sales" values are treated as numbers, not text.
- Saves the clean data into the MongoDB database.

2. Analysis Logic
We use MongoDB's "Aggregation Framework" to answer the business questions.
- Grouping : This is like a Pivot Table in Excel. We group data by Product ID or Month.
- Sum : add up the Sales column for each group.

3. Specific Insights Calculated
- Top 5 Products : The sum sales for every product and pick the top 5 highest earners.
- Monthly Revenue : Calculate how much money was made in every single month from 2015 to 2018.
- Yearly Growth : Calculate the total for each year and compare it to the previous year to find the percentage growth.


KEY RESULTS :

- Best Seller : The product "TEC-CO-10004722" is the number 1 item with over $61,000 in sales.

-  Growth Trend :
  > 2016 was a slow year (sales dropped by 4%).
  > 2017 was a massive recovery (sales grew by 30%).
  > 2018 continued to see strong growth (up 20%).
