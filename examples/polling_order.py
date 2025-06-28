import asyncio
from apays import APaysClient, APayError

async def main():
    client = APaysClient(client_id=312, secret_key="87d075d3-760c-41ff-ba3f-03df57e836ad")
    try:
        # Создаем платеж и сразу получаем ID
        resp = await client.create_order(10.50)
        print("Order ID:", resp.order_id)

        # Ожидаем завершения платежа (polling)
        final = await client.start_order_polling(
            order_id=resp.order_id,
            interval=5,    # проверяем каждые 5 секунд
            timeout=120    # не дольше 2 минут
        )
        print("Final status:", final.order_status)
    except APayError as e:
        print("Ошибка APays:", e)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
