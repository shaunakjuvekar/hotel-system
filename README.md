# Hotel System - Cloud-Native Microservices Architecture

This repository contains the codebase for a **Hotel Booking System**, designed with a scalable, event-driven microservices architecture using AWS services. The project is based on a serverless and containerized infrastructure and focuses on efficient management of hotel bookings and related operations.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Architecture Overview
The Hotel Booking System is built using microservices patterns, with an emphasis on scalability, performance, and high availability. The architecture includes the following components:
- **API Gateway**: Routes requests to different microservices.
- **AWS Lambda**: Processes various requests (CRUD operations, booking logic, SNS topic handling).
- **Amazon ECS**: Hosts containerized services behind a Network Load Balancer (NLB).
- **AWS DynamoDB**: Manages hotel data storage.
- **Amazon S3**: Stores media assets such as hotel images.
- **AWS SNS**: Event notifications for specific actions such as storing hotel data in Elasticsearch (e.g., new booking).

The system is designed to handle dynamic scalability, and microservices communicate via API Gateway, Lambda functions, and containerized ECS services.

## Features
- **Hotel Management**: Add, edit, and delete hotel details.
- **Booking System**: Book, modify, or cancel hotel reservations.
- **User Authentication**: Secure login and user management with AWS Cognito.
- **Media Uploads**: Upload hotel images and other assets via S3.
- **Event-Driven Architecture**: Triggering Elasticsearch ingestion through AWS SNS.

## Technologies Used
- **Backend**: Python, AWS Lambda, ECS
- **Frontend**: React, JavaScript
- **Database**: DynamoDB
- **Storage**: S3 for media files
- **Auth**: AWS Cognito
- **Infrastructure**: AWS API Gateway, Network Load Balancer (NLB)

## Getting Started

### Prerequisites
- Python 3.10
- AWS CLI installed and configured
- Docker
- Node.js and npm
- AWS Account

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shaunakjuvekar/hotel-system.git
   cd hotel-system

   
2. Install frontend dependencies: 

```bash
cd frontend
npm install

```
3. The following API endpoints are available for various functionalities:
GET /hotels: Fetch the list of available hotels.
POST /hotels: Add a new hotel. 

