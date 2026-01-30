
# SQL Data Warehouse Project

This is an example ETL (Extract, Transform, Load) pipeline for building a data warehouse from multiple data sources. The project implements a three-tier data architecture (Bronze, Silver, Gold) with star schema design.

## Live Demo
Check out our deployed application: [https://kelompok-nine.streamlit.app/](https://kelompok-nine.streamlit.app/)

## Project Structure

```
.
├── datasets
│   ├── source_crm
│   └── source_erp
├── scripts
│   ├── bronze
│   ├── gold
│   └── silver
├── tests
├── dashboard.py
├── etl_pipeline.py
├── generate_dummy_data.py
└── README.md
```

## Technologies Used
- Python
- Pandas
- SQLAlchemy
- SQLite
- Streamlit
- SQL

## Architecture Overview
- **Bronze Layer**: Raw data layer (staging area)
- **Silver Layer**: Cleaned and transformed data
- **Gold Layer**: Aggregated data for reporting and analytics

## Dashboard Features
- Interactive visualizations
- Sales analytics
- Customer insights
- Product performance metrics

## How to Run

### 1. Prerequisites

Make sure you have Python 3.8+ installed. You'll also need to install some Python libraries.

```bash
pip install pandas sqlalchemy streamlit
```

### 2. Generate Sample Data

First, run the script to generate or prepare raw data.

```bash
python generate_dummy_data.py
```

### 3. Build Data Warehouse (ETL)

After the raw data is ready, run the ETL pipeline to process it and load it into the data warehouse with star schema design.

```bash
python etl_pipeline.py
```

### 4. Run Dashboard

To visualize the data and ensure everything is connected properly, run the Streamlit dashboard application.

```bash
streamlit run dashboard.py
```

Open your browser and navigate to the URL displayed in the terminal.

## Contributing
Contributions are welcome! Feel free to submit a Pull Request.

## Repository
Find this project on GitHub: [https://github.com/pierredior/sql-data-warehouse](https://github.com/pierredior/sql-data-warehouse)

## License
This project is open source and available under the [MIT License](LICENSE).
