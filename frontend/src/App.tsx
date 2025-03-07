import React from "react";
import { Route, Routes } from "react-router";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<h1>Hello World</h1>} />
      <Route path="/sign-in" element={<h1>Sign In</h1>} />
      <Route path="/sign-up" element={<h1>Sign Up</h1>} />
    </Routes>
  );
};

export default App;
