FROM python:3.14-slim

WORKDIR /mcp

COPY requirements.txt /mcp/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /mcp/requirements.txt

COPY . /mcp

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]