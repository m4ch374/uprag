const chatKeys = {
  all: ["chat"] as const,
  lists: () => [...chatKeys.all, "lists"] as const,
  get: () => [...chatKeys.all, "get"] as const,
  getId: (id: string) => [...chatKeys.get(), id] as const,
};

export default chatKeys;
