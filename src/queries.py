# Obtiene todos las repuestas de la pregunta 1
quest1_q1 = '''
   SELECT * FROM Respuesta
   WHERE num_pregunta = 1;
'''

# Obtiene la carrera de los estudiantes que conocen el EIU
quest1_q2 = '''
    SELECT R.num_pregunta, R.num_opcion, O.titulo
    FROM Respuesta R, Opcion O
    WHERE (R.num_opcion = O.num_opcion)
    AND   (R.num_pregunta = O.num_pregunta)
    AND   (R.num_pregunta = 3)
    AND   (R.num_encuesta IN (SELECT num_encuesta
                          FROM Respuesta
                          WHERE num_pregunta = 1
                          AND   num_opcion = 1));
'''

# Obtiene la carrera de los estudiantes que no conocen el EIU
quest1_q3 = '''
    SELECT R.num_pregunta, R.num_opcion, O.titulo
    FROM Respuesta R, Opcion O
    WHERE (R.num_opcion = O.num_opcion)
    AND   (R.num_pregunta = O.num_pregunta)
    AND   (R.num_pregunta = 3)
    AND   (R.num_encuesta IN (SELECT num_encuesta
                          FROM Respuesta
                          WHERE num_pregunta = 1
                          AND   num_opcion = 2));
'''

# Obtiene el semestre de los estudiantes que conocen el EIU
quest1_q4 = '''
    SELECT R.num_pregunta, R.num_opcion, O.titulo
    FROM Respuesta R, Opcion O
    WHERE (R.num_opcion = O.num_opcion)
    AND   (R.num_pregunta = O.num_pregunta)
    AND   (R.num_pregunta = 2)
    AND   (R.num_encuesta IN (SELECT num_encuesta
                          FROM Respuesta
                          WHERE num_pregunta = 1
                          AND   num_opcion = 1));
'''

# Obtiene el semestre de los estudiantes que no conocen el EIU
quest1_q5 = '''
    SELECT R.num_pregunta, R.num_opcion, O.titulo
    FROM Respuesta R, Opcion O
    WHERE (R.num_opcion = O.num_opcion)
    AND   (R.num_pregunta = O.num_pregunta)
    AND   (R.num_pregunta = 2)
    AND   (R.num_encuesta IN (SELECT num_encuesta
                          FROM Respuesta
                          WHERE num_pregunta = 1
                          AND   num_opcion = 2));
'''

# Obtiente todas las respuestas de la pregunta 6
quest2_q1 = '''
     SELECT respuesta
     FROM Respuesta
     WHERE num_pregunta = 6;
'''

# Obtiente todas las respuestas de la pregunta 7
quest3_q1 = '''
     SELECT respuesta
     FROM Respuesta
     WHERE num_pregunta = 7;
'''