import anvil.users
#EventzAnvilAPI  May 6-24

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.


import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#

import pika
import anvil.server
import datetime
import uuid
import atexit
from enum import Enum
import itertools
import operator
from uuid import getnode as get_mac
from anvil.tables import app_tables
import dateutil.parser

''' Enum for record action codes inserted in message metadata'''
class RecordAction(Enum):
    INSERT = 0
    UPDATE = 1
    DELETE = 2
''''''
def get_anvil_server_session_id():
  return anvil.server.session['session_id']

  
  
'''

Publisher
  
'''
class Publisher(object):
    '''
    The Publisher provides a mechanism for publishing data to the Broker.
    DS_Init will create one and put it in the DS_Parameters object.
    '''

    def __init__(self):
#         self.dsParam = dsParam
        self.exchange = 'amq.topic'
        self.brokerUserName = 'lqcoztwn'
        self.brokerPassword = '7ZJpQw7rSg1LyHLe0zx1rx2a3O27JktI'
        self.brokerIP = 'codfish-01.rmq.cloudamqp.com'
        self.encrypt = False
        self.applicationId = '5bd21f12-e131-4666-aaff-c76fdeefedcf'
        self.tenant = '00000000-0000-0000-0000-000000000000'
        self.cert = ''
        self.key = ''
        self.CaCert = ''
        self.virtualhost = 'lqcoztwn'
        self.channel = None
        self.connection = False
        self.publish_OK = False

        atexit.register(self.stop)

    # The publish method formats a message, adding metadata, and sends it to the AMQP broker
    #
    def publish(self, recordType, dataTuple, action = RecordAction.INSERT.value, link = '00000000-0000-0000-0000-000000000000',
                userId = '', versionLink = '00000000-0000-0000-0000-000000000000', versioned = False,
                sessionID = '00000000-0000-0000-0000-000000000000', umd1 = '', umd2 = '', umd3 = '', umd4 = '',
                umd5 = ''):

        '''
        The publish method formats a message, adding metadata, and sends it to the AMQP broker
        There is to be one publisher keeping one channel open. It is passed through DS_Parameters
        to functions that need to publish

        recordType = 0
        action = 1
        recordId = 2
        link = 3
        tenant = 4
        userId = 5
        publishDateTime = 6
        applicationId = 7
        versionLink = 8
        versioned = 9
        sessionId = 10          # UUID identifying the user's session so as not to confuse with other user's records
        userMetadata1 = 11      # User defined fields for query filtering
        userMetadata2 = 12
        userMetadata3 = 13
        userMetadata4 = 14
        userMetadata5 = 15
        '''

        # Make sure we have a channel to the Broker
        if self.channel is None or not self.channel.is_open:
            try:
                self.reconnect()
            except:
                print('Unable to connect to RabbitMQ server!!!')
                return None

        recordTypeSz = '{:12.2f}'.format(float(recordType)).strip()   # Make a string version

        # Prep data here

        recordId = str(uuid.uuid4())        # Give it a new Id
        if link == 0:
            link = '00000000-0000-0000-0000-000000000000'
        if self.tenant == 0:
            self.tenant = '00000000-0000-0000-0000-000000000000'
        if self.applicationId == 0:
            self.applicationId = '00000000-0000-0000-0000-000000000000'

        data = (recordTypeSz, action, recordId, link, self.tenant, userId,
                datetime.datetime.utcnow().isoformat(sep='T'), self.applicationId, versionLink, versioned, sessionID,
                umd1, umd2, umd3, umd4, umd5) + dataTuple

        # Publish it

        rk = "{0:12.2f}".format(float(recordType)).strip()

        self.publish_OK = self.channel.basic_publish(exchange=self.exchange, routing_key=rk,
                              body=str(data), properties=pika.BasicProperties(content_type="text/plain", delivery_mode=2, ),
                              )

        # Let the caller know what was published including the generated recordId
        if self.publish_OK == None:
            return str(data)
        else:
            return None

    
    def reconnect(self):
      '''Called if a connection needed  
      Set up Broker connection'''
      
      if not self.encrypt:
          parameters = pika.ConnectionParameters(host = self.brokerIP,
                                                  port=5672,
                                                  virtual_host=self.virtualhost,
                                                  credentials=(
                                                      pika.PlainCredentials(self.brokerUserName, self.brokerPassword)),
                                                  heartbeat=600,
                                                  ssl_options=None,
                                                  socket_timeout=10,
                                                  blocked_connection_timeout=10,
                                                  retry_delay=3.0,
                                                  connection_attempts=5)
      else:
          parameters = pika.ConnectionParameters(host = self.brokerIP,
                                                  port = 5671,
                                                  virtual_host = self.vitualhost,
                                                  credentials = (pika.PlainCredentials(self.brokerUserName ,self.brokerPassword)),
                                                  heartbeat=600,
                                                  # ssl=True,
                                                  ssl_options = ({
                                                      "ca_certs": self.CaCert,
                                                      "certfile": self.cert,
                                                      "keyfile": self.key,
                                                      "cert_reqs": ssl.CERT_REQUIRED,
                                                      "server_side": False,
                                                      "ssl_version": ssl.PROTOCOL_TLSv1_2
                                                  }),
                                                  socket_timeout=10,
                                                  blocked_connection_timeout=10,
                                                  retry_delay=3.0,
                                                  connection_attempts=5)
      
      self.connection = pika.BlockingConnection(parameters)
      self.channel = self.connection.channel()
      self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
      # result = self.channel.queue_declare(queue=str(self.myQueueName), exclusive=True)
      # queue_name = result.method.queue
      # print ("Publishing Message on Queue: " + queue_name)
      
        
    def stop(self):
      print('Publisher Terminating!  Closing Connection')
      if not self.channel is None:
          if self.channel.is_open:
              self.channel.stop_consuming()
  
