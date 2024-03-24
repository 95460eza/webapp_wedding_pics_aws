# Use the official Python image as the base image
# Pull from DockerHub the Docker Python images version3.13.0a4 (maintained by Python Software Foundation) along with Alpine (a lightweight Linux distribution) version (3.19).
# Often used due to its small size
#FROM python:3.13.0a4-alpine3.19
FROM public.ecr.aws/lambda/python:3.12


# First copy ONLY the requirements.txt  to leverage Docker cache
# Copy FROM is (Relative to the Dockerfile location) .... INTO a folder TO BE created (here called app) INSIDE the Docker Image (Destination)
COPY app/requirements.txt   ${LAMBDA_TASK_ROOT}

# pip3 is used when you run python3, but using pip will MOST of the time AUTOMATICALLY point to pip for you if needed
# install INSIDE THE CONTAINER the dependencies found in requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade flask

# Copy ALL content FROM (Relative to Dockerfile location).... INTO the work directory /app INSIDE the Docker Image (Destination)
# COPY /app ${LAMBDA_TASK_ROOT} copies the contents of the /app directory (including its subdirectories and files) into the "ROOT" of the Docker image
# Otherwis BELOW CODE would copy the contents of the app directory (including its folder structure) into the "SPECIFIED" destination directory ${LAMBDA_TASK_ROOT} within the Docker image
# After that Docker knows in which file everything is located (kind of indexing)
COPY app/   ${LAMBDA_TASK_ROOT}

# Using "EXPOSE" won't create an error when deploying with Zappa, but it won't have any impact on the deployment EITHER!!
# The EXPOSE instruction in a Dockerfile is used to inform Docker that the APP INSIDE the container listens on the specified ports at runtime (FROM THE APP Definition code),
# But Docker doesn't publish this ports! To ALLOW EXTERNAL access to the application running inside the container, you need to MAP THAT port to a port of your LOCAL HOST (ex: 5000)
# using for Ex: ********* docker run -p 8000:5000 my-container ******************
#EXPOSE 8000

# For Zappa, set CMD to the HANDLER FUNCTION (MUST be called lambda_handler) DEFINED inside the APP Definition code (Ex: app.py file). It could be a parameter override not in the Dockerfile
# You don't need the CMD ["app.lambda_handler"] in your Dockerfile when deploying a Flask application with "ZAPPA". To avoid any issues, it's recommended to keep the Dockerfile
# focused on setting up the necessary environment and dependencies for your application TO RUN WITHIN THE Docker container. 
# NO CMD NEDEED. Specify rather Zappa configurations in the "zappa_settings.json" file!!!!!!!!!!!!!!
#CMD [ "app.lambda_handler" ]
#CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:80", "run:flask_web_app"]
                                                   


