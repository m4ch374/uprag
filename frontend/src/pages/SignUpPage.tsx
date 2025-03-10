import { SignUp } from "@clerk/clerk-react";
import React from "react";

const SignUpPage: React.FC = () => {
  return (
    <div className="w-full h-screen flex justify-center items-center">
      <SignUp signInUrl="/sign-in" forceRedirectUrl={"/"} />;
    </div>
  );
};

export default SignUpPage;
