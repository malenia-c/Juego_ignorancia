import pymysql


##Procedimiento para conectar y extraer información de la BD
def recupera_categoria():
    ##Se crea un objeto de conexion a la BD
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    ## Se crea un cursor para ejecutar consultas a la base de datos
    cursor = conn.cursor()
    ##Se utiliza el cursor para ejecutar la consulta sobre la tabla de categorias
    cursor.execute('select descripcion from categoria')
    ##Se crea una lista para contener las categorias extraidas de la base de datos
    categoria = cursor.fetchall()
    #cerrar la base de datos
    conn.close()
    #print(categorias)
    return categoria



## procedimiento main
def recupera_preguntas(cat):
    ##Se crea un objeto de conexion a la BD
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    ## Se crea un cursor para ejecutar consultas a la base de datos
    cursor = conn.cursor()
    ## consulta de busqueda
    consulta = 'select b.id_pregunta, b.pregunta, b.opcion1, b.opcion2, b.opcion3, b.opcion4, b.correcto, b.id_categoria '
    consulta = consulta + 'from categoria a, pregunta b '
    consulta = consulta + "where a.descripcion='" + cat + "' and b.id_categoria=a.id_categoria "
    ##Se utiliza el cursor para ejecutar la consulta sobre la tabla de preguntas
    cursor.execute(consulta)
    pregunta = cursor.fetchall()
    #print(preguntas)
    ##cerrar la base de datos
    conn.close()
    return pregunta


def tabla_categorias():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    cursor = conn.cursor()
    cursor.execute('select id_categoria, descripcion from categoria')
    cats = cursor.fetchall()
    conn.close()
    return cats


def insertar_categoria(descript):
    conn = pymysql.connect(host="locahost", user="root", passwd="", db="ignorancia")
    cursor = conn.cursor()
    cursor.execute("insert into categoria (description) values(%s)", (descript))
    conn.commit()
    conn.close


def borra_categoria(ab):
    conn= pymysql.connect(host="localhost", user="root", passwd="", bd="ignorancia")
    cursor = conn.cursor()
    cursor.execute("insert into categoria (description) values(%s)", (ab))
    conn.commit()
    conn.close


def selec_categoria(ab):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    cursor = conn.cursor()
    cursor.execute('select id_categoria, descripcion from categoria where Id_categoria=%s', (ab,))
    dato = cursor.fetchone()
    return dato


def modif_categoria(ab, descripcion):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    cursor = conn.cursor()
    cursor.execute('update categoria set descripcion=%s where Id_categoria=%s', (descripcion, ab))
    conn.commit()
    conn.close()


def tabla_preguntas(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia')
    cursor = conn.cursor()
    cursor.execute('select id_pregunta, pregunta, opcion1, opcion2, opcion3, opcion4, correcto, id_categoria from pregunta where id_categoria = %s', (id))
    preguntas = cursor.fetchall()
    conn.close()
    return preguntas

def inserta_pregunta(datos, id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia2')
    cursor = conn.cursor()
    cursor.execute(
        'insert into pregunta (pregunta, opcion1, opcion2, opcion3, opcion4, correcto, id_categoria) values (%s,%s,%s,%s,%s,%s,%s)',
        (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], id)
    )
    conn.commit()
    conn.close()

def selec_pregunta(ab):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia2')
    cursor = conn.cursor()
    cursor.execute('select id_pregunta, pregunta, opcion1, opcion2, opcion3, opcion4, correcto, id_categoria from pregunta where id=' + ab)
    dato = cursor.fetchone()
    return dato

def borra_pregunta(ab):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia2')
    cursor = conn.cursor()
    cursor.execute('delete from pregunta where id_pregunta=%s', (ab,))
    conn.commit()
    conn.close()

def modif_pregunta(ab, datos):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='ignorancia2')
    cursor = conn.cursor()
    cursor.execute('update pregunta set pregunta=%s, opcion1=%s, opcion2=%s, opcion3=%s, opcion4=%s, correcto=%s where id_pregunt=%s',
                   (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], ab))
    conn.commit()
    conn.close()