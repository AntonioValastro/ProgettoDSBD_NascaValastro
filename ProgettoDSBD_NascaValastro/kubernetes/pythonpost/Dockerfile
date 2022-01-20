FROM python:3
WORKDIR /app
ENV FLASK_APP=post.py
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT 5000
EXPOSE 5000
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
