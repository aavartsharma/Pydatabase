# PyDatabase Project Overview

This document provides a detailed explanation of all the files in the PyDatabase project and how they connect to form a secure, flexible, and cross-platform database system.

---

## **Project Structure**

```
pydatabase/
├── config.py              # Configuration and settings
├── security.py           # Security and encryption utilities
├── database.py           # Core database implementation
├── server.py            # FastAPI server
├── clients/
│   ├── web_client.js    # JavaScript client
│   └── PyDatabaseClient.kt  # Kotlin client
├── base/                # application storage (created at runtime)
│   ├── data/            # database files (created at runtime)
│   └── logs/            # Log files (created at runtime)
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

---

## **File Descriptions**

### 1. `config.py` - Project Configuration
This file contains all the configuration settings required for the project, such as directory paths, network configurations, and security-related keys.

- **Purpose**:
  - Centralizes all project settings for easy management.
  - Ensures that directories like `data/` and `logs/` are created during the server startup.

- **Key Components**:
  - `DATABASE_DIR`: Directory for storing the SQLite database.
  - `SECRET_KEY`: Used for JWT token creation.
  - `ENCRYPTION_KEY`: Used for encrypting database files.

- **How It Connects**:
  - Used by the `server.py` for initializing directories.
  - Accessed by `security.py` for encryption keys.

---

### 2. `security.py` - Security and Encryption Utilities
This file provides essential security features such as encryption, password hashing, and JWT token authentication.

- **Purpose**:
  - Encrypt/decrypt sensitive data stored in the database.
  - Securely hash and verify passwords.
  - Generate and validate JWT tokens for client authentication.

- **Key Components**:
  - AES encryption using the `cryptography` library.
  - Password hashing using PBKDF2.
  - JWT token management for session authentication.

- **How It Connects**:
  - Used by `database.py` to encrypt/decrypt data at rest.
  - Used by `server.py` for user authentication and token verification.
  - Shared by all components to ensure consistent security practices.

---

### 3. `database.py` - Core Database Implementation
This file handles all interactions with the SQLite database. It supports both document-based storage (like MongoDB) and SQL queries.

- **Purpose**:
  - Provide a layer to securely interact with SQLite.
  - Support document-style operations (e.g., insert, find, update, delete).
  - Execute SQL queries with proper validation and logging.

- **Key Components**:
  - `execute_query`: Securely execute SQL queries with parameterized inputs.
  - `insert`, `find`, `update`, `delete`: Document-style operations.
  - Query logging for tracking all database activities.

- **How It Connects**:
  - Called by `server.py` to handle database requests from clients.
  - Uses `security.py` for encrypting/decrypting stored data.

---

### 4. `server.py` - FastAPI Server
This file implements the RESTful API using FastAPI. It serves as the central component that connects the clients to the database.

- **Purpose**:
  - Expose API endpoints for clients to interact with the database.
  - Handle authentication using JWT tokens.
  - Validate and route requests to the appropriate database operations.

- **Key Components**:
  - `/login`: Endpoint for user authentication.
  - `/query`: Endpoint for executing SQL queries.
  - `/users`: Example endpoint for document-based storage operations.
  - Middleware for rate limiting and request validation.

- **How It Connects**:
  - Uses `security.py` for authentication and encryption.
  - Uses `database.py` for all database-related operations.
  - Acts as the entry point for client interactions.

---

### 5. `clients/web_client.js` - JavaScript Client
This file provides a client library for web applications to interact with the PyDatabase server.

- **Purpose**:
  - Simplify API interactions for web developers.
  - Provide helper methods for authentication, document storage, and SQL queries.

- **Key Components**:
  - `login`: Authenticate with the server and store the JWT token.
  - `insert`, `find`, `update`, `delete`: Document-style operations.
  - `executeQuery`: Send SQL queries to the server.

- **How It Connects**:
  - Sends requests to the `server.py` endpoints.
  - Uses the `/login` endpoint to authenticate and retrieve a JWT token.

---

### 6. `clients/PyDatabaseClient.kt` - Kotlin Client
This file provides a client library for Android applications to interact with the PyDatabase server.

- **Purpose**:
  - Simplify API interactions for mobile developers.
  - Provide strongly-typed helper methods for authentication and database operations.

- **Key Components**:
  - `login`: Authenticate with the server and store the JWT token.
  - `insertInto`, `selectAll`, `updateTable`: Document-style and SQL query support.
  - `createTable`: Create new database tables via the server.

- **How It Connects**:
  - Sends HTTP requests to the `server.py` endpoints.
  - Handles authentication via the `/login` endpoint.

---

### 7. `requirements.txt` - Python Dependencies
This file lists all the Python libraries required to run the project.

- **Purpose**:
  - Ensure consistent dependencies across different environments.
  - Make it easy to set up the project using `pip install -r requirements.txt`.

---

### 9. `README.md` - Project Documentation
This file provides an overview of the project, setup instructions, and usage examples.

- **Purpose**:
  - Serve as a quick-start guide for new developers.
  - Explain how to set up and use the PyDatabase system.

---

## **How the Components Work Together**

### **Step 1: Server Startup**
1. Run `server.py`.
2. `config.py` initializes necessary directories (`data/`, `logs/`).
3. FastAPI server starts and begins listening for client requests.

### **Step 2: Client Authentication**
1. Client sends a login request to `/login` with a password.
2. `server.py` verifies the password using `security.py`.
3. If valid, a JWT token is issued to the client.

### **Step 3: Database Operations**
1. Client sends an authenticated request (e.g., to insert data).
2. `server.py` validates the JWT token and routes the request to `database.py`.
3. `database.py` performs the requested operation:
   - Document-style or SQL query.
   - Encrypts/decrypts data using `security.py`.
4. Response is sent back to the client.

### **Step 4: Query Logging**
1. For every database operation, `database.py` logs the query with metadata (e.g., timestamp, user).
2. Logs are stored in the SQLite database for monitoring and debugging.

---

## **Example Workflow**

1. **User Login**:
   - The user logs in via the web or mobile client.
   - A JWT token is issued upon successful authentication.

2. **Data Insertion**:
   - The client sends a request to insert a new document into the `users` collection.
   - The server encrypts the data and stores it in the SQLite database.

3. **Query Execution**:
   - The client sends a SQL query to retrieve all users over 18 years old.
   - The server validates the query, executes it securely, and returns the results.

4. **Query Logging**:
   - The server logs the executed query along with the timestamp and user details.

---

## **Future Enhancements**

1. **Multi-User Support**:
   - Add roles and permissions for different users.

2. **Cloud Integration**:
   - Extend the system to work with cloud-based databases like PostgreSQL.

3. **Monitoring Dashboard**:
   - Build a web-based dashboard to visualize query logs and database statistics.

4. **Backup and Restore**:
   - Add automatic backup functionality for the SQLite database.

---
