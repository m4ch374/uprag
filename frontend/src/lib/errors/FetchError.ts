import { FetchStatusCode } from "../constants/errors/FetchStatusCodes";

class FetchError extends Error {
  public stats_code: number | undefined = undefined;

  constructor(err_obj: { status_code: number; message: string }) {
    super(err_obj.message);
    this.stats_code = err_obj.status_code;
  }

  // Epic ts jargon
  isUnauthorized() {
    return (
      this.stats_code ===
      parseInt((FetchStatusCode.UNAUTHORIZED as number).toString())
    );
  }
}

export default FetchError;
