// Demo residents and tools, loaded the first time the app opens.
export const demoResidents = [
  {
    id: "r1",
    name: "Ana Costa",
    email: "ana@example.com",
    street: "Mill Lane",
  },
  {
    id: "r2",
    name: "Ben Hall",
    email: "ben@example.com",
    street: "Mill Lane",
  },
  {
    id: "r3",
    name: "Chloe Brown",
    email: "chloe@example.com",
    street: "River Road",
  },
];

export const categories = [
  "Garden",
  "Power tools",
  "Hand tools",
  "Ladders",
  "Cleaning",
];

export const demoTools = [
  {
    id: "t1",
    ownerId: "r1",
    name: "Hedge trimmer",
    category: "Garden",
    condition: "Good",
    pickup: "Mill Lane 4",
  },
  {
    id: "t2",
    ownerId: "r2",
    name: "Cordless drill",
    category: "Power tools",
    condition: "Like new",
    pickup: "Mill Lane 9",
  },
  {
    id: "t3",
    ownerId: "r3",
    name: "Ladder 3 m",
    category: "Ladders",
    condition: "Worn",
    pickup: "River Road 2",
  },
  {
    id: "t4",
    ownerId: "r2",
    name: "Pressure washer",
    category: "Cleaning",
    condition: "Good",
    pickup: "Mill Lane 9",
  },
];
