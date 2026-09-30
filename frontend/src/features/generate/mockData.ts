export interface ServiceDetail {
  id: string;
  type: string;
  location: string;
  status: "Active" | "Inactive" | "Suspended";
}

export interface MockCustomer {
  id: string;
  name: string;
  services: ServiceDetail[];
}

export const MOCK_CUSTOMERS: MockCustomer[] = [
  {
    id: "CUST-1001",
    name: "ASG India",
    services: [
      { id: "SRV-A1", type: "MPLS", location: "Mumbai HQ", status: "Active" },
      { id: "SRV-A2", type: "ILL", location: "Delhi Branch", status: "Active" },
      { id: "SRV-A3", type: "P2P", location: "Bangalore Hub", status: "Inactive" },
    ]
  },
  {
    id: "CUST-1002",
    name: "Sun Pharma",
    services: [
      { id: "SRV-S1", type: "SD-WAN", location: "Ahmedabad", status: "Active" },
      { id: "SRV-S2", type: "MPLS", location: "Pune", status: "Active" },
    ]
  },
  {
    id: "CUST-1003",
    name: "Tata Motors",
    services: [
      { id: "SRV-T1", type: "ILL", location: "Pune Plant", status: "Active" },
      { id: "SRV-T2", type: "P2P", location: "Mumbai Corp", status: "Active" },
      { id: "SRV-T3", type: "SD-WAN", location: "Chennai", status: "Active" },
      { id: "SRV-T4", type: "MPLS", location: "Jamshedpur", status: "Suspended" },
    ]
  },
  {
    id: "CUST-1004",
    name: "HDFC Bank",
    services: [
      { id: "SRV-H1", type: "MPLS", location: "Mumbai", status: "Active" },
      { id: "SRV-H2", type: "MPLS", location: "Delhi", status: "Active" },
    ]
  },
  {
    id: "CUST-1005",
    name: "Reliance Industries",
    services: [
      { id: "SRV-R1", type: "ILL", location: "Navi Mumbai", status: "Active" },
      { id: "SRV-R2", type: "SD-WAN", location: "Jamnagar", status: "Active" },
      { id: "SRV-R3", type: "MPLS", location: "Hazira", status: "Active" },
    ]
  },
  {
    id: "CUST-1006",
    name: "Wipro",
    services: [
      { id: "SRV-W1", type: "ILL", location: "Bangalore", status: "Active" },
    ]
  },
  {
    id: "CUST-1007",
    name: "Infosys",
    services: [
      { id: "SRV-I1", type: "SD-WAN", location: "Mysore", status: "Active" },
    ]
  }
];
