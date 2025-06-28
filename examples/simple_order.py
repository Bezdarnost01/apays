import asyncio
from apays import APaysClient, APayError

async def main():
    client = APaysClient(client_id=123, secret_key="abc123")
    try:
        # Создаем платеж на 99.99 рублей
        resp = await client.create_order(99.99)
        print("Order ID:", resp.order_id)
        print("Payment URL:", resp.url)
    except APayError as e:
        print("Ошибка APays:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())