
# ☁️ AWS / Cloud Services for Deployment
For deploying this PDF search backend, a robust and scalable set of AWS services would be ideal:

- **Backend API:**
  - **AWS EC2 Machine:** For hosting the backend API.

- **Database (Postgres):**
  - **AWS RDS (Relational Database Service):** Managed PostgreSQL database.

- **Search (Elasticsearch):**
  - **AWS OpenSearch Service:** Managed OpenSearch (Elasticsearch) service.

- **Asynchronous Processing:**
  - **AWS SQS (Simple Queue Service):** Api will use SQS to queue PDF processing tasks, worker will pick up tasks from the queue.
  - **AWS Lambda:** Serverless functions to process PDFs. This will download the pdf from S3, perform extraction, embedding and indexing in OpenSearch.
  - **AWS S3:** Storage for uploaded PDFs and processed results.


