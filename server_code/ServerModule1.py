import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from EventzAnvilAPI import Subscriber

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
@anvil.server.callable
def get_pizza():
  return app_tables.pizza_oven.search()

# @anvil.server.callable
# def set_session_id(s):
#   print(f'Setting Session Id: {s}')
#   anvil.server.session['session_id'] = s
  
# @anvil.server.callable
# def launch_subscriber_task():
#   print("Launching the subscriber task")
#   subscriber = Subscriber()
#   subscriber_task = anvil.server.launch_background_task('background_subscriber_task',subscriber)
#   if subscriber_task: 
#     print(f"I have a subscriber_task: {subscriber_task}")
# #     subscriber_task.run
#   return subscriber_task

# @anvil.server.background_task
# def background_subscriber_task(subscriber):
#   # subscriber = Subscriber()
#   print(f'Subscriber: {subscriber}')
#   anvil.server.task_state['session'] = ''
#   anvil.server.task_state['recordType'] = ''
#   anvil.server.task_state['records'] = []
#   subscriber.subscriber_task(anvil.server.task_state)
#   return subscriber.subscriber_task()

