import { useUser } from "@clerk/clerk-react";
import React from "react";
import { Navigate, Outlet } from "react-router";
import NavBar from "./NavBar";

const ProtectedRoutes: React.FC = () => {
  const { isSignedIn, isLoaded } = useUser();

  if (!isSignedIn && isLoaded) return <Navigate to="/" />;

  return (
    <div className="w-full h-screen bg-slate-100 flex">
      <NavBar />
      <div className="m-4 flex-1 rounded-sm bg-white">
        <Outlet />
      </div>
    </div>
  );
};

export default ProtectedRoutes;