'''

  Subscriber
  
'''          
# @anvil.server.portable_class
class Subscriber(object):
  def __init__(self):
    print("Initalizing Subscriber")
    self.exchange = 'amq.topic'
    self.channel = None
    self.queue_name = None
    self.routingKeys = ['300000.00']
    self.systemRoutingKeys = []
    self.session_id = ''
    anvil.server.session['session_id'] = ''
    self.message_dict = {}
    anvil.server.task_state['session'] = ''
    anvil.server.task_state['recordType'] = ''
    anvil.server.task_state['records'] = []
    self.deviceId = ':'.join((itertools.starmap(operator.add, zip(*([iter("%012X" % get_mac())] * 2)))))
    self.deviceName = 'Bobs MAC'
    self.location = 'London, Ontario Canada'
    self.applicationId = '5bd21f12-e131-4666-aaff-c76fdeefedcf'
    self.applicationName = 'System Monitor'
    self.aPublisher = Publisher()
    self.applicationUser = 'Anvil'



  def subscriber_task(self):
    
    '''A task to report receipt of messages subscribed to'''
    # RUN
    print("Running the subscriber_task")
    if self.channel is None or not self.channel.is_open:
      try:
          self.reconnect()
      except Exception as e: 
        print(e)
        print('Unable to connect to RabbitMQ server!!!')
        return
    
    print("Waiting for RabbitMQ DS messages from queue: " + self.queue_name)
  
    # Get next request
    print('queue:' + self.queue_name)
    self.channel.basic_consume(self.queue_name, on_message_callback=self.callback, auto_ack=True)
    self.channel.start_consuming()
 
