# -*- coding: utf-8 -*-

from odoo import models, fields # type: ignore


class UnidadEducativa(models.Model):
    _name = 'colegio.unidadEducativa'
    _description = 'Unidad Educativa'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    tipo = fields.Char(string='Tipo', required=True)
    gestion_ids = fields.One2many('colegio.gestion', 'unidad_educativa_id', string='Gestiones')


class TipoGestion(models.Model):
    _name = 'colegio.tipoGestion'
    _description = 'Tipo de Gestión'

    nombre = fields.Char(string='Nombre', required=True)

class Gestion(models.Model):
    _name = 'colegio.gestion'
    _description = 'Gestión'

    id = fields.Integer(string='ID', required=True)
    anio = fields.Integer(string='Año', required=True)
    tipo_gestion_id = fields.Many2one('colegio.tipoGestion', string='Tipo de Gestión', required=True)
    unidad_educativa_id = fields.Many2one('colegio.unidadEducativa', string='Unidad Educativa', required=True)
    nivel_gestion_ids = fields.One2many('colegio.nivelGestion', 'gestion_id', string='Niveles de Gestión')


class NivelGestion(models.Model):
    _name = 'colegio.nivelGestion'
    _description = 'Nivel de Gestión'

    id = fields.Integer(string='ID', required=True)
    gestion_id = fields.Many2one('colegio.gestion', string='Gestión', required=True)
    nivel_id = fields.Many2one('colegio.nivel', string='Nivel', required=True)

class Nivel(models.Model):
    _name = 'colegio.nivel'
    _description = 'Nivel'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    nivel_gestion_ids = fields.One2many('colegio.nivelGestion', 'nivel_id', string='Niveles de Gestión')


class Profesor(models.Model):
    _name = 'colegio.profesor'
    _description = 'Profesor'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    telefono = fields.Char(string='Teléfono')
    sueldo = fields.Integer(string='Sueldo')
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    asignaturas = fields.Char(string='Asignaturas')
    carga_horaria = fields.Integer(string='Carga Horaria')
    curso_ids = fields.One2many('colegio.curso', 'tutor_id', string='Cursos')


class Curso(models.Model):
    _name = 'colegio.curso'
    _description = 'Curso'

    id = fields.Integer(string='ID', required=True)
    nro = fields.Integer(string='Número', required=True)
    paralelo = fields.Char(string='Paralelo', required=True)
    tutor_id = fields.Many2one('colegio.profesor', string='Tutor')
    nivel_gestion_id = fields.Many2one('colegio.nivelGestion', string='Nivel de Gestión')
    inscripcion_ids = fields.One2many('colegio.inscripcion', 'curso_id', string='Inscripciones')


class Inscripcion(models.Model):
    _name = 'colegio.inscripcion'
    _description = 'Inscripción'

    id = fields.Integer(string='ID', required=True)
    curso_id = fields.Many2one('colegio.curso', string='Curso', required=True)
    estudiante_id = fields.Many2one('colegio.estudiante', string='Estudiante', required=True)
    resumen_calificacion_ids = fields.One2many('colegio.resumenCalificacion', 'inscripcion_id', string='Resumenes de Calificaciones')


class Estudiante(models.Model):
    _name = 'colegio.estudiante'
    _description = 'Estudiante'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    RUE = fields.Char(string='RUE')
    CI = fields.Char(string='CI')
    correo = fields.Char(string='Correo')
    inscripcion_ids = fields.One2many('colegio.inscripcion', 'estudiante_id', string='Inscripciones')
    parentesco_ids = fields.One2many('colegio.parentesco', 'estudiante_id', string='Parentescos')


class Parentesco(models.Model):
    _name = 'colegio.parentesco'
    _description = 'Parentesco'

    id = fields.Integer(string='ID', required=True)
    estudiante_id = fields.Many2one('colegio.estudiante', string='Estudiante', required=True)
    apoderado_id = fields.Many2one('colegio.apoderado', string='Apoderado', required=True)



