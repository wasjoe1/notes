# Intro
# ping vs trace route vs netcat
# ICMP vs IP packets
# TCP vs UDP
# Network Tables
# Miscellaneous

# ------------------------------------------------------------------------------------------------------------
# Intro

## Network layers
[5 layer network model]
1. App          -> HTTP, FIX, SMTP, IMAP,                           App message
                FTP (port 21), SFTP (port 22),
                DNS (port 53), DHCP (port 67 server, 68 client)
2. Transport    -> TCP, UDP                                         TCP / UDP segment               header (ports) + message
3. Network      -> IP                                               IP datagram                     header(IP addr) + header (ports) + message

4. Data         -> Ethernet                                         Ethernet frames                 header (MAC addr) + header(IP addr) + header (ports) + message
5. Physical     -> Wire?                                            actual 1s & 0s

## IEEE vs IETF/ RFC
- IEEE (institute of electrical & electronics engineers)
- IETF (internet engineering task force)
- RFC (request for comments) - is published by IETF; defines technical standards, protocols, procedures, & best practices for the internet

organization        semantics documentation                
IEEE                IEEE 802.3(wired), IEEE 802.1(wireless)
IETF                RFCs (RFC 894, RFC 826 etc.)

* IEEE(layers 1 & 2) -> i.e. IEEE 802.3 focs on physical & data link layers; define HW voltages, cable types (copper vs fiber) etc.; define ethernet neworking MAC addressing etc.
* RCF/ IETF -> define network, transport & app layers; how data is routed(IP), how to reliably send packet(TCP), what it represents(HTTP)


# ------------------------------------------------------------------------------------------------------------
# ping vs trace route vs netcat
- ping [L2]
    => uses ICMP echo request and Echo reply messages
    - the host reponds if the host is reachable
    - else it might be down or packets filtered
    * checks host & latency
- trace route [L2_&_L3]
    => sends multiple small UDP packets with increasing TTL, such that u can see when the packets are dropped and an ICMP error message is returned at the network layer
    - each router decrements TTL by 1, when TTL =0, router replied with ICMP "time exceeded"
    - trace route captures these replies & discovers the path (each hop)
    * checks the path
- netcat [L3]
    - sends UDP/ TCP packets to the remote server at a port
    - host port can be open, closed, filtered
        - open -> process bound to that port, ready to receive packet
        - closed -> OS replies with ICMP "port unreachable"     => many firewalls drop ICMP errors, so might still might get no reply
        - filtered -> firewall blocked, no ICMP reply
    - echo "hello" | nc -u 192.168.1.5 5000 => -u flag switches netcat to use UDP instead of TCP

# ------------------------------------------------------------------------------------------------------------
# ICMP vs IP packets
* why can u ping but not connect to host?
* why can u not ping but can connect to host?

# ------------------------------------------------------------------------------------------------------------
# TCP vs UDP

# ------------------------------------------------------------------------------------------------------------
# Network Tables
- NAT(network address translation) table    | translates private IP to public IP | <private IP : public IP> | routers | [L3] Nework layer; since its IP to IP, can change ports also (since ur mapping the private ip to a port on the public addres)
- Forwarding table                          | forwards traffic to the next hop interface/ IP | <public IP: public IP> | routers | [L3] Network layer; since its IP to IP
- ARP table                                 | routes traffic from router/host to correct mac address | <private IP: MAC address> | routers & host | [L3] Network & [L2] data link layer; there is intereaction between MAC & IP
- Mac addressing table                      | Resolves mac address to the interface | <MAC address: interface> | in routers, switches & hosts | [L2] Data Link layer; only deals with MAC address & not physical interfaces

* there is actually a key difference between __Forwarding__ & __Routing__ tables though they map the same thing
* Forwarding table stores the simplified, optimized version of the routing table 
* Routing 

# ------------------------------------------------------------------------------------------------------------
# Miscellaneous
* 7 layer is the OSI model
* 5 layer is the TCP/IP model
* DHCP and DNS uses UDP