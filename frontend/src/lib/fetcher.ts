import axios, {
  AxiosInstance,
  CreateAxiosDefaults,
  AxiosResponse,
  AxiosError,
} from "axios";
import { TEndpoint } from "./types/GlobalTypes";
import FetchError from "./errors/FetchError";
import { ErrorMessages } from "./constants/errors/ErrorMessages";
import { FetchStatusCode } from "./constants/errors/FetchStatusCodes";

type Method = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

type ContentType =
  | "application/java-archive"
  | "application/EDI-X12"
  | "application/EDIFACT"
  | "application/javascript"
  | "application/octet-stream"
  | "application/ogg"
  | "application/pdf"
  | "application/xhtml+xml"
  | "application/x-shockwave-flash"
  | "application/json"
  | "application/ld+json"
  | "application/xml"
  | "application/zip"
  | "application/x-www-form-urlencoded"
  | "multipart/form-data";

class Fetcher<T extends TEndpoint<unknown, unknown>> {
  private instance: AxiosInstance;

  private endpoint: string | undefined;

  private payload: T["request"] | undefined;

  private constructor(method: Method) {
    const axiosConf: CreateAxiosDefaults = {
      // INTERNAL_SERVER_ROUTE is empty string when it reaches client
      baseURL: import.meta.env.VITE_PUBLIC_SERVER_ROUTE,
      method,
      headers: {
        Accept: "application/json",
      },
    };

    this.instance = axios.create(axiosConf);
    return this;
  }

  static init = <T extends TEndpoint<unknown, unknown>>(
    method: Method,
    endpoint: string,
  ) => {
    const fetcher = new Fetcher<T>(method);

    fetcher.endpoint = endpoint;
    return fetcher;
  };

  withToken(token: string) {
    this.instance.defaults.headers.common.Authorization = `Bearer ${token}`;
    return this;
  }

  withData(data: T["request"], contentType: ContentType = "application/json") {
    this.instance.defaults.headers.common["Content-Type"] = contentType;

    this.payload = data;

    return this;
  }

  withQueryParams(params: T["request"]) {
    this.instance.defaults.params = params;
    return this;
  }

  async fetchData(signal?: AbortSignal) {
    try {
      const resp: AxiosResponse<T["response"], unknown> =
        await this.instance.request({
          url: this.endpoint,
          data: this.payload,
          signal,
        });

      return resp.data;
    } catch (e) {
      if (!axios.isAxiosError(e)) {
        throw new FetchError({
          message: ErrorMessages.GENERIC_ERROR_MSG,
          status_code: FetchStatusCode.PRE_REQUEST_ERROR,
        });
      }

      const errResp = e as AxiosError<{ error: string }, unknown>;
      throw new FetchError({
        message:
          errResp?.response?.data.error || ErrorMessages.GENERIC_ERROR_MSG,
        status_code: errResp?.response?.status || FetchStatusCode.REQUEST_ERROR,
      });
    }
  }
}

export default Fetcher;
