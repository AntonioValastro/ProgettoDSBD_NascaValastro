FROM python:3
WORKDIR /app
ENV FLASK_APP=follow.py
COPY . ./
RUN pip3 install mysql-connector-python
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
