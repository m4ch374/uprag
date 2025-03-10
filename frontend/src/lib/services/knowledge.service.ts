import {
  QueryClient,
  useMutation,
  UseMutationOptions,
  useQuery,
} from "@tanstack/react-query";
import knowledgeKeys from "../constants/knowledge.keys";
import Fetcher from "../fetcher";
import {
  TKnowledgeCreate,
  TKnowledgeCreateRequest,
  TKnowledgeCreateResponse,
  TKnowledgeDelete,
  TKnowledgeDeleteResponse,
  TKnowledgeList,
  TKnowledgeListResonse,
} from "../types/services/knowledge.servies";

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

export const useCreateKnowledge = (
  accessToken: string,
  queryClient: QueryClient,
  mutationOptions?: Omit<
    UseMutationOptions<
      TKnowledgeCreateResponse,
      unknown,
      TKnowledgeCreateRequest,
      unknown
    >,
    "mutationFn"
  >,
) =>
  useMutation({
    mutationFn: (knowledge: TKnowledgeCreateRequest) =>
      Fetcher.init<TKnowledgeCreate>("POST", "/knowledge")
        .withToken(accessToken)
        .withData(knowledge, "multipart/form-data")
        .fetchData(),
    onSuccess: resp =>
      queryClient.setQueryData(
        knowledgeKeys.lists(),
        (prev: TKnowledgeListResonse) => ({
          ...prev,
          knowledges: [...(prev?.knowledges || []), resp],
        }),
      ),
    ...mutationOptions,
  });

export const useDeleteKnowledge = (
  accessToken: string,
  queryClient: QueryClient,
  mutationOptions?: Omit<
    UseMutationOptions<TKnowledgeDeleteResponse, unknown, string, unknown>,
    "mutationFn"
  >,
) =>
  useMutation({
    mutationFn: (knowledge_id: string) =>
      Fetcher.init<TKnowledgeDelete>("DELETE", `/knowledge/${knowledge_id}`)
        .withToken(accessToken)
        .fetchData(),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: knowledgeKeys.lists() }),
    ...mutationOptions,
  });
