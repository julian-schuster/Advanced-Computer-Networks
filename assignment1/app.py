from ryu.base import app_manager 
from ryu.ofproto import ofproto_v1_0
from ryu.lib import dpid as dpid_lib
from ryu.controller import dpset
import threading
import json


class Firewall():


	def __init__(self):
	
		self.ProtocolTypes = {'IP':"IP",'UDP':"UDP",'TCP':"TCP"}

	def addFirewallRule(self,sw,rules,type,ports = None):

		ofp_protocol = sw.ofproto
		ofp_parser = sw.ofproto_parser

		
		if type == self.ProtocolTypes['IP']:
		
			flow_match = ofp_parser.OFPMatch(dl_type=0x0800, nw_src=rules['src'], nw_dst=rules['dst'])

			flow_mod = ofp_parser.OFPFlowMod(datapath=sw,
				                      match=flow_match,
				                      command=ofp_protocol.OFPFC_ADD		
						      )
			sw.send_msg(flow_mod)
			
		else:	
			NetworkProtocol = None
			DefaultPort = None

			if type == self.ProtocolTypes['TCP']:
				NetworkProtocol = 6
				DefaultPort = 22
			elif type ==  self.ProtocolTypes['UDP']:
				NetworkProtocol = 17
				DefaultPort = 5002

			if ports is not None and len(ports) > 0:
				for i in range(0,len(ports)):
					flow_match = ofp_parser.OFPMatch(dl_type=0x0800,
									nw_src=rules['src'],
									nw_dst=rules['dst'],
									nw_proto = NetworkProtocol,
									tp_dst = ports[i])

					flow_mod = ofp_parser.OFPFlowMod(datapath=sw,match=flow_match,command=ofp_protocol.OFPFC_ADD)
					sw.send_msg(flow_mod)
					
			else:

				flow_match = ofp_parser.OFPMatch(dl_type=0x0800,
								nw_src=rules['src'],
								nw_dst=rules['dst'],
								nw_proto = NetworkProtocol,
								tp_dst = DefaultPort)

				flow_mod = ofp_parser.OFPFlowMod(datapath=sw,match=flow_match,command=ofp_protocol.OFPFC_ADD)
				sw.send_msg(flow_mod)
					

					


class OpenFlowApp(app_manager.RyuApp):
  
  OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
  
  _CONTEXTS = {
    'dpset': dpset.DPSet,
  }  
  
  def __init__(self, *args, **kwargs):
    super(OpenFlowApp, self).__init__(*args, **kwargs)

    self._dpset = kwargs['dpset']

    self.datapathid= '0000000000000001'

    self.datapathid2= '0000000000000002'

    self.datapaths = {'path1':self.datapathid,'path2':self.datapathid2}

    threading.Timer(10.0, self._add_flows).start()

  def _add_flows(self):

    ofp_datapath = self._dpset.get(dpid_lib.str_to_dpid(self.datapaths['path1'])) 
    ofp_datapath2 = self._dpset.get(dpid_lib.str_to_dpid(self.datapaths['path2'])) 


    #Firewall
    firewall = Firewall()

    rules = None
    with open('firewallrules.json') as f:
    	rules = json.load(f)

    for rule in rules:
        CurrentDatapath = None
        if rule['datapath'] == 1:
            CurrentDatapath = ofp_datapath 
        elif rule['datapath'] == 2:
            CurrentDatapath = ofp_datapath2
		
        self.logger.info("add firewall rules: [dp=%s]", dpid_lib.dpid_to_str(CurrentDatapath.id))
        firewall.addFirewallRule(CurrentDatapath,{'src':rule['src_ip'],'dst':rule['dst_ip']},rule['proto'],rule['ports'])


    #SUBNETZ 1

    ofp_protocol = ofp_datapath.ofproto
    ofp_parser = ofp_datapath.ofproto_parser

    self.logger.info("add flows: [dp=%s]", dpid_lib.dpid_to_str(ofp_datapath.id))

    # Flow 1: all from port 1
    flow1_match = ofp_parser.OFPMatch(in_port=1)
    flow1_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow1_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow1_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow1_actions)
    
    ofp_datapath.send_msg(flow1_mod)

    # Flow 2: all from port 2
    flow2_match = ofp_parser.OFPMatch(in_port=2)
    flow2_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow2_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow2_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow2_actions)
    
    ofp_datapath.send_msg(flow2_mod)

    # Flow 3: all from port 3
    flow3_match = ofp_parser.OFPMatch(in_port=3)
    flow3_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow3_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow3_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow3_actions)
    
    ofp_datapath.send_msg(flow3_mod)

    #SUBNETZ 2

    ofp_protocol = ofp_datapath2.ofproto
    ofp_parser = ofp_datapath2.ofproto_parser

    self.logger.info("add flows: [dp=%s]", dpid_lib.dpid_to_str(ofp_datapath2.id))

    # Flow 4: all from port 1
    flow4_match = ofp_parser.OFPMatch(in_port=1)
    flow4_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow4_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath2,
                                      match=flow4_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow4_actions)
    
    ofp_datapath2.send_msg(flow4_mod)

    # Flow 5: all from port 2
    flow5_match = ofp_parser.OFPMatch(in_port=2)
    flow5_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow5_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath2,
                                      match=flow5_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow5_actions)
    
    ofp_datapath2.send_msg(flow5_mod)

    # Flow 6: all from port 3
    flow6_match = ofp_parser.OFPMatch(in_port=3)
    flow6_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow6_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath2,
                                      match=flow6_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow6_actions)
    
    ofp_datapath2.send_msg(flow6_mod)

  


	
    