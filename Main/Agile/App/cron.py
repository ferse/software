from django_cron import CronJobBase, Schedule
from datetime import date, timedelta
from .models import Sprint, User_Story, Proyecto

class Cron(CronJobBase):
    RUN_EVERY_MINS = 86400

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
    code = 'App.cerrar'

    def do(self):
        sprints = Sprint.objects.filter(fecha_fin=date.today())
        for sprint in sprints:
            user_stories = User_Story.objects.filter(id_sprint=sprint.pk)
            is_pending = False
            us_pending = []
            for user_story in user_stories:
                if user_story.id_estado == 1:
                    is_pending = True
                    us_pending.append(user_story)

            if is_pending:
                sprint = Sprint(
                    id_proyecto = sprint.id_proyecto,
                    descripcion=sprint.descripcion, 
                    duracion=sprint.duracion,
                    fecha_inicio=date.today(), 
                    fecha_fin=date.today() + timedelta(days=sprint.duracion),
                    )
                sprint.save()
                for i in len(us_pending):
                    item = User_Story.objects.filter(id=user_story[i].pk).first()
                    item.id_sprint = sprint.pk
                    item.save()

                sprint.id_estado_sprint = 3
                sprint.save()


        #Finalizar proyecto
        proyectos = Proyecto.objects.filter(fecha_fin=date.today())
        for proyecto in proyectos:
            sprints = Sprint.objects.filter(id_proyecto=proyecto.pk)
            is_pending = False
            for sprint in sprints:
                if sprint.id_estado_sprint == 1:
                    is_pending = True

            if not is_pending:
                proyecto.id_estado = 3
                proyecto.save()             

