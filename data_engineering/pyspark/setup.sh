# setup.sh
#!/bin/bash

# Create project directory structure
mkdir -p data_engineering/etl/pyspark/{scripts/{data_processing,transformations,performance,advanced},deployment/{aws,gcp,azure},sample_data,tests,notebooks}

# Create virtual environment
python3 -m venv pyspark-env
source pyspark-env/bin/activate

# Install requirements
pip install -r requirements.txt

# Download sample data
curl -o sample_data/employees.csv "https://example.com/sample-data/employees.csv"
curl -o sample_data/orders.json "https://example.com/sample-data/orders.json"

# Set up Jupyter kernel
python -m ipykernel install --user --name=pyspark-env --display-name="PySpark Environment"

# Create Spark configuration
mkdir -p ~/.spark/conf
cp spark-defaults.conf ~/.spark/conf/

echo "Setup complete! Run 'source pyspark-env/bin/activate' to activate the environment."