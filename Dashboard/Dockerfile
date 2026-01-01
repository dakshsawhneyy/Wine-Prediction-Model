FROM python:3.10-slim

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:PATH"

WORKDIR /app
COPY requirements.txt .

RUN python3 -m venv $VIRTUAL_ENV
RUN pip install --no-cache-dir -r requirements.txt

COPY Dashboard/dashboard.py

FROM python:3.10-slim

WORKDIR /app

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder /app/dashboard.py .

CMD ["uvicorn", "dashboard:app", "--host", "0.0.0.0", "--port", "3000"]