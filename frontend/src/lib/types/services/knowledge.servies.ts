import { TEndpoint } from "../GlobalTypes";

export type TKnowledge = {
  id: string;
  name: string;
  created_by: string;
  file_mime_type: string;
  file_extension: string;
  file_size: number;
};

// ===========================
// GET /knowledge
// ===========================

export type TKnowledgeListResonse = {
  knowledges: TKnowledge[];
};

export type TKnowledgeList = TEndpoint<void, TKnowledgeListResonse>;

// ===========================
// POST /knowledge
// ===========================

export type TKnowledgeCreateRequest = FormData;

export type TKnowledgeCreateResponse = TKnowledge;

export type TKnowledgeCreate = TEndpoint<
  TKnowledgeCreateRequest,
  TKnowledgeCreateResponse
>;

// ===========================
// POST /knowledge/:id
// ===========================

export type TKnowledgeDeleteResponse = { success: true };

export type TKnowledgeDelete = TEndpoint<void, TKnowledgeDeleteResponse>;
