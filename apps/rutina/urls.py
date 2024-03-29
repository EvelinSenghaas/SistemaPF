from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import Rutinas, ListadoDetalles, ListadoRutinas, ListadoActividades, EditarRutina, editarActividad, EditarDetalle, eliminarActividad, AgregarRutina, AgregarDetalle, agregarActividad, eliminarRutina, verRutina, verActividad, agregarRutina, inscribirseRutina, perfil, verClase, eliminarDetalle, agregarEvaluacionNivel, listadoEvaluacionNivel, editarEvaluacionNivel, verRevisiones, actualizarFicha, obtenerActividadesSesion, obtenerCantidadMusculos, auditoria, comprobarRevision, detalleAuditoria, obtenerRevisionActividadesSesion, seleccionarHorarioClaseRevision, comprobarActualizacionFicha, editarPerfil, listadoRutinas, ocultarClases, bajaRutina, evolucionActividad, cambiarSistema, cambiarProfesor

urlpatterns = [
    path('listado/<int:pk>',  login_required(listadoRutinas), name = 'rutinas'),
    path('actividades/',  login_required(ListadoActividades.as_view()), name = 'actividades'),
    
    path('agregar_detalle',login_required(AgregarDetalle.as_view(success_url="/rutinas/administrar_detalles/")), name = 'agregar_detalle'),
    path('editar_detalle/<int:pk>', login_required(EditarDetalle.as_view(success_url="/rutinas/administrar_detalles/")), name='editar_detalle'),
    path('administrar_detalles/', login_required(ListadoDetalles.as_view()), name='administrar_detalles/'),
    path('eliminar_detalle/<int:pk>', login_required(eliminarDetalle), name='eliminar_detalle'), 
    
    path('agregar_actividad',login_required(agregarActividad), name = 'agregar_actividad'),
    path('editar_actividad/<int:pk>', login_required(editarActividad), name='editar_actividad'),
    path('eliminar_actividad/<int:pk>', login_required(eliminarActividad), name='eliminar_actividad'), 
    path('ver_actividad/<int:pk>', login_required(verActividad), name='ver_actividad'),
    
    path('agregar_rutina/<int:pk>',login_required(agregarRutina), name = 'agregar_rutina'),
    path('editar_rutina/<int:pk>', login_required(EditarRutina.as_view(success_url="/rutinas/administrar_rutinas/")), name='editar_rutina'),
    path('eliminar_rutina/<int:pk>', login_required(eliminarRutina), name='eliminar_rutina'),    
    path('ver_rutina/<int:pk>', login_required(verRutina), name='ver_rutina'),
    path('administrar_rutinas/', login_required(Rutinas.as_view()), name='administrar_rutinas/'),
    path('baja_rutina/<int:pk1>/<int:pk2>', login_required(bajaRutina), name='baja_rutina/'),
    
    path('inscribir_rutina/<int:pk1>/<int:pk2>', login_required(inscribirseRutina), name='inscribir_rutina/'), 
    
    path('ver_perfil/<int:pk>', login_required(perfil), name='ver_perfil'),
    
    path('clases/<int:pk>', login_required(verClase), name='clases'),
    
    path('administrar_evaluacion_nivel/<int:pk>', login_required(listadoEvaluacionNivel), name='administrar_evaluacion_nivel'),
    path('agregar_evaluacion_nivel/<int:pk>', login_required(agregarEvaluacionNivel), name='agregar_evaluacion_nivel'),
    path('editar_evaluacion_nivel/<int:pk>', login_required(editarEvaluacionNivel), name='editar_evaluacion_nivel'),
    
    
    path('revisiones/<int:pk>', login_required(verRevisiones), name='revisiones'),
    path('actualizar_ficha/', login_required(actualizarFicha), name='actualizar_ficha'),
    path('seleccionar_horario_clase_revision/', login_required(seleccionarHorarioClaseRevision), name='seleccionar_horario_clase_revision'),
    
    
    path('obtener_actividades_ajax/', login_required(obtenerActividadesSesion), name='obtener_actividades_ajax'),
    path('obtener_cantidad_musculos_ajax/', login_required(obtenerCantidadMusculos), name='obtener_cantidad_musculos_ajax'),
    path('comprobar_revision_ajax/', login_required(comprobarRevision), name='comprobar_revision_ajax'),
    path('ver_detalles_ajax/', login_required(detalleAuditoria), name='ver_detalles_ajax'),
    path('obtener_revision_sesion_ajax/', login_required(obtenerRevisionActividadesSesion), name='obtener_revision_sesion_ajax'),
    path('comprobar_actualizacion_ficha_ajax/', login_required(comprobarActualizacionFicha), name='comprobar_actualizacion_ficha_ajax'),
    path('ocultar_clases_ajax/', login_required(ocultarClases), name='ocultar_clases_ajax'),
    path('evolucion_actividad_ajax/', login_required(evolucionActividad), name='evolucion_actividad_ajax'),
    
    
    path('auditoria/', login_required(auditoria), name='auditoria'),
    
    path('editar_perfil/<int:pk>', login_required(editarPerfil), name='editar_perfil'),
    
    path('cambiar_a_sistema/<int:pk>', login_required(cambiarSistema), name='cambiar_a_sistema'),
    path('cambiar_a_profesor/<int:pk>', login_required(cambiarProfesor), name='cambiar_a_profesor'),
    
    
]