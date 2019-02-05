from django_cron import CronJobBase, Schedule
from project.models import Task, Employee
from django.utils.timezone import datetime
from datetime import timedelta
from django.template.loader import get_template
from django.core.mail import send_mail


class NotifyEmployeeJob(CronJobBase):
    """
    Notifies an employee by email if they have a task that will reach it's end date two days before
    """
    RUN_AT_TIME = ['04:00']  # UTC, according to the TIME_ZONE setting

    schedule = Schedule(run_at_times=RUN_AT_TIME)
    code = 'tms.notify_employee_job'

    NOTIFY_DAYS = 2

    def do(self):
        print(' ')
        self.log('---------- EXECUTION STARTED ----------')
        print(' ')

        today = datetime.today()
        fastforward = today + timedelta(days=self.NOTIFY_DAYS)

        expiring_tasks = Task.objects.filter(enddate__date=fastforward).all()

        task_list = {}

        for task in expiring_tasks:
            assignee = str(task.assignedto.empid)
            if assignee not in task_list:
                task_list[assignee] = []
            task_list[assignee].append(task)

            assignments = task.assignees.all()
            for assignment in assignments:
                assignee = str(assignment.assign_to_id)
                if assignee not in task_list:
                    task_list[assignee] = []
                task_list[assignee].append(task)

        emp_email_list = Employee.objects.filter(empid__in=task_list.keys()).values_list('empid', 'email')

        for email in emp_email_list:
            empid, address = email[0], str(email[1])
            if empid in task_list:
                success = self.send_email(address, task_list[empid])
                if success:
                    self.log('Sent email successfully to empid=%s, email=%s' % (empid, address))
                else:
                    self.log('Failed to send email to empid=%s, email=%s' % (empid, address), scope='error')

    def log(self, msg, scope="log"):
        now = datetime.today()
        print('[NotifyEmployeeJob][%s %s] %s' % (scope.upper(), now, msg))

    def send_email(self, receiver, tasks):
        try:
            self.log('Will send email to %s' % receiver)
            _sender = 'notifications@pms.stats.gov.sa'
            _receiver = receiver
            subject = 'نظام إدارة المشاريع | إشعار بإنتهاء مهمة قريباً'
            context = {'tasks': tasks, 'host': 'http://192.168.0.192:801', 'receiver': _receiver, 'sender': _sender}
            message = get_template('project/email/task_expiring.html').render(context)
            send_mail(subject, message, _sender, [_receiver], fail_silently=False, html_message=message,)
            return True
        except Exception as e:
            self.log(e, scope='exception')
            return False
