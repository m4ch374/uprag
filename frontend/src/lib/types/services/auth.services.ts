import { TEndpoint } from "../GlobalTypes";

// ===========================
// POST /auth/onboard
// ===========================

export type TAuthOnboard = TEndpoint<void, { sucess: true }>;
