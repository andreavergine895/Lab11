from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione



class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def get_all_rifugi():

        conn=DBConnect.get_connection()
        result={}  #creo diz risultati

        cursor=conn.cursor(dictionary=True)
        query= "SELECT * FROM rifugio"
        cursor.execute(query)

        for row in cursor:
            result[row["id"]]=Rifugio(**row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni_fino_anno(year:int):

        conn=DBConnect.get_connection()
        result = []  #creo la lista dei risultati
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione WHERE anno <= %s"
        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