class Apoderado(models.Model):
    _name = 'colegio.apoderado'
    _description = 'Apoderado'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    telefono = fields.Char(string='Teléfono')
    direccion = fields.Char(string='Dirección')
    relacion = fields.Char(string='Relación')
    correo = fields.Char(string='Correo')
    parentesco_ids = fields.One2many('colegio.parentesco', 'apoderado_id', string='Parentescos')


class Asignatura(models.Model):
    _name = 'colegio.asignatura'
    _description = 'Asignatura'

    id = fields.Integer(string='ID', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    asignacion_ids = fields.One2many('colegio.asignacion', 'asignatura_id', string='Asignaciones')


class PlanEstudio(models.Model):
    _name = 'colegio.planEstudio'
    _description = 'Plan de Estudio'

    id = fields.Integer(string='ID', required=True)
    dia = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ], string='Día', required=True)
    inicio = fields.Datetime(string='Inicio', required=True)
    fin = fields.Datetime(string='Fin', required=True)
    asignacion_ids = fields.One2many('colegio.asignacion', 'plan_estudio_id', string='Asignaciones')



class Asignacion(models.Model):
    _name = 'colegio.asignacion'
    _description = 'Asignación'

    id = fields.Integer(string='ID', required=True)
    profesor_id = fields.Many2one('colegio.profesor', string='Profesor', required=True)
    curso_id = fields.Many2one('colegio.curso', string='Curso', required=True)
    asignatura_id = fields.Many2one('colegio.asignatura', string='Asignatura', required=True)
    plan_estudio_id = fields.Many2one('colegio.planEstudio', string='Plan de Estudio', required=True)
    resumen_calificacion_ids = fields.One2many('colegio.resumenCalificacion', 'asignacion_id', string='Resumen de Calificaciones')


class ResumenCalificacion(models.Model):
    _name = 'colegio.resumenCalificacion'
    _description = 'Resumen de Calificación'

    id = fields.Integer(string='ID', required=True)
    promedio = fields.Float(string='Promedio', required=True)
    asignacion_id = fields.Many2one('colegio.asignacion', string='Asignación', required=True)
    calificacion_ids = fields.One2many('colegio.calificacion', 'resumen_calificacion_id', string='Calificaciones')
    inscripcion_id = fields.Many2one('colegio.inscripcion', string='Inscripción', required=True)


class Calificacion(models.Model):
    _name = 'colegio.calificacion'
    _description = 'Calificación'

    id = fields.Integer(string='ID', required=True)
    nota = fields.Float(string='Nota', required=True)
    periodo = fields.Integer(string='Periodo', required=True)
    resumen_calificacion_id = fields.Many2one('colegio.resumenCalificacion', string='Resumen de Calificación', required=True)


####################### ANTIGUA TABLA

class profesor(models.Model):
     _name = 'colegio.profesor'
     _description = 'profesor'

     name = fields.Char(string="Nombre", required=True)
     description =  fields.Text(string="Descripcion")
     edad = fields.Integer(string="Edad", required=True)
     fecha_nacimiento = fields.Date(string ="Fecha de Nacimiento")
     saldo = fields.Float(string ="Saldo")
     estado = fields.Boolean(string ="Estado del profesor")
     grado = fields.Selection(
        [
            ("basico","Basico"),
            ("primaria","Primaria"),
            ("secundaria","Secundaria"),
        ],
        string = "Grado",
        default = "primaria",
        required = True,
     )


     
     
class alumno(models.Model):
     _name = 'colegio.alumno'
     _description = 'alumnos'

     name = fields.Char(string="Nombre", required=True)
     profesor = fields.Many2one("colegio.profesor")
     edad = fields.Integer(string="Edad", required=True)
     fecha_nacimiento = fields.Date(string ="Fecha de Nacimiento")
     direccion = fields.Text(string="direccion")
     carnet_identidad = fields.Text(string = "carnet de identidad")
     grado = fields.Selection(
        [
            ("basico","Basico"),
            ("primaria","Primaria"),
            ("secundaria","Secundaria"),
        ],
        string = "Grado",
        default = "primaria",
        required = True,
     )