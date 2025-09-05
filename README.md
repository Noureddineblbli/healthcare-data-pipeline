Healthcare Data Integration & Compliance Pipeline
An enterprise-grade healthcare data integration and compliance pipeline that processes daily batch data from multiple medical sources. The pipeline ingests patient data from FHIR APIs, lab results from HL7 files, and insurance claims data, then applies HIPAA-compliant transformations including PII masking and data standardization. The system uses Apache NiFi for data ingestion, Apache Spark for heavy-duty processing, Snowflake as the cloud data warehouse, and dbt for analytics transformations. All components are orchestrated by Apache Airflow and monitored with Great Expectations for data quality assurance. The pipeline produces compliance-ready reports, analytics dashboards, and ML-ready feature datasets following a Bronze-Silver-Gold data architecture pattern.
Architecture Overview
This project uses a modern, containerized data stack to orchestrate a secure and repeatable data pipeline. The flow of data is designed to follow best practices in data engineering, moving from raw ingestion to analytics-ready datasets.
Data Flow
Ingestion (NiFi): Apache NiFi is the entry point, responsible for pulling data from external sources like FHIR APIs and SFTP servers (for HL7 files).
Orchestration (Airflow): Apache Airflow acts as the central brain. It schedules and triggers all downstream tasks, ensuring that processes run in the correct order and handling dependencies and retries.
Processing (Spark): Airflow triggers Spark jobs to perform heavy-duty transformations. This includes standardizing HL7 data, masking Personally Identifiable Information (PII) to meet HIPAA standards, and structuring the data into Bronze, Silver, and Gold layers.
Storage (PostgreSQL & Snowflake):
PostgreSQL: Serves as the metadata database for Airflow, tracking DAG runs, task states, and connections.
Snowflake (Planned): The final destination for the processed Gold data, serving as the enterprise cloud data warehouse for analytics and reporting.
Analytics & Quality (dbt & Great Expectations - Planned):
dbt: Will be used for final transformations within Snowflake, building analytics models.
Great Expectations: Will be integrated into the pipeline to enforce data quality and validate data at each stage.
ASCII Architecture Diagram
code
Code
[Sources]--->[NiFi]--->[Raw Storage/Bronze]--->[Spark]--->[Processed/Silver/Gold]--->[Snowflake]
   |            ^               ^                    ^               ^                    |
   |            |               |                    |               |                    |
   +----[Airflow Orchestration]---------------------------------------------------------+
                         |                    |               |                    |
                         +-- Triggers NiFi    +-- Triggers Spark|                    |
                                              |                    +-- Triggers dbt    |
                                              |                                        |
                                              +----------[Great Expectations]----------+
                                                          (Data Quality)
Technology Stack
Component	Role
Apache Airflow	Workflow orchestration and scheduling.
Apache NiFi	Data ingestion and flow management.
Apache Spark	Large-scale data processing and transformation.
PostgreSQL	Metadata database for Apache Airflow.
Docker & Docker Compose	Containerization for all services.
Snowflake (Planned)	Cloud data warehouse for final analytics.
dbt (Planned)	In-warehouse data transformation and modeling.
Great Expectations (Planned)	Data quality validation and testing.
Prerequisites
Before you begin, ensure you have the following installed on your system:
Docker
Docker Compose (v2.0 or later)
Project Structure
code
Code
.
├── apps/                 # Spark applications (e.g., Python scripts, JARs)
├── dags/                 # Airflow DAG files
├── data/                 # Local data storage for Spark/NiFi
├── .env                  # Your local environment configuration (DO NOT COMMIT)
├── .env.template         # Environment variable template
├── docker-compose.yml    # Defines all services
└── README.md             # This file
Setup and Installation
Follow these steps to get the entire data pipeline running on your local machine.
1. Clone the Repository
code
Bash
git clone <https://github.com/Noureddineblbli/healthcare-data-pipeline.git>
cd <yhttps://github.com/Noureddineblbli/healthcare-data-pipeline.git>
2. Create the Environment Configuration
Copy the template file to create your own local configuration.
code
Bash
cp .env.template .env
Important: Open the .env file and edit the placeholder values. You must set a secure POSTGRES_PASSWORD and AIRFLOW__WEBSERVER__SECRET_KEY.
3. Create Required Local Directories
These directories are mounted into the containers and are required for the services to start correctly.
code
Bash
mkdir -p dags apps data
4. Build and Start the Services
Use Docker Compose to build and start all the services in the background.
code
Bash
docker-compose up -d --build
The initial startup may take a few minutes as Docker needs to download the images and the Airflow init service needs to set up the database.
Service Access
Once the containers are running, you can access the services via your web browser or other tools:
Service	URL	Username	Password
Airflow UI	http://localhost:8080	admin	admin (or as set in .env)
Spark Master UI	http://localhost:8081	N/A	N/A
NiFi UI	http://localhost:8181/nifi	N/A	N/A
PostgreSQL DB	localhost:5432	(as set in .env)	(as set in .env)
How to Stop the Pipeline
To stop all running services, run:
code
Bash
docker-compose down
To stop services and remove all persisted data (including the PostgreSQL and NiFi databases), run:
code
Bash
docker-compose down --volumes