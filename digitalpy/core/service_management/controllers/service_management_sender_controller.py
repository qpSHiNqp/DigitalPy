#######################################################
# 
# core_name_controller.py
# Python implementation of the Class service_management
# Generated by Enterprise Architect
# Created on:      16-Dec-2022 10:56:02 AM
# Original author: Giu Platania
# 
#######################################################
from typing import List

from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.IAM.iam_facade import IAM

USER_DELIMITER = ";"

class ServiceManagementSenderController(Controller):
	"""contains the business logic related to sending messages to services
	"""

	def __init__(self, request, response, service_management_action_mapper, sync_action_mapper, configuration):
		super().__init__(request, response, sync_action_mapper, configuration)
		self.iam = IAM(sync_action_mapper, request, response, configuration)

	def initialize(self, request: Request, response: Response):
		self.request = request
		self.response = response
		self.iam.initialize(request, response)

	def broadcast_service_management(self, Event):
		"""this method will broadcast the component
		"""
		pass

	def publish(self, recipients: List[str], message: Node, **kwargs) -> List[str]:
		"""this method is used to create the topic to publish a message
		to a set of services based on the recipients

		Args:
			recipients (List[str]): a list of recipients id's
			model_object (Node): the message to be sent to the list of recipients

		Returns:
			List[str]: a list of topics to which the message should be published

		"""
		main_topics = {}

		return_topics: List[str] = []

		self.iam.get_connections_by_id(recipients)

		for recipient_object in self.response.get_value("connections"):
			recipient_main_topic = f"/{recipient_object.service_id}/{recipient_object.protocol}/{self.response.get_action()}/"
			if recipient_main_topic in main_topics:
				main_topics[recipient_main_topic]+= str(recipient_object.get_oid())+USER_DELIMITER
			else:
				main_topics[recipient_main_topic] = str(recipient_object.get_oid())+USER_DELIMITER
		
		# iterate the main topics dictionary,
		# concatenate the ids and finally add them
		# all into one list 
		# TODO add memoization to prevent duplicate serialization of the same protocol
		for main_topic, ids in main_topics.items():
			self.request.set_value("protocol", main_topic.split("/")[2])
			sub_response = self.execute_sub_action("serialize")
			formatter = ObjectFactory.get_instance("formatter")
			formatter.serialize(sub_response)
			return_topics.append(main_topic.encode()+ids.encode()+b","+sub_response.get_values())

		self.request.set_value("topics", return_topics)

	def execute(self, method = None):
		pass
