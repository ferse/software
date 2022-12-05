from django_cron import CronJobBase, Schedule
from datetime import date, timedelta
from .models import Backlog, Estado_Proyecto, Estado_Sprint, Sprint, User_Story, Proyecto

class Cron(CronJobBase):
    RUN_EVERY_MINS = 86400

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'App.cerrar'

    sprints = Sprint.objects.filter(fecha_fin=date.today()).exclude(id_estado_sprint = Estado_Sprint(pk = 3))
    for sprint in sprints:
        backlogs = Backlog.objects.filter(id_sprint=sprint.pk)
        backlog_pending = []
        is_pending = False
        for backlog in backlogs:
            user_stories = User_Story.objects.filter(id=backlog.id_us.pk)
#            us_pending = []
            if backlog.id_estado != 3:
                is_pending = True
                backlog_pending.append(backlog)
#            for user_story in user_stories:
#                if user_story. != 3:
#                    is_pending = True
#                    is_array = False
#                    us_pending.append(user_story)
#                    if is_array == False:
#                        backlog_pending.append(backlog)
#                        is_array = True

        if is_pending:
            new_sprint = Sprint(
                id_proyecto = sprint.id_proyecto,
                descripcion=sprint.descripcion, 
                duracion=sprint.duracion,
                fecha_inicio=date.today(), 
                fecha_fin=date.today() + timedelta(days=sprint.duracion),
                id_estado_sprint = Estado_Sprint(pk = 1)
                )
            new_sprint.save()
            for i in  range(len(backlog_pending)):
                #item = User_Story.objects.filter(id=user_story[i].pk).first()
                item = Backlog.objects.filter(id=backlog_pending[i].pk).first()
                item.id_sprint = new_sprint
                item.save()

            sprint.id_estado_sprint = Estado_Sprint(pk = 3)
            sprint.save()


    #Finalizar proyecto
    proyectos = Proyecto.objects.filter(fecha_fin=date.today())

    for proyecto in proyectos:
        sprints = Sprint.objects.filter(id_proyecto=proyecto.pk)
        is_pending = False
        for sprint in sprints:
            if sprint.id_estado_sprint.pk != 3:
                is_pending = True

        if not is_pending:
            proyecto.id_estado = Estado_Proyecto(pk=3)
            proyecto.save()             