#   @anvil.server.callable
  def reconnect(self):
      # Set up RabbitMQ connection
      
      print("Reconnecting")      
      encrypt = False
      brokerIP = 'shrimp-01.rmq.cloudamqp.com'
      virtualhost = 'moxlxjny'
      brokerUserName = 'moxlxjny'
      brokerPassword = 'JQ2V1MQ_ba6or8Kg0_upQXQ1Osjy_J_9'
      self.queue_name = ''
      self.firstData = 16
      self.tenant = '00000000-0000-0000-0000-000000000000'
  
      if not encrypt:
        parameters = pika.ConnectionParameters(host = brokerIP,
                                                port = 5672,
                                                virtual_host = virtualhost,
                                                credentials = (pika.PlainCredentials(brokerUserName, brokerPassword)),
                                                heartbeat=600,
                                                ssl_options=None,
                                                socket_timeout=10,
                                                blocked_connection_timeout=10,
                                                retry_delay=3.0,
                                                connection_attempts=5)
      else:
        parameters = pika.ConnectionParameters(host = brokerIP,
                                                port = 5671,
                                                virtual_host = virtualhost,
                                                credentials = (pika.PlainCredentials(brokerUserName, brokerPassword)),
                                                heartbeat=600,
                                                # ssl=True,
                                                ssl_options = ({
                                                    "ca_certs": self.CaCert,
                                                    "certfile": self.cert,
                                                    "keyfile": self.key,
                                                    "cert_reqs": ssl.CERT_REQUIRED,
                                                    "server_side": False,
                                                    "ssl_version": ssl.PROTOCOL_TLSv1_2
                                                }),
                                                socket_timeout=10,
                                                blocked_connection_timeout=10,
                                                retry_delay=3,
                                                connection_attempts=5)

      self.connection = pika.BlockingConnection(parameters)
      self.channel = self.connection.channel()
      self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic", durable=True)
      result = self.channel.queue_declare(str(self.queue_name), exclusive=True )
      print(f"5 result:{result}")  
      self.queue_name = result.method.queue
      print(f"6 Queue name:{self.queue_name}")  
      workingRoutingKeys = self.routingKeys + self.systemRoutingKeys
  
      for routingKey in workingRoutingKeys:
          self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routingKey)
  
#       LOGGER.info("Subscriber Thread: Connection established and queue (%s) bound.", self.queue_name)
      print("Subscriber Thread: Connection established and queue (%s) bound.", self.queue_name)
      
  def run(self):
      if self.running:
          if self.channel is None or not self.channel.is_open:
              try:
                  self.reconnect()
              except:
                  LOGGER.error('Unable to connect to RabbitMQ server!!!')

      LOGGER.info("Running Subscriber Thread.")

      # Monitor RMQ and write incoming data to local archive if we have one

      # Create the local archive if none and we want one
      if len(self.archivePath) > 0 and os.path.isfile(self.archivePath) == 0:
          # if os.path.isfile(self.archivePath) == 0:
          LOGGER.info("Creating new local archive")
          file = open(self.archivePath, "a", newline='')
          file.close()

      print("Waiting for RabbitMQ DS messages from queue %s", self.queue_name)
      LOGGER.info("Waiting for RabbitMQ DS messages from queue %s", self.queue_name)

      # Get next request
      self.channel.basic_consume(self.queue_name, on_message_callback=self.callback, auto_ack=True)

      try:
          self.channel.start_consuming()
      except pika.exceptions.StreamLostError:
          LOGGER.info("Stream Lost")
      LOGGER.error("Should never get here !!!")

  #
  # Close connections to RabbitMQ and stop the thread
  #   Launched when thread stopped in pcbMrp when closeEvent() is fired
  #
  
  @anvil.server.callable
  def stop(self):
    print('Subscriber Thread Terminating')
    if not self.channel is None:
          if self.channel.is_open:
              try:
                  self.channel.queue_delete(queue=self.queue_name)
                  self.channel.stop_consuming()
                  self.connection.close()
                  print('Terminating Subscriber!')
              except:
                  self.channel.queue_delete(queue=self.queue_name)
                  self.connection.close()
                  print('Terminating Subscriber! ex')
  #                    self.connection.close()
  #                    self.stop()
  
  #
  # Bind the broker's queue to a record type (routing key)
  #
  @anvil.server.callable
  def bind(self, recordType):
  
      rk = "{0:10.2f}".format(recordType).strip()
  
      if '.00' in rk:
          rk = "{0:10.1f}".format(recordType).strip()
  
      self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=rk)
  
  #
  # Pass the message on to the main application
  #
  
  @anvil.server.callable
  def alert_main_app(self, bodyTuple):
  
      # Write the Local Archive if we are subscribing to this record type and there is a local archive
  
      recordType = rt = bodyTuple[0]
      print(f'Alerting MAin App for record type: {recordType}')
  
      if (rt in self.routingKeys or '#' in self.routingKeys):     # Do we care about this message ??
  
