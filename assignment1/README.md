# Programming Assignment 1: SDN
## Einfacher Router und Firewall

### Mininet Topologie
2 Hosts pro Subnetz (h1 und h2 bzw. h3 und h4), 1 Switch pro Subnetz  (sw1 und sw2), 1 Host als Router zwischen den beiden Subnetzen (router, vgl. Grafik)

![Topologie](/lab1/topo.png)

### Router
Der Router ist ein Host mit aktiviertem IP-Forwarding.

### Switches
Die Switches implementieren die Funktion der Firewall und das Forwarding in den Subnetzen bzw. zum Router.

### Firewall
Die Firewall lässt grundsätzlich alles durch, was nicht durch einen Eintrag in der Flow-Tabelle blockiert wird.
Alle Firewall-Regeln werden in firewallrules.json definiert und automatisch eingelesen.

Jede Regel ist ein Objekt mit den Properties `"proto", "datapath", "ports", "src_ip"` und `"dst_ip"`. Alle Properties müssen immer angegeben werden.

- "proto": zu blockierendes Protokoll (zulässige Parameter: `"IP", "TCP", "UDP"`)
- "datapath": Switch, auf dem die Regel festgelegt wird (zulässige Parameter: `1` (= Switch in 10.0.0.0/24), `2` (= Switch in 10.0.1.0/24))
- "ports": Array mit den zu blockierenden Ports (leeres Array für das gesamte Protokoll)
- "src_ip": Quell-IP-Adresse (als String)
- "dst_ip": Ziel-IP-Adresse (als String)

Hinweis: jeder Eintrag steht für eine Richtung, d.h. für Blockade einer Response muss ein eigener Eintrag auf dem anderen Switch angelegt werden.

#### Beispiel
```yaml
[
  {
    "proto": "IP",
    "datapath": 1,
    "ports": [],
    "src_ip": "10.0.0.2",
    "dst_ip": "10.0.1.2"
  },
  {
    "proto": "TCP",
    "datapath": 2,
    "ports": [
      5566,
      5567
    ],
    "src_ip": "10.0.1.3",
    "dst_ip": "10.0.0.3"
  },
  {
    "proto": "UDP",
    "datapath": 2,
    "ports": [
      5000,
      5001,
      5002
    ],
    "src_ip": "10.0.1.3",
    "dst_ip": "10.0.0.3"
  }
]
```


### Quellen
1. Router: https://whurst.net/wp-content/uploads/SDN-Mininet-Topologie.pdf
2. OpenFlow: Unterrichtsmaterial OpenFlowTopo.py
3. OpenFlow: Unterrichtsmaterial OpenFlowApp.py
4. OpenFlow: Unterrichtsmaterial OpenFlowAppLazySolution.py
5. OpenFlow: Unterrichtsmaterial OpenFlowTopoH3.py
