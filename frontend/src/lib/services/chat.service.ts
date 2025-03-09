import {
  QueryClient,
  useMutation,
  UseMutationOptions,
  useQuery,
  UseQueryOptions,
} from "@tanstack/react-query";
import Fetcher from "../fetcher";
import {
  TChatCreate,
  TChatCreateRequest,
  TChatCreateResponse,
  TChatGet,
  TChatGetResponse,
} from "../types/services/chat.services";
import chatKeys from "../constants/chat.keys";
import { TChatGPTHistoryItem } from "../types/GlobalTypes";

export const useCreateChat = (
  accessToken: string,
  queryClient: QueryClient,
  mutationOptions?: Omit<
    UseMutationOptions<TChatCreateResponse, unknown, TChatCreateRequest>,
    "mutationFn"
  >,
) =>
  useMutation({
    mutationFn: (body: TChatCreateRequest) =>
      Fetcher.init<TChatCreate>("POST", "/chat")
        .withToken(accessToken)
        .withData(body)
        .fetchData(),
    onSuccess: data => {
      queryClient.setQueryData(chatKeys.getId(data.id), data);
    },
    ...mutationOptions,
  });

export const useGetChat = (
  accessToken: string,
  chatId: string,
  queryOptions?: Omit<
    UseQueryOptions<TChatGetResponse, unknown, TChatGPTHistoryItem[]>,
    "queryKey" | "queryFn"
  >,
) => {
  return useQuery({
    queryKey: chatKeys.getId(chatId),
    queryFn: () =>
      Fetcher.init<TChatGet>("GET", `/chat/${chatId}`)
        .withToken(accessToken)
        .fetchData(),
    select: data => JSON.parse(data.history) as TChatGPTHistoryItem[],
    enabled: !!chatId && !!accessToken,
    ...queryOptions,
  });
};
