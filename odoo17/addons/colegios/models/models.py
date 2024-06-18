# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError # type: ignore
from odoo import models, fields, api # type: ignore

class alumno(models.Model):
    _name = 'colegios.alumno'
    _description = 'alumno'

    fotografia = fields.Binary(string="Fotografia")
    ci = fields.Char(string="CI", required=True, copy=False)
    nombres = fields.Char(string="Nombres", required=True)
    ap_paterno = fields.Char(string="Apellido Paterno", required=True)
    ap_materno = fields.Char(string="Apellido Materno", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    genero = fields.Selection(
        [
            ("masculino","masculino"),
            ("femenino","femenino"),
        ],
        string = "Genero",
        default = "masculino",
        required = True,
     )
    nota_id = fields.One2many("colegios.nota","alumno_id",string = "Notas")
    profesor = fields.One2many("colegios.nota","profesor_id", string="Profesores")
    apoderado_nombre = fields.Char(string="Apoderado", related="parentesco_id.apoderado_id.nombre", readonly=True)
    parentesco_descripcion = fields.Text(string="Parentesco", compute="_compute_parentesco_descripcion")
    parentesco_id = fields.One2many("colegios.parentesco", "alumno_id", string="Parentescos")

    curso_id = fields.Many2one("colegios.curso", string="Curso")

    # Restricciones únicas
    _sql_constraints = [
        ("unique_ci", "unique(ci)", "El número de CI debe ser único por alumno.")
    ]

    @api.depends("parentesco_id")
    def _compute_parentesco_descripcion(self):
        for alumno in self:
            descripcion_parentescos = ", ".join(parentesco.descripcion for parentesco in alumno.parentesco_id)
            alumno.parentesco_descripcion = descripcion_parentescos


      # Validaciones adicionales
    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for alumno in self:
            if alumno.fecha_nacimiento and alumno.fecha_nacimiento > fields.Date.today():
                raise ValidationErr('La fecha de nacimiento no puede estar en el futuro.')


class profesor(models.Model):
    _name = 'colegios.profesor'
    _description = 'profesor'

    ci = fields.Char(string="CI")
    nombre = fields.Char(string="Nombre", required=True)
    fotografia = fields.Binary(string="Fotografia")
    ap_paterno = fields.Char(string="Apellido Paterno")
    ap_materno = fields.Char(string="Apellido Materno")
    direccion = fields.Char(string="Dirección")
    genero = fields.Selection(
        [
            ("masculino","masculino"),
            ("femenino","femenino"),
        ],
        string = "Genero",
        default = "masculino",
        required = True,
     )
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    rda = fields.Integer(string="RDA")
    telefono = fields.Char(string="Teléfono")
    correo = fields.Char(string="Correo")
    alumno =fields.One2many("colegios.nota", "alumno_id", string="Alumnos")



class apoderado(models.Model):
    _name = 'colegios.apoderado'
    _description = 'apoderado'

    ci = fields.Char(string="CI")
    nombre = fields.Char(string="Nombre", required=True)
    ap_paterno = fields.Char(string="Apellido Paterno")
    ap_materno = fields.Char(string="Apellido Materno")
    genero = fields.Selection(
        [
            ("masculino","masculino"),
            ("femenino","femenino"),
        ],
        string = "Apoderado",
        default = "masculino",
        required = True,
     )
    ocupacion = fields.Char(string="Ocupación")
    grado_instruccion = fields.Char(string="Grado de Instrucción")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    telefono = fields.Char(string="Teléfono")

class gestion(models.Model):
    _name = 'colegios.gestion'
    _description = 'gestion'

    nombre = fields.Char(string="Nombre")
    fecha_inicio = fields.Date(string="Fecha de Inicio")
    fecha_fin = fields.Date(string="Fecha de Fin")

class parentesco(models.Model):
    _name = 'colegios.parentesco'
    _description = 'parentesco'

    alumno_id = fields.Many2one("colegios.alumno", string="Alumno", required=True)
    apoderado_id = fields.Many2one("colegios.apoderado", string="Apoderado", required=True)
    #descripcion = fields.Char(string="Descripcion")
    descripcion = fields.Selection(
        [
            ("padre","padre"),
            ("madre","madre"),
            ("tio","tio"),
            ("abuelo","abuelo"),
            ("hermano","hermano"),
        ],
        string = "Descripcion",
        default = "padre",
        required = True,
     )

class curso(models.Model):
    _name = 'colegios.curso'
    _description = 'curso'

    nombre = fields.Char(string="Nombre")
    nota_id = fields.One2many("colegios.nota", "curso_id", string="Notas")

class cursogestion(models.Model):
    _name = 'colegios.cursogestion'
    _description = 'Curso - Gestión'

    gestion_id = fields.Many2one('colegios.gestion', string='Gestión', required=True)
    curso_id= fields.Many2one('colegios.curso', string='Curso', required=True)
    turno = fields.Selection([('mañana', 'Mañana'), ('tarde', 'Tarde')], string='Turno')

class materia(models.Model):
    _name = 'colegios.materia'
    _description = 'materia'

    nombre = fields.Char(string="Nombre")
    distintivo = fields.Integer(string="Distintivo")
    nota_ids = fields.One2many("colegios.nota", "materia_id", string ="Notas")
    alumno_ids = fields.Many2many("colegios.alumno",string="Alumnos", compute = "_compute_alumno_ids")

    @api.depends("nota_ids","nota_ids.alumno_id")
    def _compute_alumno_ids(self):
        for materia in self:
            materia.alumno_ids = materia.nota_ids.mapped("alumno_id")

class especialidad(models.Model):
    _name = 'colegios.especialidad'
    _description = 'especialidad'

    descripcion = fields.Char(string="Descripción")

class profesorespecialidad(models.Model):
    _name = 'colegios.profesorespecialidad'
    _description = 'profesor - Especialidad'

    profesor_id = fields.Many2one("colegios.profesor", string="Profesor", required=True)
    especialidad_id = fields.Many2one("colegios.especialidad", string="Especialidad", required=True)

class horario(models.Model):
    _name = 'colegios.horario'
    _description = 'horario'

    dia = fields.Char(string="Día")
    hora_ini = fields.Float(string="Hora de Inicio")
    hora_fin = fields.Float(string="Hora de Fin")

class materiacursogestion(models.Model):
    _name = 'colegios.materiacursogestion'
    _description = 'materia - Curso - Gestión'

    gestion_id = fields.Many2one("colegios.cursogestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    materia_id = fields.Many2one("colegios.materia", string="Materia", required=True)
    profesor_id = fields.Many2one("colegios.profesor", string="Profesor", required=True)

class paralelo(models.Model):
    _name = 'colegios.paralelo'
    _description = 'paralelo'

    descripcion = fields.Char(string="Descripción")

class materiacursogestionparalelo(models.Model):
    _name = 'colegios.materiacursogestionparalelo'
    _description = 'materia - Curso - Gestión - Paralelo'

    materia_id = fields.Many2one("colegios.materia", string="Materia", required=True)
    gestion_id = fields.Many2one("colegios.cursogestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    paralelo_id = fields.Many2one("colegios.paralelo", string="Paralelo", required=True)

class materiacursogestionparalelohorario(models.Model):
    _name = 'colegios.materiacursogestionparalelohorario'
    _description = 'materia - Curso - Gestión - Paralelo - Horario'

    materia_id = fields.Many2one("colegios.materia", string="Materia", required=True)
    gestion_id = fields.Many2one("colegios.cursogestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    paralelo_id = fields.Many2one("colegios.paralelo", string="Paralelo", required=True)
    horario_id = fields.Many2one("colegios.horario", string="Horario", required=True)

class periodo(models.Model):
    _name = 'colegios.periodo'
    _description = 'periodo'
    descripcion = fields.Char(string="Descripcion")
    
class nota(models.Model):
    _name = 'colegios.nota'
    _description = 'nota'

    alumno_id = fields.Many2one("colegios.alumno", string="Alumno", required=True)
    gestion_id = fields.Many2one("colegios.gestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    materia_id = fields.Many2one("colegios.materia", string="Materia", required=True)
    profesor_id = fields.Many2one("colegios.profesor", string="Profesor", required=True)
    periodo_id = fields.Many2one("colegios.periodo", string="Periodo", required=True)
    promedio_periodo = fields.Integer(string="Promedio del Periodo")
    descripcion = fields.Char(string="Descripción", compute= "_compute_descripcion")

    @api.depends("promedio_periodo")
    def _compute_descripcion(self):
        for record in self:
            if record.promedio_periodo >=51:
                record.descripcion = "Aprobado"
            else:
                record.descripcion = "Reprobado"
    # Campos relacionados para mostrar los nombres en lugar de IDs
    alumno_name = fields.Char(string="Nombre del Alumno", related="alumno_id.nombres", readonly=True)
    alumno_ap_pater = fields.Char(string="Apellido del Alumno", related="alumno_id.ap_paterno", readonly=True)
    gestion_name = fields.Char(string="Nombre de la Gestión", related="gestion_id.nombre", readonly=True)
    curso_name = fields.Char(string="Nombre del Curso", related="curso_id.nombre", readonly=True)
    materia_name = fields.Char(string="Nombre de la Materia", related="materia_id.nombre", readonly=True)
    profesor_name = fields.Char(string="Nombre del profesor", related="profesor_id.nombre", readonly=True)
    periodo_name = fields.Char(string="Nombre del Periodo", related="periodo_id.descripcion", readonly=True)
   
    
    def consultar_notas(self):
        consulta_sql = """
            SELECT a.id, a.ci, a.nombres, a.ap_paterno, a.ap_materno, g.nombre, c.nombre, m.nombre, n.promedio_periodo
            FROM colegios_nota AS n
            INNER JOIN colegios_alumno AS a ON n.alumno_id = a.id
            INNER JOIN colegios_gestion AS g ON n.gestion_id = g.id
            INNER JOIN colegios_curso AS c ON n.curso_id = c.id
            INNER JOIN colegios_materia AS m ON n.materia_id = m.id
        """
        self.env.cr.execute(consulta_sql)
        resultados = self.env.cr.fetchall()
        return resultados
    
    def consultar_notas22(self, alumno_id):
        consulta_sql = """
            SELECT a.id, a.ci, a.nombres, a.ap_paterno, a.ap_materno, g.nombre, c.nombre, m.nombre, n.promedio_periodo
            FROM colegios_nota AS n
            INNER JOIN colegios_alumno AS a ON n.alumno_id = a.id
            INNER JOIN colegios_gestion AS g ON n.gestion_id = g.id
            INNER JOIN colegios_curso AS c ON n.curso_id = c.id
            INNER JOIN colegios_materia AS m ON n.materia_id = m.id
            WHERE n.alumno_id =%s
        """
        self.env.cr.execute(consulta_sql, alumno_id)
        resultados = self.env.cr.fetchall()
        return resultados
    

class secretaria(models.Model):
    _name = 'colegios.secretaria'
    _description = 'secretaria'

    nombre = fields.Char(string="Nombre", required=True)
    ap_paterno = fields.Char(string="Apellido Paterno")
    ap_materno = fields.Char(string="Apellido Materno")
    direccion = fields.Char(string="Dirección")
    telefono = fields.Char(string="Teléfono")

class matricula(models.Model):
    _name = 'colegios.matricula'
    _description = 'matricula'

    monto = fields.Integer(string="Monto")
    fecha = fields.Date(string="Fecha")

class inscripcion(models.Model):
    _name = 'colegios.inscripcion'
    _description = 'inscripción'

    fecha = fields.Date(string="Fecha")
    alumno_id = fields.Many2one("colegios.alumno", string="Alumno", required=True)
    secretaria_id = fields.Many2one("colegios.secretaria", string="Secretaria", required=True)
    matricula_id = fields.Many2one("colegios.matricula", string="Matricula", required=True)

    alumno_name = fields.Char(string="Nombre del Alumno", related="alumno_id.nombres", readonly=True)
    secretaria_name = fields.Char(string="Nombre de le Secretaria", related="secretaria_id.nombre", readonly=True)
    matricula_monto = fields.Integer(string="Costo de la Matricula", related="matricula_id.monto", readonly=True)


class inscripcioncursogestion(models.Model):
    _name = 'colegios.inscripcioncursogestion'
    _description = 'inscripción - Curso - Gestión'

    inscripcion_id = fields.Many2one("colegios.inscripcion", string="Inscripción", required=True)
    gestion_id = fields.Many2one("colegios.gestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)

class lugarnac(models.Model):
    _name = 'colegios.lugarnac'
    _description = 'lugar de Nacimiento'

    pais = fields.Char(string="País")
    departamento = fields.Char(string="Departamento")
    provincia = fields.Char(string="Provincia")
    localidad = fields.Char(string="Localidad")

class direccionactual(models.Model):
    _name = 'colegios.direccionactual'
    _description = 'dirección Actual'

    departamento = fields.Char(string="Departamento")
    provincia = fields.Char(string="Provincia")
    municipio = fields.Char(string="Municipio")
    localidad = fields.Char(string="Localidad")
    zona = fields.Char(string="Zona")
    avenida = fields.Char(string="Avenida")
    n_vivienda = fields.Integer(string="Número de Vivienda")

class rude(models.Model):
    _name = 'colegios.rude'
    _description = 'RUDE'

    codigo_rude = fields.Integer(string='Código RUDE', required=True)
    inscripcion_id = fields.Many2one("colegios.inscripcion", string="Inscripción", required=True)
    lugar_nac_id = fields.Many2one("colegios.lugar_nacimiento", string="Lugar de Nacimiento")
    direccionactual_id = fields.Many2one("colegios.direccion_actual", string="Dirección Actual")

class pagomensual(models.Model):
    _name = 'colegios.pagomensual'
    _description = 'pago mensual'

    alumno_id = fields.Many2one("colegios.alumno", string="Alumno", required=True)
    gestion_id = fields.Many2one("colegios.gestion", string="Gestión", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    mes = fields.Char(string="Mes")
    monto = fields.Integer(string="Monto")
    estado = fields.Char(string="Estado", compute = "_compute_estado")

    @api.depends("monto")
    def _compute_estado(self):
        for record in self:
            if record.estado == 0 or record.monto == 10 or record.monto == 15 or record.monto == 19 or record.monto == 1 or record.monto == 2:
                record.estado = "Deudor"
            else:
                record.estado = "Cancelado"

    alumno_name = fields.Char(string="Nombre del Alumno", related="alumno_id.nombres", readonly=True)
    gestion_name = fields.Char(string="Nombre de la Gestion", related="gestion_id.nombre", readonly=True)
    curso_name = fields.Char(string="Nombre del Curso", related="curso_id.nombre", readonly=True)

class NotaPersonal(models.Model):
    _name = 'colegios.nota.personal'
    _description = 'Nota Personal'

    alumno_id = fields.Many2one("colegios.alumno", string="Alumno", required=True)
    curso_id = fields.Many2one("colegios.curso", string="Curso", required=True)
    materia_id = fields.Many2one("colegios.materia", string="Materia", required=True)
    promedio_periodo = fields.Integer(string="Promedio del Periodo")
    descripcion = fields.Char(string="Descripción", compute= "_compute_descripcion")

    @api.depends("promedio_periodo")
    def _compute_descripcion(self):
        for record in self:
            if record.promedio_periodo >=51:
                record.descripcion = "Aprobado"
            else:
                record.descripcion = "Reprobado"
    def consultar_notas(self):
        consulta_sql = """
            SELECT alumno.nombres AS nombre_alumno, materia.nombre AS nombre_materia,
                   curso.nombre AS nombre_curso, nota.promedio_periodo AS promedio_periodo,
                   nota.descripcion AS estado
            FROM colegios_nota_personal nota
            INNER JOIN colegios_alumno alumno ON nota.alumno_id = alumno.id
            INNER JOIN colegios_materia materia ON nota.materia_id = materia.id
            INNER JOIN colegios_curso curso ON nota.curso_id = curso.id
        """
        self.env.cr.execute(consulta_sql)
        resultados = self.env.cr.dictfetchall()
        return resultados
    # Campos relacionados para mostrar los nombres en lugar de IDs
    alumno_name = fields.Char(string="Nombre del Alumno", related="alumno_id.nombres", readonly=True)
    curso_name = fields.Char(string="Nombre del Curso", related="curso_id.nombre", readonly=True)
    materia_name = fields.Char(string="Nombre de la Materia", related="materia_id.nombre", readonly=True)   
