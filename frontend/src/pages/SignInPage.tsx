import { SignIn } from "@clerk/clerk-react";
import React from "react";

const SignInPage: React.FC = () => {
  return (
    <div className="w-full h-screen flex justify-center items-center">
      <SignIn signUpUrl="/sign-up" forceRedirectUrl={"/"} />;
    </div>
  );
};

export default SignInPage;
