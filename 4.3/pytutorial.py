# Tutorial Controller
# Starts as a hub, and your job is to turn this into a learning switch.

import logging

from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.ipv4 import ipv4
from nox.lib.packet.packet_utils import mac_to_str, mac_to_int, ip_to_str, ipstr_to_int

log = logging.getLogger('nox.coreapps.tutorial.pytutorial')


class pytutorial(Component):

	def __init__(self, ctxt):
		Component.__init__(self, ctxt)
		# Use this table to store MAC addresses in the format of your choice;
		# Functions already imported, including mac_to_str, and mac_to_int,
		# should prove useful for converting the byte array provided by NOX
		# for packet MAC destination fields.
		# This table is initialized to empty when your module starts up.
		self.mac_to_port = {} # key: MAC addr; value: port
		
	def learn_and_forward(self, dpid, inport, packet, buf, bufid):
		"""Learn MAC src port mapping, then flood or send unicast."""
		ip_header = packet.find('ipv4')
		idle_timeout = 600
		hard_timeout = 3600
		attrs = extract_flow(packet)
		attrs[core.IN_PORT] = inport
		attrs[core.DL_DST] = packet.dst
		if dpid == 1:
		# policies for switch 1
			if ip_header is not None:
				ipstr = ip_to_str(ip_header.dstip)
				if ipstr == "10.0.0.4":
					outport = 1
					actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
					self.send_openflow(dpid, bufid, buf, actions, inport)
					#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
				elif ipstr == "10.0.0.5":
					outport = 2
					actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
					self.send_openflow(dpid, bufid, buf, actions, inport)
					#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)	
				elif ipstr == "10.0.0.6":
					outport = 3
					actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
					self.send_openflow(dpid, bufid, buf, actions, inport)
					#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
				elif ipstr == "10.0.0.7":
					outport = 4
					actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
					self.send_openflow(dpid, bufid, buf, actions, inport)
					#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
			else:
				if mac_to_int(packet.src) == 4:
					outport = [2,3]
					actions = [[openflow.OFPAT_OUTPUT, [0, 2]],[openflow.OFPAT_OUTPUT, [0, 3]]]
				elif mac_to_int(packet.src) == 5:
					outport = [1,3]
					actions = [[openflow.OFPAT_OUTPUT, [0, 1]],[openflow.OFPAT_OUTPUT, [0, 3]]]
				else: 			
					outport = [1,2]
					actions = [[openflow.OFPAT_OUTPUT, [0, 1]],[openflow.OFPAT_OUTPUT, [0, 2]]]	
				self.send_openflow(dpid, bufid, buf, actions, inport)

		if dpid == 2:
		# policies for switch 2
			if mac_to_int(packet.src) == 7:
				if ip_header is not None:
					ipstr = ip_to_str(ip_header.dstip)
					if ipstr == "10.0.0.4" or ipstr == "10.0.0.5":	
						outport = 1
						actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
						self.send_openflow(dpid, bufid, buf, actions, inport)
						#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
					elif ipstr == "10.0.0.6":
						outport = 3
						actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
						self.send_openflow(dpid, bufid, buf, actions, inport)
						#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
				else:
					actions = [[openflow.OFPAT_OUTPUT, [0, 1]], [openflow.OFPAT_OUTPUT, [0, 3]]]
					outport = [1,3]
					self.send_openflow(dpid, bufid, buf, actions, inport)

			else:
				if ip_header is not None:
					ipstr = ip_to_str(ip_header.dstip)
					if ipstr == "10.0.0.4" or ipstr == "10.0.0.5":	
						outport = 1
						actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
						self.send_openflow(dpid, bufid, buf, actions, inport)
						#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
					elif ipstr == "10.0.0.6":
						outport = 3
						actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
						self.send_openflow(dpid, bufid, buf, actions, inport)
						#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
					elif ipstr == "10.0.0.7":
						outport = 4
						actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
						self.send_openflow(dpid, bufid, buf, actions, inport)
						#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
				else:
					if mac_to_int(packet.src) == 4 or mac_to_int(packet.src) == 5: 
						actions = [[openflow.OFPAT_OUTPUT, [0, 3]], [openflow.OFPAT_OUTPUT, [0, 4]]]
						outport = [3,4]
					elif mac_to_int(packet.src) == 6:
						actions = [[openflow.OFPAT_OUTPUT, [0, 1]], [openflow.OFPAT_OUTPUT, [0, 4]]]	
						outport = [1,4]
					self.send_openflow(dpid, bufid, buf, actions, inport)
				
		if dpid == 3:
		# policies for switch 3
			ipstr = ip_to_str(ip_header.dstip)
			if ipstr == "10.0.0.4" or ipstr == "10.0.0.5":	
				outport = 2
				actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
				self.send_openflow(dpid, bufid, buf, actions, inport)
				#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
			else:
				outport = 1
				actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
				self.send_openflow(dpid, bufid, buf, actions, inport)
				#self.install_datapath_flow(dpid, attrs, idle_timeout, hard_timeout, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, buf)
		
		message = " packet to host " + str(mac_to_int(packet.dst)) + " from host " + str(mac_to_int(packet.src)) + " go to port " + str(outport) + " of switch " + str(dpid)
		log.info(message)		

	def packet_in_callback(self, dpid, inport, reason, len, bufid, packet):
		"""Packet-in handler""" 
		if not packet.parsed:
			log.debug('Ignoring incomplete packet')
		else:
			self.learn_and_forward(dpid, inport, packet, packet.arr, bufid)

		return CONTINUE

	def install(self):
		self.register_for_packet_in(self.packet_in_callback)

	def getInterface(self):
		return str(pytutorial)

def getFactory():
	class Factory:
		def instance(self, ctxt):
			return pytutorial(ctxt)

	return Factory()