#           if len(self.archivePath) > 0 and self.master_archive:     # Do we have write access to a local archive ??
#               self.utilities.archive(bodyTuple, self.archivePath)     # If so put it in the local archive

          if get_anvil_server_session_id() == self.session_id:
            print('Clearing session')
            anvil.server.task_state['session'] = ''
            anvil.server.task_state['recordType'] = ''
            anvil.server.task_state['records'] = []
  
            
  
          # Alert the main loop

          self.session = str(uuid.uuid4())      # Generate a session
          metadatax = [field for i, field in enumerate(bodyTuple) if i >0 and i<16]
          metadata = ", ".join([str(x) for x in metadatax])
          payloadx = [field for i, field in enumerate(bodyTuple) if i > 15]
          payload = ", ".join([str(x) for x in payloadx])
          print(f'Session ID: {self.session}')
          print(f"Metadata: {metadata}")
          print(f"Payload: {payload}")
          self.message_dict['session'] = self.session
          self.message_dict['recordType'] = recordType
          self.message_dict['metadata'] = metadata
          self.message_dict['payload'] = payload
          published = metadatax[5]
          print(f"Published: {published}")
#           published_dt = datetime.datetime.strptime(published, "%Y-%m-%dT%H:%M:%S.UUUUUU")
          published_dt = dateutil.parser.isoparse(published)

          
          app_tables.log.add_row(Published = published_dt, RecordType = recordType, Metadata = metadata, Payload = payload)
          

          # A change in state indicates to the client that there is new data in the database

          anvil.server.task_state['session'] = self.session
          anvil.server.task_state['recordType'] = recordType
          anvil.server.task_state['records'] = [self.message_dict]


 
  #
  # Execute callback when request received
  #
  
  @anvil.server.callable
  def callback(self, ch, method, properties, body):
  
      print("DS message is %s", body.decode('utf_8'))
      
      firstData = 16
      
      bodyStr = body.decode('utf_8')
      # i = bodyStr.find(',')  # see who sent this
      # sender = bodyStr[2:i - 1]
  
      # j = bodyStr.find(',', i+1)  # see if this was generated by a Versioner (second field 0 = False, 1 = True)
      # versionSz = bodyStr[i+1:(j)]
      # aVersion = int(versionSz)
  
      print(f"External DS message received: {bodyStr}")
      # bodyStr = bodyStr[i + 1:]  # Make this a tuple without dbid
      # bodyStr = bodyStr[j + 1:]  # Make this a tuple
      # bodyStr = '(' + bodyStr
      bodyTuple = eval(bodyStr)
      recordType = bodyTuple[0]
      tenantNo = bodyTuple[4]
      print(f"Record Type: {str(recordType)}")
      rt = int(float(recordType) * 100)
      myTime = datetime.datetime.utcnow().isoformat(sep='T')
  
      print(f"bodyTuple[firstData]:{str(bodyTuple[self.firstData])}")
      print("rt: %i", rt)
  
      #if tenant is not the same then ignore message
      if self.tenant == tenantNo:
  
          # Handle System Messages
  
          if int(rt) in range(900000000, 910000099):
              print("IN RANGE")
              if float(recordType) == 9000010.00:  # Ping Request
                  print("Got Ping Request")
                  if bodyTuple[self.firstData] == '0':  # All ?
                      print("Ping All Received.")
