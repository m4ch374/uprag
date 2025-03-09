import { TEndpoint } from "../GlobalTypes";

export type TChat = {
  id: string;
  created_by: string;
  history: string;
  knowledge: string[];
};

// ===========================
// GET /chat/:id
// ===========================

export type TChatGetResponse = TChat;

export type TChatGet = TEndpoint<void, TChatGetResponse>;

// ===========================
// POST /chat
// ===========================

export type TChatCreateRequest = {
  user_query: string;
  knowledge: string[];
};

export type TChatCreateResponse = TChat;

export type TChatCreate = TEndpoint<TChatCreateRequest, TChatCreateResponse>;

// ===========================
// POST /chat/:id
// ===========================

export type TChatContinueRequest = {
  user_query: string;
  knowledge: string[];
};

export type TChatContinueResponse = TChat;

export type TChatContinue = TEndpoint<
  TChatContinueRequest,
  TChatContinueResponse
>;
