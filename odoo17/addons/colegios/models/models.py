# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore

class alumno(models.Model):
    _name = 'colegios.alumno'
    _description = 'alumno'

    ci = fields.Char(string="CI")
    nombres = fields.Char(string="Nombres", required=True)
    ap_paterno = fields.Char(string="Apellido Paterno")
    ap_materno = fields.Char(string="Apellido Materno")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    genero = fields.Selection(
        [
            ("masculino","masculino"),
            ("femenino","femenino"),
        ],
        string = "Alumno",
        default = "masculino",
        required = True,
     )
    apoderado_nombre = fields.Char(string="Apoderado", related="parentesco_id.apoderado_id.nombre", readonly=True)
    parentesco_descripcion = fields.Text(string="Parentesco", compute="_compute_parentesco_descripcion")
    parentesco_id = fields.One2many("colegios.parentesco", "alumno_id", string="Parentescos")

    @api.depends("parentesco_id")
    def _compute_parentesco_descripcion(self):
        for alumno in self:
            descripcion_parentescos = ", ".join(parentesco.descripcion for parentesco in alumno.parentesco_id)
            alumno.parentesco_descripcion = descripcion_parentescos

class profesor(models.Model):
    _name = 'colegios.profesor'
    _description = 'profesor'

    ci = fields.Char(string="CI")
    nombre = fields.Char(string="Nombre", required=True)
    ap_paterno = fields.Char(string="Apellido Paterno")
    ap_materno = fields.Char(string="Apellido Materno")
    direccion = fields.Char(string="Dirección")
    genero = fields.Selection(
        [
            ("masculino","masculino"),
            ("femenino","femenino"),
        ],
        string = "Profesor",
        default = "masculino",
        required = True,
     )
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    rda = fields.Integer(string="RDA")
    telefono = fields.Char(string="Teléfono")
    correo = fields.Char(string="Correo")

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
    #descripcion = fields.Char(string="Descripción")
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

class cursogestion(models.Model):
    _name = 'colegios.cursogestion'
    _description = 'Curso - Gestión'

    nombre = fields.Many2one('colegios.gestion', string="Gestión", required=True)
    description = fields.Many2one('colegios.curso', string="Curso", required=True)
    turno = fields.Char(string="Turno")

class materia(models.Model):
    _name = 'colegios.materia'
    _description = 'materia'

    nombre = fields.Char(string="Nombre")
    distintivo = fields.Integer(string="Distintivo")

class especialidad(models.Model):
    _name = 'colegios.especialidad'
    _description = 'especialidad'

    descripcion = fields.Char(string="Descripción")

class profesorespecialidad(models.Model):
    _name = 'colegios.profesorespecialidad'
    _description = 'profesor - Especialidad'

    profesor = fields.Many2one('colegios.profesor', string="Profesor", required=True)
    especialidad = fields.Many2one('colegios.especialidad', string="Especialidad", required=True)

class horario(models.Model):
    _name = 'colegios.horario'
    _description = 'horario'

    dia = fields.Char(string="Día")
    hora_ini = fields.Float(string="Hora de Inicio")
    hora_fin = fields.Float(string="Hora de Fin")

class materiacursogestion(models.Model):
    _name = 'colegios.materiacursogestion'
    _description = 'materia - Curso - Gestión'

    gestion_id = fields.Many2one('colegios.cursogestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)
    materia_id = fields.Many2one('colegios.materia', string="Materia", required=True)
    profesor_id = fields.Many2one('colegios.profesor', string="Profesor", required=True)

class paralelo(models.Model):
    _name = 'colegios.paralelo'
    _description = 'paralelo'

    descripcion = fields.Char(string="Descripción")

class materiacursogestionparalelo(models.Model):
    _name = 'colegios.materiacursogestionparalelo'
    _description = 'materia - Curso - Gestión - Paralelo'

    materia_id = fields.Many2one('colegios.materia', string="Materia", required=True)
    gestion_id = fields.Many2one('colegios.cursogestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)
    paralelo_id = fields.Many2one('colegios.paralelo', string="Paralelo", required=True)

class materiacursogestionparalelohorario(models.Model):
    _name = 'colegios.materiacursogestionparalelohorario'
    _description = 'materia - Curso - Gestión - Paralelo - Horario'

    materia_id = fields.Many2one('colegios.materia', string="Materia", required=True)
    gestion_id = fields.Many2one('colegios.cursogestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)
    paralelo_id = fields.Many2one('colegios.paralelo', string="Paralelo", required=True)
    horario_id = fields.Many2one('colegios.horario', string="Horario", required=True)

class periodo(models.Model):
    _name = 'colegios.periodo'
    _description = 'periodo'
    tipo = fields.Selection(
        [
            ("bimestre","Bimestre"),
            ("trimestre","Trimeste"),
            ("semestre","Semestre"),
        ],
        string = "Periodo",
        default = "Bimestre",
        required = True,
     )
    
class nota(models.Model):
    _name = 'colegios.nota'
    _description = 'nota'

    alumno_id = fields.Many2one('colegios.alumno', string="Alumno", required=True)
    gestion_id = fields.Many2one('colegios.gestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)
    materia_id = fields.Many2one('colegios.materia', string="Materia", required=True)
    periodo_id = fields.Many2one('colegios.periodo', string="Periodo", required=True)
    promedio_periodo = fields.Float(string="Promedio del Periodo")
    descripcion = fields.Char(string="Descripción")

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

    monto = fields.Float(string="Monto")
    fecha = fields.Date(string="Fecha")

class inscripcion(models.Model):
    _name = 'colegios.inscripcion'
    _description = 'inscripción'

    fecha = fields.Date(string="Fecha")
    alumno_id = fields.Many2one('colegios.alumno', string="Alumno", required=True)
    secretaria_id = fields.Many2one('colegios.secretaria', string="Secretaria", required=True)
    matricula_id = fields.Many2one('colegios.matricula', string="Matricula", required=True)

class inscripcioncursogestion(models.Model):
    _name = 'colegios.inscripcioncursogestion'
    _description = 'inscripción - Curso - Gestión'

    inscripcion_id = fields.Many2one('colegios.inscripcion', string="Inscripción", required=True)
    gestion_id = fields.Many2one('colegios.gestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)

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

    inscripcion_id = fields.Many2one('colegios.inscripcion', string="Inscripción", required=True)
    lugar_nac_id = fields.Many2one('colegios.lugar_nacimiento', string="Lugar de Nacimiento")
    direccionactual_id = fields.Many2one('colegios.direccion_actual', string="Dirección Actual")

class pagomensual(models.Model):
    _name = 'colegios.pagomensual'
    _description = 'pago mensual'

    alumno_id = fields.Many2one('colegios.alumno', string="Alumno", required=True)
    gestion_id = fields.Many2one('colegios.gestion', string="Gestión", required=True)
    curso_id = fields.Many2one('colegios.curso', string="Curso", required=True)
    mes = fields.Char(string="Mes")
    monto = fields.Float(string="Monto")
