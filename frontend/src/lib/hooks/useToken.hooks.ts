import { useAuth, useUser } from "@clerk/clerk-react";
import { useEffect, useState } from "react";

const useToken = () => {
  const { isLoaded, isSignedIn } = useUser();
  const { getToken } = useAuth();

  const [token, setToken] = useState("");

  useEffect(() => {
    if (!isLoaded || !isSignedIn) return;

    void getToken().then(token => {
      setToken(token || "");
    });
  }, [isLoaded, isSignedIn, getToken]);

  return token;
};

export default useToken;
