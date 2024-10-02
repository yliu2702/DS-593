FROM python:3.9

WORKDIR /postgres_python

COPY . .

RUN pip install --no-cache-dir -r requirement.txt 

CMD ["python", "main.py"]