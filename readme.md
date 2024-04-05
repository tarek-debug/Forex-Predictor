# CurrencyExchangeInsights

## Purpose
CurrencyExchangeInsights aims to enhance decision-making for traders and businesses by providing predictive insights and actionable recommendations on currency exchange rate movemegnts. By leveraging a microservices architecture that includes machine learning models and real-time data via API integrations, this project serves as a comprehensive tool for navigating the complexities of the foreign exchange market.

## Microservices Architecture

### Data Integration Service
- **Responsibility:** Fetches real-time and historical exchange rate data from external APIs, primarily [**Frankfurter**](https://www.frankfurter.app) for current and historical rates published by the European Central Bank. It processes and stores this data for use by the Prediction Service.
- **Technologies:** Python, Flask for creating RESTful services, and a database (e.g., PostgreSQL) for storing fetched data.

### Prediction Service
- **Responsibility:** Utilizes LSTM (Long Short-Term Memory) networks, a type of recurrent neural network, to predict future exchange rates based on the data provided by the Data Integration Service. It employs TensorFlow or PyTorch for constructing and training the machine learning models.
- **Technologies:** Python, TensorFlow or PyTorch for machine learning.

### Gateway API Service
- **Responsibility:** Acts as the primary interface for user interactions, routing requests to the appropriate services (Data Integration or Prediction). It also serves a minimalistic frontend developed with HTML/CSS/JavaScript, allowing users to view predictions, set alerts, and customize their experience.
- **Technologies:** Flask for the API, and standard web technologies for the frontend.

## Deployment
- **Containerization:** Each microservice is containerized using Docker, ensuring isolated environments and dependencies.
- **Orchestration:** Deployed on a Kubernetes cluster for scalable management of services, utilizing Helm charts for deployment configurations.

## Workflow
1. **Data Ingestion:** The Data Integration Service regularly fetches and stores data from external APIs.
2. **Data Processing:** The fetched data is cleaned, processed, and made available for the Prediction Service.
3. **Model Training and Prediction:** The Prediction Service continuously trains its model and provides future exchange rate predictions.
4. **User Interaction:** Through the Gateway API Service, users can request predictions, set alerts, and access the system via a simple frontend.

## Project Rubric Compliance

### Modular Services
- Demonstrates a microservices-based architecture with clear separation of concerns and responsibilities among services.

### Machine Learning
- Employs advanced machine learning techniques within the Prediction Service for accurate forecasting.

### Containers and Kubernetes
- Each microservice is containerized and managed using Kubernetes, showcasing best practices in cloud-native development and deployment.

## Getting Started
To start using CurrencyExchangeInsights, clone this repository and follow the setup instructions detailed in the documentation for deploying the microservices on your Kubernetes cluster.

## Contributing
We welcome contributions to improve CurrencyExchangeInsights. Please see our contributing guidelines for more information on how to get involved.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
