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
            print("Server connection error", error)

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

        except (Exception, Error) as error:
            print("Error creating table", error)

    def insert_image(self, image: Image):
        try:
            insert_query = (f'INSERT INTO inbox(request_code, file_name, reg_date) '
                            f'VALUES (\'{image.request_code}\', \'{image.file_name}\', \'{image.reg_date}\')')
            self.cursor.execute(insert_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while inserting data", error)

    def get_images(self, request_code):
        try:
            select_images_query = f'SELECT * FROM inbox WHERE request_code = \'{request_code}\''

            self.cursor.execute(select_images_query)
            record = self.cursor.fetchall()

            return record

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def delete_images(self, request_code):
        try:
            delete_images_query = f'DELETE FROM inbox WHERE request_code = \'{request_code}\''

            self.cursor.execute(delete_images_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while deleting data", error)
