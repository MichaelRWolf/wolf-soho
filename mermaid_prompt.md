### Prompt to Generate Mermaid Code

Take the following Markdown file, which describes a home network setup, including nodes, network connections, and modes of operation. Generate a Mermaid diagram that represents:

1. All nodes and their connections as described in the "Network Connections" section.
2. Separate subgraphs for each mode described in the "Modes" section (Offline Mode, Free WiFi Mode, Expensive WiFi Mode).

Use proper Mermaid syntax for the graph, and ensure subgraphs are labeled with descriptive titles matching the modes.

#### Input Example
```markdown
### Home Network Description

#### Nodes
1. Portable Router:
   - Acts as a repeater for WiFi or provides local LAN/WiFi access.
   - Can connect to external WiFi (e.g., public WiFi or iPhone hotspot).

2. Public WiFi:
   - Free internet access available in locations such as libraries or coffee shops.

3. iPhone Hotspot:
   - Mobile hotspot providing internet access (limited data and expensive).

4. MacBook:
   - Connects to the router via LAN/WiFi or directly to iPhone hotspot.
   - Accesses the NAS for local storage and uses the best available internet connection.

5. NAS:
   - Connects to the router via LAN/WiFi for local storage.
   - Can access the internet through the router, depending on the mode.

#### Network Connections
- Portable Router:
  - Can repeat WiFi signals (e.g., public WiFi or iPhone hotspot).
  - Provides LAN and WiFi connectivity for MacBook and NAS.

- MacBook:
  - Uses the Portable Router for NAS access and internet (when available).
  - Can connect directly to the iPhone hotspot for internet (bypassing the router).

- NAS:
  - Always connected to the Portable Router for local storage.
  - Internet access depends on the Portable Router's upstream connection.

#### Modes
1. Offline Mode:
   - Internet: None.
   - Access: MacBook communicates with NAS through the Portable Router.

2. Free WiFi Mode:
   - Internet: Portable Router connects to public WiFi and shares internet with both MacBook and NAS.
   - Access: MacBook communicates with NAS through the Portable Router.

3. Expensive WiFi Mode:
   - Internet: MacBook connects directly to iPhone hotspot for internet. NAS does not use the internet to save costs.
   - Access: MacBook communicates with NAS through the Portable Router.

#### Steps to Enter Each Mode

1. Offline Mode:
   - Ensure the Portable Router is not connected to any upstream WiFi.
   - Connect the MacBook and NAS to the Portable Router via LAN/WiFi.

2. Free WiFi Mode:
   - Connect the Portable Router to a public WiFi network in repeater mode.
   - Connect the MacBook and NAS to the Portable Router via LAN/WiFi.

3. Expensive WiFi Mode:
   - Connect the MacBook directly to the iPhone hotspot for internet.
   - Ensure the Portable Router is not connected to the iPhone hotspot.
   - Connect the MacBook and NAS to the Portable Router via LAN/WiFi for local access only.
