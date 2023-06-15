import sqlite3

class BotDateBase:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `bot_shop_users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))


    def add_user(self, user_id, g_refferal_url, g_invite_id=None):
        """Добавляем юзера в базу"""
        if g_invite_id != None:
            result = self.cursor.execute("INSERT INTO `bot_shop_users`(`user_id`, `ref_link`, `invite_id`) VALUES (?,?,?)",
                                         (user_id, g_refferal_url, g_invite_id,))
            return self.conn.commit()
        else:
            result = self.cursor.execute("INSERT INTO `bot_shop_users`(`user_id`,`ref_link`) VALUES (?,?)",
                                         (user_id, g_refferal_url,))
            return self.conn.commit()

    def get_balance(self, user_id):
        # Проверка баланса
        result = self.cursor.execute("SELECT `balance` FROM `bot_shop_users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()

    def get_ref_balance(self, user_id):
        # Проверка реф-баланса
        result = self.cursor.execute("SELECT `ref_balance` FROM `bot_shop_users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def count_reeferals(self, user_id):
        """Достаем количество рефералов"""
        return self.cursor.execute("SELECT COUNT(`id`) as count FROM `bot_shop_users` WHERE `invite_id` = ?", (user_id,)).fetchone()[0]

    def get_histor_order(self, user_id):
        """Достаем историю заказов"""
        return self.cursor.execute("SELECT bot_shop_history_order.id, bot_shop_items_in_orders.price*bot_shop_items_in_orders.amount ,date FROM bot_shop_history_order JOIN bot_shop_items_in_orders ON bot_shop_items_in_orders.order_id=bot_shop_history_order.id WHERE `user_id` = ? GROUP BY order_id",
                                   (user_id,)).fetchall()

    def get_account_sold_order_history(self, call_str):
        """Достаем проданные товары"""
        return self.cursor.execute(
            "SELECT `id`,`desc`,`category_id`,`country`,`price` FROM `bot_shop_product` WHERE status=0 AND `id` = ?",
            (call_str,)).fetchall()

    def get_histor_balance(self, user_id):
        """Достаем историю пополнение"""
        return self.cursor.execute("SELECT `id`,`method`, `summa`,`date` FROM `bot_shop_history_balance` WHERE `user_id` = ?",
                                   (user_id,)).fetchall()
    def get_account_sale_tovar_vnalichii(self):
        result = self.cursor.execute("SELECT name_category, country, price FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 1")
        return result.fetchall()

    def get_on_off(self):
        """Вкл/выкл"""
        result = self.cursor.execute("SELECT `on_off` FROM `bot_shop_settings`")
        return result.fetchall()
    def change_on_off(self, on_off):
        """Вкл/выкл"""
        result = self.cursor.execute("UPDATE `bot_shop_settings` SET `on_off` = ?", (on_off,))
        return self.conn.commit()

    def get_user_id(self):
        """Достаем user_id для рассылок"""
        result = self.cursor.execute("SELECT `user_id` FROM `bot_shop_users`")
        return result.fetchall()
    def get_old_balance(self, pol_id):
        """Пополняем баланс / админ панель"""
        result = self.cursor.execute("SELECT `balance` FROM `bot_shop_users` WHERE `user_id` = ?", (pol_id,))
        return result.fetchall()

    def new_balance(self, new_balan, pol_id):
        """Пополняем баланс / админ панель и после покупки"""
        result = self.cursor.execute("UPDATE `bot_shop_users` SET `balance` = ? WHERE `user_id` = ?", (new_balan, pol_id,))
        return self.conn.commit()

    def new_ref_balance(self, user_id):
        """реф счет"""
        result = self.cursor.execute("UPDATE `bot_shop_users` SET `ref_balance` = 0 WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

    def get_account_sale(self):
        """Достаем товары"""
        result = self.cursor.execute(
            "SELECT bot_shop_product.id, desc, name_category, country, price FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 1 ORDER BY name_category")
        return result.fetchall()

    def get_account_sold(self):
        """Достаем проданные товары"""
        result = self.cursor.execute(
            "SELECT bot_shop_product.id, desc, name_category, country, price FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 0")
        return result.fetchall()

    def dell_product_id(self, ids):
        """Удаление товара по id """
        result = self.cursor.execute("DELETE FROM bot_shop_product WHERE `id` = ?", (ids,))
        return self.conn.commit()

    def add_prod_admin(self, fullx, cattex, llocalx, priceadx):
        """Добавления товара админ панель """
        result = self.cursor.execute(
            "INSERT INTO `bot_shop_product` (`desc`, `category_id`, `country`, `price`) VALUES (?,?,?,?)",
            (fullx, cattex, llocalx, priceadx,))
        return self.conn.commit()

    def get_account_alls(self):
        result = self.cursor.execute(
            "SELECT desc, name_category, country, price, bot_shop_product.id FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 1")
        return result.fetchall()
    
    def get_accounts_by_category(self,category_name):
        result = self.cursor.execute(
            "SELECT desc, name_category,name_for_user, country, price, bot_shop_product.id FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 1 AND name_category= ? ",(category_name,))
        return result.fetchall()
    
    def get_vkplay_by_country(self,category_name, country):
        result = self.cursor.execute(
            "SELECT desc, name_category,name_for_user, country, price, bot_shop_product.id FROM bot_shop_product JOIN bot_shop_category ON bot_shop_category.id=bot_shop_product.category_id WHERE status = 1 AND name_category= ? AND country= ?",(category_name,country,))
        return result.fetchall()
    
    def get_user_name_category(self,category_name):
        result = self.cursor.execute(
            "SELECT name_for_user FROM bot_shop_category WHERE name_category= ? ",(category_name,))
        return result.fetchall()
    
    def add_buy_finish(self, id_change):
        """Последний этап покупки """
        result = self.cursor.execute("UPDATE `bot_shop_product` SET `status` = 0 WHERE `id` = ?", (id_change,))
        return self.conn.commit()

    def add_order(self,user_id):
        self.cursor.execute("INSERT INTO bot_shop_history_order (user_id) VALUES (?)", (user_id,))
        self.conn.commit()
        result=self.cursor.execute("SELECT id, user_id, date FROM bot_shop_history_order WHERE user_id= ? ORDER BY id DESC LIMIT 1", (user_id,))
        return result.fetchall()
        
    def add_items_inside_order(self,order_id,category_id, amount,price,tovar_id):
        self.cursor.execute("INSERT INTO bot_shop_items_in_orders (order_id,category_id, amount, price,product_id) SELECT ?, bot_shop_category.id, ? , ?, ? FROM bot_shop_category WHERE name_category = ?", (order_id,amount,price,tovar_id,category_id ))
        self.conn.commit()


    def add_balance_history(self, user_id, po_summa, po_method,id_check):
        """Добавления товара в историю заказа """
        result = self.cursor.execute(
            "INSERT INTO `bot_shop_history_balance` (`user_id` ,`summa`,`method`,'id_check') VALUES (?,?,?,?)",
            (user_id, po_summa, po_method,id_check,))
        return self.conn.commit()

    def check_invite_id(self, user_id):
        """Проверка invite ссылку"""
        result = self.cursor.execute("SELECT `invite_id` FROM `bot_shop_users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def proc_ref_balance(self, balanc_proc, invi):
        """реф счет"""
        result = self.cursor.execute("UPDATE `bot_shop_users` SET `ref_balance` = ? WHERE `user_id` = ?", (balanc_proc, invi,))
        return self.conn.commit()

    def edit_product(self, edit_product_id):
        result = self.cursor.execute("SELECT `id`, `category_id`, `country`, `desc`, `status`, `price` FROM bot_shop_product WHERE `id` = ?", (edit_product_id,))
        return result.fetchall()

    def edit_product_end(self, new_edit_category, new_edit_coutry, new_edit_desc,new_edit_price,new_edit_status,new_edit_id):
        """Последний этап покупки """
        result = self.cursor.execute("UPDATE `bot_shop_product` SET `category_id` = ?, `country` = ?, `desc` = ?, `price` = ?, `status` = ? WHERE `id` = ?", (new_edit_category, new_edit_coutry, new_edit_desc,new_edit_price,new_edit_status,new_edit_id,))
        return self.conn.commit()

    def check_id_item(self,id_prod):
        result= self.cursor.execute("SELECT id FROM bot_shop_product WHERE id =?",(id_prod,))
        return result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()


    def test(self):
        result=self.cursor.execute("SELECT * FROM bot_shop_history_order")
        return result.fetchall()
    
    def get_inside_order(self,id_order):
        """"Берет элементы из заказа и выводит на экран"""
        result= self.cursor.execute("SELECT order_id, bot_shop_items_in_orders.amount, country,name_category, bot_shop_items_in_orders.price, desc,bot_shop_items_in_orders.price*bot_shop_items_in_orders.amount,date FROM bot_shop_history_order JOIN bot_shop_items_in_orders ON bot_shop_items_in_orders.order_id=bot_shop_history_order.id JOIN bot_shop_category ON bot_shop_items_in_orders.category_id=bot_shop_category.id JOIN bot_shop_product ON bot_shop_product.id=bot_shop_items_in_orders.product_id WHERE `order_id`= ?",(id_order,))
        return result.fetchall()