#                       pingRecord = (self.deviceId, self.deviceName, self.location, self.applicationId,
#                                     self.applicationName, myTime)
                      pingRecord = (self.deviceId, self.deviceName, self.location, self.applicationId,
                                    self.applicationName, myTime)

  
                      self.aPublisher.publish(9000011.00, pingRecord, RecordAction.INSERT.value,
                                              '00000000-0000-0000-0000-000000000000',
                                              self.applicationUser, '00000000-0000-0000-0000-000000000000',
                                              False, '00000000-0000-0000-0000-000000000000',
                                              '', '', '', '', '')
                  elif bodyTuple[self.firstData] == '1':  # Device Ping ?
                      deviceWanted = bodyTuple[self.firstData + 1].replace('\'', '').strip()
                      print("Device Ping Received:[%s] Me:[%s]", deviceWanted, self.deviceId)
                      if deviceWanted == self.deviceId:
                          print("It's for Me!!")
                          pingRecord = (self.deviceId, self.deviceName, self.location, self.applicationId,
                                        self.applicationName, myTime)
                          self.aPublisher.publish(9000011.00, pingRecord, RecordAction.INSERT.value,
                                                  '00000000-0000-0000-0000-000000000000',
                                                  self.applicationUser, '00000000-0000-0000-0000-000000000000',
                                                  False, '00000000-0000-0000-0000-000000000000',
                                                  '', '', '', '', '')
  
                  elif bodyTuple[self.firstData] == '2':  # Application Ping
                      appWanted = bodyTuple[self.firstData + 2].replace('\'', '').strip()
                      print("Application Ping Received:[%s] Me:[%s]", appWanted, self.applicationId)
  
                      if appWanted == self.applicationId:
                          print("It's for Me!!")
                          pingRecord = (self.deviceId, self.deviceName, self.location, self.applicationId,
                                        self.applicationName, myTime)
                          self.aPublisher.publish(9000011.00, pingRecord, RecordAction.INSERT.value,
                                                  '00000000-0000-0000-0000-000000000000',
                                                  self.applicationUser, '00000000-0000-0000-0000-000000000000',
                                                  False, '00000000-0000-0000-0000-000000000000',
                                                  '', '', '', '', '')
                  else:
                      print('Invalid Ping Type:' + bodyTuple[self.firstData])
  
              # Pass unhandled messages to the main thread
  
              else:
                  self.alert_main_app(bodyTuple)
  
          else:
              self.alert_main_app(bodyTuple)
      else:
          # Here I sent this message
          self.alert_main_app(bodyTuple)
  
      def createSubscriberTask(self):
          return self.SubscriberThread(self)

#
# The Librarian Client will send a query to the Librarian through the AMQP broker
#

