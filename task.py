from google.appengine.ext import ndb
from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

class task(messages.Message):
	name = messages.StringField(1, required=True)
	owner = messages.StringField(2)

class taskModel(ndb.Model):
	name = ndb.StringProperty(required=True)
	owner = ndb.StringProperty()

class taskList(messages.Message):
	items = messages.MessageField(task, 1, repeated = True)

@endpoints.api(name='tasks', version='v1',
		description='API for task Management')
class taskApi(remote.Service):

	@endpoints.method(task, task,
			name='task.insert',
			path='task',
			http_method='POST')

	def insert_task(self, request):
		taskModel(name=request.name, owner = request.owner).put()
		return request

	@endpoints.method(message_types.VoidMessage, taskList,
			name='task.list',
			path='tasks',
			http_method='GET')

	def list_tasks(self, unused_request):
		tasks = [task(name=task_model.name, owner=task_model.owner) for task_model in taskModel.query()]
		'''tasks = []
		for task_model in taskModel.query():
			tasks.append(task(name=task_model.name, owner=task_model.owner))'''
		response = taskList(items=tasks)
		return response
	
application = endpoints.api_server([taskApi])
