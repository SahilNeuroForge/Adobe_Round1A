FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxrender-dev libxext6 gcc g++
RUN pip install --no-cache-dir torch==1.12.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
