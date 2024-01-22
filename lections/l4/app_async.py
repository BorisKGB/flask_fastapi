import asyncio


async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(1)  # (sleep) allow anyone to interrupt me while i sleep


async def print_letters():
    for letter in ['a', 'b', 'c', 'd', 'e', 'f']:
        print(letter)
        await asyncio.sleep(0.5)  # (sleep) allow anyone to interrupt me while i sleep


async def main():
    task1 = asyncio.create_task(print_numbers())  # create task1
    task2 = asyncio.create_task(print_letters())  # create task2
    await task1  # (?run? and wait for task1) allow task1 to interrupt me
    await task2  # (?run? and wait for task2) allow task2 also to interrupt me


async def count():
    print("start")
    await asyncio.sleep(1)
    print("1 sec")
    await asyncio.sleep(2)
    print("2 sec")
    return "done"


async def main2():
    result = await asyncio.gather(count(), count(), count())  # ?
    print(result)


async def main3():
    tasks = [asyncio.create_task(count() for i in range(5))] # create 5 tasks
    await asyncio.gather(*tasks)  # run and wait for tasks


#asyncio.run(main())
asyncio.run(main2())
