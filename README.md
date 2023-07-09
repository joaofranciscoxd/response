# Wikipedia Scrapper

## Description

Wikipedia Scrapper is a Python application that extracts facts from Wikipedia pages and stores them in a database. It uses web scraping techniques to retrieve information from targeted pages and provides functionality for analyzing and processing the extracted data.

## Installation

To install and run the Wikipedia Scrapper, follow these steps:

1. Download the project
2. Navigate to the project directory: `cd wikipedia-scrapper`
3. Create and activate a virtual environment: `python -m venv venv` (Windows) or `python3 -m venv venv` (Mac/Linux) and `source venv/bin/activate`
4. Install the required dependencies: `pip install -r requirements.txt`
5. Configure the database connection in `database.py`
6. Set timezone and time for the first and second scripts
7. Run the application: `python scheduler.py`

## Usage

The Wikipedia Scrapper provides the following functionality:

- Scrap Wikipedia "Did you know..." section to extract facts
- Storing the extracted facts in a database
- Analyzing facts for metadata such as date, length, and relevance
- Retrieving and displaying stored facts based on various filters

To scrape Wikipedia "Did you know..." section and store facts in the database, run the `scheduler.py` script. 

To visualize tables recorded, run the whole workbench.ipynb file.

## Critique

### Self-Critique & Scaling

#### Improvements

Reflecting on the project, here are some areas I would improve if I had more time:

1. **Improve Error Handling:** Implement more robust error handling in order to deal with exceptions and edge cases, providing clear error messages and recovery mechanisms for potential failures.

2. **Optimization and Efficiency:** Identify potential performance bottlenecks and optimize critical sections of the code for improved efficiency, especially when scaling the project to handle larger volumes of data or increased frequency of execution.

3. **Improve Test Coverage:** Expand the test suite to cover more scenarios and edge cases, ensuring comprehensive test coverage to validate the functionality and reliability of the codebase.

4. **Improved Logging and Monitoring:** Implement a robust logging and monitoring system to capture and track important events, errors, and performance metrics, enabling better visibility and troubleshooting capabilities.

#### Scaling

If this project were to scale, several areas would likely face challenges first:

1. **Web Scraping Performance:** As the number of targeted pages and languages increase, the web scraping process may become slower and more resource-intensive. Implementing strategies such as asynchronous processing, distributed scraping can help improve performance.

2. **Database Scalability:** With a larger volume of data, the database may experience scalability issues. Sharding, replication, or employing distributed databases like MongoDB or Apache Cassandra (NoSQL databases) can help handle larger datasets and increased read/write loads.

3. **Infrastructure and Server Load:** As the code runs more frequently throughout the day, the server infrastructure may need to handle higher loads. Scaling horizontally by adding more servers or utilizing cloud-based solutions like AWS or Google Cloud can help distribute the load and improve availability.

4. **Concurrency and Parallel Processing:** To handle increased concurrency and parallel processing, employing technologies like message queues (RabbitMQ, Apache Kafka) or task/job schedulers (Celery, Apache Airflow) can help manage and distribute workloads effectively.

#### Content Access Challenges

Handling content access challenges requires adopting various strategies:

1. **Website Structure Changes:** Monitor the target websites for structural changes using web scraping libraries or tools like BeautifulSoup or Scrapy. Implement robust error handling to adapt to website changes and ensure continued data extraction.

2. **IP Blocking:** Rotate IP addresses using proxy servers or utilize IP rotation services to prevent IP blocking. Implement IP rotation policies and monitor IP reputation to ensure uninterrupted access to target websites.

3. **Captcha Validations:** Implement CAPTCHA-solving mechanisms using CAPTCHA-solving services or CAPTCHA recognition libraries to automate the process. Monitor and handle CAPTCHA challenges with appropriate retry and error handling mechanisms.