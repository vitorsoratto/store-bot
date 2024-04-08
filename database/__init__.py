""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""


import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


    # [[ Store ]]
    async def add_item(
        self, name: str, desc: str, price: float, stock: int = 0
    ) -> bool:
        """
        This function will add a item to the database.

        :param name: The name of the item.
        :param desc: The description of the item.
        :param price: The price of the item.
        :param stock: The stock of the item (default 0).
        """
        await self.connection.execute(
            "INSERT INTO item(name, description, price, stock) VALUES (?, ?, ?, ?)",
            (
                name,
                desc,
                price,
                stock,
            ),
        )
        await self.connection.commit()
        return True

    async def update_item_stock(
            self, item_id: int, stock: int
        ) -> int:
        """
        This function will update the stock of a item.

        :param item_id: The ID of the item.
        :param stock: The new stock of the item.
        """
        await self.connection.execute(
            "UPDATE item SET stock=? WHERE id=?",
            (
                stock,
                item_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT stock FROM item WHERE id=?",
            (
                item_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_item(self, item_id: int):
        """
        This function will get the item from the database.

        :param item_id: The ID of the item.
        :return: The item.
        """
        rows = await self.connection.execute(
            "SELECT id, name, description, price, stock FROM item WHERE id=?",
            (
                item_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result

    async def get_items(self) -> list:
        """
        This function will get all the items from the database.

        :return: A list of all the items.
        """
        rows = await self.connection.execute(
            "SELECT id, name, description, price, stock FROM item",
        )
        async with rows as cursor:
            result = await cursor.fetchall()

            result_list = []
            for row in result:
                result_list.append(row)
            return result_list

    async def remove_item(self, item_id: int) -> int:
        """
        This function will remove a item from the database.

        :param item_id: The ID of the item.
        """
        await self.connection.execute(
            "DELETE FROM item WHERE id=?",
            (
                item_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM item WHERE id=?",
            (
                item_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def search_item(self, name: str) -> list:
        """
        This function will search for a item in the database.

        :param name: The name of the item.
        :return: The item.
        """
        rows = await self.connection.execute(
            "SELECT id, name, description, price, stock FROM item WHERE name=?",
            (
                name,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
