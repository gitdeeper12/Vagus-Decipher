
Vagus-Decipher AI v1.0.0 (BIO-MED-02)

Neural Decoding of Vagus Nerve Electrophysiology

FROM python:3.11-slim

WORKDIR /app

Install system dependencies

RUN apt-get update && apt-get install -y 
    gcc 
    g++ 
    && rm -rf /var/lib/apt/lists/*

Copy requirements and install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

Copy source code

COPY vagus_decipher/ ./vagus_decipher/
COPY configs/ ./configs/
COPY data/ ./data/

Set environment variables

ENV VAGUS_LOG_LEVEL=INFO
ENV VAGUS_INTERFACE_TYPE=implanted_cuff
ENV VAGUS_SAMPLING_RATE=30000

Create output directory

RUN mkdir -p /app/results

Default command

CMD ["python", "-c", "from vagus_decipher import version; print(f'Vagus-Decipher v{version} ready')"]
