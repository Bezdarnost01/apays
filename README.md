<p align="center">
  <h1 align="center">apays</h1>
</p>

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)  
[![httpx](https://img.shields.io/badge/httpx-%3E%3D0.24.0-blue.svg)](https://www.python-httpx.org/)  
[![pydantic v2](https://img.shields.io/badge/pydantic-v2-blue.svg)](https://pydantic.dev/)  

**apays** is an asynchronous Python client for the APays payment API. It provides methods to create payments, check status, and (optionally) poll until completion.

> ## [GitHub Repository](https://github.com/Bezdarnost01/apays)

## Quick start

```python
import asyncio
from apays import APaysClient, APayError

async def main():
    client = APaysClient(client_id=123, secret_key="abc123")
    try:
        # Создаём платёж на сумму 45.67 (будет сконвертировано в 4567 копеек)
        resp = await client.create_order(45.67)
        print("Order ID:", resp.order_id)
        print("Payment URL:", resp.url)

        # Проверяем статус
        status = await client.get_order(resp.order_id)
        print("Current status:", status.order_status)
    except APayError as e:
        print("APays error:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Polling example

```python
import asyncio
from apays import APaysClient, APayError

async def main():
    client = APaysClient(client_id=123, secret_key="abc123")
    try:
        resp = await client.create_order(10.50)
        print("Order ID:", resp.order_id)

        # Ждём завершения платежа (проверяем каждые 5 секунд, максимум 2 минуты)
        final = await client.start_order_polling(
            order_id=resp.order_id,
            interval=5.0,
            timeout=120.0
        )
        print("Final status:", final.order_status)
    except APayError as e:
        print("APays error:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## FastAPI integration

```python
# src/apays/dependencies.py
from contextlib import asynccontextmanager
from apays import APaysClient

@asynccontextmanager
async def get_apays_client():
    client = APaysClient(client_id=123, secret_key="abc123")
    try:
        yield client
    finally:
        await client.close()
```

```python
# app.py
from fastapi import FastAPI, Depends
from apays.dependencies import get_apays_client
from apays import OrderStatusResponse

app = FastAPI()

@app.get("/create-payment/")
async def create_payment(amount: float, client=Depends(get_apays_client)):
    resp = await client.create_order(amount)
    return {"order_id": resp.order_id, "payment_url": resp.url}

@app.get("/payment-status/{order_id}")
async def payment_status(order_id: str, client=Depends(get_apays_client)) -> OrderStatusResponse:
    return await client.get_order(order_id)
```

## Installation

```bash
pip install apays
```

## License

MIT © [Your Name](https://github.com/Bezdarnost01)
