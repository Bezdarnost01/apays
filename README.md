<p align="center">
  <h1 align="center">apays</h1>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+">
  </a>
  <a href="https://www.python-httpx.org/">
    <img src="https://img.shields.io/badge/httpx-%3E%3D0.24.0-blue.svg" alt="httpx">
  </a>
  <a href="https://pydantic.dev/">
    <img src="https://img.shields.io/badge/pydantic-v2-blue.svg" alt="pydantic v2">
  </a>
</p>

**apays** — это асинхронный Python-клиент для API платёжной системы APays. Он предоставляет методы для создания платежей, проверки их статуса и (опционально) опроса до завершения.

> ## [Репозиторий на GitHub](https://github.com/Bezdarnost01/apays)

## Быстрый старт

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
        print("Ошибка APays:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Пример polling

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
        print("Ошибка APays:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Установка

Вы можете установить его напрямую из GitHub или из PyPi:

```bash
pip install git+https://github.com/Bezdarnost01/apays.git@main#egg=apays
```

```bash
pip install apays
```

## Лицензия

MIT © [Bezdarnost01](https://github.com/Bezdarnost01)
