import { useMutation, UseMutationOptions } from "@tanstack/react-query";
import Fetcher from "../fetcher";
import { TAuthOnboard } from "../types/services/auth.services";

export const useOnboard = (
  accessToken: string,
  mutationOptions?: Omit<
    UseMutationOptions<unknown, unknown, void>,
    "mutationFn"
  >,
) =>
  useMutation({
    mutationFn: () =>
      Fetcher.init<TAuthOnboard>("POST", "/auth/onboard")
        .withToken(accessToken)
        .fetchData(),
    ...mutationOptions,
  });
