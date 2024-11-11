FROM python:3.11-slim-buster


COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python","fast.py"]
#or you can do CMD ["uvicorn","fast:app","--host","0.0.0.0"] without the main function inside the fast.py file