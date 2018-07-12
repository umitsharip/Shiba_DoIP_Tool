import socket 
import sys

PROTOCOL_VERSION = 							'02'
INVERSE_PROTOCOL_VERSION = 					'FD'

##Payload type definitions##
DOIP_GENERIC_NEGATIVE_ACKNOWLEDGE = 		'0000'
DOIP_VEHICLE_ID_REQUEST = 					'0001'
DOIP_VEHICLE_ID_REQUEST_W_EID = 			'0002'
DOIP_VEHICLE_ID_REQUEST_W_VIN = 			'0003'
DOIP_VEHICLE_ANNOUNCEMENT_ID_RESPONSE = 	'0004'
DOIP_ROUTING_ACTIVATION_REQUEST = 			'0005'
DOIP_ROUTING_ACTIVAQTION_RESPONSE = 		'0006'
DOIP_ALIVE_CHECK_REQUEST = 					'0007'
DOIP_ALIVE_CHECK_RESPONSE = 				'0008'
#0x009-0x4000: Reserved by ISO13400
DOIP_ENTITY_STATUS_REQUEST = 				'4001'
DOIP_ENTITY_STATUS_RESPONSE = 				'4002'
DOIP_DIAGNOSTIC_POWER_MODE_INFO_REQUEST = 	'4003'
DOIP_DIAGNOSTIC_POWER_MODE_INFO_RESPONSE = 	'4004'
#0x4005-0x8000 Reserved by ISO13400
DOIP_DIAGNOSTIC_MESSAGE = 					'8001'
DOIP_DIAGNOSTIC_POSITIVE_ACKNOWLEDGE = 		'8002'
DOIP_DIAGNOSTIC_NEGATIVE_ACKNOWLEDGE = 		'8003'
#0x8004-0xEFFF Reserved by ISO13400
#0xF000-0xFFFF Reserved for manufacturer-specific use


def DoIP_Pack():
    print "DoIP Pack"

class DoIP_Client:
	def __init__(self,address = '172.26.200.15',port = 13300, ECUAddr = '1111'):
		#init tcp socket
		self.localIPAddr = address 
		self.localPort = port
		self.localECUAddr = ECUAddr
		self.targetIPAddr = None
		self.targetPort = None
		self.targetECUAddr = None
		self.isTCPConnected = 0
		self.isRoutingActivated = 0

		try:
			self.TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.TCP_Socket.bind((self.localIPAddr,self.localPort))
			print "Socket successfully created: Binded to %s:%d" %(address, port)
		except socket.error as err:
			print "Socket creation failed with error %s" %(err)
			
	def __enter__(self):
		return self
				
	def ConnectToDoIPServer(self, address = '172.26.200.101', port = 13400,  routingActivation = True, targetECUAddr = '2004'):
		if self.isTCPConnected:
			print "Error :: Already connected to a server. Close the connection before starting a new one"
		else:
			try:
				print "Connecting to DoIP Server at %s:%d" %(address,port)
				self.targetIPAddr = address
				self.targetPort = port
				self.TCP_Socket.connect((address, port)) 
				self.isTCPConnected = 1	
			except socket.error as err: 
				print "Unable to connect to socket at %s:%d. Socket failed with error %s" % (address, port, err)
				self.targetIPAddr = None
				self.targetPort = None
				self.isTCPConnected = 0
			
		if routingActivation == True: 
			self.RequestRoutingActivation()
			
	def DisconnectFromDoIPServer(self):
		if self.isTCPConnected:
			try: 
				print "Disconnecting from DoIP server"
				self.TCP_Socket.shutdown(socket.SHUT_RDWR)
				self.isTCPConnected = 0
			except socket.error as err:
				print "Unable to disconnect from socket at %s:%d. Socket failed with error %s." %(self.targetIPAddr, self.targetPort, err)
				print "Warning :: Socket is currently in a metastable state." 
			finally:
				self.targetIPAddr = None
				self.targetPort = None
				self.isTCPConnected = 0
		else:
			print "Error::DoIP client is not connected to a server"
	
	def RequestRoutingActivation(self,targetECUaddr = '2004'):
		if self.isTCPConnected:
			try: 
				print "Requesting routing activation"
				############self.TCP_Socket.send()#############
				############self.TCP_Socket.receive()##########
				self.isRoutingActivated = 1;
				self.targetECUAddr = targetECUaddr
			except socket.error as err:
				print "Unable to activate routing with ECU:%d. Socket failed with error %s" % (ECUID, err)
				self.isRoutingActivated = 0;
				self.targetECUAddr = None
		else:
			print "Unable to request routing activation. Currently not connected to a DoIP server"	 
    
	def	Terminate(self):
		print "Closing DoIP Client"
		self.TCP_Socket.close()
		print "Good bye"
	
	def __exit__(self, exc_type, exc_value, traceback):
		print "Closing DoIP Client"
		self.TCP_Socket.close()
        
        
if __name__ == '__main__':
	iHub = DoIP_Client()
	iHub.ConnectToDoIPServer()
	iHub.DisconnectFromDoIPServer()
	iHub.ConnectToDoIPServer()
	iHub.DisconnectFromDoIPServer()
	iHub.Terminate()