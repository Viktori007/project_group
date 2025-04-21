import MySQLdb
from MySQLdb import OperationalError


class Database:

    @staticmethod
    def connect():
        try:
            connection = MySQLdb.connect(
                host='localhost',
                user='root',
                password='',
                database="fabric",
                port=3306
            )
        except OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None
        return connection

    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """Выполняет SQL-запрос с проверкой соединения и переподключением при необходимости."""
        try:
            conn = Database.connect()
            if not conn:
                return None

            cur = conn.cursor()
            cur.execute(query, params)

            if commit:
                conn.commit()

            if fetch_one:
                result = cur.fetchone()
            elif fetch_all:
                result = cur.fetchall()
            else:
                result = None

            cur.close()
            return result

        except OperationalError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None

    @staticmethod
    def auth(login, password):
        """Аутентификация пользователя с проверкой роли."""
        query = "SELECT Users.Id, Name FROM Users join UserRoles on Users.RoleId=UserRoles.Id WHERE Login = %s AND Password = %s LIMIT 1"
        result = Database.execute_query(query, (login, password), fetch_one=True)
        if result:
            return {"id": result[0], "role": result[1]}

    @staticmethod
    def get_projects():
        """Получает список проектов."""
        query = "SELECT Id, Name FROM Products"
        result = Database.execute_query(query, fetch_all=True)
        return [(row[0], row[1]) for row in result] if result else None

    @staticmethod
    def save_project(pr_data):
        """Сохраняет проект в базу данных."""
        try:
            conn = Database.connect()
            curr = conn.cursor()
            query = f"""SELECT Id from CalculationUnits where Name='{"см"}'"""
            curr.execute(query)
            unit_id = curr.fetchone()[0]
            if pr_data[0] is None:
                curr.execute(
                    "INSERT INTO Products (Name, Grid, Width, Height, MainUnitId) VALUES (%s, %s,%s,%s, %s)",
                    (pr_data[1], pr_data[2], pr_data[3] / 10, pr_data[4] / 10, unit_id))
                pr_id = curr.lastrowid
            else:
                pr_id = pr_data[0]
                curr.execute(
                    "UPDATE Products SET Name = %s, Grid = %s, Width =%s, Height=%s WHERE Id = %s",
                    (pr_data[1], pr_data[2], pr_data[3] / 10, pr_data[4] / 10, pr_data[0]))
            conn.commit()
            conn.close()
            return pr_id
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def open_project(project_id):
        """Открывает проект по его ID."""
        query = "SELECT Id, Name, Grid FROM Products WHERE Id = %s"
        return Database.execute_query(query, (project_id,), fetch_one=True)

    @staticmethod
    def add_material(name, unit_id, material_type_id, image_id, width, height, color):
        """Добавляет новый материал в базу данных."""
        query = """
        INSERT INTO Materials (Name, UnitId, MaterialTypeId, ImageId, Width, Height, Color)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, unit_id, material_type_id, image_id, width, height, color)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def add_image(image_data):
        """Добавляет изображение в базу данных."""
        query = "INSERT INTO Images (Data) VALUES (%s)"
        return Database.execute_query(query, (image_data,), commit=True)

    @staticmethod
    def get_materials():
        """Получает список материалов."""
        query = "SELECT * FROM Materials JOIN MaterialTypes ON Materials.MaterialTypeId = MaterialTypes.Id"
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def get_image_data(image_id):
        """Получает данные изображения по его ID."""
        query = "SELECT Data FROM Images WHERE Id = %s"
        return Database.execute_query(query, (image_id,), fetch_one=True)

    @staticmethod
    def get_material_by_name(name):
        """Получает материал по его названию."""
        query = "SELECT * FROM Materials WHERE Name = %s"
        return Database.execute_query(query, (name,), fetch_one=True)

    @staticmethod
    def get_material_image_id(material_id):
        """Получает ID изображения для материала."""
        query = "SELECT ImageId FROM Materials WHERE Id = %s"
        return Database.execute_query(query, (material_id,), fetch_one=True)

    @staticmethod
    def get_last_insert_id():
        """Получает ID последней вставленной записи."""
        query = "SELECT LAST_INSERT_ID()"
        return Database.execute_query(query, fetch_one=True)

    @staticmethod
    def save_material_product_links(product_id, material_ids):
        """Сохраняет связи между материалами и продуктом в таблицу MaterialProduct."""
        conn = Database.connect()
        cursor = conn.cursor()
        try:
            for material_id in material_ids:
                print(f"Сохранение связи: MaterialId={material_id}, ProductId={product_id}")
                cursor.execute("""
                    INSERT INTO MaterialProduct (MaterialsId, ProductId)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                    MaterialsId = VALUES(MaterialsId),
                    ProductId = VALUES(ProductId)
                """, (material_id, product_id))
            conn.commit()
            print("Связи успешно сохранены.")
        except Exception as e:
            print(f"Ошибка при сохранении связей материалов и продукта: {e}")
        finally:
            conn.close()

    def get_project_id_by_order_and_project(self, order_id, project_name):
        """Возвращает ID проекта по заказу и названию проекта."""
        conn = Database.connect()
        cursor = conn.cursor()

        if order_id:
            cursor.execute("""
                SELECT p.Id
                FROM Products p
                JOIN OrderItems oi ON p.Id = oi.ProductId
                JOIN Orders o ON oi.OrderId = o.Id
                WHERE o.Id = %s AND p.Name = %s
            """, (order_id, project_name))
        else:
            cursor.execute("""
                SELECT Id
                FROM Products
                WHERE Name = %s
            """, (project_name,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return None
