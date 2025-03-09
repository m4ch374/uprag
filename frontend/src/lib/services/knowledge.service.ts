import { useQuery } from "@tanstack/react-query";
import knowledgeKeys from "../constants/knowledge.keys";
import Fetcher from "../fetcher";
import { TKnowledgeList } from "../types/services/knowledge.servies";

export const useListKnowledge = (
  accessToken: string,
  queryOptions?: Omit<TKnowledgeList, "queryKey" | "queryFn">,
) =>
  useQuery({
    queryKey: knowledgeKeys.lists(),
    queryFn: () =>
      Fetcher.init<TKnowledgeList>("GET", "/knowledge")
        .withToken(accessToken)
        .fetchData(),
    enabled: !!accessToken,
    ...queryOptions,
  });
