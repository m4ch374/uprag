import { StatusCodes } from "http-status-codes";

enum FetchCode {
  PRE_REQUEST_ERROR = -1,
  REQUEST_ERROR = -2,
}

export const FetchStatusCode = {
  ...StatusCodes,
  ...FetchCode,
};
