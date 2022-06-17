import psycopg2
from psycopg2 import Error
from image import Image


class AppDb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="kbftwbht",
                                               password="LYRC4ctQmbtkglf33Jmtuns_2L8HpUwD",
                                               host="tyke.db.elephantsql.com",
                                               port="5432",
                                               database="kbftwbht")
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You're connected to - ", record, "\n")

            self.create_table()

        except (Exception, Error) as error:
            print("Server error", error)

    def create_table(self):
        try:
            create_table_query = ("CREATE TABLE IF NOT EXISTS inbox (\n"
                                  "                            id SERIAL PRIMARY KEY,\n"
                                  "                            request_code varchar(36) NOT NULL,\n"
                                  "                            file_name varchar(150) NOT NULL,\n"
                                  "                            reg_date timestamp NOT NULL\n"
                                  "                            );")

            self.cursor.execute(create_table_query)
            self.connection.commit()
            print('Table was created')

        except (Exception, Error) as error:
            print("Server error", error)

    def insert_image(self, image: Image):
        try:
            insert_query = (f'INSERT INTO inbox(request_code, file_name, reg_date) '
                            f'VALUES (\'{image.request_code}\', \'{image.file_name}\', \'{image.reg_date}\')')
            print(insert_query)
            self.cursor.execute(insert_query)
            self.connection.commit()
            print("Row was successfully added")

        except (Exception, Error) as error:
            print("Server error", error)

    def get_images(self, request_code):
        try:
            select_images_query = f'SELECT request_code, file_name, reg_date ' \
                                  f'FROM inbox WHERE request_code = \'{request_code}\''
            print(select_images_query)

            self.cursor.execute(select_images_query)
            record = self.cursor.fetchall()

            return record

        except (Exception, Error) as error:
            print("Server error", error)

    def delete_images(self, request_code):
        try:
            delete_images_query = f'DELETE FROM inbox WHERE request_code = \'{request_code}\''

            self.cursor.execute(delete_images_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Server error", error)


if __name__ == '__main__':
    db = AppDb()
    print(db.get_images('1d018bf5-4adc-46ad-8245-3c0a555109bf'))
