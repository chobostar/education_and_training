# Computer Networking Fundamentals For Developers, DevOps, and Platform Engineers

https://labs.iximiuz.com/courses/computer-networking-fundamentals?x=1

## LAN, VLAN, VXLAN

LAN (Local Area Network) - broadly a computer network that interconnects computers within a limited area such as a residence, school, office building, or data center. A LAN is not limited to a single IP subnetwork. Like a Wide area network (WAN), a LAN can consist of multiple IP networks communicating via routers. The main determinant of a LAN is the locality (i.e. proximity) of the participants, not the L3 topology.

Collision domain - a network segment (via a shared medium or hubs) where simultaneous data transmissions collide with one another. <br>
👎  The bigger a collision domain the worse for the network.

L2 segment - multiple L1 segments interconnected using a shared switch (aka bridge) or (somewhat recursively) multiple L2 segments merged into a bigger L2 segment by an upper-layer switch where nodes can communicate with each other using their L2 addresses (MAC) or by broadcasting frames.

**VLAN** - (broadly) any broadcast domain that is partitioned and isolated at the data link layer (L2).
Frames with different IDs logically belong to different networks. This creates the appearance and functionality of network traffic that is physically on a single network segment but acts as if it is split between separate network segments. VLANs can keep network applications separate despite being connected to the same physical (or virtual) network.

L3 - the task of sending an IP packet within an L3 segment boils down to sending an Ethernet frame with the IP packet inside to the L2 segment's node that owns that destination IP.

there cannot be more than 4096 VLANs sharing the same underlying L2 segment.

When the IP to MAC translation is not known, the transmitting node sends a broadcast L2 frame with a query like "Who has IP 192.168.38.12?"
Once the destination MAC address is known for the sender node, it just wraps an IP packet into an L2 frame destined to that MAC address. 
Thus, an L3 segment heavily relies on the underlying L2 segment capabilities.

Technically nothing prevents us from having multiple L3 segments over a single L2 broadcast domain.
a single L3 segment can be configured over multiple L2 segments interconnected via a router. The technique is called Proxy ARP and it's documented in (rather dated) RFC 1027

Communication between any two L3 segments always requires **at least one router**.

Routers are usually connected to multiple network segments simultaneously, and when the gateway router gets such a frame, 
it unwraps it and resends the underlying IP packet using one of its other interfaces.

In interesting corollary to this - **a next-hop router of every router has to reside on one of the L2 segments the router is directly connected to**.

On every **VXLAN** node, outgoing Ethernet frames are captured, then wrapped into UDP datagrams (encapsulated), and sent over an L3 network to the destination VXLAN node. 
On arrival, Ethernet frames are extracted from UDP packets (decapsulated) and injected into the destination's network interface. 
This technique is called tunneling. As a result, **VXLAN nodes create a virtual L2 segment**, hence an L2 broadcast domain.

Most of the real-world VXLANs probably reside in one or few tightly connected data centers. However, since VXLAN requires only IP to IP connectivity of the participating nodes, 
it essentially allows one to turn arbitrary internetwork nodes into a virtualized L2 segment.

VXLAN can be even seen as inverse to VLAN:
- VLAN splits a single L2 segment (and broadcast domain) into multiple non-intersecting segments that can be used to set up multiple L3 segments. 
- VXLAN, on the contrary, can combine multiple L3 segments back into one virtual L2 segment. 

## Bridge vs. Switch
https://labs.iximiuz.com/courses/computer-networking-fundamentals/bridge-vs-switch

