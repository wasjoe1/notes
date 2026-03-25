# Cast methods
"cast" - transmitting data packets to specific or all destinations in network communications
There are 3 main methods of casts:
- unicast -> 1 to 1
- multicast -> 1 to some
- broadcast -> 1 to ALL

## Recap (Optional)

# -------------------------------------------------------------------------------------------------
## Recap (Optional)
A recap that these are the network layers & the documentations that define the semantics for the network protocols,
before diving into how casting methods are involved in networks

* I wrote this section here as i was solidifying my understanding of the concepts below to ensure i dont mix up
casting methods with previously learn network concepts

### Network layers
1. App          -> HTTP, FIX
2. Transport    -> TCP, UDP
3. Network      -> IP

4. Data         -> Ethernet
5. Physical     -> Wire?

### IEEE vs IETF/ RFC
- IEEE (institute of electrical & electronics engineers)
- IETF (internet engineering task force)
- RFC (request for comments) - is published by IETF; defines technical standards, protocols, procedures, & best practices for the internet

organization        semantics documentation                
IEEE                IEEE 802.3(wired), IEEE 802.1(wireless)
IETF                RFCs (RFC 894, RFC 826 etc.)

* IEEE(layers 1 & 2) -> i.e. IEEE 802.3 focs on physical & data link layers; define HW voltages, cable types (copper vs fiber) etc.; define ethernet neworking MAC addressing etc.
* RCF/ IETF -> define network, transport & app layers; how data is routed(IP), how to reliably send packet(TCP), what it represents(HTTP)
