from django.conf.urls import url ,include
from .views import *

#application namespace
app_name = 'ns-project'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.


    # The home page
    url(r'^dashboard/$', Dashboard, name='dashboard'),
    url(r'^$', Dashboard, name='index'),
    url(r'^$', Dashboard, name='dashboard'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^add-sheet/$', AddSheet, name='add-sheet'),
    url(r'^sheet/(?P<pk>\d+)/edit/$', EditSheet, name='edit-sheet'),
    url(r'^sheet/(?P<pk>\d+)/submit/$', SubmitSheet, name='submit-sheet'),
    url(r'^sheet/(?P<pk>\d+)/change/$', ChangeStatus, name='change-status'),
    url(r'^my_sheet/$', MySheet, name='my-sheet'),
    # url(r'^all_sheets/$', ManagerPage, name='all-sheets'),
    url(r'^all_employees_sheets/$', AllSheets, name='emps-sheets'),
    url(r'^all_dept_sheet/$', AllDept, name='dept-sheets'),
    #url(r'^all_emp/$', IsManager, name='all-emp'),
    url(r'^sheet/(?P<deptcode>\d+)/dept/$', DeptSheet, name='dept-sheet'),
    # url(r'^sheet/(?P<empid>\d+)/update/$', EditSheet, name='edit-sheet'),
    url(r'^sheet/(?P<empid>\d+)/update/$', UpdateSheet, name='update-sheet'),
    url(r'^sheet/(?P<empid>\d+)/details/$', DetailseSheet, name='detials-sheet'),
    url(r'^sheet/(?P<empid>\d+)/show/$', EmpSheet, name='emp-sheet'),
    url(r'^add_project/$', AddProject, name='add-project'),
    url(r'^project_list/$', ProjectList, name='project-list'),
     url(r'^project_list/(?P<project_status>\w+)$', ProjectList, name='project-list'),
    url(r'^project_detail/(?P<pk>\d+)$', ProjectDetail, name='project-detail'),
    url(r'^project_edit/(?P<pk>\d+)$', ProjectEdit, name='project-edit'),
    url(r'^project_delete/(?P<pk>\d+)$', ProjectDelete, name='project-delete'),
    url(r'^task_list_external/(?P<task_status>\w+)$', TaskListExternal, name='task-list-external'),
    url(r'^project_task/(?P<pk>\d+)$', ProjectTask, name='project-task'),
    url(r'^project_task/(?P<pk>\d+)/(?P<task_status>\w+)$', ProjectTask, name='project-task'),
    url(r'^project_task_detail/(?P<projectid>\d+)/(?P<taskid>\d+)$', ProjectTaskDetail, name='project-task-detail'),
    # url(r'^project_team/(?P<pk>\d+)$', ProjectTeam, name='project-team'),
    url(r'^task_update_start/(?P<pk>\d+)$', updateStartDate, name='task-update-start'),
    url(r'^update_finish_task/(?P<pk>\d+)$',updateTaskFinish, name='update-finish-task'),
    url(r'^update_close_task/(?P<pk>\d+)$',updateTaskClose, name='update-close-task'),
    url(r'^update_cancel_task/(?P<pk>\d+)$',updateTaskCancel, name='update-cancel-task'),
    url(r'^update_pause_task/(?P<pk>\d+)$',updateTaskPause, name='update-pause-task'),
    url(r'^update_assignto_task/(?P<pk>\d+)$',updateTaskAssignto, name='update-assignto-task'),
    url(r'^update_assignto_task/(?P<pk>\d+)/(?P<save>\w+)$',updateTaskAssignto, name='update-assignto-task'),
    url(r'^update_progress_task/(?P<pk>\d+)$',updateTaskProgress, name='update-progress-task'),
    url(r'^project_gantt/(?P<pk>\d+)$',ganttChart, name='project-gantt'),
    url(r'^kanban/(?P<pk>\d+)$',Kanban, name='kanban'),
    url(r'^project_follow_up/$',projectFlowUp, name='project-follow-up'),
    url(r'^project_task_delete/(?P<projectid>\d+)/(?P<taskid>\d+)$', ProjectTaskDelete, name='project-task-delete'),
    url(r'^project_task_edit/(?P<projectid>\d+)/(?P<taskid>\d+)$', ProjectTaskEdit, name='project-task-edit'),
    url(r'^project/(?P<project_id>\d+)/team$',ProjectTeam, name='project-team'),
    url(r'^project/(?P<project_id>\d+)/addtask$',AddTask, name='add-task'),
    url(r'^project/dashboard_manager$',DashboardManager, name='dashboard-manager'),
    url(r'^project/dashboard_pm$',DashboardPM, name='dashboard-pm'),
    url(r'^project/dashboard_employee/$',DashboardEmployee, name='dashboard-employee'),
    url(r'^project/dashboard_employee/(?P<empid>\d+)/$',DashboardEmployee, name='dashboard-employee'),
    url(r'^download/(?P<file_name>.+)$', Download, name='download'),
    url(r'^email/$', senmail, name='email'),
    url(r'^project_report/$', ProjectReport, name='project-report'),
    url(r'^project_report/(?P<selectedDpt>.+)$', ProjectReport, name='project-report'),
    #login from drupal
    url(r'^auth/(?P<email>.*)/(?P<signature>.*)/(?P<time>.*)/$', loginfromdrupal, name='loginfromdrupal'),
    #delegation page
    url(r'^add_delegation/$',adddelegation, name='add-delegation'),
    url(r'^delegation/(?P<pk>\d+)/edit/$', editdelegation, name='edit-delegation'),
    url(r'^delegation/$',delegation, name='delegation'),
    url(r'^my_delegation/$',mydelegation, name='my-delegation'),
    url(r'^.*\.html', gentella_html, name='gentella'),
    url(r'^add-project-phase/(?P<project_id>\d+)$', add_project_phase, name='add-project-phase'),
    url(r'^edit-project-phase/(?P<phase_id>\d+)$', edit_project_phase, name='edit-project-phase'),

    # url(r'^phases_list/(?P<project_id>\d+)$', phases_list, name='phases-list'),
    url(r'^phases_list/(?P<project_id>\d+)/(?P<phase_status>\w+)?$', phases_list, name='phases-list'),
    url(r'^project_phase_detail/(?P<projectid>\d+)/(?P<phase_id>\d+)$', ProjectPhaseDetail, name='project-phase-detail'),
    url(r'^phase-tasks-list/(?P<projectid>\d+)/(?P<phase_id>\d+)/(?P<task_status>\w+)?$', PhaseTaskList, name='phase-task-list'),
    url(r'^project-phase-delete/(?P<projectid>\d+)/(?P<phase_id>\d+)$', ProjectPhaseDelete, name='project-phase-delete'),


    url(r'^export-project', export_project_xls, name='export-project'),
    url(r'^export-task', export_task_xls, name='export-task'),

    url(r'^update_assignto_group/(?P<pk>\d+)$', updateTaskAssigntoGroup, name='update-assignto-group'),
]
