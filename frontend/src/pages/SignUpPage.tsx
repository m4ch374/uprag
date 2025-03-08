import { SignUp } from "@clerk/clerk-react";
import React from "react";

const SignUpPage: React.FC = () => {
  return (
    <div className="w-full h-screen flex justify-center items-center">
      <SignUp signInUrl="/sign-in" forceRedirectUrl={"/onboard"} />;
    </div>
  );
};

export default SignUpPage;
