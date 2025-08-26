
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


# 🚀 Project Setup and Requirements

### Prerequisites
 - **Docker Desktop:** Ensure Docker Desktop is installed and running on your machine.
 - [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Clone the Repository
 - Clone the repository using Git
    ```sh
    git clone https://github.com/niteshjangid29/pdf-search.git
    cd pdf-search
    ```

### RUN ElasticSearch (preferred using docker)
 - Run below command in terminal to start ElasticSearch
    ```sh
    curl -fsSL https://elastic.co/start-local | sh
    ```

 - **Note:** You will get credentials in the terminal output, which are required for accessing the Elasticsearch API.
    ```sh
    Elasticsearch UserName, Password and API Key (required for further steps)
    ```

 - Verify that Elasticsearch is running by accessing the following URL in your browser:
   ```sh
   http://localhost:9200
   ```

### RUN Backend API
- Update the environment variables in the `.env` file (Database is Hosted)
    ```sh
    DATABASE_URL = "postgresql://neondb_owner:npg_mOL4n7eRUwEz@ep-square-tree-ad3xa2qc-pooler.c-2.us-east-1.aws.neon.tech/pdf-data?sslmode=require"
    JWT_SECRET = "fdsfneahuw324234ggafergvjndsncwei38aqovzje2uf"
    EXPIRY_TIME=60
    ES_HOST = "http://localhost:9200"
    ES_API_KEY = "<your-elasticsearch-api-key>"
    INDEX_NAME = "pdf_documents"
   ```

- Build the Docker image of the project (in root of the project)
    ```sh
    docker build -t pdf-search .
    ```

- Run the Docker container
    ```sh
    docker run -p 8000:8000 pdf-search
    ```

### Lets go!
The project is now set up and running! You can start using the PDF search API at
```sh
http://localhost:8000
```

# API Endpoints

This document provides a detailed overview of the API endpoints for the PDF Semantic Search application. All API endpoints are available under the main application URL.

---

## Authentication Endpoints

This section covers endpoints related to user registration, login, and profile management.

### 1. Register a New User

- **Endpoint:** `POST /register`
- **Description:** Creates a new user account.
- **Authorization:** None required.

Request Body:
```json
{
  "fullname": "John Doe",
  "email": "john.doe@example.com",
  "password": "a_strong_password"
}
```

Success Response (200 OK):

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "fullname": "John Doe",
  "email": "john.doe@example.com"
}
```

### 2. User Login
- **Endpoint:** POST `/login`
- **Description:** Authenticates a user and returns a JWT access token.
- **Authorization:** None required.

Request Body:
```json
{
  "email": "john.doe@example.com",
  "password": "a_strong_password"
}
```

Success Response (200 OK):

```json
{
  "access_token": "ey...",
  "token_type": "bearer"
}
```

### 3. Get User Profile
- **Endpoint:** GET `/profile`
- **Description:** Retrieves the profile information of the currently authenticated user.
- **Authorization:** Bearer Token required.

Success Response (200 OK):
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "fullname": "John Doe",
  "email": "john.doe@example.com"
}
```

## PDF Management Endpoints
These endpoints are for uploading, searching, and managing PDF documents. All endpoints in this section require authentication.

**Authorization Header**
For all protected routes, you must include the JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### 1. Upload a PDF
- **Endpoint:** POST `/upload-pdf`
- **Description:** Uploads a PDF file. The system processes the file, extracts its content, creates vector embeddings, and indexes it for searching.
- **Authorization:** Bearer Token required.

Request Body:
- This is a multipart/form-data request. The file should be sent under the key file.

Success Response (200 OK):

Returns the metadata of the newly created PDF record.
```json
{
  "id": "f0e9d8c7-b6a5-4321-fedc-ba0987654321",
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "file_name": "project_report.pdf",
  "uploaded_at": "2025-08-26T15:00:00.456Z"
}
```

### 2. Search Within a PDF
- **Endpoint:** POST `/search`
- **Description:** Performs a semantic search for a query string within a specific PDF document.
- **Authorization:** Bearer Token required.

Request Body:
```json
{
  "query": "project budget details",
  "pdf_id": "f0e9d8c7-b6a5-4321-fedc-ba0987654321"
}
```

Success Response (200 OK):
```
[
  {
    "type": "text",
    "page_number": 5,
    "content": "The total allocated budget for the project is $500,000, with a contingency of 15%.",
    "score": 0.912
  },
  {
    "type": "table",
    "page_number": 6,
    "content": "Table with Headers: Item, Cost. Row 1: Item is Phase 1 Development, Cost is $200,000.",
    "score": 0.875
  }
]
```

### 3. Get All User Documents
- **Endpoint:** GET `/pdfs`
- **Description:** Retrieves a list of metadata for all PDF documents uploaded by the authenticated user.
- **Authorization:** Bearer Token required.

Success Response (200 OK):
```
[
  {
    "id": "f0e9d8c7-b6a5-4321-fedc-ba0987654321",
    "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "file_name": "project_report.pdf",
    "uploaded_at": "2025-08-26T15:00:00.456Z"
  },
  {
    "id": "b1c2d3e4-f5a6-b789-c123-d4567890efab",
    "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "file_name": "marketing_plan.pdf",
    "uploaded_at": "2025-08-25T11:20:10.789Z"
  }
]
```
