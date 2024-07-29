# Use an official Spark base image
FROM bitnami/spark:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY log_processor.py /app/

# Install necessary Python packages
RUN pip install pyspark

# Set environment variables
ENV IVY_HOME=/tmp/.ivy2
ENV SPARK_HOME=/opt/bitnami/spark

# Ensure the Ivy directory is writable
RUN mkdir -p $IVY_HOME/local && chmod -R 777 $IVY_HOME

# Disable Kerberos by setting environment variables
ENV HADOOP_USER_NAME=root
ENV HADOOP_CONF_DIR=/opt/bitnami/hadoop/conf
ENV SPARK_SUBMIT_OPTS="-Djava.security.krb5.conf=/dev/null"

# Set the entry point to the Spark submit command
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", "--master", "local[2]", "--conf", "spark.jars.ivy=/tmp/.ivy2", "/app/log_processor.py"]

