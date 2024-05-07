# ForEx Predictor
![Forex Logo](Forex_logo.png)

## Purpose
ForEx Predictor s aims to enhance decision-making for traders and businesses by offering predictive insights and actionable recommendations on currency exchange rate movements. This project, leveraging a microservices architecture with machine learning models and API integrations for real-time data, serves as a comprehensive tool for navigating the complexities of the foreign exchange market.

## Microservices Architecture

### Diagram
![Microservices Architecture Diagram](project_diagram.png)

### UI Container
- **Responsibility:** Serves the frontend interface of CurrencyExchangeInsights, providing an intuitive and responsive user experience. It includes:
  - **Login Page**: Secure authentication for accessing user-specific insights and history.
  - **Home Page**: Central dashboard for currency predictions, real-time data viewing, and initiating new queries.
  - **History Page**: Displays a log of past queries and predictions, offering users insights into their past decisions.
  - **Profile Page**: Allows users to manage their account details and preferences.
- **Technologies:** Utilizes web technologies (HTML, CSS, JavaScript) for frontend development. The architecture supports SPA frameworks (e.g., React, Angular, Vue.js) for dynamic content delivery.

### Gateway API Service
- **Responsibility:** Acts as the central interface for user interactions, directing requests to the appropriate services. It serves the frontend, enabling users to view predictions, set alerts, and customize their experience.
- **Technologies:** Flask for the API; HTML/CSS/JavaScript for the frontend components.

### Prediction Service
- **Responsibility:** Employs LSTM (Long Short-Term Memory) networks for predicting future exchange rates based on historical data. Additionally, it generates and supplies graphical representations of predictions.
- **Technologies:** Python with TensorFlow or PyTorch for constructing and training machine learning models.

### Data Storage Service
- **Responsibility:** Handles storage and retrieval of historical data requests and prediction outcomes, supporting queries for historical information and managing user-generated history.
- **Technologies:** Python and Flask for creating RESTful services, SQLite for data persistence.

## Deployment
- **Containerization:** Docker is employed to containerize each microservice, ensuring isolated environments and dependency management.
- **Orchestration:** Kubernetes orchestrates the deployment, scaling, and management of containerized services, with Helm charts facilitating deployment configurations.

## Workflow
1. **User Interaction:** The Gateway API Service facilitates user requests for predictions, alerts, and system interactions through the frontend.
2. **Prediction Execution:** Continual model training within the Prediction Service enables the provision of updated exchange rate predictions and visualizations.
3. **Data Handling:** Historical and predictive data management is centralized within the Data Storage Service, ensuring dynamic and interactive content availability.

## Project Rubric Compliance

### Modular Services
- Showcases a microservices-based architecture with a clear division of responsibilities.

### Machine Learning/AI
- Applies sophisticated machine learning techniques for precise forecasting within the Prediction Service.

### Containers and Kubernetes
- Demonstrates cloud-native development and deployment best practices through the use of containerization and Kubernetes orchestration.

## Getting Started with Forex Predictor

This section provides detailed instructions on deploying and running the Forex Predictor application using Docker and Kubernetes. Ensure you have Docker, kubectl, and minikube (or any other Kubernetes cluster) installed on your system to proceed with the setup.

### Prerequisites
1. **Docker**: Install Docker on your system to create containers for each service.
2. **Kubernetes**: Install a Kubernetes cluster management tool, such as Minikube or use a cloud provider's Kubernetes service.
3. **kubectl**: Install kubectl to interact with your Kubernetes cluster.
4. **gCloud CLI**: Install gCloud CLI to connect to GKE clusters
5. **Helm**: Optionally, install Helm to manage Kubernetes charts easily.

### Deploying Forex Predictor
Follow these steps to deploy the Forex Predictor application on Kubernetes:

1. **Start Your Kubernetes Cluster**:
   - For Minikube: Run `minikube start` to initiate a local Kubernetes cluster.

2. **Clone the Repository**:
   - Clone this repository to your local machine to access the Kubernetes configuration files.
   ```bash
   git clone https://github.com/your-username/forex-predictor.git
   ```
   ```bash
   cd forex-predictor
   ```

