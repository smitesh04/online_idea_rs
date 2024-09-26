import pymysql

class DbConfig():
    con = pymysql.Connect(host='localhost', user='root', password='actowiz', database='online_idea_rs')
    cur = con.cursor(pymysql.cursors.DictCursor)
    data_table = 'data'

    qr = f'''
        CREATE TABLE IF NOT EXISTS {data_table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            size VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            sku VARCHAR(255) NOT NULL,
            brand VARCHAR(255) NOT NULL,
            product_type VARCHAR(255) NOT NULL,
            currency VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            mrp VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL,
  UNIQUE KEY `sku` (`sku`))
    '''

    cur.execute(qr)
    con.commit()