import React from "react";
import { Navigate, Route, Routes } from "react-router";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import { useUser } from "@clerk/clerk-react";
import ProtectedRoutes from "./components/ProtectedRoutes";
import ChatPage from "./pages/ChatPage";
import OnboardingPage from "./pages/OnboardingPage";
import ChatPageID from "./pages/ChatPageID";
import KnowledgePage from "./pages/KnowledgePage";

// no lazy load yolo
const App: React.FC = () => {
  const { isSignedIn } = useUser();

  return (
    <Routes>
      <Route
        path="/"
        element={isSignedIn ? <Navigate to="/onboard" /> : <SignInPage />}
      />
      <Route path="/sign-in" element={<SignInPage />} />
      <Route path="/sign-up" element={<SignUpPage />} />
      <Route element={<ProtectedRoutes />}>
        <Route path="/onboard" element={<OnboardingPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/chat/:id" element={<ChatPageID />} />
        <Route path="/knowledge" element={<KnowledgePage />} />
      </Route>
    </Routes>
  );
};

export default App;
