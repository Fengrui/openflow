"""Custom topology example


Three connected switches plus 5 hosts:

           host     switch    host
             \      /    \     /
              \    /      \   /
     host --- switch --- switch --- host
 
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo, Node

class MyTopo( Topo ):

    def __init__( self, enable_all = True ):
        "Create custom topo."

        # Add default members to class.
        super( MyTopo, self ).__init__()

        # Set Node IDs for hosts and switches
        h4 = 4
        h5 = 5
        h6 = 6
        h7 = 7
        s1 = 1
        s2 = 2
        s3 = 3

        # Add nodes
        self.add_node( s1, Node( is_switch=True ) )
        self.add_node( s2, Node( is_switch=True ) )
        self.add_node( s3, Node( is_switch=True ) )
        self.add_node( h4, Node( is_switch=False ) )
        self.add_node( h5, Node( is_switch=False ) )
        self.add_node( h6, Node( is_switch=False ) )
        self.add_node( h7, Node( is_switch=False ) )	

        # Add edges
        self.add_edge( h4, s1 )
        self.add_edge( h5, s1 )
        self.add_edge( s1, s2 )
        self.add_edge( s2, s3 )
        self.add_edge( s1, s3 )
        self.add_edge( s2, h6 )
        self.add_edge( s2, h7 )

        # Consider all switches and hosts 'on'
        self.enable_all()


topos = { 'mytopo': ( lambda: MyTopo() ) }
