from database.DB_connect import DBConnect
from model.countries import Country


class DAO():
    @staticmethod
    def getCountriesByYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)  # sto dando la forma di dizionario per fare l'unpack dei dati

        result = []
        query = """SELECT DISTINCT c.StateAbb, c.CCode, c.StateNme
                    FROM country AS c
                    JOIN contiguity AS s ON c.CCode = s.state1no OR c.CCode = s.state2no
                    WHERE s.year < %s
                    """
                    #UNION
                    
                    #SELECT DISTINCT c.StateAbb, c.CCode, c.StateNme
                    #FROM country AS c
                    #JOIN contiguity2006 AS v ON c.CCode = v.state1no OR c.CCode = v.state2no
                    #WHERE v.year < %s

        cursor.execute(query, (year, ))
        # cursor.fetchall() mi crea una
        for row in cursor:
            result.append(Country(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgesByYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)  # sto dando la forma di dizionario per fare l'unpack dei dati

        result = []
        query = """
                select distinct c.state1no, state2no 
                from contiguity c 
                where c.`year` < %s and c.conttype = 1 and c.state1no < state2no
                
                
                """
        #union
                #select distinct s.state1no, s.state2no
                #from contiguity2006 s
                #where s.`year` < %s and s.conttype = 1 and s.state1no < s.state2no



        cursor.execute(query, (year, ))
        # cursor.fetchall() mi crea una
        for row in cursor:
            result.append((row["state1no"], row["state2no"]))
        cursor.close()
        conn.close()
        return result