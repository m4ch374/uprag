const knowledgeKeys = {
  all: ["knowledge"] as const,
  lists: () => [...knowledgeKeys.all, "lists"] as const,
  get: () => [...knowledgeKeys.all, "get"] as const,
  getId: (id: string) => [...knowledgeKeys.get(), id] as const,
};

export default knowledgeKeys;
