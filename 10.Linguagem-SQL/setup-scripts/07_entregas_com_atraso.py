import pymysql
import pymysql.cursors

def gerar_entregas_com_atraso():
    # Configuração da conexão
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='database-dev-mysql',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # A sua consulta SQL para selecionar dados
            sql_query = """
            WITH amostra_15perc_pedido AS (
                SELECT *
                FROM pedido
                ORDER BY RAND()
                    LIMIT 75
            ),
            calc_dataprevista AS (
                SELECT
                    id AS pedido_id,
                    DATE_ADD(data_pedido, INTERVAL 5 DAY) AS data_prevista
                FROM amostra_15perc_pedido
            ),
            calc_dataentrega AS (
                SELECT
                    p.pedido_id,
                    p.data_prevista,
                    DATE_ADD(p.data_prevista, INTERVAL FLOOR(1 + RAND()*(3-1)) DAY) AS data_entrega
                FROM calc_dataprevista p
            ),
            amostra_transportadora AS (
                SELECT id AS transportadora_id
                FROM transportadora
                ORDER BY RAND()
                    LIMIT 15
            ),
            amostra_entrega_com_atraso AS (
                SELECT
                    d.pedido_id,
                    t.transportadora_id,
                    d.data_prevista,
                    d.data_entrega
                FROM calc_dataentrega d
                JOIN (
                    SELECT
                        transportadora_id,
                        @row_number:=@row_number + 1 AS rn
                    FROM amostra_transportadora, (SELECT @row_number:=0) rn
                ) t ON (d.pedido_id % 15) + 1 = t.rn
            )
            SELECT pedido_id, transportadora_id, data_prevista, data_entrega FROM amostra_entrega_com_atraso;
            """
            cursor.execute(sql_query)
            results = cursor.fetchall()

            # Executar o comando INSERT diretamente
            if results:
                insert_query = "INSERT INTO entrega (pedido_id, transportadora_id, data_prevista, data_entrega) VALUES (%s, %s, %s, %s)"
                for result in results:
                    cursor.execute(insert_query, (result['pedido_id'], result['transportadora_id'], result['data_prevista'], result['data_entrega']))
                connection.commit()  # Garante que as mudanças sejam salvas no banco de dados

            print(f"Inserted {len(results)} rows into Entrega.")

    finally:
        connection.close()


def main():
    gerar_entregas_com_atraso()


if __name__ == "__main__":
    main()
