# MD-Housing
Machine Learning and Neural Networks to determine house prices of houses in the Maryland area.

sold_details.py:
- The BeautifulSoup web scraper that obtains house details from Zillow.com and formats them into a row that appends to the MD Housing.csv file.
- Since Zillow only shows at most 500 houses at a time, the html links are based on different regions of the city to ensure less than 500 houses are shown at a time. A for loop from the first page to the last page (last page's added into the for loop manually).
- Filters include:
1. All Home Types except "Manufactured" and "Lots/Land."
2. "1+" Beds
3. "1+" Bathrooms
4. All houses with prices > 0.
5. Square feet > 500
6. Lot size > 1000

MD House Predicting.ipynb:
The Jupyter Notebook on the ML/DL project.

house_selling.py:
A single Python script on the MD House Predicting.ipynb file without in Notebook snippets.
