import useToken from "@/lib/hooks/useToken.hooks";
import { useOnboard } from "@/lib/services/auth.service";
import { useAuth } from "@clerk/clerk-react";
import { useQueryClient } from "@tanstack/react-query";
import React, { useEffect } from "react";
import { useNavigate } from "react-router";

const OnboardingPage: React.FC = () => {
  const token = useToken();

  const { signOut } = useAuth();
  const queryClient = useQueryClient();

  const navigate = useNavigate();

  const onboard = useOnboard(token, {
    onSuccess: () => void navigate("/chat"),
    onError: async e => {
      await signOut();
      queryClient.clear();
      await navigate("/");
      console.log(e);
    },
  });

  useEffect(() => {
    if (!token || onboard.isPending) return;

    onboard.mutate();
  }, [token]);

  return (
    <div className="flex flex-col items-center justify-center w-full h-screen text-4xl font-bold">
      Loading...
    </div>
  );
};

export default OnboardingPage;
