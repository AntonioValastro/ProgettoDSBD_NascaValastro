FROM python:3
WORKDIR /app
ENV FLASK_APP=user.py
COPY . ./
RUN pip3 install mysql-connector-python
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
