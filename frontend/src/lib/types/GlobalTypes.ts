export type TEndpoint<Request, Response> = {
  request: Request;
  response: Response;
};

export type TChatGPTHistoryItem = {
  role: "system" | "user" | "assistant" | "developer";
  content: string;
};