3. **Load Docker Images**: Replace Dockerhub username with yours.
   - Build Docker images for each service or pull them from your registry.
   ```bash
   docker build -t [DockerHub Username]/fxp-ui-image:v0.0.1 ./pages
   ```
   ```bash
   docker build -t [DockerHub Username]/forex-gateway:v0.0.1 ./gateway
   ```
   ```bash
   docker build -t [DockerHub Username]forex-prediction:v0.0.1 ./prediction
   ```
   ```bash
   docker build -t [DockerHub Username]forex-data-storage:v0.0.1 ./data_storage
   ```

4. **Create Namespace and Deploy Services to Kubernetes**: Make sure to change to rename the image container names to the ones you built in your dockerhub account.

   ```bash
   cd apps
   ```
   ```bash
   kubectl create namespace fxp-apps
   ```
   ```bash
   kubectl apply -f configmap.yaml
   ```
   ```bash
   kubectl apply -f data-storage-deployment.yaml
   ```
   ```bash
   kubectl apply -f data-storage-service.yaml
   ```
   ```bash
   kubectl apply -f gateway-deployment.yaml
   ```
   ```bash
   kubectl apply -f gateway-service.yaml
   ```
   ```bash
   kubectl apply -f prediction-deployment.yaml
   ```
   ```bash
   kubectl apply -f prediction-service.yaml
   ```
   ```bash
   kubectl apply -f ui-deployment.yaml
   ```
   ```bash
   kubectl apply -f ui-service.yaml
   ```
   ```bash
   kubectl apply -f fxp-ui-ingress.yaml
   ```

5. **Access the Application**:
   - Use `minikube service list` to find the IP and port of the UI service or check your cloud Kubernetes service dashboard.
   - Access the Forex Predictor UI via the provided URL in your browser.

### Monitoring and Logs
- Monitor the status of the pods and services using:
  ```bash
  kubectl get pods
  ```
  ```bash
  kubectl get services
   ```
- View logs for a specific service:
  ```bash
  kubectl logs <pod-name>
  ```
### Accessing the App Locally (Optional)
  To access your app from a local browser for development and testing, you can set up port forwarding to the UI service using this command:
  ```bash
  kubectl port-forward svc/fxp-ui 8080:80 -n fxp-apps
  ```
  ```bash
  kubectl port-forward svc/fxp-gateway 8081:80 -n fxp-apps
   ```
  ```bash
  kubectl port-forward svc/fxp-prediction 8082:80 -n fxp-apps
   ```
  ```bash
  kubectl port-forward svc/fxp-data-storage 8083:80 -n fxp-apps
   ```
### Connecting to GKE Cluster
- Install gCloud CLI. Once the gcloud CLI is installed, be sure to restart VSCode or other IDE or command line shell after this to get the path updates.
- Log into Google with the IAM

```bash
gcloud auth login
```
- Get the GKE context. Once the above authentication works, run:
 
```bash
gcloud components install gke-gcloud-auth-plugin
```
- Then, run

```bash
gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1 --project horizontal-ray-375222
```

- To see the contexts list of kubernewtes clusters you have enter
```bash 
kubectl config get-contexts
```

- To see the current context, enter-
```bash 
kubectl config current-context 
```

- To switch to the GKE Kubernets cluster, enter-
```bash
kubectl config set-context gke_horizontal-ray-375222_us-central1_autopilot-cluster-1
``` 
- To confirm you can access the cluster 
```bash 
kubectl get nodes
```
  
### Updating the Application
- To update any service, rebuild the Docker image and update the Kubernetes deployment:
  ```bash
  docker build -t forex-service:new ./path/to/service/Dockerfile
  ```
  ```bash
  kubectl set image deployment/forex-service forex-service=forex-service:new
   ```

### Cleaning Up
- To stop and remove all running services:
  ```bash
  kubectl delete all --all
  ```

This setup provides a robust foundation for running the Forex Predictor application in a production-like environment on Kubernetes.

## Contributing
We encourage contributions to CurrencyExchangeInsights. See our contributing guidelines for more details on participating.

## License
This project is licensed under the MIT License. Refer to the LICENSE file for details.

## Acknowledgments
Components and inspiration were drawn from these repositories:
- User Authentication: [Flask User Authentication](https://github.com/anuraagnagar/flask-user-authentication/tree/main)
- Frankfurter API: [Frankfurter](https://github.com/hakanensari/frankfurter)
