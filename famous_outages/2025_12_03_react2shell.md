# 2025_12_03_react2shell

## description
- issue casued by a serialization-related bug in React that Amazon helped mitigate
- React vulnerability CVE-2025-55182 aka React2Shell:
    unsafe handling of serialized data sent from client to server in react server components (refer to context below to understand react server components)
- Cloudflare in an attempt to mitigate this issue, took down itself
- related link: https://www.youtube.com/watch?v=7vw445i8gOI&t=20s => from primetime "How React took down Cloudflare" 

## context (react server components)
in classic React: => SPA (single page apps)
    Browser (client) -> downloads JS -> JS runs entirely in browser
    
    => react runs entirely in browser => server sends JS files
    => everything is static; classic client-side react

in RSC (React server components):
    browser (client) -req-> server (node.js running React) -> server execs React components & then serializes component output (RSC payload) -> browser deserializes & renders
    
    => runs react on the server
    => executess server components (browser will only execute client components)
    => this is a hybrid of client-side & server-side rendering (does not completely hydrate the html and send only static html to the client)
    => instead it sends a binary message via the flight protocol, & the client side reaceives a React payload 

## problem
React's issue:
- affected versions of React did not properly validate/ safely deserialize incoming payloads
- attacker could potentially craft a malicious serialized payload that upon deserialization at the server, result in unauthenticated remote code execution (RCE) on the server
- basically unauthenticated code could potentially run on the server side, compromising the entire server => classic unsafe deserialization bug

Relation to cloudflare:
- when trying to mitigate this cloudflare took down itself => outage occurred
    why did cloudflare want to prevent this?
    - protect customers: cloudflare servers sit in front of large amts of websites & can help mitigate malicious reqs
    - protect their infrastructure: the unauthenticated code will not run on cloudflare (proxy server) BUT even if origin server doesnt crash, exploit traffic can overwhelm cloudflare edges <= malicious payloads can cause DOS(denial of service) effects on cloudflare nodes
- bug itself didnt cause cloudflare outage; it was the mitigation effort
    - serialized payloads can be large
    - cloudflare WAF(web application firewall) inspects requests in-memory before forwarding them to the origin server(actual domain severs)
    - originally, cloudflare's WAF had a buffer limit of 128kb => some serizlized payload > 128 kb & thus cloudflare's WAF would not inspect the whole payload/ only see the first 128kb of data
    - cloudflare increased it to 1MB(as suggested by next.js) <= ISSUE WAS CAUSED HERE!!
- issue breakdown:
    - FL1 (front line 1) program written in lua, cloudflare's 1st layer edge request processing program, handles HTTP/HTTPS reqs at the edge nodes b4 any other internal components => this program was the one causing issue
    - FL2 (front line 2) program same as FL1 but written in rust => no issue
    - IT(internal testing) tool -> used in the FL1 & FL2 programs; it could nto handle the new larger buffer size & hence was turned off
    - FL1 then went down as a specific code was to run the internal testing tool & use the result from it
    - upon "execute", NULL was returned & then FL1 processes crashed
    - whereas for RUST, the NULL did not cause any issues for it
