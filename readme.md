
# Flask App Documentation

This documentation provides a comprehensive guide on setting up, running, and using the Flask app. It covers various aspects such as virtual environment setup, running and app functionality, unit testing, authentication, and deployment.

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    1. [File Structure](#file-structure)
    2. [Installation](#installation)
    3. [Environment Configuration](#environment-configuration)
3. [Running the App](#running-the-app)
4. [App Overview](#app-overview)
    1. [Endpoints](#endpoints)
    2. [Authentication](#authentication)
5. [Unit Testing](#unit-testing)

6. [Future Developments](#future-changes)

## Introduction
This Flask app provides various functionalities such as user registration, authentication, generating random arrays, and more. It includes unit tests, rate limiting.
This documentation provides a comprehensive guide for setting up, running, and using the Flask app.

## Getting Started

### File Structure
```plaintext
flask_app_folder/
├── app.py
├── testing/
│   ├── test_app.py
├── users_db/
│   └── users.yaml
├── .env
├── requirements.txt
```


### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/siri15243/flask_app.git
   cd flask_app
   ```
2. Create a virtual environment and activate it

   ```bash
   python -m venv flask_app_venv
   source flask_app_venv/bin/activate
   ```
3. Install the required libraries and dependencies listed in the `requirements.txt` file

   ```bash
   pip3 install -r requirements.txt
   ```

### Environment Configuration
Environment Configuration :\
Before running the application, make sure to configure the environment variables by creating a .env file in the root directory of your project. This file should contain key-value pairs for various configuration settings. In this case, we'll use the .env file to specify the port on which the Flask app will run.

Create a `.env` file in the project root directory and set the desired port for the app

 ```bash
    PORT=5000
```
Replace `5000` with the port number you want your app to run on.



## Running the App

Run the app using Gunicorn or waitress or as a simple python file with the specified port in the `.env` :

*NOTE*  : *`Gunicorn provides a reliable way to run Flask apps in a production-like environment`*
```bash
    gunicorn -b 0.0.0.0:$PORT app:app
                (or)
    waitress-serve --listen=127.0.0.1:$PORT app:app
                (or)
    python3 app.py
```
Here in case of `Gunicorn` deployment, *`-b 0.0.0.0:$PORT`* specifies that the app should bind to all available network interfaces on the specified port.

With these steps, your Flask app will be up and running on the port defined in the .env file. This allows you to easily manage the port configuration without modifying the code directly.

Please ensure that you've installed Gunicorn and have the virtual environment activated before running the commands.


## App Overview
The Flask app is designed to provide a user registration and authentication system along with an array generation API. The app uses JWT (JSON Web Tokens) for user authentication and secure API access.

### Endpoints


1. **`/health`** : Allows users to check if the app is up and running. This endpoint can be used in auto monitoring tools like Kubernetes to check if the app is running in the background.

2. **`/register`** : 
Allows users to register with a username and password. Prevents duplicate username registrations.

   HTTP Method: `POST`

   Request Body:

      ```json
      {
      "username": "new_user",
      "password": "new_password"
      }
   ```

   Response -> Status Code: 200 (OK)

      ```json
      {
      "message": "User registered successfully"
      }
   ```

   Body (Failure - Username already exists):

      ```json
      {
      "message": "User registered already, Please login"
      }
      ```

3. **`/login`** : 
Allows users to log in with their registered username and password. Returns a JWT token on successful login. This JWT Token can be used to authenticate the future queries of protected endpoints such as `/generate_array` in our case.

   HTTP Method: `POST`

   Request Body:

      ```json
      {
      "username": "user1",
      "password": "password1"
      }
   ```
   Response -> Status Code: 200 (OK)

      ```json
      {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
   ```

   Status Code: 401 (Unauthorized)
   Body (Failure - Authentication):
      ```json
      {
      "message": "Authentication failed"
      }
   ```

4. **`/generate_array`** : Generates a 500-dimensional random float array when provided with an input sentence. Requires a valid JWT token for authenticated access.

   HTTP Method: `POST`

   Request Body:

   ```json
      {
      "sentence": "This is a sample sentence"
      }
   ```

   Headers:
   Authorization: Bearer `<JWT Token>` \
   Response:

   Status Code: 200 (OK)
   ```json
      [
      0.123,
      0.456,
      ...
      ]
   ```
   Status Code: 401 (Unauthorized)
   Body (Failure - Authentication):

   ```json
      {
      "message": "Token is missing"
      }
   ```
#### Endpoint Summary
In summary, the `/register` endpoint allows users to create accounts, the `/login` endpoint provides authentication, and the `/generate_array` endpoint generates random float arrays based on input sentences. The app ensures secure registration, login, and authenticated access to certain functionalities using JWT tokens.

These endpoints collectively provide user registration, login, and data generation functionalities while adhering to security measures and access control mechanisms.


### Authentication

The app uses JWT for user authentication. Users receive tokens upon successful login, which they include in the headers of authenticated API requests.

## Unit Testing
### Handling Test Cases

The app is tested using the Flask-Testing framework. Various test cases are implemented to ensure each endpoint's correctness and robustness.

1. Valid Input
Tests if the `/generate_array` endpoint successfully generates a random array when provided with valid input.

2. Invalid Input
Tests the handling of invalid input for the `/generate_array` endpoint.

3. User Registration
Tests user registration using the `/register` endpoint. Checks if the response is correct for both new and existing users.

4. User Login
Tests user login using the `/login` endpoint. Validates the response on both successful and unsuccessful login attempts.

5. Array Generation (Authenticated)
Tests array generation with an authenticated user using the `/generate_array` endpoint. Ensures that an authenticated user can successfully generate an array.

6. Array Generation (Unauthenticated)
Tests array generation without providing a JWT token. Validates that an unauthenticated user cannot generate an array.

7. Monitoring (Additional Test Case)
Tests the `/generate_array` endpoint with an authenticated user to monitor API behavior.



## Conclusion

This guide provided steps to set up a virtual environment, install packages from a requirements.txt file, and run your Flask app using the Gunicorn web server. Using a virtual environment helps isolate your project's dependencies, and Gunicorn provides a reliable way to run Flask apps in a production-like environment. It provides an in-depth understanding of the Flask app's architecture, endpoints, unit testing strategy, and authentication mechanism. By following the provided steps, users can run the app and tests to validate its functionality and security.

Remember to deactivate the virtual environment when you're done using your app:

   ```bash
   deactivate
   ```
With these steps, you can ensure a clean and organized environment for your Flask app while also utilizing a robust web server for deployment.


## Future Developments

1. **Monitoring with Prometheus and Grafana**
   - Integrate Prometheus and Grafana to monitor the health and performance of the app.
   - Set up Prometheus to scrape metrics and Grafana to visualize and create dashboards.
   - Monitor response times, error rates, and resource utilization.
   

2. **Enhanced Authentication**
   - Consider replacing JWT token-based authentication with more robust methods such as user-based authentication.
   - Implement OAuth 2.0 for secure authentication and authorization with third-party services.
   - Provide options for multi-factor authentication to enhance security.

3. **Security** 
   - Forcing the user to access the endpoint from a secured connection (`https`)
   - Database utilities can be used to overcome the privacy information exposure in the codebase for the authentication purposes.

4. **Docker and Microservices**
   - Containerize the app using Docker to ensure consistent deployments across various environments.
   - Break down the app into microservices to modularize functionality and enhance scalability.
   - Utilize Docker Compose for simplified multi-container deployments.

5. **Kubernetes for Scalability**
   - Deploy the app on Kubernetes to take advantage of container orchestration.
   - Utilize Kubernetes scaling features to automatically adjust resources based on traffic demands.
   - Set up Kubernetes-based monitoring using tools like Prometheus and Kubernetes Dashboard.


6. **Caching**
   - Introduce caching mechanisms to optimize frequently accessed data and reduce response times.
   - Consider using caching solutions like Redis to store and manage cached data.


7. **Logging and Error Handling**
   - Implement detailed logging and error handling mechanisms to capture and troubleshoot issues.
   - Use tools like ELK stack (Elasticsearch, Kibana) for centralized logging and analysis.


8. **Continuous Integration and Deployment (CI/CD)**
    - Set up automated CI/CD pipelines to streamline development, testing, and deployment processes.
    - Utilize tools like Jenkins or GitLab CI/CD for automated builds, tests, and deployments.


These future developments can enhance the functionality, performance, and security of your Flask app, ensuring it remains adaptable and competitive in the evolving landscape.