class LibrarianClient(object):

    '''
    The Librarian Client, when instantiated, accepts dsQuery objects, connects to the Librarian microservice,
    sends the query and awaits a response. When the response arrives it closes the connection and returns the
    response to the caller. Querys are passe using the call method
    e.g. call(userName, tenant, startDate, endDate, limit, queries)
    where:
        userName is an ascii string identifying who is making the query
        tenant is a uuid identifying the tenant in a multi-tenant situation. Only the data belonging to the tenant
            is returned.
        startDate, and endDate when not = '' specify a date range so that only data published within the range is
            returned.
        limit is an integer specifying the maximum number of record to be returned. The result set will be truncated
            to the number specified. A limit ot 0 means all the data will be returned.
        queries is a list of dsQuery objects used by the Librarian service to filter the data. Multiple queries are
            anded. There is no or capability.
    '''

    def __init__(self, dsParam, logger):

        self.brokerIP = dsParam.broker_IP
        self.brokerUserName = dsParam.broker_user_name
        self.brokerPassword = dsParam.broker_password
        self.encrypt = dsParam.encrypt
        self.cert = dsParam.path_to_certificate
        self.key = dsParam.path_to_key
        self.CaCert = dsParam.path_to_CaCert
        self.vitualhost = dsParam.virtualhost

        self.logger = logger

        self.timeout = False

        if not self.encrypt:
            parameters = pika.ConnectionParameters(host=self.brokerIP,
                                                   port=5672,
                                                   virtual_host=self.vitualhost,
                                                   credentials=(
                                                       pika.PlainCredentials(self.brokerUserName, self.brokerPassword)),
                                                   heartbeat=0,
                                                   # ssl=False,
                                                   socket_timeout=10,
                                                   blocked_connection_timeout=10,
                                                   retry_delay=3,
                                                   connection_attempts=5)
        else:
            parameters = pika.ConnectionParameters(host=self.brokerIP,
                                                   port=5671,
                                                   virtual_host=self.vitualhost,
                                                   credentials=(
                                                       pika.PlainCredentials(self.brokerUserName, self.brokerPassword)),
                                                   heartbeat=0,
                                                   ssl=True,
                                                   ssl_options=({
                                                       "ca_certs"   : self.CaCert,
                                                       "certfile"   : self.cert,
                                                       "keyfile"    : self.key,
                                                       "cert_reqs"  : ssl.CERT_REQUIRED,
                                                       "server_side": False,
                                                       "ssl_version": ssl.PROTOCOL_TLSv1_2
                                                   }),
                                                   socket_timeout=10,
                                                   blocked_connection_timeout=10,
                                                   retry_delay=3,
                                                   connection_attempts=5)

        # credentials = pika.PlainCredentials(self.brokerUserName, self.brokerPassword)
        # parameters = pika.ConnectionParameters(self.brokerIP, 5672, '/', credentials)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_qos(prefetch_size=0, prefetch_count=10)

        self.channel.basic_consume(self.callback_queue , on_message_callback=self.on_response, auto_ack=True)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, userName, tenant, startDate, endDate, limit, queries):

        # Prepare the query(s)
        qdList = []
        t = threading.Timer(60, self.timerExpired) # Query timeout
        for q in queries:
            # qdList.append(q.__dict__)
            qdList.append(q)
        # query = dsQuery(limit, userName, tenant, startDate, endDate, qdList)
        queryDict = {'limit': limit, 'user': userName, 'tenant': tenant, startDate: startDate, 'endDate': endDate,
                'queryTerms': qdList}
        # queryDict = query.__dict__
        querySz = json.dumps(queryDict, cls = to_json)

        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                   correlation_id=self.corr_id ), body=querySz)

        t.start()  # Start the Timer. If it times out the method timerExpired() will execute
        LOGGER.info("Launched a query %s", qdList)
        print("Launching a query %s", qdList)

        while self.response is None and self.timeout==False:
            self.connection.process_data_events()

        if self.timeout == True:
            LOGGER.warning('Librarian not responding')
            print(self, 'Librarian not responding')
            t.cancel()
            # self.logger.log('eventzAPI', 0, 0, 0, 'Librarian not responding')
            return None

        # def log(self, user_id, errorType, errorLevel, errorAction, errorText):

        # ToDo Handle large result sets via a socket connection

        print(f'Query Result: {self.response}')

        result_set = ast.literal_eval(self.response.decode("utf_8"))

        # print(f'Query Result: {result_set}')

        # for record in result_set:
        #     print(f'Looking at: {record}')
        #     if record[0] == '*':
        #         message_length = record[1]
        #         host = record[2]
        #         host_ip = record[3]
        #         print(f'Length: {message_length} Host: {host} Host IP: {host_ip}')
        #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         s.connect((host_ip, 1234))
        #         full_msg = ''
        #         while True:
        #             msg = s.recv(1024)
        #             full_msg += msg.decode("utf-8")
        #             if len(full_msg) >= message_length:
        #                 print('Returning Full Message.')
        #                 return full_msg
        #     else:
        #         break

        t.cancel()

        return ast.literal_eval(self.response.decode("utf_8"))



#

